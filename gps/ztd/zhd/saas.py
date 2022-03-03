



import math


def saas(lat:float, ps:float, h:float)->float:
    """saas zhd模型，使用地面气压和高程计算zhd，精度mm级
                        0.0022768*p
    zhd = ---------------------------------------
            1-0.00266*cos(2\shai)-0.28*10**-6*h
    Args:
        lat (float): 纬度
        ps (float): 地面气压
        h (float): 地面高程大地高

    Returns:
        float: zhd
    """
    return (0.0022768*ps)/(1-0.00266*math.cos(2*lat)-0.28*10**-6*h)