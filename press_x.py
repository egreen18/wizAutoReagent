import pyautogui as auto
import time
from tools import checkGen, loadTemplates, osResGen
os_res = osResGen()
templates = loadTemplates(os_res)
runtime = 10000
now = time.time()
while time.time() < now+runtime:
    if checkGen(templates['in_client']):
        auto.press('x')