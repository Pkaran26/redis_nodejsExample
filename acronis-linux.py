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
  file_url = "https://download.wetransfer.com/eugv/ffc2a37ff4c0931553a6f7d5c9fb848720240503131601/bda88f1f5e29bb8974b04736fe743235008a02f9/CyberProtect_AgentForLinux_x86_64.bin?cf=y&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRlZmF1bHQifQ.eyJleHAiOjE3MTQ3NDQ1MTYsImlhdCI6MTcxNDc0MzkxNiwiZG93bmxvYWRfaWQiOiIyODE3ODVmMC01NjBiLTQzMmEtOGNkZS1hZWM0Mzk3ZWI1MWYiLCJzdG9yYWdlX3NlcnZpY2UiOiJzdG9ybSJ9.V36nmxmuNZhkE8EzY84IN2Z4UrgrowXed9-ztseBMMI"

  r = requests.get(file_url, stream = True) 

  with open(file_name,"wb") as file: 
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk: 
        file.write(chunk);print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\r')
  print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\n')
  print(file_name + ' is installing...')
  print(os.system("sudo chmod +x ./" + file_name))
  print(os.system("sudo ./" + file_name + " --skip-registration"))

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
