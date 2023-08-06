import os
import shutil
import zipfile
import json
from cryptography.fernet import Fernet

#-----------------------------read---------------------------------------

def readfile(file):
    with open(file, 'r') as f:
        return f.read()

def readfileline(file, line):
    with open(file, 'r') as f:
        return f.readlines()[line]

#-----------------------------move---------------------------------------

def movefile(file, to):
    shutil.move(file, to)

def movefolder(folder, to):
    shutil.move(folder, to)

#-----------------------------copy---------------------------------------

def copyfile(file, to):
    shutil.copy(file, to)

def copyfolder(folder, to):
    shutil.copytree(folder, to)

#-----------------------------remove--------------------------------------

def removefile(file):
    os.remove(file)

def removefolder(folder):
    shutil.rmtree(folder)

#-----------------------------renamefile-----------------------------------

def renamefile(file, to):
    os.rename(file, to)

def renamefolder(folder, to):
    os.rename(folder, to)

#----------------------------------create-----------------------------------

def createfolder(folder):
    os.mkdir(folder)

def createfile(file):
    open(file, 'a').close()

#----------------------------------write------------------------------------

def writefile(file, data):
    with open(file, 'a') as f:
        f.write(data + '\n')
        f.close()

def writefile2(file, data):
    with open(file, 'w') as f:
        f.write(data)
        f.close()

def writefile3(file, data):
    with open(file, 'a') as f:
        f.write(data)
        f.close()

def writefileline(file, line, data):
    with open(file, 'r') as f:
        lines = f.readlines()
        lines[line] = data
        with open(file, 'w') as f:
            f.writelines(lines)

def writejson(file, data):
    with open(file, 'r+') as f:
        _data = json.load(f)
        _data.update(data)
        f.seek(0)
        json.dump(_data, f, indent=4)


#----------------------------------append-----------------------------------

def appendfile(file, data):
    with open(file, 'a') as f:
        f.write(data)

def appendfileline(file, line, data):
    with open(file, 'r') as f:
        lines = f.readlines()
        lines[line] = data
        with open(file, 'a') as f:
            f.writelines(lines)

#---------------------------------------open---------------------------------

def openfile(ide, file):
    os.system(f"{ide} {file}")

#---------------------------------------run---------------------------------

def runfile(file):
    os.system(f"start {file}")

def runpy(file):
    os.system(f"python {file}")

def runjs(file):
    os.system(f"node {file}")

def runjava(file):
    os.system(f"java {file}")

def runbash(file):
    os.system(f"bash {file}")

def runcpp(file):
    os.system(f"g++ {file}")

def runc(file):
    os.system(f"gcc {file}")

def runphp(file):
    os.system(f"php {file}")

def runruby(file):
    os.system(f"ruby {file}")

def rungo(file):
    os.system(f"go {file}")

def runperl(file):
    os.system(f"perl {file}")

def rundocker(file):
    os.system(f"docker {file}")

def runvim(file):
    os.system(f"vim {file}")

def runnano(file):
    os.system(f"nano {file}")

def rungedit(file):
    os.system(f"gedit {file}")

def runkate(file):
    os.system(f"kate {file}")

#--------------------------------------kill---------------------------------

def kill(file):
    os.system(f"taskkill /f /im {file}")

#--------------------------------------zip----------------------------------

def unzip(file, to):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(to)

def comzip(file, to):
    with zipfile.ZipFile(file, 'w') as zip_ref:
        zip_ref.write(to)

#--------------------------------------encrypt----------------------------------

def encrypt(file, password):
    with open(file, 'rb') as f:
        data = f.read()
    fernet = Fernet(bytes(password))
    encrypted = fernet.encrypt(data)
    with open(file, 'wb') as f:
        f.write(encrypted)

def decrypt(file, password):
    with open(file, 'rb') as f:
        data = f.read()
    fernet = Fernet(bytes(password))
    decrypted = fernet.decrypt(data)
    with open(file, 'wb') as f:
        f.write(decrypted)

#----------------------------------size------------------------------------

def sizefile(file):
    size = 0

    for path, dirs, files in os.walk(file):
        for f in files:
            size += os.path.getsize(os.path.join(path, f))

    return size / 1000000

def sizefolder(folder):
    size = 0

    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)

    return size / 1000000

#----------------------------------all-------------------------------------

def allfiles(folder):
    return os.listdir(folder)
