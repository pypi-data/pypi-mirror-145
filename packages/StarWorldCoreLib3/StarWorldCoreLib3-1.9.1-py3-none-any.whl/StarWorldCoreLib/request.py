"""
 ____  _           __        __         _     _  ____               _     _ _    _____       ____                            _   
/ ___|| |_ __ _ _ _\ \      / /__  _ __| | __| |/ ___|___  _ __ ___| |   (_) |__|___ /      |  _ \ ___  __ _ _   _  ___  ___| |_ 
\___ \| __/ _` | '__\ \ /\ / / _ \| '__| |/ _` | |   / _ \| '__/ _ \ |   | | '_ \ |_ \ _____| |_) / _ \/ _` | | | |/ _ \/ __| __|
 ___) | || (_| | |   \ V  V / (_) | |  | | (_| | |__| (_) | | |  __/ |___| | |_) |__) |_____|  _ <  __/ (_| | |_| |  __/\__ \ |_ 
|____/ \__\__,_|_|    \_/\_/ \___/|_|  |_|\__,_|\____\___/|_|  \___|_____|_|_.__/____/      |_| \_\___|\__, |\__,_|\___||___/\__|
                                                                                                          |_|                       
"""
import requests
from json import loads

class request:
    """
    StarWorldCoreLib3 Request.
    """
    class post:
        """
        Send POST request.
        """
        def __init__(self,url,data={},headers={'userAgent':'StarWorldCoreLib3-Request'},stream=False) -> None:
            """
            Initialize POST request.
            """
            self.__url = url
            self.urlio = requests.post(self.__url,data=data,headers=headers,stream=stream)
            self.content = self.urlio.content
            self.text = self.urlio.text
            self.json = lambda:loads(self.urlio.content)
            self.status_code = self.urlio.status_code
        def __del__(self) -> None:
            """
            Delete POST request.
            """
            self.urlio.close()
        def __repr__(self) -> str:
            """
            Repeat POST request.
            """
            return str("<"+"Post"+" "+str(self.__url)+" "+str(self.status_code)+">")
    class get:
        """
        Send GET request.
        """
        def __init__(self,url,data={},headers={'userAgent':'StarWorldCoreLib3-Request'},stream=False) -> None:
            """
            Initialize GET request.
            """
            self.__url = url
            self.urlio = requests.get(self.__url,data=data,headers=headers,stream=stream)
            self.content = self.urlio.content
            self.text = self.urlio.text
            self.json = lambda:loads(self.urlio.content)
            self.status_code = self.urlio.status_code
        def __del__(self) -> None:
            """
            Delete GET request.
            """
            self.urlio.close()
        def __repr__(self) -> str:
            """
            Repeat GET request.
            """
            return str("<"+"Get"+" "+str(self.__url)+" "+str(self.status_code)+">")