import unittest
import numpy as np

CIR_LP = 0
CIR_HP = 1

def L_matching(Rs, Rl, f0, tp):
    '''
    Rs: source resistor
    Rl: load resistor
    f0: central frequency(MHz)
    tp: circuit type
    '''
    w0 = (f0 * (10 ** 6)) * (2 * np.pi) 
    if Rl > Rs:
        Q = np.sqrt((Rl / Rs) - 1)
        X1 = Rl / Q
        X2 = Rs * Q
        if tp == CIR_LP:
            return Q, (X2 / w0), (1 / (X1 * w0))
        elif tp == CIR_HP:
            return Q, (X1 / w0), (1 / (X2 * w0))
    elif Rl < Rs:
        Q = np.sqrt((Rs / Rl) - 1)
        X1 = Q * Rl
        X2 = Rs / Q
        if tp == CIR_LP:
            return Q, (X1 / w0), (1 / (X2 * w0))
        elif tp == CIR_HP:
            return Q, (X2 / w0), (1 / (X1 * w0))
    else:
        return 0, 0, 0

def pi_matching(Rs, Rl, f0, maxQ):
    pass

def T_matching():
    pass

def tapped_cap_matching():
    pass

class UTTMatching(unittest.TestCase):
    def test_L(self):
        Q, L, C = L_matching(50, 250, 900, CIR_LP)
        self.assertTrue((Q - 2) < 1e-1)
        self.assertTrue((L - 17.684e-9) < 1e-11)
        self.assertTrue((C - 1.415e-12) < 1e-14)

        Q, L, C = L_matching(50, 250, 900, CIR_HP)
        self.assertTrue((Q - 2) < 1e-1)
        self.assertTrue((L - 22.105e-9) < 1e-11)
        self.assertTrue((C - 1.768e-12) < 1e-14)
    
        Q, L, C = L_matching(250, 100, 500, CIR_LP)
        self.assertTrue((Q - 1.22) < 1e-1)
        self.assertTrue((L - 38.985e-9) < 1e-11)
        self.assertTrue((C - 1.559e-12) < 1e-14)

        Q, L, C = L_matching(250, 100, 500, CIR_HP)
        self.assertTrue((Q - 1.22) < 1e-1)
        self.assertTrue((L - 64.975e-9) < 1e-11)
        self.assertTrue((C - 2.599e-12) < 1e-14)

if __name__ == "__main__":
    unittest.main()
