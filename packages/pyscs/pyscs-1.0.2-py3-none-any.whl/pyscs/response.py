# encoding=utf-8

# reponse class

class Response():

    def __init__(self, data: any= None ,code:int = 0, msg: str = "", version: str="", role: str="") -> None:
        self.code = code 
        self.msg = msg 
        self.version = version 
        self.role = role 
        self.data = data


class Status():

    def __init__(self, pname: str = "", name: str="", pid: int=0,
            status: str = "", command: str="", path: str="",
            cannotStop: bool = False, start: int=0, version: str="",
            isCron: bool = False, restartCount: int=0, disable: bool = False,
            cpu: int = 0, mem: int=0, os: str="",
            ) -> None:
        self.pname = pname 
        self.name = name 
        self.pid = pid 
        self.status = status 
        self.command = command
        self.path = path
        self.cannotStop = cannotStop
        self.start = start
        self.version = version
        self.isCron = isCron
        self.restartCount = restartCount
        self.disable = disable
        self.cpu = cpu
        self.mem = mem
        self.os = os

