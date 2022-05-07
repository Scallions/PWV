
from gps.ztd.zhd.saas import saas




print(saas(68, 987, 56))


from gps.libs.config import Config

cfg = Config("config.yml")
print(cfg.ZHD)
print(cfg.TM)


from gps.libs import manager


print(manager.TM_MODELS.components_dict)


tm = cfg.TM

print(tm.calc_tm(lat=68, lon=-40, doy=125, year=2015, h=2671))

from gps.tm import GPT3

print(GPT3.calc_tm(lat=68, lon=-40, doy=125, year=2015, h=2671))


def download(file):
    pass


