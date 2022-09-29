import requests
from bs4 import BeautifulSoup
import re


class CrawlWeatherFromVNMHA:

    def __init__(self):
        self.url = "http://vnmha.gov.vn/nchmf-new/show-city-weather"
        self.html = None
        self.time_for_weather = None
        self.information_weather = []
        self.data = {}

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

    def get_time(self):
        soup = self.html
        box_time = soup.find("div", class_="col-md-9 col-sm-12").find("p")
        string_all_time = box_time.text
        if re.search(r"lúc:", string_all_time) is not None:
            start, end = re.search(r"lúc:", string_all_time).span()
            time_weather = string_all_time[end:].strip()
        else:
            time_weather = string_all_time
        self.time_for_weather = time_weather
        return self.time_for_weather

    def get_information_weather_for_all(self):
        data = []
        soup = self.html
        box_weather = soup.find("div", class_="col-md-9 col-sm-12").find("div", class_="row")
        all_box_location_weather = box_weather.find_all("div", class_="col-md-4")
        if not len(all_box_location_weather):
            return []
        for each_loaction in all_box_location_weather:
            data_new = self.get_information_weather_in_location(each_loaction)
            data.append(data_new)
        return data

    def get_information_weather_in_location(self, box_location_weather):
        return {"Địa điểm":self.get_location(box_location_weather),
                "Nhiệt độ": self.get_temperature(box_location_weather),
                "Trạng thái": self.get_status_in_location(box_location_weather)}

    def get_status_in_location(self, box_location_weather):
        box_image = box_location_weather.find("div", class_="weather-icon").find("img").get("src")
        return self.covert_image_to_status(box_image)

    @staticmethod
    def covert_image_to_status(image):
        if re.search(r"261\.png$", image):
            return "Nhiều mây"
        if re.search(r"340\.png$", image):
            return "Có nắng, ít mây"
        if re.search(r"300\.png$", image):
            return "Có nắng, nhiều mây"
        if re.search(r"40\.png$", image):
            return "Nhiều mây, có mưa giông"


    @staticmethod
    def get_location(box_location_weather):
        return box_location_weather.find("div", class_="info").find("h3").text.strip()

    @staticmethod
    def get_temperature(box_location_weather):
        string_all = box_location_weather.find("div", class_="info").find("p").text.strip()
        if re.search(r"Nhiệt độ :", string_all) is not None:
            start, end = re.search(r"Nhiệt độ :", string_all).span()
            temperature = string_all[end:].strip()
        else:
            temperature = string_all
        return temperature

    def get_data(self):
        self.html = self.requests_html(self.url)
        self.time_for_weather = self.get_time()
        self.information_weather = self.get_information_weather_for_all()
        self.data["Time"] = self.time_for_weather
        self.data["Information"] = self.information_weather
        return self.data

wether = CrawlWeatherFromVNMHA()
wether.get_data()
print(wether.data)