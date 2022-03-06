

def pwv(zwd:float, tm:float) -> float:
    ri_v = 997
    r_v = 461.495
    k2 = 22.97
    k3 = 375463
    Pi = 1e8 / (ri_v*r_v*(k3/tm)+k2)
    return zwd * Pi