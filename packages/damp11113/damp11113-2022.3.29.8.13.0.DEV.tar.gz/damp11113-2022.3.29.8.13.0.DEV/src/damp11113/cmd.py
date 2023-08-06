import os

class color():
    def __init__(self) -> None:
        pass

    def black(self):
        os.system('color 0')
    def blue(self):
        os.system('color 1')
    def green(self):
        os.system('color 2')
    def Aqua(self):
        os.system('color 3')
    def red(self):
        os.system('color 4')
    def purple(self):
        os.system('color 5')
    def yellow(self):
        os.system('color 6')
    def white(self):
        os.system('color 7')
    def gray(self):
        os.system('color 8')
    def lightblue(self):
        os.system('color 9')
    def lightgreen(self):
        os.system('color a')
    def lightaqua(self):
        os.system('color b')
    def lightred(self):
        os.system('color c')
    def lightpurple(self):
        os.system('color d')
    def lightyellow(self):
        os.system('color e')
    def lightwhite(self):
        os.system('color f')

def title(title):
    os.system(f'title {title}')

def pause():
    os.system('pause')

def cexit():
    os.system('exit')

def clear():
    os.system('cls')

def size(x, y):
    os.system('mode con: cols={} lines={}'.format(x, y))

def cmd(command='echo hello world!'):
    return os.system(command)