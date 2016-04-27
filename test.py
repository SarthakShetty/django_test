import requests
import json
url = "Https://gcm-http.googleapis.com/gcm/send"
headers = {'Content-Type':'application/json','Authorization':'key=AIzaSyDxQkGcIlivICF6NxbRTRHXz7K58A36S50'}
data = {};notification={}
data["message"] = "Hey! How does this look?"
notification["body"] = "Sarthak : " + data["message"]
notification["title"] = "New Message from EGM - GroupName"
payload ={}
payload["notification"] = notification
payload["data"] = data
#to = "APA91bGEbcLO-Jr5VK5GC7Y2RPTT-Z75V0VH7ik01Yxh4-eyQhYzc16BIkYZq6l7NPdqvYkDpuazbLNewMscJR4yip1d7RP_v3sJfMuF98dOqfODzyqfu_06FvnFBr_m-nT6k8blO66PkefNkLeEpVoVtA978vxOFA"

to = "APA91bFErs9cRy7WR5A4xlmdCOKBr6SHf_uP8E7Tz54rgXA4YQ8q5N91kngWPEKoFiq6WaLm7VPMmaLMhooU5jDFkWgT3LigcvCZAwMg-aExPr0q531mWN_H-NMS0nx4VRClBLiS3u1FScgUcebd4gre-MpHhCkEqg"

payload["to"]  = to #print payload
payload = json.dumps(payload)
#print payload
r = requests.post(url,data = payload,headers=headers)
print r,'\n',r.content
