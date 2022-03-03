
from gps.ztd.zhd.saas import saas




print(saas(68, 987, 56))

import yaml
from yaml import Loader

with open("config.yml") as f:

    cfg = yaml.load(f.read(), Loader=Loader)

print(cfg)