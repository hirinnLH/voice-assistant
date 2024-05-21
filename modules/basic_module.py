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
            # 'longitude': float(data.get('longitude')),
            # 'latitude': float(data.get('latitude'))
        }
        return location
    else:
        return None


def get_city_weather(city: list):
    # api地址
    url = 'http://t.weather.sojson.com/api/weather/city/'

    # 读取json文件
    with open('utils/city.json', 'rb') as f:
        # 使用json模块的load方法加载json数据，返回一个字典
        cities = json.load(f)

    final_result = ""
    if len(city) == 0:
        ip_address = _get_ip_address()
        city.append(_get_location_by_ip_address(ip_address)['city'])
    for each_city in city:
        # 通过城市的中文获取城市代码
        city_code = cities.get(each_city)
        if city_code is None:
            print("Not supported city")
            return
        # 网络请求，传入请求api+城市代码
        response = requests.get(url + city_code)
        # 将数据以json形式返回，这个d就是返回的json数据
        d = response.json()
        # 当返回状态码为200，输出天气状况
        if d['status'] == 200:
            city_result = "城市：" + d["cityInfo"]["parent"] + " " + d["cityInfo"]["city"] + "\n"
            time_result = "时间：" + d["time"] + " " + d["data"]["forecast"][0]["week"] + "\n"
            temper_result = "温度：" + d["data"]["forecast"][0]["high"] + " " + d["data"]["forecast"][0]["low"] + "\n"
            weather_result = "天气：" + d["data"]["forecast"][0]["type"]
            final_result = city_result + time_result + temper_result + weather_result

    return final_result


BasicFunction = {
    'datetime_query': get_current_time,
    'weather_query': get_city_weather
}
