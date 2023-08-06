from bitarray import bitarray
from bitarray.util import int2ba
from crc8 import crc8


class PHR():
    def __init__(self, rate=0, length=1, scrambler=0):
        """
        PHY Header for MR-OFDM
        See 18.2.1.3 in 802.15.4g specification
        0-4   : Rate (RA4-RA0)
            Specifies the data rate of the payload (=MCS)
        5     : Reserved
        6-16  : Frame length (L10-L0)
            Total number of octets contained in the PSDU (prior to FEC encoding)
        17-18 : Reserved
        19-20 : Scrambler (S1-S0)
            Scrambling seed (0 - 3)
        21    : Reserved
        22-29 : HCS (H7-H0)
            Header check sequence (8 bit CRC over PHR fields)
        30-35 : Tail (T5-T0)

        """
        # Check values and types
        if not isinstance(rate, int):
            raise ValueError("Invalid rate type")
        if not (0 <= rate <= 6):
            raise ValueError(f"Invalid rate value {rate}")
        if not isinstance(length, int):
            raise ValueError("Invalid length type")
        if not (1 <= length <= 2**11):
            raise ValueError(f"Invalid length value {length}")
        if not isinstance(scrambler, int):
            raise ValueError("Invalid scrambler type")
        if not (0 <= scrambler <= 3):
            raise ValueError(f"Invalid scrambler value {scrambler}")
        

        # Store values
        self._RA = rate
        self._L = length
        self._S = scrambler

    def value(self):
        """
        Returns the byte-array value of the PHY Header
        """
        crc = crc8()

        # Calculate the HCS CRC
        output = bitarray(36).setall(0)
        output[0:4+1] = int2ba(self._RA, endian='big', length=4)
        output[6:16+1] = int2ba(self._L, endian='big')
        output[19:20+1] = int2ba(self._S, endian='big')
        crc.update(output[0:22+1].tobytes())
        HCS = hash.digest[0]
        output[22:29+1] = int2ba(HCS, endian='big')

        return output.tobytes()

    