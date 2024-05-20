import datetime
import requests, json


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


def get_city_weather(city: list):
    #api地址
    url = 'http://t.weather.sojson.com/api/weather/city/'

    #读取json文件
    f = open('city.json', 'rb')

    #使用json模块的load方法加载json数据，返回一个字典
    cities = json.load(f)

    #通过城市的中文获取城市代码
    city = cities.get(city[0])

    #网络请求，传入请求api+城市代码
    response = requests.get(url + city)

    #将数据以json形式返回，这个d就是返回的json数据
    d = response.json()

    #当返回状态码为200，输出天气状况
    if d['status'] == 200:
        print("城市：", d["cityInfo"]["parent"], d["cityInfo"]["city"])
        print("时间：", d["time"], d["data"]["forecast"][0]["week"])
        print("温度：", d["data"]["forecast"][0]["high"], d["data"]["forecast"][0]["low"])
        print("天气：", d["data"]["forecast"][0]["type"])


BasicFunction = {
    'datetime_query': get_current_time,
    'weather_query': get_city_weather
}
