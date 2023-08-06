from pygments import console
import requests
import damp11113

list = ['grade', 'clock', 'title', 'rannum', 'ranstr', 'ranuuid', 'mcserver', 'ip_port_check', 'ddos_attack', 'readtextweb',
        'loadfile', 'installpackage', 'readfile', 'readfileline', 'movefile', 'movefolder', 'copyfile', 'copyfolder', 'removefile', 'removefolder',
        'renamefile', 'renamefolder', 'createfolder', 'createfile', 'writefile', 'writefileline', 'openurl', 'appendfile', 'appendfileline', 'openfile'
        'runfile', 'runpy', 'runjs', 'runjava', 'runbash', 'runcpp', 'runc', 'runphp', 'runruby', 'runperl', 'rungo', 'sendtext', 'sendfile',
        'mqtt_publish', 'tcp_send', 'udp_send', 'mqtt_subscribe', 'tcp_receive', 'udp_receive', 'runngrok', 'flask_run', 'flask_run_debug', 'flask_run_ssl',
        'flask_run_debug_ssl', 'runwebshell', 'runwebshell_debug', 'runwebshell_ssl', 'runwebshell_debug_ssl', 'killngrok', 'killflask', 'killwebshell',
        'cnd', 'runvim', 'runnano', 'rungedit', 'runkate', 'kill', 'ytload', 'writefile2', 'unzip', 'comzip', 'clear', 'size', 'color',
        'ranchoice', 'ranchoices', 'ranshuffle', 'ranuniform', 'ranrandint', 'ranrandrange', 'encrypt', 'decrypt', 'rankeygen', 'vlc_player',
        'mcstatus', 'cexit', 'pause', 'bin2str', 'str2bin', 'binary_send', 'binary_receive', 'typing', 'line_notify', 'timestamp','uuid2name', 'sound_receive',
        'sound_send', 'decryptext', 'encryptext', 'install_server', 'install_loader', 'install_optifine', 'install_mods', 'timer', 'ffmpeg_stream',
        'writefile3', 'sizefolder', 'sizefile', 'list2str', 'byte2str', 'full_cpu', 'full_gpu', 'file_receive', 'file_send', 'writejson',
        'full_disk', 'byte2str', 'str2int', 'str2list', 'clip2frames', 'getallfolders', 'getallfiles', 'sort_files', 'ardstatus', 'sec2mph', 'pyversion',
        'osversion', 'im2pixel']

ip = 'http://localhost'
__version__ = 'V2022.3.29.8.13.0 DEV' # 2022/03/29 | 8 file (no check) | 130 function | dev version

def vercheck():
    try:
        response = requests.get(f"{ip}/api/damp11113%20library/ver.txt")
        if response.status_code == 404:
            return False
        elif response.status_code == 200:
            if response.text == __version__:
                return True
            else:
                return False
        else:
            return False
    except:
        return False
def info(fullname=False, fullversion=False, funcscount=False, funcslist=False, copyright=False, author=False):
    if fullname:
        return f'damp11113 library | {__version__} | author damp11113 | Copyright (c) 2021-2022 damp11113 All rights reserved. (MIT License) | {len(list)} functions |'
    if fullversion:
        return f'{__version__}'
    if funcscount:
        return f'{len(list)}'
    if funcslist:
        return f'{list}'
    if copyright:
        return f'Copyright (c) 2021-2022 damp11113 All rights reserved. (MIT License)'
    if author:
        return f'damp11113'
    return f'damp11113  {__version__}'

def defcheck(use):
    if use in list:
        print(f'[{console.colorize("green", "✔")}] {use}')
        rech = True

    else:
        print(f'[{console.colorize("red", "❌")}] {use}')
        rech = False
    return rech


print(console.colorize("yellow", "SDK check update..."))
try:
    response = requests.get(f"{ip}/api/damp11113%20library/ver.txt")
    if response.status_code == 404:
        print(f'{console.colorize("red", "check update failed. please try again")}')
        print(f'{console.colorize("yellow", f"version: {__version__}")}')
    elif response.status_code == 200:
        if response.text == __version__:
            print(f'{console.colorize("green", "no update available")}')
            print(f'{console.colorize("green", f"SDK version: {__version__}")}')
        else:
            print(console.colorize("yellow", "update available"))
            print(f'{console.colorize("yellow", f"version: {__version__}")}')
            print(f'{console.colorize("green", f"new: {response.text}")}')
    else:
        pass

except:
    print(console.colorize("red", "check update failed. please try again"), f'{__version__}')
