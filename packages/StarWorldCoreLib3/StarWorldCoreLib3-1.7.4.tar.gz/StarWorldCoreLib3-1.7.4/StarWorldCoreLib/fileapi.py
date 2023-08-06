import os
import json

def file_locate(file="",fl=__file__):
    ic = str(os.path.split(os.path.realpath(fl))[0]).replace("\\","/")+"/"+file
    return ic

class JsonConfigurator:
    def __init__(self,file) -> None:
        """
        The 'file' parameter must use an existing file
        """
        self.file = file
        self.file_output = open(file,"rb")
        self.dict_content = json.loads(self.file_output.read())
    def parse(self) -> dict:
        return self.dict_content
    def addition(self,key,value) -> None:
        self.dict_content[key] = value
        file_input = open(self.file,"wb")
        file_input.write(json.dumps(self.dict_content).encode("utf-8"))
        file_input.close()
    def remove(self,key) -> None:
        self.dict_content.pop(key)
        file_input = open(self.file,"wb")
        file_input.write(json.dumps(self.dict_content).encode("utf-8"))
        file_input.close()
    def save(self,file) -> None:
        file_input = open(file,"wb")
        file_input.write(json.dumps(self.dict_content).encode("utf-8"))
        file_input.close()
    def __del__(self) -> None:
        self.file_output.close()
    def __str__(self) -> str:
        return json.dumps(self.dict_content,indent=4)

