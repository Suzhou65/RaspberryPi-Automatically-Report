# Raspberry Pi Automatically Report
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/)
[![rpi](https://github.takahashi65.info/lib_badge/raspberry-pi.svg)](https://www.raspberrypi.org/)
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/RaspberryPi-Automatically-Report)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/RaspberryPi-Automatically-Report.svg)](https://github.com/axetroy/github-size-badge)

Simply Python automatically report module working on Raspberry Pi.

## Contents
- [Raspberry Pi Automatically Report](#raspberry-pi-automatically-report)
  * [Usage](#usage)
    + [Automatically running](#automatically-running)
    + [Email sending](#email-sending)
    + [Temperature alert](#temperature-alert)
    + [IP address change detection](#ip-address-change-detection)
  * [Python module](#python-module)
  * [Function](#python-module)
    + [Temperature report](#temperature-report)
    + [Temperature high alert](#temperature-high-alert)
    + [IPv4 address check](#ipv4-address-check)
    + [IP address check](#ip-address-check)
    + [Program Checker](#program-checker)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module-1)
  * [License](#license)
  * [Resources](#resources)

## Usage
### Automatically running
[![cron](https://github.takahashi65.info/lib_badge/cron-jobs.svg)](https://en.wikipedia.org/wiki/Cron)  
Automatically execute via cron, recommend using crontab.
  
**For example:**  
- coretemp_warning.py will automatically running every hours from 9:00 to 22:00.
- ip_overwatch64.py will automatically running every hour.

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
0 */1   * * *   pi python /home/pi/python_script/ip_overwatch64.py
#
```

### Email sending
Google account needed, sign in using App passwords.  
If you know other mail service domain & port setting, it can be modify easy.
```python
sender_account = "midsummer@lewd.dream"
sender_password = "3f7a9d18e117a65860"
receiver = "kokosuki@lewd.dream"
```
- **sender_account** is the Google account for sending mail. 
- **sender_password** is the App passwords.
- **receiver** is the receiving address.

### Temperature alert
Critical value is necessary, can be integer or floating point.
```python
critical = 55
```
- **critical** is the critical value, unit of temperature is degree celsius.

### IP address change detection
For initialization, default address is necessary.
```python
ipv4 = "1.1.1.1"
ipv6 = "2606:4700:4700::1111"
```
- **ipv4** is the IPv4 address.
- **ipv6** is the IPv6 address.

## Python module
- Import the module
```python
import automatically_report
```
```python
import automatically_report as automatically
```

- Alternatively, you can import the function independent
```python
from automatically_report import temp_report
```

## Function
### Temperature report
```python
from automatically_report import temp_report

sender_account = "midsummer@lewd.dream"
sender_password = "3f7a9d18e117a65860"
receiver = "kokosuki@lewd.dream"

cpu_status =temp_report(sender_account, sender_password, receiver)
print(cpu_status)
```
It will sending email and print CPU temperature as result.
```text
41
```
If error occurred, it will return error massage.

### Temperature high alert
```python
from automatically_report import temp_warning

sender_account = "midsummer@lewd.dream"
sender_password = "3f7a9d18e117a65860"
receiver = "kokosuki@lewd.dream"
critical = 55

critical_level = temp_warning(sender_account, sender_password, receiver, critical)
print(critical_level)
```
It will sending email if the CPU temperature higher then critical value. otherwise it will print:
```text
Core temperature under critical value
```
If error occurred, it will return error massage.

### IPv4 address check
```python
from automatically_report import address_check_4

sender_account = "midsummer@lewd.dream"
sender_password = "3f7a9d18e117a65860"
receiver = "kokosuki@lewd.dream"
ipv4 = "1.1.1.1"

check4 = address_check_4(sender_account, sender_password, receiver, ipv4)
print(check4)
```
It will sending email if the IPv4 address change, otherwise it will print:
```text
IPv4 address no change.
```
This function will also return the boolean of compare, and IP address by list as result.
```python
[True, True, '114.514.19.19']
```
If error occurred, it will return error massage.

### IP address check
```python
from automatically_report import address_check_64

sender_account = "midsummer@lewd.dream"
sender_password = "3f7a9d18e117a65860"
receiver = "kokosuki@lewd.dream"
ipv4 = "1.1.1.1"
ipv6 = "2606:4700:4700::1111"

check64 = address_check_64(sender_account, sender_password, receiver, ipv4, ipv6)
print(check64)
```
It will sending email if the IP address change, otherwise it will print:
```text
IP address no change
```
This function will also return the boolean of compare, and IP address by list as result.
```python
[True, False, False, '114.514.19.19', '8930:8100:1145:141:919:36:114:514']
```
If error occurred, it will return error massage.

### Program Checker
```python
from automatically_report import program_checker

sender_account = "midsummer@lewd.dream"
sender_password = "3f7a9d18e117a65860"
receiver = "kokosuki@lewd.dream"
program = "HentaiAtHome.jar"

ps_result = program_checker(sender_account, sender_password, receiver, program)
print(ps_result)
```
It will sending email if the program not found in list, otherwise it will print it, this function will return the result by list.
```python
['20552 Sl+ java-jarHentaiAtHome.jar']
```
If error occurred, it will return error massage.

## Dependencies
### Python version
- Python 3.6 or above

### Python module
- os
- subprocess
- datetime
- socket
- requests
- json
- smtplib
- email
- csv

## License
General Public License -3.0

## Resources
- [RPI vcgencmd usage](http://www.elinux.org/RPI_vcgencmd_usage)  
- [RPi-Core-Temp-Python-Script](https://github.com/PanosXY/RPi-Core-Temp-Python-Script)
- [Python Ps-grep Processes Kill](https://puremonkey2010.blogspot.tw/2013/09/python-ps-grep-processes-kill.html)
- [Monitor the core temperature of your Raspberry Pi](https://medium.com/@kevalpatel2106/monitor-the-core-temperature-of-your-raspberry-pi-3ddfdf82989f)
