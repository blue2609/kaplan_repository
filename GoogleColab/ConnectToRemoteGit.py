privateKey = SSH_PRIVATE_KEY

import os 
import re

# create the .ssh folder if it doesn't exist
if not os.path.exists('/root/.ssh'):
    os.mkdir('/root/.ssh')

# create the private key file
with open('/root/.ssh/id_rsa','w',encoding='utf8') as privateKeyFile:
    privateKeyFile.write(privateKey)

!chmod 600 /root/.ssh/id_rsa

# add bitbucket.org as known hosts
!ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

# create the SSH_AUTH_SOCK environment variable
ssh_agent_output = !`ssh-agent -s`
ssh_auth_sock = re.split(':|=|;',ssh_agent_output[0])[2]
os.environ['SSH_AUTH_SOCK'] = ssh_auth_sock

# add the private key?? 
!ssh-add /root/.ssh/id_rsa
!ssh -T git@bitbucket.org