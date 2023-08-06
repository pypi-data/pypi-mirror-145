from SDPA_MR_OFDM import tests
from importlib.util import module_for_loader
from SDPA_MR_OFDM.modulator import mr_ofdm_modulator
import numpy as np
from glob import glob



mod = mr_ofdm_modulator(MCS=)

def test_M1():
    """
    Tests if the modulator is capable of producing a header similar to the one 
    presented in Table M.1 (P. 162)
    """
    modulator = mr_ofdm_modulator()
    # TODO : Compare header from modulator with Table M.1
    

# def test_M2():
#     """
#     Tests if the header with convolutional encoding is equal to the Table M.2 (P. 163)
#     """
#     pass

# def test_M3():
#     """
#     Tests if the header after interleaving is equal to the Table M.3 (P. 164)
#     """
#     pass

# def test_M4():
#     """
#     Tests is the OFDM header after bit mapping is equal to the Table M.4 (P. 165)
#     """
#     pass

# def test_M5():
#     """
#     Tests if the OFDM header in the frequency domain is equal to table M.5 (P. 165-167) 
#     """
#     pass

# def test_M6():
#     """
#     Tests if the first and last 48 bits are the same after scrambling and pad insertion
#     """
#     pass

# def test_M7():
#     """
#     Tests if the first and last 48 bits are the same after convolutional encoding
#     """
#     pass

# def test_M8():
#     """
#     Tests if the first and last 48 bits are the same after interleaving
#     """
#     pass

# def test_M9():
#     """
#     Tests if the bit mapping of the OFDM payload matches the Table M.9
#     """
#     pass

# def test_M10():
#     """
#     Tests if the complete package in the frequency domain matches Table M.10
#     """
#     pass

def test_M11_STF():
    """
    Tests if the STF is valid in the time domain
    """
    modulator = mr_ofdm_modulator()
    I, Q = modulator._STF()

    data_th = np.genfromtxt("SDPA_MR_OFDM/tests/Table M.11.csv", delimiter=',', dtype=complex)
    Ith, Qth = data_th[:I.size, 1].real, data_th[:I.size, 1].imag

    # Rounding because values are extracted from a pdf with 3 decimals
    I_error = np.sum(np.abs(np.round(I,3) - np.round(Ith, 3)))
    assert I_error < (1e-3 * np.sum(np.abs(I))), f"Real part error : {I_error:.5f}"

    Q_error = np.sum(np.abs(np.round(Q,3) - np.round(Qth, 3)))
    assert Q_error < (1e-3 * np.sum(np.abs(Q))), f"Imaginary part error : {Q_error:.5f}"




