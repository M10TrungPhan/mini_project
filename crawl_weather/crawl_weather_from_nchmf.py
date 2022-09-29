import requests
from bs4 import BeautifulSoup
import re
import json

class CrawlWeatherFromNCHMF:

    def __init__(self):
        self.url = "https://nchmf.gov.vn/Kttv/vi-VN/1/index.html"
        self.html = None
        self.data_total_location = []

    @staticmethod
    def requests_html(url):
        res = None
        for i in range(5):
            try:
                res = requests.get(url)
                break
            except:
                res = None
        if res is None:
            return None
        return BeautifulSoup(res.text, "lxml")

    @staticmethod
    def get_all_href_location(soup):
        all_href_location = []
        box_wrap = soup.find("div", class_="wt-city uk-position-relative uk-box-shadow-small")
        all_box_location = box_wrap.find_all("li")
        for each in all_box_location:
            all_href_location.append(each.find("a", class_="name-wt-city").get("href"))
        return all_href_location

    def get_weather_data_in_location(self, url_location):
        soup = self.requests_html(url_location)
        name_location = self.get_name_location(soup)
        data_for_location = {"location": name_location}
        box_weather_today = soup.find("div", class_="content-news fix-content-news")
        data_today = self.get_weather_today(box_weather_today)
        box_weather_prediction = soup.find("div", class_="ten-days-weather")
        data_prediction = self.get_prediction_weather_ten_day(box_weather_prediction)
        data_for_location["today_forecast"] = data_today
        data_for_location["incoming_days_forecast"] = data_prediction
        return data_for_location

    @staticmethod
    def get_name_location(soup):
        name_box = soup.find("h1", class_="tt-news")
        name = None
        if name_box is not None:
            name = name_box.text.strip()
        if re.search(r"Thời tiết", name) is not None:
            start, end = re.search(r"Thời tiết", name).span()
            name = name[end:].strip()
        return name

    def get_weather_today(self, box_weather_today):
        data_today = []
        all_box_prediction_today = box_weather_today.find_all("div", class_="text-weather-location fix-weather-location")
        for each in all_box_prediction_today:
            data_new = self.get_current_weather(each)
            data_today.append(data_new)
        return data_today

    @staticmethod
    def get_current_weather(box_current):
        name_box = box_current.find("a")
        if name_box is None:
            name = None
        else:
            name = name_box.text
        if box_current is None:
            return None
        box_time = box_current.find("div", class_="time-update")
        # GET TIME
        if box_time is not None:
            update_time = box_time.text
            if re.search(r"Cập nhật:", update_time) is not None:
                start, end = re.search(r"Cập nhật:", update_time).span()
                update_time = update_time[end:].strip()
                update_time = re.sub(r"\s+", " ", update_time)
        else:
            update_time = None
        # GET ATTRIBUTE
        box_attribute = box_current.find("ul", class_="list-info-wt uk-list")
        atrribute = {}
        if box_attribute is not None:
            all_element_attribute = box_attribute.find_all("li")
            for each_element in all_element_attribute:
                name_attribute = each_element.find("div", class_="uk-width-1-4")
                value_attribute = each_element.find("div", class_="uk-width-3-4")
                if (name_attribute is not None) and (value_attribute is not None):
                    atrribute[name_attribute.text.strip()] = value_attribute.text.replace(":", "").strip()
        return {"type_of_prediction": name, "updated_time": update_time, "prediction": atrribute}

    def get_prediction_weather_ten_day(self, box_weather_prediction):
        data_prediction = []
        all_box_prediction = box_weather_prediction.find_all("div", class_="item-days-wt")
        for each_box in all_box_prediction:
            data_new = self.get_prediction_weather_one_day(each_box)
            data_prediction.append(data_new)
        return data_prediction

    def get_prediction_weather_one_day(self, box_prediction):
        data_one_day = {}
        # GET TIME PREDICTION
        box_time_prediction = box_prediction.find("div", class_="date-wt")
        if box_time_prediction is not None:
            time_prediction = box_time_prediction.text.strip()
        else:
            time_prediction = None
        data_one_day["forecast_time"] = time_prediction
        # GET ATTRIBUTE PREDICTION
        all_box_attribute = box_prediction.find_all("div", class_="temp-days-wt")

        for each_box in all_box_attribute:
            image = each_box.find("img")
            if image is None:
                continue
            image = image.get("src")
            name_attribute = self.get_name_attribute_from_icon(image)
            value_attribute = each_box.find("span")
            if value_attribute is None:
                continue
            value_attribute = value_attribute.text.replace("", "").strip()
            data_one_day[name_attribute] = value_attribute
        # GET DESCRIPTION PREDICTION
        box_description = box_prediction.find("div", class_="text-temp")
        description = None
        if box_description is not None:
            description = box_description.text.strip()
        data_one_day["description"] = description
        return data_one_day

    @staticmethod
    def get_name_attribute_from_icon(image):
        if re.search(r"temperature_Hi\.png$", image) is not None:
            return "highest_temperature"
        if re.search(r"temperature_Lo\.png$", image) is not None:
            return "lowest_temperature"
        if re.search(r"temperature_Humidity\.png$", image) is not None:
            return "humidity"
        if re.search(r"probabilityofrain\.png$", image) is not None:
            return "rain_probability"
        if re.search(r"W\.jpg$", image) is not None:
            return "wind_spped"
        return "Unknown"

    def get_weather_for_all_location(self):
        data_all_location = []
        soup_index = self.requests_html(self.url)
        all_location_url = self.get_all_href_location(soup_index)
        for each_url in all_location_url:
            data_new = self.get_weather_data_in_location(each_url)
            data_all_location.append(data_new)
        self.data_total_location = data_all_location
        json.dump(self.data_total_location, open("data_total.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
        return self.data_total_location


abc = CrawlWeatherFromNCHMF()
abc.get_weather_for_all_location()