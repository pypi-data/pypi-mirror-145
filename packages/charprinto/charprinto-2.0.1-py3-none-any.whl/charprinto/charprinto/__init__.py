__version__ = '2.0.1'
from termcolor import colored
import cursor
import sys
import os
from time import sleep
def charprint(string, color, cursorused=True, end="\n"):
        if cursorused == True:
            cursor.show()
        for i in string:
            sys.stdout.write(colored(i, color=color))
            sys.stdout.flush()
        sys.stdout.write(end)
        sys.stdout.flush()
        if cursorused == True:
            cursor.hide()
def charinput(string, color, cursorused=True, end="\n"):
        charprint(string, color, cursorused=cursorused, end=end)
        return input("")
def blanket():
        os.system("clear")
        for i in range(3):
            for f in range(3):
                sys.stdout.write("#")
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()
        sleep(3)
        os.system("clear")

charprint = charprint
charinput = charinput
blanket = blanket