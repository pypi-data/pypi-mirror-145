import os
from mcstatus import *
import json
import requests
import damp11113.network as network
import damp11113.file as file
import sys



class mcstatus_exception(Exception):
    pass

class uuid2name_exception(Exception):
    pass

class server_exeption(Exception):
    pass

class install_exception(Exception):
    pass

#------------------------server------------------------------

def mcserver(server, local='./', java='java', ramuse='1024'):
    try:
        print("Server started.")
        os.chdir(local)
        os.system(f'{java} -Xms{ramuse}M -Xmx{ramuse}M -jar {server}.')
        print("Server stopped.")
    except Exception as e:
        raise server_exeption(e)

#------------------get-uuid2name------------------

class uuid2name:
    def __init__(self) -> None:
        pass

    def getmcuuid(self, player_name):
        try:
            r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}")
            if r.text == '':
                raise uuid2name_exception(f"{player_name} not found")
            else:
                return json.loads(r.text)['id']
        except Exception as e:
            raise uuid2name_exception(e)

    def getmcname(self, player_uuid):
        try:
            r = requests.get(f"https://api.mojang.com/user/profiles/{player_uuid}/names")
        except Exception as e:
            raise uuid2name_exception(e)
        try:
            o = json.loads(r.text)[0]['name']
            return o
        except KeyError:
            raise uuid2name_exception(f"player not found")

    def getmcnamejson(self, player_uuid):
        try:
            return requests.get(f"https://api.mojang.com/user/profiles/{player_uuid}/names").text
        except Exception as e:
            raise uuid2name_exception(f"get mc name error: {e}")

    def getmcuuidjson(self, player_name):
        try:
            return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").text
        except Exception as e:
            raise uuid2name_exception(f"get mc uuid error: {e}")

#----------------------mcstatus------------------------

class mcstatus():
    def __init__(self, ip):
        self.server = MinecraftServer.lookup(ip)

    def raw(self):
        try:
            return self.server.status().raw
        except Exception as e:
            raise mcstatus_exception(f"raw mc status error: {e}")

    def players(self):
        try:
            return self.server.status().players
        except Exception as e:
            raise mcstatus_exception(f"players mc status error: {e}")

    def favicon(self):
        try:
            return self.server.status().favicon
        except Exception as e:
            raise mcstatus_exception(f"favicon mc status error: {e}")

    def description(self):
        try:
            return self.server.status().description
        except Exception as e:
            raise mcstatus_exception(f"description mc status error: {e}")

    def version(self):
        try:
            return self.server.status().version
        except Exception as e:
            raise mcstatus_exception(f"version mc status error: {e}")

    def ping(self):
        try:
            return self.server.ping()
        except Exception as e:
            raise mcstatus_exception(f"ping mc status error: {e}")

    def query_raw(self):
        try:
            return self.server.query().raw
        except Exception as e:
            raise mcstatus_exception(f"query raw mc status error: {e}")

    def query_players(self):
        try:
            return self.server.query().players
        except Exception as e:
            raise mcstatus_exception(f"query players mc status error: {e}")

    def query_map(self):
        try:
            return self.server.query().map
        except Exception as e:
            raise mcstatus_exception(f"query map mc status error: {e}")

    def query_motd(self):
        try:
            return self.server.query().motd
        except Exception as e:
            raise mcstatus_exception(f"query motd mc status error: {e}")

    def query_software(self):
        try:
            return self.server.query().software
        except Exception as e:
            raise mcstatus_exception(f"query software mc status error: {e}")


# -----------------------install----------------------------

class install_server():
    def __init__(self) -> None:
        pass

    def paper(self, version, builds, file):
        try:
            network.loadfile(f'https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{builds}/downloads/{file}', file)
            mcserver('/', file, 'java', '1024')
            file.writefile2('eula.txt', 'eula=true')
            print("Paper installed.")
        except Exception as e:
            raise install_exception(f"install paper error: {e}")
        
    def spigot(self, version):
        try:
            network.loadfile(f'https://download.getbukkit.org/spigot/spigot-{version}.jar', f'spigot-{version}.jar')
            mcserver('/', f'spigot-{version}.jar', 'java', '1024')
            file.writefile2('eula.txt', 'eula=true')
            print("Spigot installed.")
        except Exception as e:
            raise install_exception(f"install spigot error: {e}")

class install_loader():
    def __init__(self) -> None:
        pass

    def forge(self, version):
        try:
            network.loadfile(f'https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar', f'forge-{version}-installer.jar')
            os.system(f'java -jar forge-{version}-installer.jar --installClient')
            print(f"Forge {version} installed.")
        except Exception as e:
            raise install_exception(f"install forge error: {e}")

    def fabric(self, loaderversion):
        try:
            network.loadfile(f'https://maven.fabricmc.net/net/fabricmc/fabric-installer/{loaderversion}/fabric-installer-{loaderversion}.jar', f'fabric-installer-{loaderversion}.jar')
            os.system('java -jar fabric-installer-0.10.2.jar')
            print(f"Fabric {loaderversion} installed.")
        except Exception as e:
            raise install_exception(f"install fabric error: {e}")

def install_optifine(version):
    try:
        network.loadfile(f'https://optifine.net/downloadx?f={version}.jar&x=c034c1658159573187673e5157b8d593', f'{version}.jar')
        os.system('java -jar OptiFine_1.8.9_HD_U_F5.jar')
        print(f"Optifine {version} installed.")
    except Exception as e:
        raise install_exception(f"install optifine error: {e}")


class install_mods():
    def __init__(self) -> None:
        pass

    def download(self, mod):
        try:
            loading = '|'
            load = requests.get(f'https://www.curseforge.com/minecraft/mc-mods/{mod}/files', stream=True)
            for chunk in load.iter_content(chunk_size=1024):
                if chunk:
                    with open(f'{mod}.jar', 'wb') as f:
                        f.write(chunk)
                        sys.stdout.write(loading+'|')
                        sys.stdout.flush()
            sys.stdout.write('download complete!')
            sys.stdout.flush()
        except Exception as e:
            raise install_exception(f"download mod error: {e}")
