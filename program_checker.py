#coding=utf-8
import sys
import automatically_report

#Program checker
def program_checker(disalbe_phone_book):
    #Get time
    report_time = automatically_report.current_time()
    #Get program check result
    process_result = automatically_report.process()
    #Check result
    if type(process_result) is bool:
        if bool(process_result) is True:
            print(f"{report_time} | Query not found. Configuration is necessary.")
        elif bool(process_result) is False:
            print(f"{report_time} | Error. Please check error.log.")
    elif type(process_result) is list:
        print(f"{report_time} | Program found in process list.")
    elif type(process_result) is int:
        print(f"{report_time} | Program not found in process list.")
        #Generate message
        message_container = "Program not found."
        #Directly configure email
        if bool(disalbe_phone_book) is True:
            #If set "disalbe_phone_book" True
            sender_account = ""
            sender_password = ""
            receiver_address = ""
            #Sending Mail
            automatically_report.sending_alert(message_container,sender_account, sender_password, receiver_address, disalbe_phone_book=True)
            #Complete report
            print(f"{report_time} | Status report complete.")
        #Read email configuration
        elif bool(disalbe_phone_book) is False:
            mail_config = automatically_report.configuration(update_config=False)
            sender_account = mail_config["mail"]["sender"]
            if len(sender_account) is 0:
                print(f"{report_time} | Email configuration is necessary.")
            else:
                #Sending Mail
                automatically_report.sending_alert(message_container, disalbe_phone_book=False)
                print(f"{report_time} | Status report complete.")

#Email configuration mode selection
disalbe_phone_book = False
#Running report
program_checker(disalbe_phone_book)
#END
sys.exit(0)
