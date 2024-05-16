import datetime
import requests


def get_current_time():
    """
    To get the current time from system time

    return
    str: Current system time
    """
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time


def _get_ip_address():
    """
    To get the ip address for current device

    return
    str: ip address for current device
    """
    response = requests.get('https://api.ipify.org')
    return response.text


def _get_location_by_ip_address(ip_address: str):
    url = 'https://ip.taobao.com/outGetIpInfo?ip={}&accessKey=alibaba-inc'.format(ip_address)
    response = requests.get(url)
    result = response.json()
    if result['code'] == 0:
        data = result['data']
        location = {
            'city': data.get('city'),
            'longitude': float(data.get('longitude')),
            'latitude': float(data.get('latitude'))
        }
        return location
    else:
        return None


BasicFunction = {
    'get_current_time': get_current_time
}
