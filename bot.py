from pyautogui import *
import pyautogui
import time
import random
import pytesseract
import ctypes, time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Presses a key
def KeyPress(key):
    PressKey(key)
    time.sleep(.05)
    ReleaseKey(key) 

# double press a key
def doubleKeyPress(key1,key2):
    PressKey(key1)
    PressKey(key2)
    time.sleep(0.2)
    ReleaseKey(key1)
    ReleaseKey(key2)

# finds the location of an image on the screen and returns the coordinates
def find(pic, timeout = 5):
    count = 0
    while True:
        print('looking for it..')
        sleep(0.1)
        try:
            position = pyautogui.locateOnScreen(pic, confidence=0.85) 
            print('found it')
            return position
        except:
            count +=1
            if(count >= timeout):
                return False
            sleep(0.5)

# Restarts the game
def restartGame():
    sleep(0.2)
    print("shifttab")
    doubleKeyPress(0x2A,0x0F)
    sleep(1)
    click(find('lc/resolution.png'))
    sleep(1)
    click(find('lc/resolution2.png'))
    sleep(1)
    click(find('lc/restart.png'))
    sleep(1)
    click(find('lc/keep.png',10))

# Loots ressources from the cart
def lootCart():
    sleep(0.2)
    click(find('lc/cart.png'))
    sleep(0.3)
    click(find('lc/collect.png'))
    sleep(0.1)
    click(find('lc/x.png'))

# Finds a match
def findmatch():
    sleep(0.2)
    click(find('lc/builderattack.png'))
    sleep(0.3)
    click(find('lc/builderattack2.png'))

# deploys units in specific locations
def attack():
    pos = [[870,444],[1070,444],[1070,640],[870,640],[680,500],[1000,250],[1250,450],[1000,700],[700,700],[650,240],[1300,230],[1250,750],[930,875],[350,490],[1000,125],[1600,469],[1620,469],[1600,500]]
    sleep(1)
    KeyPress(0x02)
    for x in pos:
        click(x)
        sleep(random.uniform(0.2,0.4))
    KeyPress(0x10)
    click((1600,600))
    click((1600,400))

# current game loop
while True:
    sleep(1)
    lootCart()
    findmatch()
    find('lc/boost.png')
    attack()
    restartGame()
    sleep(4)
    find('lc/shop.png',15)

# matchmaking
def clouding():
    total = 0
    while total < 750000:
        print('lf next..')
        sleep(0.1)
        try:
            png = pyautogui.locateOnScreen('next.png', confidence=0.9) 
            print('found it')
            pyautogui.click(png)
            sleep(3)
             ##    attempt to read gold and elixir
            gold = pyautogui.screenshot(('gold.png'),region=(80,125,120,30))
            elixir = pyautogui.screenshot(('elixir.png'),region=(80,172,120,30))
            print('screenie')
            sleep(4)

            gold = ('gold.png')
            elixir = ('elixir.png')
            # Convert the image to grayscale
            g = pytesseract.image_to_string(gold, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            e = pytesseract.image_to_string(elixir, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            g = g.replace(' ','')
            g = g.replace('.','')
            g = g.replace(',','')
            e = e.replace(' ','')
            e = e.replace('.','')
            e = e.replace(',','')
            print(g)
            print(e)
            total = int(e) + int(g)
            print('gold : ' + g)
            print('elixir : ' + e)
        except:
            print('where is it?')
            sleep(0.5)
    attack()