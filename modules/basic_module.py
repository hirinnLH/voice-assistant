import datetime

import json
import requests


def get_current_time():
    """
    To get the current time from system time

    return
    str: Current system time
    """
    current_datetime = datetime.datetime.now()
    current_time = {
        "year": current_datetime.year,
        "month": current_datetime.month,
        "day": current_datetime.day,
        "hour": current_datetime.hour,
        "minute": current_datetime.minute,
        "second": current_datetime.second,
        "weekday": current_datetime.weekday()
    }
    return current_time


def _get_ip_address():
    """
    To get the ip address for current device

    return
    str: ip address for current device
    """
    response = requests.get("https://api.ipify.org")
    return response.text


def _get_location_by_ip_address(ip_address: str):
    url = "https://ip.taobao.com/outGetIpInfo?ip={}&accessKey=alibaba-inc".format(ip_address)
    response = requests.get(url)
    result = response.json()
    if result["code"] == 0:
        data = result["data"]
        location = {
            "city": data.get("city"),
            # "longitude": float(data.get("longitude")),
            # "latitude": float(data.get("latitude"))
        }
        return location
    else:
        return None


def get_city_weather(cities: list):
    # api address
    url = "http://t.weather.sojson.com/api/weather/city/"

    # read city code from json file
    with open("utils/data/weather_city_code.json", "rb") as f:
        city_code_list = json.load(f)

    final_result = ""
    if len(cities) == 0:
        ip_address = _get_ip_address()
        current_city = _get_location_by_ip_address(ip_address)
        if current_city is None or current_city["city"] == "XX":
            cities.append("上海")
        else:
            cities.append(current_city["city"])
    for each_city in cities:
        # get city code through city's name
        city_code = city_code_list.get(each_city)
        if city_code is None:
            print("Not supported city")
            return
        response = requests.get(url + city_code)
        weather_response = response.json()
        # when status code is 200, return the weather result
        if weather_response["status"] == 200:
            city_weather = {
                "status": "success",
                "city": weather_response["cityInfo"]["city"],
                "time": weather_response["time"],
                "weekday": weather_response["data"]["forecast"][0]["week"],
                "high_temper": weather_response["data"]["forecast"][0]["high"],
                "low_temper": weather_response["data"]["forecast"][0]["low"],
                "weather_type": weather_response["data"]["forecast"][0]["type"],
                "weather_notice": weather_response["data"]["forecast"][0]["notice"]
            }
        else:
            city_weather = {
                "status": "error"
            }
    return city_weather


BasicFunction = {
    "datetime_query": get_current_time,
    "weather_query": get_city_weather
}
