import json
import os

def write(file,key,value,encode = "utf-8"):
    try:
        f = open(file,"r",encoding = encode)
    except:
        try:
            f = open(file,"a",encoding = encode)
            f.write("{}")
        except:
            return False
    conf = json.loads(f.read())
    try:
        conf[key] = value
        conf_text = json.dumps(conf)
        f.close()
        #print(conf,conf_text)
        with open(file,"w",encoding = encode) as f:
            f.write(conf_text)
        return True
    except:
        return False

def read(file,key,default = "",encode = "utf-8"):
    try:
        f = open(file,"r",encoding = encode)
    except:
        try:
            f = open(file,"w",encoding = encode)
            f.write("{}")
            f.close()
            f = open(file,"r",encoding = encode)
        except:
            return False
    conf = json.loads(f.read())
    try:
        return conf[key]
    except:
        conf[key] = default
        write(file,key,default,encode)
        return conf[key]

class openjson(object):
    def __init__(self,file,encoding = "utf-8"):
        super().__init__()
        self.file = file
        self.e = encoding
    def readall(self,json = True):
        try:
            with open(self.file,"r",encoding = self.e) as f:
                if json:
                    return json.load(f)
                else:
                    return f.read()
        except:
            return None
    def add(self,key,value):
        write(self.file,key,value,self.e)
        return read(self.file,key,encoding = self.e)
    def getvalue(self,key,value = ""):
        return read(self.file,key,value,self.e)
        
"""

if __name__ == "__main__":
    print(openjson("test.json").getvalue("nmsl","StarWorld"))
"""
