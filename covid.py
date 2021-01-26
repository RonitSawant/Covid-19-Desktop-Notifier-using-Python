from tkinter import *
import bs4
import requests
import threading
import time
import datetime
import plyer
from PIL import Image,ImageTk

def get_Data(url):
	r = requests.get(url)
	return r

def get_corona_detail_india():
	url = "https://www.mohfw.gov.in/"
	data = get_Data(url)
	bs = bs4.BeautifulSoup(data.text,'html.parser')
	info = bs.findAll(True,{"class":["bg-blue","bg-green","bg-red","bg-orange"]})
	covid_info = ""
	for mydata in info:
		count = mydata.find("strong").get_text()
		text = mydata.find("span").get_text()
		covid_info += text + " : " + count + "\n"
	return covid_info


def get_corona_detail_mah():
	url = "https://www.mohfw.gov.in/"
	data = get_Data(url)
	bs = bs4.BeautifulSoup(data.text,'html.parser')
	mahinfo = ""
	for tr in bs.findAll('tr'):
		mahinfo += tr.get_text()
	item_list = mahinfo.split("\n\n")
	state = "Maharashtra"
	for item in item_list[1:36]:
		state_data = item.split('\n')
		if state_data[1] == state:
			stext = f"{state_data[1]}\nActive Cases : {state_data[2]}\nCured/Discharged : {state_data[3]}\nDeaths : {state_data[4]}\nConfirmed Cases : {state_data[5]}"
	return stext

def notify_me():
	while True:
		plyer.notification.notify(
			title = "COVID-19 cases of Maharashtra",
			message = get_corona_detail_mah(),
			timeout = 10,
			app_icon = 'corona.ico'
		)
		time.sleep(30)


#Create GUI
root = Tk()
root.iconbitmap("corona.ico")
c1 = PhotoImage(file="back2.png")
root.geometry("600x500+300+200")
root.title("COVID-19 INDIA TRACKER ")

panel = Label(root,image=c1)
panel.grid(row=0,column=0)
display = Label(root,text=get_corona_detail_india(),font=("poppins",20,"italic"))
display.grid(row=0,column=0,sticky=N)
display1 = Label(root,text=get_corona_detail_mah(),font=("poppins",20,"italic"),background='gray99')
display1.grid(row=0,column=0)

#Create new thread
th = threading.Thread(target=notify_me)
th.setDaemon(True)
th.start()

root.mainloop()