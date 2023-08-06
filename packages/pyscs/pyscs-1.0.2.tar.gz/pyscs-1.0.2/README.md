# scs lib for python3

```python
from pyscs.scs import SCS

scs = SCS()
# set script can be stop right now
msg, code = scs.can_stop()
if code == 200:
    print("success")
elif code == 201:
    print("warning: " + msg)
else:
    print(msg)

# set script can not be stop except exec scs.can_stop()
msg, code = scs.can_not_stop()
if code == 200:
    print("success")
elif code == 201:
    print("warning: " + msg)
else:
    print(msg)


from pyscs import Script
# add script or server
s = Script("test", "python test.py")
# When dir is not empty and is not exist and get is not empty, It will command get first
s.dir = "/home/test"
s.get = "cd /home && git clone xxxx"
msg, code = scs.add_script(s)
if code == 200:
    print("success")
elif code == 201:
    print("warning: " + msg)
else:
    print(msg)


...
```


# code 说明

| code        | information    |  
| --------   | -----:   | 
| 200        | success      |  
| 201        | waiting config reload      |  
| 203        | token error      |  
| 404        |  not found name or pname      |  
| 500        |  internal error      |  