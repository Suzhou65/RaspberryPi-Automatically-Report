# Raspberry Pi Automatically Report
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![rpi](https://github.takahashi65.info/lib_badge/raspberry-pi.svg)](https://www.raspberrypi.org/)
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/RaspberryPi-Automatically-Report)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/RaspberryPi-Automatically-Report.svg)](https://github.com/axetroy/github-size-badge)

Simply Python automatically report module working on Raspberry Pi.

## Contents
- [Raspberry Pi Automatically Report](#raspberry-pi-automatically-report)
  * [Contents](#contents)
  * [Usage](#usage)
    + [Scheduling](#scheduling)
    + [Email sending](#email-sending)
    + [Temperature alert](#temperature-alert)
    + [IP address change detection](#ip-address-change-detection)
    + [Program or process checking](#program-or-process-checking)
  * [Configuration file](#configuration-file)
  * [Modules instantiation](#modules-instantiation)
  * [Python module](#python-module)
  * [Function](#function)
    + [Temperature report](#temperature-report)
    + [Temperature high alert](#temperature-high-alert)
    + [IP address check](#ip-address-check)
    + [Program Checker](#program-checker)
    + [Error handling](#error-handling)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module-1)
  * [License](#license)
  * [Resources](#resources)

## Usage
### Scheduling
- Schedule  
You can using schedule module for job scheduling, you can found the scheduling setting at scripts examples.
```python
import schedule

#Execute setting
schedule.every(30).minutes.do( #Something Package as function)
#Loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
#Crtl+C to exit
except KeyboardInterrupt:
  print("GoodBye ...")
```
- Crontab  
Alternatively, automatically execute via cron.
```shell
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
0 9-22/1 * * *  pi python /home/pi/python_script/coretemp_warning.py
0 */1   * * *   pi python /home/pi/python_script/ip_address_notice.py
#
```
### Email sending
- Google account needed, sign in using App passwords.
- Receiver is unlimited.
First time running email sending, it will asking configuration.
```text
Mail Configuration not found, please initialize.

Please enter the sender account: example@gmail.com
Please enter the sender password: •••••••••
Please enter the receiver address: receiver@gmail.com
```
You can also set disalbe_phone_book to True, directly setting email configuration.
```python
#Email configuration Mode
disalbe_phone_book = False

#If set "disalbe_phone_book" True
sender_account = "example@gmail.com"
sender_password = "•••••••••"
receiver_address = "receiver@gmail.com"
```
### Temperature alert
Critical value is necessary, can be integer or floating point. Configure store at ```config.json```.
```json
"tempture_alert": {
  "critical": 55.0
  },
```
The critical value, unit of temperature is ```degree celsius```.
### IP address change detection
If default address is empty, it will fill in when initialization.
```json
"ip_address_alert": {
  "ipv4": "1.1.1.1",
  "ipv6": "2606:4700:4700::1111"
  },
```
### Program or process checking
If default address is empty, it will print error message when initialization, or return ```True``` as result.
```text
Query not found. Configuration is necessary.
```
Configure store at ```config.json```.
```json
"program_checker": {
  "program": ""
  },
```

## Configuration file
Status4HaH store configuration as JSON format file, named ```config.json.```.  
You can editing the clean copy, which looks like this:
```json
{
    "mail": {
        "sender": "",
        "scepter": "",
        "receiver": ""
    },
    "tempture_alert": {
        "critical": 55.0
    },
    "ip_address_alert": {
        "ipv4": "",
        "ipv6": ""
    },
    "program_checker": {
        "program": ""
    },
    "last_update_time": ""
}
```
If you fill in with correct configure, it will skip initialization step.

## Modules instantiation
If you want to using schedule module for job scheduling, install this module are needed.
- [schedule](https://pypi.org/project/schedule/)

## Python module
- Import the module
```python
import automatically_report
```
```python
import automatically_report as auto
```
- Alternatively, you can import the function independent
```python
from automatically_report import get_address

get_address(mode_select=False)
```

## Function
### Temperature report
```python
import automatically_report

temperature = automatically_report.cputemperature(float_mode=True)
```
If you enable ```float_mode```, it will return ```float```. otherwise it will return ```integer```.

Runnable script refer to ```coretemp_notice.py```. After sending email it will print.
```
2021-02-26 11:11:11 | Temperature report complete.
```
### Temperature high alert
Refer to ```coretemp_warning.py```.

It will sending email if the CPU temperature higher then critical value.
```text
2021-02-26 11:11:19 | Temperature report complete.
```
Otherwise it will print:
```text
2021-02-26 11:11:31 | Core temperature under critical value.
```
### IP address check
Refer to ```ip_address_notice.py```.

Configure the ```mode_select``` to select IPv4 only or IPv6 only.
- If you set ```mode_select``` to ```IPv4```  
Compare IPv4 only.
- If you set ```mode_select``` to ```IPv6```  
Compare IPv6 only.

If address no change, it will print.
```text
2021-02-26 11:28:56 | No changes detected.
```
If changes detected, depend on ```mode_select```, it will sending email and print.
- IPv4 only
```text
2021-02-26 11:28:14 | 114.514.19.19
```
- IPv6 only
```text
2021-02-26 11:28:14 | 8930:8100:1145:141:919:36:114:514
```
- If ```mode_select``` is default (```False```)
```text
2021-02-26 11:28:14 | [True, False] | 1.1.1.1 | 8930:8100:1145:141:919:36:114:514
```
```False``` means that IPv6 has been change.
### Program Checker
Refer to ```program_checker.py```.
If the query program or process not found, it will sending email and print.
```text
2021-02-26 11:12:55 | Program not found.
2021-02-26 11:12:55 | Status report complete.
```
Otherwise it will print:
```text
2021-02-26 11:13:20 | Program found in process list.
```
### Error handling
Error message store at ```error.log```

## Dependencies
### Python version
- Python 3.6 or above
### Python module
- os
- re
- sys
- json
- email
- socket
- getpass
- smtplib
- logging
- requests
- datetime
- subprocess

## License
General Public License -3.0

## Resources
- [RPI vcgencmd usage](http://www.elinux.org/RPI_vcgencmd_usage)  
- [RPi-Core-Temp-Python-Script](https://github.com/PanosXY/RPi-Core-Temp-Python-Script)
- [Python Ps-grep Processes Kill](https://puremonkey2010.blogspot.tw/2013/09/python-ps-grep-processes-kill.html)
- [Monitor the core temperature of your Raspberry Pi](https://medium.com/@kevalpatel2106/monitor-the-core-temperature-of-your-raspberry-pi-3ddfdf82989f)
