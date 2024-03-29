#coding=utf-8
import sys
import automatically_report

#Temperature report
def temp_report(disalbe_phone_book):
    #Get time
    report_time = automatically_report.current_time()
    #Get temperature
    get_temperature = automatically_report.cputemperature(float_mode=True)
    #Generate message
    message_container = f"RaspberryPi CoreTemp | {get_temperature} °C"
    #Directly configure email
    if bool(disalbe_phone_book) is True:
        #If set "disalbe_phone_book" True
        sender_account = ""
        sender_password = ""
        receiver_address = ""
        #Sending Mail
        automatically_report.sending_alert(message_container, sender_account, sender_password, receiver_address, disalbe_phone_book=True)
        #Complete report
        print(f"{report_time} | Temperature report complete.")
    #Read email configuration
    elif bool(disalbe_phone_book) is False:
        mail_config = automatically_report.configuration(update_config=False)
        sender_account = mail_config["mail"]["sender"]
        if len(sender_account) is 0:
            print(f"{report_time} | Email configuration is necessary.")
        else:
            #Sending Mail
            automatically_report.sending_alert(message_container, disalbe_phone_book=False)
            print(f"{report_time} | Temperature report complete.")

#Email configuration mode selection
disalbe_phone_book = False
#Running report
temp_report(disalbe_phone_book)
#END
sys.exit(0)
