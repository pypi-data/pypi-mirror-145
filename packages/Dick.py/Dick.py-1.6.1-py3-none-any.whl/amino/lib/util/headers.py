from amino.lib.util import device
import hmac
import base64
from hashlib import sha1
from uuid import uuid4
import requests
sid = None
def sigg(data):
    da={"data":data}
    p=requests.post(f"http://172.105.51.123/sig-gen",data=da).json()
    return p["sig"]

class Headers:
    def __init__(self, data = None, type = None, deviceId: str = None, sig: str = None):
        if deviceId:
            dev = device.DeviceGenerator(deviceId=deviceId)
        else:
            dev = device.DeviceGenerator()

        headers = {
            "NDCDEVICEID": dev.device_id,
            #"NDC-MSG-SIG": dev.device_id_sig,
            "Accept-Language": "en-US",
            "Content-Type": "application/json",
            "User-Agent": dev.user_agent,
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        if data:
            #print(data)
            headers["Content-Length"] = str(len(data))
            signature=None
            try: signature=sigg(data)
            except: pass
            headers["NDC-MSG-SIG"] = signature
        if sid: headers["NDCAUTH"] = f"sid={sid}"
        if type: headers["Content-Type"] = type
        #if sig: headers["NDC-MSG-SIG"] = sig
        self.headers = headers
 
 
