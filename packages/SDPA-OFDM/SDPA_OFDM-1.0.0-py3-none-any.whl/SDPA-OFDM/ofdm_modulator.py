"""
Main OFDM modulator class

Must be instanciated as such :
    modulator = ofdm_modulator(settings)

Output can be requested by calling the appropriate function, i.e.
    I, Q = modulator.getIQ()
"""


from modulations import get_modulator
import math


class ofdm_modulator():
    def __init__(self, N_FFT=32, BW=8e6, modulation='BPSK', rate=None, rep=None, padding=None):
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
        rate : ?
            TODO : Implement
        rep : ?
            TODO : Implement
        padding : ?
            TODO : Implement
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
            #             
        self.N_FFT = N_FFT
        self.BW = BW
        self.modulator = get_modulator(modulation)