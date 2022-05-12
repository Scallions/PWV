
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

import paddle

from model.dcgenerator import DCGenerator

b = 3
inp = paddle.randn([b,24,64])
gan = DCGenerator(2000, 24)
out = gan(inp)
# assert out.shape == [b,31,66]
# assert 1 == 1
print(out.shape)

from model.dcdiscriminator import DCDiscriminator


dis = DCDiscriminator(24)
# out = paddle.rand([3,24,64,64])
out, c = dis(out)
print(out.shape, c.shape)

# from data.pwv import PWVDataset

# data_dir = "/Volumes/HDD/Data/ztd/"

# ds = PWVDataset(data_dir + "all_r/pwv_1h_hz_grl_long_fill.csv", data_dir+"pwv.nc")

