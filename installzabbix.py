#!/bin/sh
#zabbix-agent installer
import sys
import os
import socket
import re
import subprocess

# Getting Host Name
def get_host_name():
    hostname=""
    print("1. Machine's Hostname\n2. Enter Hostname Manually\n")
    select_host_name = input("Select the hostname (1, 2): ")
    if select_host_name == "1":
        hostname = socket.gethostname()
        
    elif select_host_name == "2":
	    hostname = input("Enter the hostname, please: ")
    	   
    return hostname

# Check Hostname Validation
def valid_host_name(hostname):
    if hostname != "" or hostname != None or hostname != "localhost":
	    return True
    else:
	    return False			    
    return hostname


# Remove Existing Zabbix Agent
def remove_zabbix_agent():
    try:
        os.system('sudo yum remove zabbix-release')
        os.system('sudo yum remove zabbix-agent')
        run = subprocess.getstatusoutput('sudo ps -ef | grep zabbix_agentd | grep -v grep')
        file_ = os.path.exists('/etc/zabbix')
        if run:
            os.system('sudo service zabbix-agent stop')
            print("Zabbix agent service stopped")
        if file_:
            os.system('sudo rm -rf /etc/zabbix')
            print("Zabbix removed")
    except Exception as e:
        print(e)	


# Asking Zabbix Server IP Address
def zabbix_server_IP():
    server_IP = input("Enter the zabbix server IP, please (exm: 192.168.X.X ): ") 
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
	
	    #print("-----------------Installation Started, Updating----------------\n")
	    #os.system("sudo yum update")
		
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
        get_repo = subprocess.getstatusoutput('sudo yum list installed | grep zabbix-release')
		
        if get_repo:
            print("---------------------Repo downloaded---------------------\n")
            os.system('sudo yum install zabbix-agent')
            os.system('systemctl start zabbix-agent')
			
            print("---------------------Server/Server Active Configuration--------------------\n")
            while True:
                server_IP = zabbix_server_IP()
                print(server_IP)
                if valid_IP(server_IP):
                    print("---------------------Server IP Confirmed---------------------\n")
                    os.system("sudo sed -i 's/^Server=.*/Server="+server_IP+"/g' /etc/zabbix/zabbix_agentd.conf")
                    os.system("sudo sed -i 's/^ServerActive=.*/ServerActive="+server_IP+"/g' /etc/zabbix/zabbix_agentd.conf")
                    print("Zabbix server set at: "+server_IP)
                    break
                else:
                    print("Server IP was not confirmed, try again...\n")
                    continue
									

            print('--------------------Hostname Configuration-------------------\n')
            while True:
                user_host_name = get_host_name()
                if valid_host_name(user_host_name):
                    os.system("sudo sed -i 's/Hostname=.*/Hostname="+user_host_name+"/g' /etc/zabbix/zabbix_agentd.conf")
                    print("Hostname Set: "+user_host_name)
                    break
                else:
                    print("Hostname was not confirmed, try again...\n")
                    continue	
		
            print('-------------------Firewall Configuration------------------\n')
            os.system('sudo firewall-cmd --add-port=10050/tcp --permanent')
            os.system('sudo firewall-cmd --reload')
			
            print('--------------------Starting zabbix, Checking status-------------------\n')
            os.system('systemctl restart zabbix-agent')
            status = subprocess.getstatusoutput('chkconfig zabbix-agent on')
            run = subprocess.getstatusoutput('sudo ps -ef | grep zabbix_agentd | grep -v grep')
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