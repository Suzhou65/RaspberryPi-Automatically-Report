#coding=utf-8
import sys
import automatically_report

#IP change report
def ip_change_alert(disalbe_phone_book, mode_select=() ):
    report_time = automatically_report.current_time()
    ip_configuration = automatically_report.configuration(update_config=False)
    #Compare all
    if bool(mode_select) is False:
        list_64 = automatically_report.get_address()
        ipv4_config = ip_configuration["ip_address_alert"]["ipv4"]
        ipv6_config = ip_configuration["ip_address_alert"]["ipv6"]
        result_64 = [(ipv4_config == list_64["get4"]),(ipv6_config == list_64["get6"])]
        if False in result_64:
            ip_container4 = list_64["get4"]
            ip_container6 = list_64["get6"]
            message_container = f"IP Change Alert \r\nIPv4: {ip_container4} | IPv6: {ip_container6}"
            if bool(disalbe_phone_book) is True:
                automatically_report.sending_alert(message_container,sender_account,sender_password,receiver_address,disalbe_phone_book=True)
                print(f"{report_time} | {result_64} | {ip_container4} | {ip_container6}")
            elif bool(disalbe_phone_book) is False:
                automatically_report.sending_alert(message_container, disalbe_phone_book=False)
                print(f"{report_time} | {result_64} | {ip_container4} | {ip_container6}")
            update_config = ip_configuration
            update_config["ip_address_alert"]["ipv4"] = list_64["get4"]
            update_config["ip_address_alert"]["ipv6"] = list_64["get6"]
            update_config["last_update_time"] = report_time
            automatically_report.configuration(update_config)
        else:
            print(f"{report_time} | No changes detected.")
    #Selection Compare
    elif bool(mode_select) is True:
        #IPv4
        if mode_select == "IPv4":
            list_4 = automatically_report.get_address(mode_select)
            ipv4_config = ip_configuration["ip_address_alert"]["ipv4"]
            if ipv4_config == list_4["get4"]:
                print(f"{report_time} | No changes detected.")
            else:
                ip_container = list_4["get4"]
                message_container = f"IPv4 Change Alert \r\n IPv4: {ip_container}"
                if bool(disalbe_phone_book) is True:
                    automatically_report.sending_alert(message_container,sender_account,sender_password,receiver_address,disalbe_phone_book=True)
                    print(f"{report_time} | {ip_container}")
                elif bool(disalbe_phone_book) is False:
                    automatically_report.sending_alert(message_container, disalbe_phone_book=False)
                    print(f"{report_time} | {ip_container}")
            update_config = ip_configuration
            update_config["ip_address_alert"]["ipv4"] = list_4["get4"]
            update_config["last_update_time"] = report_time
            automatically_report.configuration(update_config)
        #IPv6
        elif mode_select == "IPv6":
            list_6 = automatically_report.get_address(mode_select)
            ipv6_config = ip_configuration["ip_address_alert"]["ipv6"]
            if ipv6_config == list_6["get6"]:
                print(f"{report_time} | No changes detected.")
            else:
                ip_container = list_6["get6"]
                message_container = f"IPv6 Change Alert \r\n IPv6: {ip_container}"
                if bool(disalbe_phone_book) is True:
                    automatically_report.sending_alert(message_container,sender_account,sender_password,receiver_address,disalbe_phone_book=True)
                    print(f"{report_time} | {ip_container}")
                elif bool(disalbe_phone_book) is False:
                    automatically_report.sending_alert(message_container, disalbe_phone_book=False)
                    print(f"{report_time} | {ip_container}")
            update_config = ip_configuration
            update_config["ip_address_alert"]["ipv6"] = list_6["get6"]
            update_config["last_update_time"] = report_time
            automatically_report.configuration(update_config)

#Email configuration mode selection
disalbe_phone_book = False
#If set True
sender_account = ""
sender_password = ""
receiver_address = ""
#Running report
ip_change_alert(disalbe_phone_book, mode_select=False)
#END
sys.exit(0)
