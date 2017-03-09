import numpy as np

TYPE_LP = 0
TYPE_HP = 1

def L_matching(Rs, Rl, f0, type):
    '''
    Rs: source resistor
    Rl: load resistor
    f0: central frequency(MHz)
    type: circuit type
    '''
    w0 = (f0 * (10 ** 6)) * (2 * np.pi) 
    if type == TYPE_LP:
        if Rl > Rs:
            Q = np.sqrt((Rl / Rs) - 1 )
            C = Q / (w0 * Rl)
            L = (1 / ((w0 ** 2) * C)) * ((Q ** 2) / (1 + (Q ** 2)))
            return Q, L, C
        elif Rl < Rs:
            Q = np.sqrt((Rs / Rl) - 1)
            L = (Q * Rl) / w0
            C = (1 / ((w0 ** 2) * L)) * ((Q ** 2) / (1 + (Q ** 2)))
            return Q, L, C
        else:
            return 0, 0, 0
    elif type == TYPE_HP:
        if Rl > Rs:
            Q = np.sqrt((Rl / Rs) - 1)
            L = Rl / (w0 * Q)
            C = (1 / ((w0 ** 2) * L)) * (1 + 1 / (Q ** 2))
            return Q, L, C 
        elif Rl < Rs:
            Q = np.sqrt((Rs / Rl) - 1)
            C = 1 / (w0 * Q * Rl)
            L = (1 / ((w0 ** 2) * C)) * (1 + 1 / (Q ** 2))
            return Q, L, C
    else:
        return 0, 0, 0
        
def pi_matching(Rs, Rl, f0, maxQ):
    pass

def T_matching():
    pass

def tapped_cap_matching():
    pass
