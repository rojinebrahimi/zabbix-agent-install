#zabbix-agent installer
import sys
import os
import commands
import socket
import re

# Getting Host IP
#def get_host_IP():
#    try:
#	 host_ip = socket.gethostbyname(socket.gethostname())
#	 print('-----------------Reaching host IP-------------------')
#	 return host_ip
#    except:
#      	 print('--------------host IP is not reachable--------------')

# Getting Host Name
def get_host_name():
    try:
	host_name = socket.gethostname()
	return host_name
    except:
	print('-----------------Hostname not reachable-----------------')

# Remove Existing Zabbix Agent
def remove_zabbix_agent():
    try:
	os.system('sudo yum remove zabbix-release')
	os.system('sudo yum remove zabbix-agent')
  	run = commands.getoutput('sudo ps -ef | grep zabbix_agentd | grep -v grep')
	file = os.path.exists('/etc/zabbix')
	if run:
		os.system('sudo service zabbix-agent stop')
		print("Zabbix agent service stopped")
	if file:
		os.system('sudo rm -rf /etc/zabbix')
		print("Zabbix removed")
    except Exception as e:
	print(e)	


# Asking Zabbix Server IP Address
def zabbix_server_IP():
    server_IP = input("Enter the zabbix server IP, please (exm: '127.0.0.1'): ") 
    return server_IP


# Check IP validation    
def valid_IP(server_IP):
    IP_add = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', server_IP)
    if IP_add:
	return True
    else:
	return False
	
# Install Zabbix Agent
def install_zabbix_agent():
    try:
    	installed = False
	remove_zabbix_agent()
	print("-----------------Disabling SELINUX------------------")
	os.system("sudo setenforce 0")
	
	print("-----------------Installation Started, Updating----------------\n")
	os.system("sudo yum update")
	
	print("----------------Installing repo----------------\n")
	version = input("Enter the version of zabbix to install(3, 4, 5): ")
	centos_version = input("Enter the version of CentOs(6, 7): ")
	try:
		repo = 'https://repo.zabbix.com/zabbix/%s.0/rhel/%s/x86_64/zabbix-release-%s.0-1.el%s.noarch.rpm'%(version, centos_version, version, centos_version)
		os.system('sudo yum install %s'%(repo))
	except Exception as e:
		print(e)
		system.exit()

	print("--------------------Getting zabbix repo-------------------\n")
	get_repo = commands.getoutput('sudo yum list installed | grep zabbix-release')
	
	if get_repo:
		print("---------------------Repo downloaded---------------------\n")
		os.system('sudo yum install zabbix-agent')
		os.system('systemctl start zabbix-agent')
		
		print("---------------------Server/Server Active Configuration--------------------\n")
		while True:
		    server_IP = zabbix_server_IP()
		    if valid_IP(server_IP):
			print("---------------------Server IP Confirmed---------------------\n")
			os.system("sudo sed -i 's/^Server=.*/Server="+(server_IP)+"/g' /etc/zabbix/zabbix_agentd.conf")
			os.system("sudo sed -i 's/^ServerActive=.*/ServerActive="+(server_IP)+"/g' /etc/zabbix/zabbix_agentd.conf")
			os.system("echo 'HostMetadata=auto_install' >> /etc/zabbix/zabbix_agentd.conf")
			break
		    else:
			print("Server IP was not confirmed, try again...\n")
			continue
								

		print('--------------------Hostname Configuration-------------------\n')
		os.system("sudo sed -i 's/Hostname=.*/Hostname=%s/g' /etc/zabbix/zabbix_agentd.conf"%get_host_name())
		print("Hostname Set: %s"%get_host_name())
	
		print('-------------------Firewall Configuration------------------\n')
		os.system('sudo firewall-cmd --add-port=10050/tcp --permanent')
		os.system('sudo firewall-cmd --reload')
		
		print('--------------------Starting zabbix, Checking status-------------------\n')
		os.system('systemctl restart zabbix-agent')
		status = commands.getoutput('chkconfig zabbix-agent on')
		run = commands.getoutput('sudo ps -ef | grep zabbix_agentd | grep -v grep')
		if run:
			print("--------------------Installation completed successfully!------------------\n")
			installed = True
			os.system('service zabbix-agent status')
		else:
			print(status)
	else:
		print("------------------Could not find zabbix-agent and install zabbix------------------")
    except Exception as e:
	print(e)
  
    finally:
        return installed

# Run Script
if install_zabbix_agent():
	print('------------------Zabbix agent was installed successfully!-----------------')
else:
	print('\n-------------------There was an error while installing zabbix------------------')
