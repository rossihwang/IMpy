import unittest
import numpy as np

CIR_LP = 0
CIR_HP = 1

def L_matching(Rs, Rl, f0, tp):
    '''
    Rs: Source resistor
    Rl: Load resistor
    f0: Central frequency(MHz)
    tp: Circuit type
    
    return: Q, L, C
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

def pi_matching(Rs, Rl, f0, dsrQ, tp):
    '''
    Rs: Source resistor
    Rl: Load resistor
    f0: Central frequency(MHz)
    dsrQ: Desired Q
    tp: Circuit type

    high pass, return Q, L1, L2, C1. low pass return Q, L1, C1, C2
    '''
    w0 = (f0 * (10 ** 6)) * (2 * np.pi) 
    if Rs < Rl:
        Q1 = dsrQ
        Rint = Rl / (1+Q1**2)  # Rint: intermediate resistor
        Q2 = np.sqrt(Rs/Rint - 1)
        X2 = Rint * (Q1 + Q2)
        B1 = Q1/Rl
        B3 = Q2/Rs
        if tp == CIR_LP:
            return dsrQ, (X2 / w0), (B3 / w0), (B1 / w0) 
        elif tp == CIR_HP:
            return dsrQ, ((1 / B3) / w0), ((1 / B1) / w0), ((1 / X2) / w0)
    elif Rs > Rl:
        Q2 = dsrQ
        Rint = Rs / (1+Q2**2)
        Q1 = np.sqrt(Rl/Rint - 1)
        X2 = Rint * (Q1 + Q2)
        B1 = Q1 / Rl
        B3 = Q2 / Rs
        if tp == CIR_LP:
            return dsrQ, (X2 / w0), (B3 / w0), (B1 / w0)
        elif tp == CIR_HP:
            return dsrQ, ((1 / B3) / w0), ((1 / B1) / w0), ((1 / X2) / w0)
    else:
        return 0, 0, 0, 0

def T_matching(Rs, Rl, f0, dsrQ, tp):
    '''
    Rs: Source resistor
    Rl: Load resistor
    f0: Central frequency(MHz)
    dsrQ: Desired Q
    tp: Circuit type

    high pass, return Q, L1, C1, C2. low pass, return Q, L1, L2, C1
    '''
    w0 = (f0 * (10 ** 6)) * (2 * np.pi)
    if Rs > Rl:
        Q1 = dsrQ
        Rint = Rl * (1 + Q1**2)
        Q2 = np.sqrt(Rint/Rs - 1)
        X1 = Q1 * Rl
        B2 = (Q1 + Q2) / Rint
        X3 = Q2 * Rs
        if tp == CIR_LP:
            return dsrQ, (X3 / w0), (X1 / w0), (B2 / w0) 
        elif tp == CIR_HP:
            return dsrQ, ((1 / B2) / w0), ((1 / X3) / w0), ((1 / X1) / w0)
    elif Rs < Rl:
        Q2 = dsrQ
        Rint = Rs * (1 + Q2**2)
        Q1 = np.sqrt(Rint/Rl - 1)
        X1 = Q1 * Rl
        B2 = (Q1 + Q2) / Rint
        X3 = Q2 * Rs
        if tp == CIR_LP:
            return dsrQ, (X3 / w0), (X1 / w0), (B2 / w0) 
        elif tp == CIR_HP:
            return dsrQ, ((1 / B2) / w0), ((1 / X3) / w0), ((1 / X1) / w0)
    else:
        return 0, 0, 0, 0

def tapped_cap_matching(Rs, Rl, f0, dsrQ):
    '''
    Rs: Source resistor
    Rl: Load resistor
    f0: Central frequency(MHz)
    bw: Bandwidth(MHz)

    return Q1, L, C1, C2
    '''
    w0 = (f0 * (10 ** 6)) * (2 * np.pi)
    L = Rs / (w0 * dsrQ)
    Qp = np.sqrt((Rl / Rs) * (1 + dsrQ ** 2) - 1)
    C2 = Qp / (w0 * Rl)
    Ceq = (C2 * (1 + Qp ** 2)) / (Qp ** 2)
    C1 = (Ceq * C2) / (Ceq - C2)
    return dsrQ, L, C1, C2

class UTTMatching(unittest.TestCase):
    
    def test_L(self):
        Q, L, C = L_matching(50, 250, 900, CIR_LP)
        self.assertTrue(np.abs(Q - 2) < 1e-1)
        self.assertTrue(np.abs(L - 17.684e-9) < 1e-11)
        self.assertTrue(np.abs(C - 1.415e-12) < 1e-14)

        Q, L, C = L_matching(50, 250, 900, CIR_HP)
        self.assertTrue(np.abs(Q - 2) < 1e-1)
        self.assertTrue(np.abs(L - 22.105e-9) < 1e-11)
        self.assertTrue(np.abs(C - 1.768e-12) < 1e-14)
    
        Q, L, C = L_matching(250, 100, 500, CIR_LP)
        self.assertTrue(np.abs(Q - 1.22) < 1e-1)
        self.assertTrue(np.abs(L - 38.985e-9) < 1e-11)
        self.assertTrue(np.abs(C - 1.559e-12) < 1e-14)

        Q, L, C = L_matching(250, 100, 500, CIR_HP)
        self.assertTrue(np.abs(Q - 1.22) < 1e-1)
        self.assertTrue(np.abs(L - 64.975e-9) < 1e-11)
        self.assertTrue(np.abs(C - 2.599e-12) < 1e-14)

    def test_Pi(self):
        Q, L1, L2, C1 = pi_matching(50, 250, 100, 3, CIR_HP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 7.957e-8, delta=1e-10)
        self.assertAlmostEqual(L2, 1.326e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 1.591e-11, delta=1e-13)

        Q, L1, C1, C2 = pi_matching(50, 250, 100, 3, CIR_LP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 1.591e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 3.183e-11, delta=1e-13)
        self.assertAlmostEqual(C2, 1.909e-11, delta=1e-13)
        
        Q, L1, L2, C1 = pi_matching(250, 50, 100, 3, CIR_HP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 1.326e-7, delta=1e-9)
        self.assertAlmostEqual(L2, 7.957e-8, delta=1e-10)
        self.assertAlmostEqual(C1, 1.591e-11, delta=1e-13)

        Q, L1, C1, C2 = pi_matching(250, 50, 100, 3, CIR_LP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 1.591e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 1.909e-11, delta=1e-13)
        self.assertAlmostEqual(C2, 3.183e-11, delta=1e-13)
        
    def test_T(self):
        Q, L1, C1, C2 = T_matching(50, 250, 100, 3, CIR_HP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 1.989e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 1.061e-11, delta=1e-13)
        self.assertAlmostEqual(C2, 6.366e-12, delta=1e-14)

        Q, L1, L2, C1 = T_matching(50, 250, 100, 3, CIR_LP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 2.387e-7, delta=1e-9)
        self.assertAlmostEqual(L2, 3.978e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 1.273e-11, delta=1e-13)
        
        Q, L1, C1, C2 = T_matching(250, 50, 100, 3, CIR_HP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 1.989e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 6.366e-12, delta=1e-14)
        self.assertAlmostEqual(C2, 1.061e-11, delta=1e-13)

        Q, L1, L2, C1 = T_matching(250, 50, 100, 3, CIR_LP)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L1, 3.978e-7, delta=1e-9)
        self.assertAlmostEqual(L2, 2.387e-7, delta=1e-9)
        self.assertAlmostEqual(C1, 1.273e-11, delta=1e-13)

    def test_tapped_cap(self):
        # cannot ensure the correctness
        Q, L, C1, C2 = tapped_cap_matching(50, 10, 100, 3)
        self.assertAlmostEqual(Q, 3, delta=1e-2)
        self.assertAlmostEqual(L, 2.652e-8, delta=1e-10)
        self.assertAlmostEqual(C1, 3.183e-10, delta=1e-12)
        self.assertAlmostEqual(C2, 1.591e-10, delta=1e-12)

if __name__ == "__main__":
    unittest.main()
