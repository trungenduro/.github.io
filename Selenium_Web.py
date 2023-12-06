from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading
import tkinter as tk
from tkinter import ttk

def GetPrices():
	global driver
	global codes
	global user_name
	elements = driver.find_elements(By.CLASS_NAME, "cell-05")
	prices=[]
	for i in range(len(elements)):
		e1 = elements[i].find_element(By.CLASS_NAME, "mbody")	
		#print(e1.text)
		if i%2==0:		
			prices.append(float( e1.text.replace(",","").split(' ')[0].replace('-','0')))
			


	elements = driver.find_elements(By.CLASS_NAME, "align-C")
	
	elements=elements[10:]
	codes=[]
	for i in range(len(elements)):
		if i%2==0:
			e1 = elements[i].find_element(By.CLASS_NAME, "mbody")	
			#print(f"{i}  {e1.text}")
			codes.append( e1.text)
		
	elements = driver.find_elements(By.CLASS_NAME, "align-L")

	hrefElements=[]
	names=[]
	for i in range(len(elements)):
		e1 = elements[i].find_elements(By.XPATH, '*')
		if len(e1)>0:
			e2 = e1[0].find_elements(By.XPATH, '*')
			names.append(e1[0].text  )
			hrefElements.append( e1[0])
	result=[]
	result.append(names)		
	result.append(codes)		
	result.append(prices)
	result.append(hrefElements)	
	
	return result	



def AddNewPrice(olds,news):
	global test
	global AllChecks
	global AllChecks
	global user_name
	global Label1_str
	global Label2_str
	for x in range(len(news[2])):
		print(test[1][x],user_name.get())	
		if 	test[1][x]==user_name.get():
			Label1_str.set(test[0][x])
			Label2_str.set(test[2][x])
		if olds[x][-1] != test[2][x]:
			#print(f"{names[x]}: {olds[x][-1]} => {test[2][x]}")
			olds[x].append(test[2][x])
			if olds[x][-1] < test[2][x]:
				AllChecks[x].append('+')
			else:
				AllChecks[x].append('-')
			
			if 	codes[x]==user_name.get():
				print(f"		{names[x]}  Giam 3   {olds[x][-10:-1]}  {''.join(AllChecks[x][-10:-1])}")
			if "--" in ''.join(AllChecks[x][-2:-1]):
				print(f"{names[x]}  Giam 3   {olds[x][-10:-1]}  {''.join(AllChecks[x][-10:-1])}")
				
			if "++" in ''.join(AllChecks[x][-2:-1]):
				print(f"{names[x]}  Tang 3  {olds[x][-10:-1]}  {''.join(AllChecks[x][-10:-1])}")
							
			if "-----" in ''.join(AllChecks[x][-5:-1]):
				print(f"{names[x]}  Ban gap  {olds[x][-10:-1]}  {''.join(AllChecks[x][-10:-1])} ")				
			if "+++++" in ''.join(AllChecks[x][-5:-1]):
				print(f"{names[x]}  Mua gap  {olds[x][-10:-1]}  {''.join(AllChecks[x][-10:-1])} ")				

	return olds		

def start():
	global driver
	global test
	global AllChecks
	global AllPrices
	global names
	global codes
	global user_name
	global Label1_str
	print("start google")
	#driver.set_window_position(-10000,0)
	driver.get('https://www.rakuten-sec.co.jp/')


	time.sleep(0.1)

	element=driver.find_element(By.ID,"form-login-id");
	element.send_keys("FKVD9994")
	#id="login_password"
	element=driver.find_element(By.ID,"form-login-pass");
	element.send_keys("trung1081")
	element.send_keys(Keys.ENTER)
	time.sleep(0.1)




	#pcm-gl-nav-01__button
	#pcm-gl-nav-01__button-inner  pcm-gl-nav-02__button
	element = driver.find_element(By.CLASS_NAME, "pcm-gl-nav-01__button-inner")
	href = element.get_attribute('href')
	element.click()
	time.sleep(0.1)

	#//pcm-gl-nav-02__button
	element = driver.find_element(By.CLASS_NAME, "pcm-gl-nav-02__button")

	elements = driver.find_elements(By.CLASS_NAME, "pcm-gl-nav-02__button")

	href = element.get_attribute('href')

	elements[1].click()
	time.sleep(0.1)

	test = GetPrices()
	AllPrices=[]
	AllChecks=[]
	names=test[0]
	for x in range(len(test[2])):
		temp=[test[2][x]]
		AllPrices.append(temp)
		AllChecks.append([''])
	i=0
	print(test[1])
	while i<100:		  
	  driver.refresh()
	  time.sleep(1)
	  test = GetPrices()
	  AllPrices=AddNewPrice(AllPrices,test)
	  i=i+1
	  print(f"======{i}======")
	#print(AllPrices)
	#print(AllChecks)
	print(f"========")

def startForm():
	global root
	root = tk.Tk()
	root.title("Greeter")
	global user_name 
	user_name= tk.StringVar()
	global Label1_str 
	Label1_str= tk.StringVar()
	global Label2_str 
	Label2_str= tk.StringVar()
	Label1_str.set("label1")
	Label2_str.set("label2")
	main = ttk.Frame(root, padding=(20, 10, 20, 0))
	main.grid()

	root.columnconfigure(0, weight=1)
	root.rowconfigure(1, weight=1)
	name_label = ttk.Label(main, text="Name:")
	name_label.grid(row=0, column=0, padx=(0, 10))
	name_entry = ttk.Entry(main, width=15, textvariable=user_name)
	name_entry.grid(row=0, column=1)
	name_entry.focus()

	Label1 = ttk.Label(main, textvariable=Label1_str)
	Label1.grid(row=1, column=0, columnspan=1, sticky="W", pady=(10, 0))

	Label2 = ttk.Label(main, textvariable=Label2_str)
	Label2.grid(row=1, column=1, columnspan=1, sticky="W", pady=(10, 0))

	buttons = ttk.Frame(main, padding=(0, 10))
	buttons.grid(row=2, column=0, columnspan=2, sticky="EW")

	# buttons.columnconfigure(0, weight=1)
	# buttons.columnconfigure(1, weight=1)

	buttons.columnconfigure((0, 1), weight=1)
	start_button = ttk.Button(buttons, text="Start", command=greet)
	start_button.grid(row=0, column=0, sticky="EW")

	ban_button = ttk.Button(buttons, text="Mua", command=greet)
	ban_button.grid(row=0, column=1, sticky="EW")

	quit_button = ttk.Button(buttons, text="Quit", command=root.destroy)
	quit_button.grid(row=0, column=2, sticky="EW")

	root.bind("<Return>", greet)
	root.bind("KP_Enter", greet)

	root.mainloop()
def greet(*args):
    #greeting_message.set(f"Hello, {name or 'World'}!")
    thread1 = threading.Thread(target=start)
    thread1.start()

AllPrices=[]
AllChecks=[]
test=[]
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options	)
startForm()	
