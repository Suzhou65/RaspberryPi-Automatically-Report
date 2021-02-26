#coding=utf-8
import os
import re
import sys
import json
import socket
import smtplib
import logging
import requests
import datetime
import subprocess
from getpass import getpass
from subprocess import PIPE
from subprocess import Popen
from email.mime.text import MIMEText

#Error handling
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a", format=FORMAT)

#Time
def current_time():
    today = datetime.datetime.now()
    return today.strftime('%Y-%m-%d %H:%M:%S')

#Configuration
def configuration( update_config=() ):
    if bool(update_config) is False:
        #Reading configuration file
        try:
            with open("config.json", "r") as configuration_file:
                #Return dictionary
                return json.load(configuration_file)
        #If file not found
        except FileNotFoundError:
            #Stamp
            time_initialize = current_time()
            #Initialization
            print("Configuration not found, please initialize.\r\n")
            sender = input("Please enter the sender address: ")
            scepter = getpass("Please enter the sender password: ")
            receiver = input("Please enter the receiver address: ")
            #Dictionary
            initialize_config = {
                "mail": {"sender": sender,
                    "scepter": scepter,
                    "receiver": receiver},
                "tempture_alert": {
                    "critical": 55},
                "ip_address_alert": {
                    "ipv4": "",
                    "ipv6": ""},
                "program_checker": {
                    "program": ""},
                "last_update_time": time_initialize
                    }
            #Save configuration file
            with open("config.json", "w") as configuration_file:
                json.dump(initialize_config, configuration_file, indent=3)
                print("Configuration saved successfully.")
                #Return dictionary after initialize
                return initialize_config
    #Update configuration file
    elif bool(update_config) is True:
        with open("config.json", "w") as configuration_file:
            json.dump(update_config, configuration_file, indent=3)
            #Return dictionary after update
            return update_config

#Using "vcgencmd measure_temp" get core temperature
def cputemperature( float_mode=() ):
        rpi_temp = os.popen("vcgencmd measure_temp").readline()
        temp_str = rpi_temp.replace("temp=","").replace("'C","").replace("\n","")
        if bool(float_mode) is False:
            return int(temp_str)
        elif bool(float_mode) is True:
            return float(temp_str)

#Get IPv4
def get_ipv4():
    ipify_params = {'format':'json'}
    iptest_params = "json"
    try:
        ipify4 = requests.get("https://api.ipify.org", params=ipify_params, timeout=2)
        if ipify4.status_code == 200:
            ipv4_json = json.loads(ipify4.text)
            ipify4.close()
            return ipv4_json.get('ip')
        else:
            pass
    except requests.exceptions.Timeout:
        try:
            iptest4 = requests.get("https://v4.ipv6-test.com/api/myip.php", params=iptest_params, timeout=3)
            if iptest4.status_code == 200:
                ipv4_json = json.loads(iptest4.text)
                iptest4.close()
                return ipv4_json.get('address')
            else:
                logging.warning(iptest4.status_code)
                return True
        except requests.exceptions.Timeout as error_time:
            logging.warning(error_time)
            return True
        except Exception as error_status:
            logging.exception(error_status)
            return False    
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Get IPv6
def get_ipv6():
    ipify_params = {'format':'json'}
    iptest_params = "json"
    try:
        ipify6 = requests.get("https://api6.ipify.org", params=ipify_params, timeout=2)
        if ipify6.status_code == 200:
            ipv6_json = json.loads(ipify6.text)
            ipify6.close()
            return ipv6_json.get('ip')
        else:
            pass
    except requests.exceptions.Timeout:
        try:
            iptest6 = requests.get("https://v6.ipv6-test.com/api/myip.php", params=iptest_params, timeout=3)
            if iptest6.status_code == 200:
                ipv6_json = json.loads(iptest6.text)
                iptest6.close()
                return ipv6_json.get('address')
            else:
                logging.warning(iptest6.status_code)
                return True
        except requests.exceptions.Timeout as error_time:
            logging.warning(error_time)
            return True
        except Exception as error_status:
            logging.exception(error_status)
            return False
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Output IP check
def get_address( mode_select=() ):
    #Default output both IPv4/IPv6
    if bool(mode_select) is False:
        dict_64 = {
            "get4": get_ipv4(),
            "get6": get_ipv6()}
        return dict_64
    #Selection
    elif bool(mode_select) is True:
        if mode_select == "IPv4":
            dict_4 = {"get4": get_ipv4()}
            return dict_4
        elif mode_select == "IPv6":
            dict_6 = {"get6": get_ipv6()}
            return dict_6

#Process check
def process():
    #Read target
    target_config = configuration(update_config=False)
    program = target_config["program_checker"]["program"]
    if len(program) is 0:
        query_empty = "Query object is necessary."
        logging.warning(query_empty)
        return True
    else:
        try:
            #Ps command
            procress_1 = Popen(["ps", "-x"], stdout=PIPE)
            procress_2 = Popen(["grep", "-i", str(program)], stdin=procress_1.stdout, stdout=PIPE)
            procress_1.stdout.close()
            #Awk filter
            procress_filter = ["awk", "{print $1,$3,$5$6$7}"]
            procress_3 = subprocess.Popen(procress_filter, stdin=procress_2.stdout, stdout=subprocess.PIPE)
            procress_2.stdout.close()
            #Bytes to list
            procress_bytes = procress_3.communicate()[0]
            procress_string =procress_bytes.decode("utf-8")
            procress_list = procress_string.split("\n")
            procress_3.stdout.close()
            #Filter empty
            while("" in procress_list):
                procress_list.remove("")
            #Filter ps itself
            procress_filter = "grep" + "-i" + str(program)
            procress_result = [x for x in procress_list if procress_filter not in x]
            #Check program exist or not
            if len(procress_result) is not 0:
                return procress_result
            else:
                return 404
        except Exception as error_status:
            logging.exception(error_status)
            return False

#Mail alert
def sending_alert(message_container, sender_account=(), sender_password=(), receiver_address=(), disalbe_phone_book=() ):
    #Read mail set from book
    if bool(disalbe_phone_book) is False:
        #Load mail configuration
        mail_config = configuration(update_config=False)
        #Try to read configuration
        try:
            sender_account = mail_config["mail"]["sender"]
            sender_password = mail_config["mail"]["scepter"]
            receiver = mail_config["mail"]["receiver"]
        #If configuration not found
        except KeyError:
            keyerror_message = "Mail Configuration not found, please initialize."
            logging.warning(keyerror_message)
            return False
    #Directly setting email configuration
    elif bool(disalbe_phone_book) is True:
        pass
    #Sending Mail
    time_sending = current_time()
    msg = MIMEText(message_container)
    msg["Subject"] = (f"Automatically Alert {time_sending}")
    msg["From"] = sender_account
    msg["To"] = receiver
    #Mail server
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(sender_account, sender_password)
        #Sending Mail
        smtpserver.sendmail(sender_account, [receiver], msg.as_string())
        smtpserver.quit()
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#END