def response_current_time(current_time: dict):
    hour = current_time.get("hour")
    minute = current_time.get("minute")
    response = "現在是%d點%d分" % (hour, minute)
    return response


def response_today_date(current_time: dict):
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    weekday = week_list[current_time.get("weekday")]
    month = current_time.get("month")
    day = current_time.get("day")
    response = "今天是%d月%d號，%s" % (month, day, weekday)
    return response


def response_today_weather(weather: dict):
    if weather.get("status") == "error":
        return "查詢失敗，別試了"
    city = weather.get("city")
    time = weather.get("time")
    weekday = weather.get("weekday")
    high_temper = weather.get("high_temper").split()[1]
    low_temper = weather.get("low_temper").split()[1]
    weather_type = weather.get("weather_type")
    weather_notice = weather.get("weather_notice")
    response = "%s%s到%s，天氣%s，%s" % (city, low_temper, high_temper, weather_type, weather_notice)
    return response


BasicResponse = {
    "time_query": response_current_time,
    "date_query": response_today_date,
    "weather_query": response_today_weather
}
