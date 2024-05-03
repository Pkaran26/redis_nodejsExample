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
  file_url = "https://download.wetransfer.com/eugv/01049b737775b3b17e3bca6c57ae6a2620240503144040/dc9acab2afb169b137c9cefe154592a2b10bb142/CyberProtect_AgentForWindows_web.exe?cf=y&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRlZmF1bHQifQ.eyJleHAiOjE3MTQ3NTIxNDgsImlhdCI6MTcxNDc1MTU0OCwiZG93bmxvYWRfaWQiOiI3OWZiNTViYS01NmRiLTQ5ZmItYjExZS1jZTJkYTI0YzBlM2YiLCJzdG9yYWdlX3NlcnZpY2UiOiJzdG9ybSJ9.nv9GGxN29Z3hC41dMSG9LqY4BiRSQl6n8l5nTFh2Z68"

  r = requests.get(file_url, stream = True) 

  with open(file_name,"wb") as file: 
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk: 
        file.write(chunk);print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\r')
  print('Downloaded: {0:.2f} MB'.format(os.path.getsize(file_name) * 0.000001), end='\n')
  print(file_name + ' is installing...')
  print(os.system(file_name + " --quiet --skip--registration"))

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
