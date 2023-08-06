"""
Main OFDM modulator class

Must be instanciated as such :
    modulator = ofdm_modulator(settings)

Output can be requested by calling the appropriate function, i.e.
    I, Q = modulator.getIQ()
"""

from SDPA_OFDM.modulations import get_modulator
from SDPA_OFDM.pn9 import pn9
import math
import numpy as np
from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq


class ofdm_modulator():
    def __init__(self, N_FFT=32, BW=8e6, modulation='BPSK', modulation_factor=1, CP=1/8, padding_left=0, padding_right=0, pilots_indices=None, pilots_values=None, frequency_spreading=1, MSB_first=True, verbose=False):
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
            Indices of pilots in the OFDM symbol.
            If 1D : pilots positions are constant throughout the symbols.
            if 2D :each column represents a new symbol. Looping will occur when all the column have been used
            None by default (no pilots).
            For a 16 FFT :
            0 is the center frequency (DC)
            -8 is the lowest index
            +7 is the highest index
        pilots_values : numpy array or str
            Pilots values.
            If 1D array     : sequence of pilots (restarts when the end is reached). A single value in the array is valid
            If "pn9"        : use a pseudo-random (PN9) sequence to generate pilots values
            None by default (no pilots)
        frequency_spreading : int
            1 : no spreading
            2 : 2x spreading (half the data rate)
            4 : 4x spreading (1/4 the data rate)
            See 18.2.3.6 Frequency spreading
        CP : float
            Cyclic prefix. This fraction ot the end of the symbol in the time domain is repeated at the beginning
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
        if pilots_indices is None and pilots_values is not None:
            raise ValueError("Pilots must have corresponding indices")
        elif pilots_indices is not None and pilots_values is None:
            raise ValueError("Pilots indices must have pilots values")
        if not isinstance(frequency_spreading, int):
            raise ValueError("frequency_spreading must be int")
        elif not frequency_spreading in [1, 2, 4]:
            raise ValueError(
                f"Invalid frequency_spreading value {frequency_spreading}, must be [1, 2, 4]")

        # Manage pilots
        if pilots_values is not None:
            # Check for types
            if not isinstance(pilots_indices, np.ndarray):
                raise ValueError("pilots_indices must be a numpy array")
            if not np.all(np.diff(pilots_indices, axis=0) >= 0):
                raise ValueError("Pilots indices must be ordered")
            if not (isinstance(pilots_values, np.ndarray) or isinstance(pilots_values, str)):
                raise ValueError("Invalid pilots values type (must be numpy array or str)")
            if not (1 <= pilots_indices.ndim <= 2):
                raise ValueError(f"Invalid pilots indices shape ({pilots_indices.shape})")

            self._N_pilots = pilots_indices.shape[0]
            
            if pilots_values == "pn9":
                # Use PN9 sequence
                self._use_pn9_sequence = True
            else:
                self._use_pn9_sequence = False
                # Check if an array is given for pilots values and it matches the size of pilots_indices
                if pilots_values.ndim > 0 and pilots_values.shape[0] == pilots_indices.shape[0]:
                    raise ValueError(f"Invalid pilots_indices dimension ({pilots_indices.ndim} for shape {pilots_indices.shape})")
            # Store the values
            self._pilots_values = pilots_values
            # Reshape to 2D (so that the rows always represent the pilots positions)
            if pilots_indices.ndim == 1:
                self._pilots_indices = pilots_indices.reshape(-1,1)
            else:
                self._pilots_indices = pilots_indices
        else:
            self._N_pilots = 0

        self._pseudo_random_sequence = pn9()
        
        

        # Save the values in the class
        self._N_FFT = N_FFT
        self._BW = BW
        self._modulator = get_modulator(modulation, MSB_first=MSB_first)
        self._verbose = verbose
        self._padding_left = padding_left
        self._padding_right = padding_right
        self._modulation_factor = modulation_factor
        self._frequency_spreading = frequency_spreading

        self._CP = CP

        self._bits_per_symbol = self._modulator.bits_per_symbol()

        self._DC_TONE = 1
        # Length is FFT minus all the non-data channels (padding + pilots)
        self._message_split_length = int((
            self._N_FFT - self._N_pilots - self._padding_left - self._padding_right - self._DC_TONE) * self._bits_per_symbol / self._frequency_spreading)

        # Used only with variable pilots indices (multiple columns)
        self._pilots_column_index = 0

        self._print_verbose(f"Bandwidth = {BW} (spacing of {2*BW/(N_FFT-1)})")

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
        mapped_message = self._modulator.convert(
            message) * self._modulation_factor
        self._print_verbose(
            f"    New message size {message.shape} -> {mapped_message.shape} ({mapped_message.shape[0]} + pilots as IFFT channels and {mapped_message.shape[1]} OFDM symbols)")
        return mapped_message

    def _frequency_spread(self, message):
        """
        Applies frequency spreading to the message (repetition)
        1 : No repetition
        2 : Data is placed in the positive values of the FFT and copied on the lower (negative) values
        4 : Data is placed in the lower positive values of the FFT and copied on the 4 others segments
        See 18.2.3.6 Frequency spreading
        """

        # NOTE :
        # The specification says :
        #   (2 x k - 1)
        #   not sure if this is supposed to say (2*k - 1) or (2 * (k-1))
        #
        # We will use is "as is", so 2*k  then - 1

        if self._frequency_spreading == 1:
            # No spreading to do
            return message
        elif self._frequency_spreading == 2:
            # d(k-Nd/2-1) = d(k) * e^(j*2*pi*(2*k-1)/4)

            # k is the index (positive and starts at 1)
            # k :
            #  0 0 0 ..
            #  1 1 1 ..
            #  2 2 2 ..
            #  . . .
            k = (
                np.arange(message.shape[0])+1).repeat(message.shape[1]).reshape(*message.shape)
            # phase is the phase matrix (for each data value)
            phase = np.exp(1j*2*np.pi*(2*k-1)/4)
            # lower portion of the FFT, message is the higher portion
            lower = message * phase

            spread_message = np.block([[lower, message]])

            return spread_message
        elif self._frequency_spreading == 4:
            # Same principle as 2x but a bit more complicated
            # message is located here :
            # ----------------Dmmmmmmmm--------
            # Setting k matrix (just like before)
            k = (
                np.arange(message.shape[0])+1).repeat(message.shape[1]).reshape(*message.shape)
            # ----------------D--------xxxxxxxx
            phase = np.exp(1j*2*np.pi*(k-1)/4)
            positive_high = message * phase
            # xxxxxxxx--------D----------------
            phase = np.exp(1j*2*np.pi*(2*k - 1)/4)
            negative_low = message * phase
            # --------xxxxxxxxD----------------
            phase = np.exp(1j*2*np.pi*(3*k - 1)/4)
            negative_high = message * phase

            spread_message = np.block(
                [[negative_low], [negative_high], [message], [positive_high]])
            return spread_message

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
        message_str = '-'*message.shape[0]

        self._print_verbose(
            "Adding OFDM " + ("pilots, " if self._N_pilots else '') + "DC Tone and padding...")
        self._print_verbose("    Message without pilots :")
        self._print_verbose(f"    {message_str} ({message.shape[0]}x)")

        # Adding padding
        self._print_verbose(
            f"    Adding padding ({self._padding_left}, {self._padding_right})")
        message_str = '0'*self._padding_left + message_str + '0'*self._padding_right
        ifft_channels = message.copy()
        # Add left padding
        if self._padding_left > 0:
            zeros = np.zeros([self._padding_left, ifft_channels.shape[1]])
            ifft_channels = np.concatenate([zeros, ifft_channels], axis=0)
        # Add right padding
        if self._padding_right > 0:
            zeros = np.zeros([self._padding_right, ifft_channels.shape[1]])
            ifft_channels = np.concatenate([ifft_channels, zeros], axis=0)

        self._print_verbose(f"    {message_str} ({message.shape[0]}x)")

        # Create a BPSK modulator for PN9 sequence (is used)
        bpsk_modulator = get_modulator('BPSK')

        # Adding pilots
        # pilot indices are given at the class instanciation
        # pilots values are either :
        # - given by pn9 sequence
        # - given by array
        if self._N_pilots > 0:
            # Start by making a backup of the old ifft_channels (before adding pilots)
            ifft_channels_old = ifft_channels.copy()
            # Create the new array
            ifft_channels = np.zeros([ifft_channels_old.shape[0] + self._N_pilots, ifft_channels_old.shape[1]], dtype=complex)

            # Iterate over the symbols
            for c in range(message.shape[1]):
                # message_str is specific to each column
                message_str_i = message_str
                # Create a temporary symbol to add the pilots
                symbol = ifft_channels_old[:, c]
                # pilot_set is the array of pilots positions for the current symbol
                # Each column represents a set of pilots indices for each symbol
                pilot_set = self._pilots_indices[:, self._pilots_column_index]
                self._print_verbose(f"    Adding pilots at {pilot_set} (set {self._pilots_column_index})")
                
                # use the pilots_column_index to select which column to set (stored in the class)
                for row in self._pilots_indices[:, self._pilots_column_index] + self._N_FFT//2:
                    if self._use_pn9_sequence:
                        # PN9 sequence
                        p = bpsk_modulator.convert(np.array([self._pseudo_random_sequence.next()]))[0]
                    else:
                        # Array
                        p = self._pilots_values[self._pilots_values_index]
                        self._pilots_values_index += 1
                        if self._pilots_values_index >= self._pilots_values.size:
                            self._pilots_values_index = 0
                        
                    # if the index is after the DC tone (not added yet, we remove one) to the index
                    if row > self._N_FFT//2:
                        row -= 1
                    symbol = np.insert(
                        symbol, row, p, axis=0)

                    # Visual stuff :
                    message_str_i = message_str_i[0:row] + \
                        'P' + message_str_i[row:]
                # Put the symbol back in the main array
                ifft_channels[:,c] = symbol

                self._pilots_column_index += 1
                if self._pilots_column_index >= self._pilots_indices.shape[1]:
                    self._pilots_column_index = 0

                self._print_verbose(
                    f"    {message_str_i} ({ifft_channels.shape[0]}x) (pilot set/index : {self._pilots_column_index})")
                
        # Adding DC Tone
        self._print_verbose("    Adding DC Tone")
        ifft_channels = np.insert(
            ifft_channels, 0 + self._N_FFT//2, 0, axis=0)
        message_str = message_str[0:self._N_FFT//2] + \
            'D' + message_str[self._N_FFT//2:]
        self._print_verbose("    Message with DC Tone :")
        self._print_verbose(f"    {message_str} ({ifft_channels.shape[0]}x)")

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
        if(self._CP > 0):
            self._print_verbose("Adding cyclic prefix...")
            prefix_length = int(signal.shape[0]*self._CP)
            prefix = signal[-prefix_length:, :]
            cyclic_signal = np.concatenate([prefix, signal])
            self._print_verbose(
                f"    Signal {signal.shape} -> {cyclic_signal.shape}")
            return cyclic_signal
        else:
            return signal

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
        I : ndarray
            Real part of the signal
        Q : ndarray
            Imaginary part of the signal
        t : ndarray
            time vector
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

        ### Frequency spreading ###
        message_split_mapped_spread = self._frequency_spread(
            message_split_mapped)

        print(f"message_split_mapped_spread = {message_split_mapped_spread.shape}")
        ### Adding pilots and padding###
        message_split_mapped_pilots = self._add_pilots_and_padding(
            message_split_mapped_spread)

        ### IFFT ###
        Ts, signal = self._ifft(message_split_mapped_pilots)

        ### Cyclic prefix ###
        signal_cyclic = self._cyclic_prefix(signal)
        t = np.arange(0, signal_cyclic.shape[0] * Ts, Ts)

        I, Q = signal_cyclic.real, signal_cyclic.imag

        return I, Q, t

    def subcarriersToIQ(self, subcarriers):
        """
        Converts a list of subcarriers to I and Q signals
        Essentially this function applies IFFT and cyclic prefix

        Parameters
        ----------
        subcarriers : ndarray
            List of subcarriers. 1D or 2D with each column corresponding to a symbol.
            Must have the same number of samples as N_FFT

        Returns
        -------
            I : ndarray
                Real part of the signal
            Q : ndarray 
                Imaginary part of the signal
            t : ndarray
                Time vector
        """
        if subcarriers.ndim == 1:
            subcarriers = subcarriers.reshape(-1, 1)
        elif subcarriers.ndim != 2:
            raise ValueError(
                f"Invalid number of dimensions ({subcarriers.ndim})")

        if subcarriers.shape[0] != self._N_FFT:
            raise ValueError(
                f"Invalid number of subcarriers ({subcarriers.shape[0]} / {self._N_FFT})")

        ### IFFT ###
        Ts, signal = self._ifft(subcarriers)

        ### Cyclic prefix ###
        signal_cyclic = self._cyclic_prefix(signal)
        t = np.arange(0, signal_cyclic.shape[0] * Ts, Ts)

        I, Q = signal_cyclic.real, signal_cyclic.imag

        return I, Q, t

    def _print_verbose(self, message: str):
        """
        Prints additionnal information if the verbose flag is True
        """
        if(self._verbose):
            print(message)
