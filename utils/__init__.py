import sys
from beepy import beep

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 


def tidy2():
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)

def doublebeep():
    beep(sound=1)
    beep(sound='coin')