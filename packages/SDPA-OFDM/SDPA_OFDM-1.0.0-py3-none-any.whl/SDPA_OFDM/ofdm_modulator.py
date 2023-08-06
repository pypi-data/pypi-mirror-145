"""
Main OFDM modulator class

Must be instanciated as such :
    modulator = ofdm_modulator(settings)

Output can be requested by calling the appropriate function, i.e.
    I, Q = modulator.getIQ()
"""

from multiprocessing.sharedctypes import Value
from tabnanny import verbose
from SDPA_OFDM.modulations import get_modulator
import math
import numpy as np
from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq


class ofdm_modulator():
    def __init__(self, N_FFT=32, BW=8e6, modulation='BPSK', padding_left=0, padding_right=0, pilots_indices=None, pilots=None, rate=None, rep=None, MSB_first=True, verbose=False):
        """
        Returns an OFDM modulator with the desired settings

        Parameters
        ----------
        N_FFT : int
            Number of FFT channels used (default 32)
        BW : int, float
            Half bandwidth in Hz, total is 2*BW (default 8 Mhz)
        modulation : {'BPSK', 'QPSK', 'QAM16'}
            Type of modulation used, by default BPSK
        padding_left : int
            Empty FFT channels on the left (negative frequencies)
        padding_right : int
            Empty FFT channels on the right (positive frequencies)
        pilots_indices : numpy array
            Indices of pilots in the OFDM symbol. If 1D, pilots positions are constant throughout the symbols. if 2D, each column represents a new symbol. Looping will occur when all the column have been used
            None by default (no pilots).
            For a 16 FFT :
            0 is the center frequency (DC)
            -8 is the lowest index
            +7 is the highest index
        pilots : numpy array
            Pilots values. If 1D, pilots will be the same for each symbol. If 2D, each column will represent the values for each symbol. Once the last column is used, the counter will loop back to the first one
            None by default (no pilots)
            Size must match pilots_indices !
        rate : ?
            TODO : Implement
        rep : ?
            TODO : Implement
        verbose : bool
            if True, prints informations throughout the process (False by default)
        MSB_first : bool
            Specifies is the MSB is first in the message (True by default)
        """
        # Check types and values
        if not isinstance(N_FFT, int):
            raise ValueError("N_FFT must be int type")
        else:
            if not math.log(N_FFT, 2).is_integer():
                raise ValueError("N_FFT must be a power of 2")
        if not (isinstance(BW, int) or isinstance(BW, float)):
            raise ValueError("BW must be int or float")
        if not isinstance(modulation, str):
            raise ValueError("modulation must be str")
            # No need to check for valid string, the modulation module will do it
        if not isinstance(padding_left, int):
            raise ValueError("padding_left must be int")
        if not isinstance(padding_right, int):
            raise ValueError("padding_right must be int")
        if pilots_indices is None and pilots is not None:
            raise ValueError("Pilots must have corresponding indices")
        elif pilots_indices is not None and pilots is None:
            raise ValueError("Pilots indices must have pilots values")
        # Check pilots_indices and pilots (for type and same shape)
        if pilots is not None:
            if isinstance(pilots_indices, np.ndarray):
                if pilots_indices.ndim == 0:
                    # ok
                    self._N_pilots = 1
                elif pilots_indices.ndim <= 2:
                    self._N_pilots = pilots_indices.shape[0]
                    if not np.all(np.diff(pilots_indices, axis=0) >= 0):
                        raise ValueError("Pilots indices must be ordered")
                else:
                    raise ValueError(f"Invalid pilots_indices dimension ({pilots_indices.ndim} for shape {pilots_indices.shape})")
            else:
                raise ValueError("pilots_indices must be a numpy array")
            if not isinstance(pilots, np.ndarray):
                raise ValueError("pilots must be a numpy array")
            else:
                if pilots.ndim > 2:
                    raise ValueError(f"Invalid pilots dimension ({pilots.ndim} for shape {pilots.shape})")
            if pilots.shape != pilots_indices.shape:
                raise ValueError(
                    "pilots and pilots_indices must have similar shape")
            self._pilots = np.round(np.squeeze(pilots)).astype(int)
            self._pilots_indices = np.round(np.squeeze(pilots_indices)).astype(int)
        else:
            self._N_pilots = 0

        # Save the values in the class
        self._N_FFT = N_FFT
        self._BW = BW
        self._modulator = get_modulator(
            modulation, HIGH=1, MSB_first=MSB_first)
        self.verbose = verbose
        self._padding_left = padding_left
        self._padding_right = padding_right

        self._IG = 1/8  # TODO : do this correctly

        self._bits_per_symbol = self._modulator.bits_per_symbol()

        # Length is FFT minus all the non-data channels (padding + pilots)
        self._message_split_length = (
            self._N_FFT - self._N_pilots - self._padding_left - self._padding_right) * self._bits_per_symbol

        # Used only with variable pilots indices (multiple columns)
        self._pilots_column_index = 0

    def _split_message(self, message, pad=False):
        """
        Splits a message into multiple parts (each with a size suitable for the IFFT)

        Parameters
        ----------
        message : 1D numpy.array
            The message to modulate. Size must be a multiple of (N_FFT - number of pilots)
        pad : bool
            Pad the message with 0s to reach the desired length. False by default
        """
        # We assume the message is 1D and with the correct number of elements
        #
        # The split order is :
        #
        # 0  n+1 . .
        # 1  n+2 . .
        # .   .  . .
        # .   .  . .
        # n  2n  . .
        #
        # Each column represents an OFDM symbol
        # Each element (row by row) is a IFFT channel (minus the pilots)
        self._print_verbose("Splitting message...")
        if pad:
            # Add 0s to reach the right size
            old_message_shape = message.shape
            missing_zeros = int(np.ceil(
                message.size / self._message_split_length) * self._message_split_length - message.size)
            message = np.concatenate([message, np.zeros(missing_zeros)])
            self._print_verbose(
                f"    Padding message with {missing_zeros} zeros ({old_message_shape} -> {message.shape})")

        message_split = message.reshape(
            self._message_split_length, -1, order='F')
        self._print_verbose(
            f"    Splitting message from length {message.size} to {message_split.shape} ({message_split.shape[0]} channels before mapping and {message_split.shape[1]} OFDM symbols)")
        return message_split

    def _constellation_map(self, message):
        """
        Maps the message with the specified constellation

        Parameters
        ----------
        message : numpy array
            Values to map along rows. Each column is a symbol 

        Returns
        -------
            mapped_message : numpy array
                Converted message
        """
        self._print_verbose(
            f"Constellation mapping using {self._modulator.name}...")
        mapped_message = self._modulator.convert(message)
        self._print_verbose(
            f"    New message size {message.shape} -> {mapped_message.shape} ({mapped_message.shape[0]} + pilots as IFFT channels and {mapped_message.shape[1]} OFDM symbols)")
        return mapped_message

    def _add_pilots_and_padding(self, message):
        """
        Adds pilots and paddings to the message (to reach IFFT size)

        Parameters
        ----------
        message : numpy array

        Returns
        -------
        ifft_channels : numpy array        
        """
        # Only adding 0s at the moment
        # TODO : Study OFDM pilots and update this code
        # Maybe add a sequential option (OFDM pilots are dependent on the previous ones)
        message_str = '-'*message.shape[0]
        
        self._print_verbose("Adding OFDM " + ("pilots and" if self._N_pilots else '') +  "padding...")
        self._print_verbose("    Message without pilots :")
        self._print_verbose(f"    {message_str} ({message.shape[0]}x)")

        # Adding padding
        self._print_verbose(
            f"    Adding padding ({self._padding_left}, {self._padding_right})")

        ifft_channels = message.copy()
        # Add left padding
        if self._padding_left > 0:
            zeros = np.zeros([self._padding_left, ifft_channels.shape[1]])
            ifft_channels = np.concatenate([zeros, ifft_channels], axis=0)
        # Add right padding
        if self._padding_right > 0:
            zeros = np.zeros([self._padding_right, ifft_channels.shape[1]])
            ifft_channels = np.concatenate([ifft_channels, zeros], axis=0)

        message_str = '0'*self._padding_left + message_str + '0'*self._padding_right
        self._print_verbose(f"    {message_str} ({message.shape[0]}x)")

        # Adding pilots. There are 3 possibilities :
        # A : pilots is a single valuex
        # B : pilots is a 1D array (multiple pilots, same for each symbol)
        # C : pilots is a 2D array (multiple pilots, different for each symbol)
        if self._N_pilots > 0:
            if self._pilots.ndim == 0:
                # A : pilots is a single value
                self._print_verbose(
                    f"    Adding pilot {self._pilots} at index : {self._pilots_indices}")
                ifft_channels = np.insert(
                    ifft_channels, self._pilots_indices + self._N_FFT//2, self._pilots, axis=0)
                message_str = message_str[0:self._pilots_indices  + self._N_FFT//2] + 'P' + message_str[self._pilots_indices  + self._N_FFT//2:]
                self._print_verbose("    Message with pilots :")
                self._print_verbose(f"    {message_str} ({ifft_channels.shape[0]}x)")

            elif self._pilots_indices.ndim == 1:
                # B : pilots is a 1D array (multiple pilots, same for each symbol)
                self._print_verbose(f"    Adding pilot {self._pilots} at indices : {self._pilots_indices}")
                for i, p in zip(self._pilots_indices + self._N_FFT//2, self._pilots):
                    ifft_channels = np.insert(
                        ifft_channels, i, p, axis=0)
                    message_str = message_str[0:i] + 'P' + message_str[i:]
                self._print_verbose("    Message with pilots :")
                self._print_verbose(f"    {message_str} ({ifft_channels.shape[0]}x)")
            else:
                # C : pilots is a 2D array (multiple pilots, different for each symbol)
                self._print_verbose("    Messages with pilots (different for each symbol) :")
                for c in range(message.shape[1]):
                    # message_str is specific to each column
                    message_str_i = message_str
                    # Iterate over the columns
                    # use the pilots_column_index to select which column to set (stored in the class)
                    for r, p in zip(self._pilots_indices[:, self._pilots_column_index] + self._N_FFT//2, self._pilots[:,self._pilots_column_index]):
                        ifft_channels[:, c] = np.insert(ifft_channels[:, c], r, p, axis=0)
                        message_str_i = message_str_i[0:r] + 'P' + message_str_i[r:]
                    
                    self._print_verbose(f"    {message_str_i} ({ifft_channels.shape[0]}x) (pilot set/index : {self._pilots_column_index})")


                    # Add 1 to the column index, if it reaches the number of columns of the pilots
                    # it loops over to 1
                    self._pilots_column_index += 1
                    if self._pilots_column_index >= self._pilots.shape[1]:
                        self._pilots_column_index = 0

        return ifft_channels

    def _ifft(self, channels):
        """
        Applies iFFT to the message (channels). The iFFT is applied on the rows (each column is a separate symbol)

        Parameters
        ----------
        channels : numpy array
            The input data of the iFFT

        Returns
        -------
        t : numpy array
            time vector
        signal : numpy array
            time domain signal
        """
        self._print_verbose(f"Applying iFFT to the signal...")
        # ifftshift is very important since the spectrum was created "how it looks" but the ifft does 0-> Fs/2 -> -Fs/2 -> 0-dF
        signal = ifft(ifftshift(channels, axes=0), axis=0)
        # Time vector (and corresponding sampling period)
        deltaF = 2*self._BW / (channels.shape[0]-1)
        Ts = 1/(signal.shape[0] * deltaF)

        return Ts, signal

    def _cyclic_prefix(self, signal):
        """
        Adds cyclic prefix to the corresponding signal (along the rows). The fraction of cyclic prefix is given by IG

        Parameters
        ----------
        signal : numpy array
            the signal

        Returns
        -------
        cyclic_signal : numpy array
            the signal with cyclic prefix
        """
        self._print_verbose("Adding cyclic prefix...")

        cyclic_signal = np.concatenate(
            [signal[0:int(signal.shape[0]*self._IG)], signal])
        self._print_verbose(
            f"    Signal {signal.shape} -> {cyclic_signal.shape}")
        return cyclic_signal

    def messageToIQ(self, message, pad=False):
        """
        Applies OFDM modulation to the provided message

        Parameters
        ----------
        message : numpy array
            Array containing the bits to transmit
        pad : bool
            Pad the message with 0s to reach the desired length. False by default

        Returns
        -------
        I : Real part of the signal
        Q : Imaginary part of the signal
        """
        # Check types and values
        if not isinstance(message, np.ndarray):
            raise ValueError("Message must be a numpy array")
        message = np.squeeze(message)
        if message.ndim != 1:
            raise ValueError("Message must be one-dimensional")
        elif np.mod(message.size, self._message_split_length) != 0 and pad == False:
            raise ValueError(
                f"Message size must be a multiple of {self._message_split_length} (it currently is {message.size})")

        ### Splitting (separating message into OFDM symbols before IFFT) ###
        message_split = self._split_message(message, pad)

        ### Constellation mapping ###
        message_split_mapped = self._constellation_map(message_split)

        ### Adding pilots and padding###
        message_split_mapped_pilots = self._add_pilots_and_padding(
            message_split_mapped)

        ### IFFT ###
        Ts, signal = self._ifft(message_split_mapped_pilots)

        ### Cyclic prefix ###
        signal_cyclic = self._cyclic_prefix(signal)
        t = np.arange(0, signal_cyclic.shape[0] * Ts, Ts)

        I, Q = signal_cyclic.real, signal_cyclic.imag

        return I, Q, t

    def _print_verbose(self, message: str):
        """
        Prints additionnal information if the verbose flag is True
        """
        if(self.verbose):
            print(message)
