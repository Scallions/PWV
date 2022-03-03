


def ztd(lon:float,lat:float,h:float,year:int,doy:int,hour:int,zwd_model:str="Gtrop", zhd_model:str="SAAS") -> float:
    """使用相应的模型计算ztd

    Args:
        lon (float): 经度
        lat (float): 纬度
        h (float): 高度
        year (int): 年
        doy (int): 年积日
        hour (int): 小时24制
        zwd_model (str, optional): zwd模型可选有:GPT3,Gtrop. Defaults to "Gtrop".
        zhd_model (str, optional): ztd模型可选有:SAAS. Defaults to "SAAS".

    Returns:
        float: 计算所得ztd
    """
    pass


def gpsztd(sitename: str):
    """gps的ztd
    """
    pass

def test():
    pass