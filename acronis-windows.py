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
  properties = os.popen('powershell Get-ItemProperty -Path "HKLM:\SOFTWARE\Acronis\BackupAndRecovery\Settings\MachineManager"').read()
  return properties.splitlines()[2][22:]

def installAgent ():
  file_name = "CyberProtect_AgentForWindows_x86_64.bin"
  file_url = "https://github.com/Pkaran26/redis_nodejsExample/raw/master/CyberProtect_AgentForWindows_web.exe"

  r = requests.get(file_url, stream = True) 

  with open(file_name,"wb") as file: 
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk: 
        file.write(chunk);print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\r')
  print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\n')
  print(file_name + ' is installing...')
  print(os.system(file_name + " --quiet --registration by-token --reg-address=" + base_url + " --reg-token=" + regToken))

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
