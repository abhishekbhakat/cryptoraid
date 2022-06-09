import sys
import time

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 


def tidy2():
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)

def tidy():
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)


def timer(sec = 0):
    for i in range(sec,0,-1):
        print("Timer : {:02d}".format(i), end='\r')
        time.sleep(1)