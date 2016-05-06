# -*- coding: utf-8 -*-
from GRFY.Crawler import *
import time

try:
    instance = GRFY(1)
    instance.crawler("http://sh.grfy.net/rent/list_2_0_0_0-0_0_0-0_0_2_0_1_.html")
except Exception,ex:
    print(ex)
