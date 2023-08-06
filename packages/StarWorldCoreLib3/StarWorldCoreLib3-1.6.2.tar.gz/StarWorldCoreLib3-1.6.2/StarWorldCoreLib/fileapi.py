import os

def file_locate(file="",fl=__file__):
    ic = str(os.path.split(os.path.realpath(fl))[0]).replace("\\","/")+"/"+file
    return ic

