import socket
import requests
import os
import sys
import xml.etree.ElementTree as ET 
base_url = "http://api.apiculus.local/api/v1"
headers = { 
  "Content-Type": "application/json",
}

regToken = sys.argv[1] #registration token 

if regToken == None:
  print('Registration token is required')
  sys.exit()

def getHost ():
  name = socket.gethostname()
  if name.find('VM-') >= 0 or name.find('vm-') >= 0:
    return name[3:]
  elif name.find('autoScaleVm-') >= 0:
    return name[12:]
  else:
    return name
  
def getInstanceID():
  tree = ET.parse('/etc/Acronis/BackupAndRecovery.config') 
  root = tree.getroot()
  for child in root:
    for subChild in child:
      for c in subChild:
        if c.attrib['name'] == 'InstanceID':
          return c.text

def installAgent ():
  file_name = "CyberProtect_AgentForLinux_x86_64.bin"
  file_url = "https://tnow-prod-apac.367791ca7abea81096902b345fee7b1f.r2.cloudflarestorage.com/2024-05-03/87879b363731b324031ce228b2940c5e/20240503Aoo3M7fn/O5WXGX/CyberProtect_AgentForLinux_x86_64%20%281%29.bin?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ee862debb448801ab1904792186e2774%2F20240503%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20240503T164623Z&X-Amz-Expires=86400&X-Amz-Signature=3df62c85083066bc7da9e3c4b9d50fe05790d20afd8d55ec6f773352b9959efe&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3D%22CyberProtect_AgentForLinux_x86_64%20%281%29.bin%22&x-id=GetObject"

  r = requests.get(file_url, stream = True) 

  with open(file_name,"wb") as file: 
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk: 
        file.write(chunk);print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\r')
  print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\n')
  print(file_name + ' is installing...')
  print(os.system("sudo chmod +x ./" + file_name))
  print(os.system("sudo ./" + file_name + " -a --skip-registration"))

  InstanceID = getInstanceID()
  print("InstanceID: ", InstanceID)
  if InstanceID == 'None':
    return print("Agent not installed properly, please check your installation")

def runScript ():
  hostname = getHost()
  print("hostname: ", hostname)
  if hostname:
      installAgent()
  else:
    print("hostname not found")

runScript()
