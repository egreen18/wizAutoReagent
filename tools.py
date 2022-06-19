import mss
import numpy as np
import cv2
import time
import pyautogui as auto
import os.path as os
import platform

def mssMon(shape):
    # Takes a resolution in the form of a 1,4 list and prepares it for input into mss screenshot function
    mon = {"top": shape[1], "left": shape[0], "width": shape[2]-shape[0], "height": shape[3]-shape[1]}
    return mon

def osResGen():
    os_res = ''
    res_val = auto.size()
    if platform.system() == 'Darwin':
        os_val = 'mac'
    elif platform.system() == 'Windows':
        os_val = 'pc'
    else:
        os_val = ''
    os_res = '_'.join([os_val, str(res_val[0])])
    return os_res

def loadTemplates(os_res):
    # This function loads game recognition templates into the workspace
    # Loading templates
    tpl_in_client = cv2.imread(os.join('templates', os_res, 'in_client_tpl.png'))        # (1772 886 1920 1080)

    # Converting to grayscale for cv2 processing
    tpl_in_client = cv2.cvtColor(np.array(tpl_in_client), cv2.COLOR_BGR2GRAY)

    templates = {
        'in_client': tpl_in_client,
    }
    return templates

def tplComp(image, tpl):
    # This function compares template and image to identify in game components
    # Perform match operations.
    res = cv2.matchTemplate(image, tpl, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.8

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # If matched area coordinates exist, arrow is identified. Return positive
    if len(loc[0]) > 0:
        return 1
    else:
        return 0

def checkGen(tpl):
    # This function takes a screenshot and calls tplComp to identify one template
    # Pulling screenshot
    with mss.mss() as sct:
        pic = sct.grab(sct.monitors[1])

    # Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    # Checking arrows against templates
    if tplComp(pic, tpl):
        identified = 1
    else:
        identified = 0

    return identified

def button(coords):
    auto.moveTo(coords)
    time.sleep(0.1)
    auto.click()
    time.sleep(0.1)

def jiggle():
    # Jiggles mouse to reactivate some buttons
    pos = auto.position()

    auto.moveTo((pos[0] + 2, pos[1] + 2))
    time.sleep(0.05)
    auto.moveTo((pos[0], pos[1]))

def pressX(templates, now, runtime):
    while time.time() < now+runtime:
        if checkGen(templates['in_client']):
            auto.press('x')

def autoReagent(runtime):
    # Initialization steps
    os_res = osResGen()
    if not os_res:
        print('Your OS and resolution combination has not been configured. Terminating.')
        return
    templates = loadTemplates(os_res)
    now = time.time()
    pressX(templates, now, runtime)
