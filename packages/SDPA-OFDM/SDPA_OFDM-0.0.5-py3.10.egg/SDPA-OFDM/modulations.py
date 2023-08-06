"""
Functions to implement modulations used for OFDM

Modulation    M
BPSK          2
QPSK          4
16-QAM        16
"""
import numpy as np


class modulator():
    def __init__(self, HIGH=1, MSB_first=True, axis=0):
        """
        Modulator class

        Parameters
        ----------
        HIGH : int, float
            Highest value of the constellation (magnitude of the furthest symbols)
        MSB_first : bool
            Describes if MSB is first in the array (default True). Ignored for BPSK modulation
        axis : int
            Specifies in which axis the conversion must be done (for 2D arrays)
        """
        # Check types and values
        if not (isinstance(HIGH, int) or isinstance(HIGH, float)):
            raise ValueError('HIGH must be int or float')
        elif HIGH < 0:
            raise ValueError('HIGH cannot be negative')
        if not isinstance(MSB_first, bool):
            raise ValueError('MSB_first must be of type bool')
        if not isinstance(axis, int):
            raise ValueError('axis must be of type int')
        elif axis < 0:
            raise ValueError('axis cannot be negative')

        self.HIGH = HIGH
        self.MSB_first = MSB_first
        self.axis = axis

    def convert():
        raise NotImplementedError("modulator class cannot be used directly")


class BPSK(modulator):
    """
    Maps >0 values to HIGH and everything else to -HIGH
    """

    def convert(self, signal):
        if isinstance(signal, int | float):
            # Single value
            output = self.HIGH if signal > 0 else -self.HIGH
        elif isinstance(signal, np.ndarray):
            # Array
            output = np.ones_like(signal) * (-self.HIGH)
            output[signal > 0] = self.HIGH
        elif isinstance(signal, list):
            output = [self.HIGH if a > 0 else -self.HIGH for a in signal]
        else:
            raise ValueError("Unsupported type")
        return output


class QPSK(modulator):
    """
    Separates the signal by group of 2 bits then Maps the signal on a circle
        00 -> sqrt(2)/2*(-1-1j)
        01 -> sqrt(2)/2*(-1+1j)
        10 -> sqrt(2)/2*(+1-1j)
        11 -> sqrt(2)/2*(+1+1j)

        HIGH is orthogonal amplitude of each symbol (by default sqrt(2)/2)
    """

    def convert(self, signal):
        if isinstance(signal, np.ndarray):
            if self.MSB_first:
                first, second = 1, 1j
            else:
                first, second = 1j, 1

            match signal.ndim:
                case 1:
                    # One-dimensional array
                    output = (BPSK(signal[::2]) * first +
                              BPSK(signal[1::2]) * second) * self.HIGH
                case 2:
                    # 2D array (mapping along the specified axis)
                    if self.axis == 0:
                        assert np.mod(
                            signal.shape[0], 2) == 0, "Invalid number of elements"
                        output = (BPSK(signal[::2, :]) * first +
                                  BPSK(signal[1::2, :]) * second) * self.HIGH
                    elif self.axis == 1:
                        assert np.mod(
                            signal.shape[1], 2) == 0, "Invalid number of elements"
                        output = (BPSK(signal[:, ::2]) * first +
                                  BPSK(signal[:, 1::2]) * second) * self.HIGH
                    else:
                        raise ValueError("Invalid axis")
                case _:
                    raise ValueError(f"Invalid signal shape ({signal.shape})")
            return output
        else:
            raise ValueError("Unsupported type")


class QAM16(modulator):
    """
    Maps the values on a 4x4 QAM matrix
    (multiple standards exists for the symbols order)

        1000  1001  1011  1010
        1100  1101  1111  1110
        0100  0101  0111  0110
        0000  0001  0011  0010

    """

    def convert(self, signal):
        # Above/Below x axis is given by MSB
        # Vertically "close" to center is given by the next bit
        # Right/Left of Y axis is given by the next bit
        # Horizontally "close" to center is given by LSB

        if(isinstance(signal, np.ndarray)):
            # We expect the signal to be a numpy array
            match signal.ndim:
                case 1:
                    # One-dimensional array
                    if self.MSB_first:
                        output = BPSK(signal[::4]) * 2/3 * self.HIGH * 1j * BPSK(signal[1::4], HIGH=1/2, LOW=3/2) + BPSK(
                            signal[2::4]) * 2/3 * self.HIGH * BPSK(signal[3::4], HIGH=1/2, LOW=3/2)
                    else:
                        output = BPSK(signal[3::4]) * 2/3 * self.HIGH * 1j * BPSK(signal[2::4], HIGH=1/2, LOW=3/2) + BPSK(
                            signal[1::4]) * 2/3 * self.HIGH * BPSK(signal[::4], HIGH=1/2, LOW=3/2)
                case 2:
                    # 2D array
                    match self.axis:
                        case 0:
                            if self.MSB_first:
                                output = BPSK(signal[::4, :]) * 2/3 * self.HIGH * 1j * BPSK(signal[1::4, :], HIGH=1/2, LOW=3/2) + BPSK(
                                    signal[2::4, :]) * 2/3 * self.HIGH * BPSK(signal[3::4, :], HIGH=1/2, LOW=3/2)
                            else:
                                output = BPSK(signal[3::4, :]) * 2/3 * self.HIGH * 1j * BPSK(signal[2::4, :], HIGH=1/2, LOW=3/2) + BPSK(
                                    signal[1::4, :]) * 2/3 * self.HIGH * BPSK(signal[::4, :], HIGH=1/2, LOW=3/2)
                        case 1:
                            if self.MSB_first:
                                output = BPSK(signal[:, ::4]) * 2/3 * self.HIGH * 1j * BPSK(signal[:, 1::4], HIGH=1/2, LOW=3/2) + BPSK(
                                    signal[:, 2::4]) * 2/3 * self.HIGH * BPSK(signal[:, 3::4], HIGH=1/2, LOW=3/2)
                            else:
                                output = BPSK(signal[:, 3::4]) * 2/3 * self.HIGH * 1j * BPSK(signal[:, 2::4], HIGH=1/2, LOW=3/2) + BPSK(
                                    signal[:, 1::4]) * 2/3 * self.HIGH * BPSK(signal[:, ::4], HIGH=1/2, LOW=3/2)
                        case _:
                            raise ValueError("Invalid axis")
                    pass
                case _:
                    raise ValueError(f"Invalid signal shape {signal.shape}")
            return output

        else:
            raise ValueError("Unsupported type")


def get_modulator_dict():
    """
    Returns the list of possible modulators
    """
    return {'BPSK': BPSK, 'QPSK': QPSK, 'QAM16': QAM16}


def get_modulator(mod: str) -> modulator:
    """
    Provides the requested modulator as subclass of modulator()

    Parameters
    ----------
    mod : str
        The requested modulator as a string

    get_modulator_list() gives the list of acceptable values
    """
    if not mod in get_modulator_dict().keys():
        raise ValueError("Invalid modulator")
    else:
        return get_modulator_dict()[mod]()
