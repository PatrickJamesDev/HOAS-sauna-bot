import selenium
from selenium import webdriver
import datetime
from datetime import datetime
from datetime import date
import time
from selenium.webdriver.common.by import By

import os

import telebot

token="xxxxxxxx"  #Telegram bot token here


bot = telebot.TeleBot(token)



url="https://booking.hoas.fi/varaus/service/timetable/426/23/01/2023"

saunas=["SAUNA, JÄMERÄNTAIVAL 11, STAIRCASE E", "SAUNA 3, JÄMERÄNTAIVAL 11, STAIRCASE M  | "] #put the names of the saunas you want to reserve here

#function uses selenium to log into the website using the given credentials
def login(url, username, password,driver): #works


    #use selenium to input username into login field and password into password field
    username_field = driver.find_element("name","login")
    username_field.send_keys(username)
    password_field = driver.find_element("name","password")
    password_field.send_keys(password)

    submit= driver.find_element("name","submit")
    submit.click()


#selects class"Saunavuorot" and then clicks it

def click_saunavuorot(url,driver): #works
# driver = webdriver.Chrome()
    # driver.get(url)
    sauna_class = driver.find_element(By.CLASS_NAME,'saunavuorot')
    sauna_class.click()

def click_reserve(url,driver): #opens reservation url and and spams it to reserve sauna
                               # if sauna turn is still available 15 minutes after it has begun, reserve it using selenium

    now = datetime.now()
    while 17<=now.hour<22 or True:
        while 14<=now.minute<=16:
            driver.get(url)

def create_url(): #creates reservation url for sauna 11M and 11E for today at the current hour

    today = date.today()
    urlM=f"https://booking.hoas.fi/varaus/service/reserve/8/{datetime.now().hour}.00/{today.year}-0{today.month}-{today.day}"
    urlE =f"https://booking.hoas.fi/varaus/service/reserve/707/{datetime.now().hour}.00/{today.year}-0{today.month}-{today.day}"

    return urlM,urlE

def check_reservation(driver): #checks to see if reservation was successful
    #if the date and time in "myReservations" matches the current date and time, then the reservation was successful
    #check to see if the date and time are equivalent


    my_reservations = driver.find_element(By.CLASS_NAME, 'myReservations')


    return my_reservations


def tele_bot(): #sends telegram message when sauna is successfully reserved:
    bot.send_message(x, f"Sauna reserved at: {datetime.now().hour}, 11M") #x is the chat id of the telegram chat you want to send the message to

def main():
    driver = webdriver.Chrome()
    driver.get(url)
    now = datetime.now()

    password="x" #password here
    username="x" #username here
    login(url, username, password,driver)
    click_saunavuorot(url,driver)

    urlM,urlE, urlX=create_url()

    click_reserve(urlE,driver)
    click_reserve(urlM, driver)

    list_of_reservations=check_reservation(driver).text.splitlines()


    if list_of_reservations[0].split()[1]==str(f"{datetime.now().day}.0{datetime.now().month}.{datetime.now().year}") and list_of_reservations[0].split()[2]==str(datetime.now().hour)+".00":
        tele_bot()





main()