from bs4 import BeautifulSoup
import requests as req
from env import ZILLOW_URL,HTTP_HEADER,CHROME_DRIVER_PATH,GOOGLE_FORM
from pprint import pprint
from selenium import webdriver
import time






def get_data():
    res = req.get(url=ZILLOW_URL,headers = HTTP_HEADER)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"html.parser")
    address_elements = soup.select("address")
    url_elements = soup.select(".list-card-img")
    price_elements = soup.select(".list-card-price")
    data = []

    for i in range(len(address_elements)):
        thisAddress = address_elements[i].getText()
        thisPrice = int(price_elements[i].getText()[1:6].replace(",",""))
        thisURL = url_elements[i].get("href")
        data.append([thisAddress,thisPrice,thisURL])

    return data



def enter_data(data):
    for i in range(len(data)):
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        driver.get(url=GOOGLE_FORM)
        time.sleep(5)
        inputs = driver.find_elements_by_class_name("exportInput")
        address_input = inputs[0]
        price_input = inputs[1]
        url_input = inputs[2]
        address_input.send_keys(data[i][0])
        price_input.send_keys(data[i][1])
        url_input.send_keys(data[i][2])
        button = driver.find_element_by_class_name("exportButtonContent")
        button.click()
        driver.quit()

    print("Submission done!")






entry_data = get_data()
enter_data(entry_data)

