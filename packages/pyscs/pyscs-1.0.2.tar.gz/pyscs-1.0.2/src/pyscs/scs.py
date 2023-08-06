# encoding=utf-8

import requests
import os
from pyscs.script import Script
from pyscs.alert import Alert
import json
from typing import List, Tuple, Dict, Union
from pyscs.response import Response, Status


class SCS:
    def __init__(self, domain="https://127.0.0.1:11111", pname: str=None, 
        name: str=None, token: str=None, debug: bool=False):
        requests.packages.urllib3.disable_warnings()
        if pname is None:
            pname = os.getenv("PNAME", "")
        if name is None:
            name = os.getenv("NAME", "")
        
        if token is None:
            token = os.getenv("TOKEN", "")
        self._domain = domain
        self._pname = pname
        self._name = name
        self._debug=debug
        self._token = token
        self._headers = {
            "Token": self._token
        }
    
    def get_pname(self) -> None:
        return self._pname
    
    def get_name(self)-> None:
        return self._name
    
    def get_token(self)-> None:
        return self._token
    
    def _post(self, url, data=None)-> Tuple[Dict or str, int]:
        if isinstance(data, dict):
            data = json.dumps(data)
        try:
            if self._debug:
                print(self._domain + url)
                print(data)
                print("---------------")
            r = requests.post(self._domain + url, verify=False, data=data, headers=self._headers,timeout=5)
            if r.status_code != 200:
                return (r.text, r.status_code)
            resp = Response(**r.json())
            if resp.code == 200:
                return resp.data, resp.code
            return resp.msg, resp.code
        except Exception as e:
            return (e.args[0], 500)

    def set_alert(self, alert: Alert) ->Tuple[str, int]:
        return self._post("/send/alert", alert.dumps())
        
    def can_stop(self, name="")-> Tuple[str, int]:
        if name == "":
            name = self._name
        if name == "":
            return "name is empty", 0
        return self._post("/canstop/" + name)
    
    def can_not_stop(self, name="")-> Tuple[str, int]:
        if name == "":
            name = self._name
        if name == "":
            return "name is empty", 0
        # data = '{"pname":"%s", "name": "%s", "value": true}' % (self._pname, self._name)
        return self._post("/cannotstop/" + name)
    

    def status_all(self)-> Tuple[List[Status], int]:
        statuss = []
        res, ok = self._post("/status")     
        for status in res:
              statuss.append(Status(**status)) 
        return statuss, ok

    def status_pname(self, pname="")-> Tuple[List[Status], int]:
        statuss = []
        res, ok = self.__op_name("status",pname)     
        for status in res:
              statuss.append(Status(**status)) 
        return statuss, ok

    def status_name(self, pname="", name="")-> Tuple[List[Status], int]:
        statuss = []
        res, ok = self.__op_name("status", pname, name)     
        for status in res:
              statuss.append(Status(**status)) 
        return statuss, ok


    def add_script(self, script: Script) -> Tuple[str, int]:
        """
        add script
        scs = SCS("https://127.0.0.1:11111", "mm", "mm_0", "sadfasdg1654346098")
        s = Script("aa", "ls")
        msg, ok = scs.add_script(s)
        if not ok:
            print(msg) 
            
        print("ok: " + msg)
        
        # name               string          
        # dir                string          
        # command            string           
        # replicate          int              
        # always             bool             
        # disableAlert       bool              
        # env                map[string]string 
        # port               int               
        # alert                 AlertTo           
        # version            string   
        return:  如果返回成功， 那么前面的值是token， 如果是失败， 那么前面的值是错误信息
        """
        if script.name == "" or script.command == "":
            return "name and command is empty", 0
        return self._post("/script", script.dump())
        

    def start_name(self, pname="", name="")-> Tuple[str, int]:
        return self.__op_name("start",pname, name)

    def start_pname(self, pname="")-> Tuple[str, int]:
        return self.__op_pname("start",pname)

    def start_all(self)-> Tuple[str, int]:
        return self.__op_all("start")

    def update_name(self, pname="", name="")-> Tuple[str, int]:
        return self.__op_name("update",pname, name)

    def update_pname(self, pname="")-> Tuple[str, int]:
        return self.__op_pname("update",pname)

    def env(self, name="")-> Tuple[Dict[str, str], int]:
        if name == "":
            name = self._name
        if name == "":
            return "name is empty", 0
        return self._post("/env/%s" % name)

    def restart_name(self, pname="", name="")-> Tuple[str, int]:
        return self.__op_name("restart",pname, name)

    def restart_pname(self, pname="")-> Tuple[str, int]:
        return self.__op_pname("restart",pname)

    def restart_all(self)-> Tuple[str, int]:
        return self.__op_all("restart")

    def stop_name(self, pname="", name="")-> Tuple[str, int]:
        return self.__op_name("stop",pname, name)

    def stop_pname(self, pname="")-> Tuple[str, int]:
        return self.__op_pname("stop",pname)

    def stop_all(self)-> Tuple[str, int]:
        return self.__op_all("stop")

    def kill_name(self, pname="", name="")-> Tuple[str, int]:
        return self.__op_name("kill",pname, name)

    def kill_pname(self, pname="")-> Tuple[str, int]:
        return self.__op_name("kill",pname, pname)

    def remove_pname(self, pname="")-> Tuple[str, int]:
        return self.__op_pname("remove",pname)

    def remove_name(self)-> Tuple[str, int]:
        return self.__op_all("remove")

    def __op_all(self, op:str, pname="", name=""):
        return self._post("/{}".format(op)) 

    def __op_pname(self, op:str, pname=""):
        if pname == "":
            pname = self._pname
        if pname == "":
            return "pname is empty", 0
        return self._post("/{}".format(op)) 

    def __op_name(self, op:str, pname="", name=""):
        if name == "":
            name = self._name
        if pname == "":
            pname = self._pname
        if name == "" or pname == "":
            return "pname or name is empty", 0
        return self._post("/{}".format(op)) 