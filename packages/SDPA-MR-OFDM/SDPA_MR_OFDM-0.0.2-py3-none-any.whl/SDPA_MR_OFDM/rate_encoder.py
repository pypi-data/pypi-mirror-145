import math

class rate_one_half():
    def __init__(self, seed=0):
        """
        1/2 rate encoder
        See 802.15.4g figure 134

        Parameters
        ----------
        seed : int
            Initial value for the flip-flops
        """
        self._value = (seed & 0x3F)
    def reset(self, seed=0):
        """
        Resets the flip-flops to the given seed value (0 by default)
        """
        self._value = seed

    def single(self, input_bit):
        """
        Returns corresponding value for the given bit 
        Parameters
        ----------
        input_bit : int
        
        Returns
        -------
        A : int 
            Output data A
        B : int
            Output data B
        """
        input_bit = 1 if input_bit > 0 else 0
        A = input_bit ^ ((self._value & 0x10) >> 4) ^ ((self._value & 0x08) >> 3) ^ ((self._value & 0x02) >> 1) ^ (self._value & 0x01)
        B = input_bit ^ ((self._value & 0x20) >> 5) ^ ((self._value & 0x10) >> 4) ^ ((self._value & 0x08) >> 3) ^ (self._value & 0x01)
        self._value = (self._value >> 1) | (0x20 if input_bit else 0)
        return A, B

    def sequence(self, input_bits):
        """
        Returns a sequence corresponding to the input sequence
        Paramters
        ---------
        input_bits : list
            Input list of bits (ints)
        Returns
        -------
        A : list
            A output bits
        B : list
            B output bits
        out : list
            Concatenated output (A and B interlaced)
        """
        A, B, out = [], [], []
        for bit in input_bits:
            a, b = self.single(bit)
            A.append(a)
            B.append(b)
            out.append(a)
            out.append(b)
        return A, B, out

class rate_three_quarter():
    def __init__(self, seed=0):
        """
        3/4 rate encoder, similar to 1/2 encoder but with ommited bits
        Parameters
        ----------
        seed : int
            Initial value for the flip flops
        """
        self._rate_one_half = rate_one_half(seed=seed)

    def sequence(self, input_bits):
        """
        Outputs A and B sequences from the input sequence
        Parameters
        ----------
        input_bits : list of int

        Returns
        -------
        A : list of int
            A output bits
        B : list of int
            B output
        """
        if len(input_bits) % 3 > 0:
            raise ValueError("input sequence must be a multiple of 3")
        
        out = []
        for i in range(0, len(input_bits), 3):
            A, B, _ = self._rate_one_half.sequence(input_bits[i:i+3])
            out.append(A[0])
            out.append(B[0])
            out.append(A[1])
            out.append(B[2])
        return out