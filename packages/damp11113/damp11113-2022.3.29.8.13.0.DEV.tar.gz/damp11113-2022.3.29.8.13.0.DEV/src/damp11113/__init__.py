import time, sys
from time import sleep
from pygments import console
from datetime import datetime
from threading import Thread
import platform
import damp11113.randoms as rd
from numba import jit, cuda
import numpy as np
from cryptography.fernet import Fernet
import damp11113.file as file
from timeit import default_timer

class time_exception(Exception):
    pass

def grade(number):
    score = int(number)
    if score == 100:
        return "Perfect"
    elif score >= 100:
        return '0 - 100 only'
    elif score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "B+"
    elif score >= 80:
        return "B"
    elif score >= 75:
        return "C+"
    elif score >= 70:
        return "C"
    elif score >= 65:
        return "D+"
    elif score >= 60:
        return "D"
    elif score >= 55:
        return "E+"
    elif score >= 50:
        return "E"

    else:
        return "F"

def clock(display="%z %A %d %B %Y  %p %H:%M:%S"):
    x = datetime.now()
    clock = x.strftime(display) #"%z %A %d %B %Y  %p %H:%M:%S"
    sleep(1)
    return clock

def check(list, use):
    if use in list:
        print(f'[{console.colorize("green", "✔")}] {use}')
        rech = 'True'

    else:
        print(f'[{console.colorize("red", "❌")}] {use}')
        rech = 'False'
    return rech

def sec2mph(sec):
    return (sec * 2.2369)

def str2bin(s):
    return ''.join(format(ord(x), '08b') for x in s)

def bin2str(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def typing(text, speed=0.3):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)

def timestamp():
    now = datetime.now()
    return datetime.timestamp(now)

def encryptext(text, key):
    f = Fernet(bytes(key))
    return f.encrypt(text.encode())

def decryptext(text, key):
    f = Fernet(bytes(key))
    return f.decrypt(text.decode())

class timer():
    def __init__(self):
        self.start = None

    def start(self):
        if self.start is None:
            raise time_exception("Timer is running. use .stop() to stop it")
        self.start = time.time()

    def stop(self):
        if self.start is None:
            raise time_exception("Timer is not running. use .start() to start it")
        elapsed = time.perf_counter() - self.start
        self.start = None
        return elapsed

def list2str(list_):
    return '\n'.join(list_)

def str2list(string):
    return string.split('\n')

def str2int(string):
    return int(string)

def byte2str(b, decode='utf-8'):
    return b.decode(decode)

def sort_files(file_list):
    return sorted(file_list, key=lambda x: int(x.split('.')[0]))

def full_cpu(min=100, max=10000, speed=0.000000000000000001):
    _range = rd.rannum(min, max)
    class thread_class(Thread):
        def __init__(self, name, _range):
            Thread.__init__(self)
            self.name = name
            self.range = _range
        def run(self):
            for i in range(self.range):
                print(f'{self.name} is running')
    for i in range(_range):
        name = f'Thread {i}/{_range}'
        thread = thread_class(name, _range)
        thread.start()
        sleep(speed)

def full_gpu(min=100, max=10000, speed=0.000000000000000001):
    _range = rd.rannum(min, max)
    def func(_range):
        for i in range(_range):
            _range[i] += 1

    @jit(target='cuda')
    def func2(_range):
        for i in range(_range):
            _range[i] += 1

    try:
        n = _range
        a = np.arange(n, dtype=np.int64)
        b = np.arange(n, dtype=np.int64)

        start = default_timer()
        func(a)
        end = default_timer()-start

        start2 = default_timer()
        func2(b)
        end2 = default_timer()-start2
        print(f'without GPU: {end} | with GPU: {end2}')
        sleep(speed)
    except:
        pass

def full_disk(min=100, max=10000,speed=0.000000000000000001):
    ra = rd.rannum(min, max)
    for i in range(ra):
        file.createfile('test.txt')
        file.writefile2('test.txt', 'test')
        file.readfile('test.txt')
        file.removefile('test.txt')
        sleep(speed)
        print(f'{i}/{ra}')

def copyright():
    print('Copyright (c) 2021-2022 damp11113'
          '\nAll rights reserved.'
          '\n '
          '\nMIT License'
          '\n '
          '\nPermission is hereby granted, free of charge, to any person obtaining a copy'
          '\nof this software and associated documentation files (the "Software"), to deal'
          '\nin the Software without restriction, including without limitation the rights'
          '\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell'
          '\ncopies of the Software, and to permit persons to whom the Software is'
          '\nfurnished to do so, subject to the following conditions:'
          '\n '
          '\nThe above copyright notice and this permission notice shall be included in all'
          '\ncopies or substantial portions of the Software.'
          '\n '
          '\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR'
          '\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,'
          '\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE'
          '\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER'
          '\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,'
          '\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE'
          '\nSOFTWARE.')
    return 'Copyright (c) 2021-2022 damp11113 All rights reserved. (MIT License)'

def pyversion(fullpython=False, fullversion=False, tags=False, date=False, compiler=False, implementation=False, revision=False):
    if fullpython:
        return f'python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} {sys.version_info.releaselevel} {platform.python_build()[0]} {platform.python_build()[1]} {platform.python_compiler()} {platform.python_implementation()} {platform.python_revision()}'
    if fullversion:
        return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    if tags:
        return platform.python_build()[0]
    if date:
        return platform.python_build()[1]
    if compiler:
        return platform.python_compiler()
    if implementation:
        return platform.python_implementation()
    if revision:
        return platform.python_revision()
    return f'{sys.version_info.major}.{sys.version_info.minor}'

def osversion(fullos=False, fullversion=False, type=False, cuser=False, processor=False):
    if fullos:
        return f'{platform.node()} {platform.platform()} {platform.machine()} {platform.architecture()[0]} {platform.processor()}'
    if fullversion:
        return f'{platform.system()} {platform.version()}'
    if type:
        return platform.architecture()[0]
    if cuser:
        return platform.node()
    if processor:
        return platform.processor()

    return platform.release()

