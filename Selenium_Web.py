from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading
import tkinter as tk
import datetime
from tkinter import ttk

def GetPrices():
	global driver
	global codes
	global user_name
	global hrefElements
	global startListUrl
	driver.get(startListUrl)
	time.sleep(0.1)
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
		#print(test[1][x],user_name.get())	

		if olds[x][-1] != test[2][x]:
			#print(f"{names[x]}: {olds[x][-1]} => {test[2][x]}")
			
			if olds[x][-1] < test[2][x]:
				AllChecks[x].append('+')
			else:
				AllChecks[x].append('-')
			if 	test[1][x]==user_name.get():
				Label1_str.set(f"{test[2][x]} ({max(olds[x])}-{min(olds[x])})")
				Label2_str.set(''.join(AllChecks[x][-10:-1]))
				print(f"{names[x]} : {olds[x][-1]} -> {test[2][x]}  {test[2][x]-olds[x][-1]}  ")
			olds[x].append(test[2][x])	
			maxP = max(olds[x])
			minP = min(olds[x])

			if 	codes[x]==user_name.get():
				print(f"		{names[x]}  Giam 3   {olds[x][-10:-1]}  {''.join(AllChecks[x][-10:-1])}")
			if "--" in ''.join(AllChecks[x][-2:-1]):
				print(f"{names[x]}  Giam 3   {olds[x][-10:-1]} {max(olds[x])}-{min(olds[x])} {''.join(AllChecks[x][-10:-1])}")
				
			if "++" in ''.join(AllChecks[x][-2:-1]):
				print(f"{names[x]}  Tang 3  {olds[x][-10:-1]} {max(olds[x])}-{min(olds[x])} {''.join(AllChecks[x][-10:-1])}")
							
			if "-----" in ''.join(AllChecks[x][-5:-1]):
				print(f"{names[x]}  Ban gap  {olds[x][-10:-1]} {max(olds[x])}-{min(olds[x])} {''.join(AllChecks[x][-10:-1])} ")				
			if "+++++" in ''.join(AllChecks[x][-5:-1]):
				print(f"{names[x]}  Mua gap  {olds[x][-10:-1]} {max(olds[x])}-{min(olds[x])} {''.join(AllChecks[x][-10:-1])} ")				

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
	global Label2_str
	global Label3_str
	global qtyStr
	global listbox
	global startListUrl
	global session
	print("start google")
	dt_now = datetime.datetime.now()
	now=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
	print(f"===start google==={now}======")
	#driver.set_window_position(-10000,0)
	driver.get('https://www.rakuten-sec.co.jp/')
	#driver.title

	time.sleep(0.1)

	element=driver.find_element(By.ID,"form-login-id");
	element.send_keys("FKVD9994")
	#id="login_password"
	element=driver.find_element(By.ID,"form-login-pass");
	element.send_keys("trung1081")
	element.send_keys(Keys.ENTER)
	time.sleep(0.1)
	session=driver.current_url.split("BV_SessionID=")[1].split('?')[0]
	print(f"url * { driver.current_url}  session={session}")
	startListUrl=f"https://member.rakuten-sec.co.jp/app/info_jp_prc_reg_lst.do;BV_SessionID={session}?eventType=init&gmn=M"


	#pcm-gl-nav-01__button
	#pcm-gl-nav-01__button-inner  pcm-gl-nav-02__button
	#element = driver.find_element(By.CLASS_NAME, "pcm-gl-nav-01__button-inner")
	#href = element.get_attribute('href')
	#element.click()
	#time.sleep(0.1)

	#//pcm-gl-nav-02__button
	#element = driver.find_element(By.CLASS_NAME, "pcm-gl-nav-02__button")

	#elements = driver.find_elements(By.CLASS_NAME, "pcm-gl-nav-02__button")

	#href = elements[1].get_attribute('href')

	#elements[1].click()
	#time.sleep(0.1)
	href=startListUrl
	buyurl=   f"https://member.rakuten-sec.co.jp/app/ord_jp_stk_new.do;BV_SessionID={session}?eventType=init&dscrCd=5136&marketCd=1&tradeType=3&ordInit=1"
	returnUrl=f"https://member.rakuten-sec.co.jp/app/ord_jp_mgn_position.do;BV_SessionID{session}?eventType=init&type=order&sub_type=jp"
	checkurl=f"https://member.rakuten-sec.co.jp/app/ass_mgn_individual_lst.do;BV_SessionID={session}?eventType=init"
	
	def CheckList():
		driver.get(checkurl)
		time.sleep(0.1)
		#general_table
		general_table = driver.find_element(By.CLASS_NAME, "pcmm-ass-mgn-table")
		tds=general_table.find_elements(By.CLASS_NAME, "pcmm--is-mr-4")
		global codeList
		global nameList
		global qtyList
		global originPriceList
		global profitList
		codeList=[]
		qtyList=[]
		nameList=[]
		originPriceList=[]
		profitList=[]

		for k in range(len(tds)):
			#print(f" {k} Code {tds[k].get_attribute('innerHTML').replace('&nbsp','')}    ")
			codeList.append(tds[k].get_attribute('innerHTML').replace('&nbsp;',''))
		#pcmm--is-aln-right
		cells=general_table.find_elements(By.CLASS_NAME, "pcmm--is-aln-right")
		for k in range(len(cells)):
			val=cells[k].get_attribute("innerHTML").strip().replace("	","").replace("<nobr>","").replace("</nobr>","").strip()
			if k%10==0:
				qtyList.append(val)
			if k%10==2:
				originPriceList.append(val)
			if k%10==8:
				profitList.append(val)		
		cells=general_table.find_elements(By.CLASS_NAME, "pcmm-typo--regular-lv3")

		for k in range(len(cells)):
			if k%6==0:
				#print(f" {k} : {cells[k].get_attribute('innerHTML')}    ")
				nameList.append(cells[k].get_attribute('innerHTML'))
	CheckList()			
	for k in range(len(codeList)):	
		print(f" {nameList[k]} {codeList[k]}  {qtyList[k]}  {profitList[k]}")	



	#driver.get(checkurl)
	time.sleep(0.1)
	test = GetPrices()
#	listbox = set(test[0])
	listbox['values'] = test[0]
	AllPrices=[]
	AllChecks=[]
	names=test[0]
	for x in range(len(test[2])):
		temp=[test[2][x]]
		AllPrices.append(temp)
		AllChecks.append([''])
	i=0
	#print(test[1])
	while i<30000:		  
	  #driver.refresh()
	  #time.sleep(0.1)


	  test = GetPrices()
	  if Label3_str.get()=="buy" or Label3_str.get()=="sell":
	  	x=listbox.current()
	  	MuaBan(test[1][x])
	  if Label3_str.get()=="buxy" or Label3_str.get()=="selxl":
	  	print(f"Mua {user_name.get()} ")
	  	
	  	x=listbox.current()
	  	print(test[3][x])
	  	test[3][x].click()
	  	print(driver.title)

	  	MuaRefs = driver.find_elements(By.CLASS_NAME, "pcmm_jpstk--is-mb-8")
	  	print(f"found {len(MuaRefs)}  mua buttons  ")
	  	if len(MuaRefs)>0:
	  		#e1 = MuaRefs[0].find_element(By.CLASS_NAME, "pcmm_jpstk-btlk-buy pcmm_jpstk-btlk-filled pcmm_jpstk-btlk--xs pcmm_jpstk-btlk--block")
	  		print(f"Mua {MuaRefs[0].get_attribute('innerHTML')}===href= {MuaRefs[0].get_attribute('href')}")
	  		btn1=MuaRefs[2].find_elements(By.XPATH, "*")
	  		driver.get(btn1[0].get_attribute('href'))
	  		print(driver.title)
	  		#muaRadios = driver.find_elements(By.ID, "buy")
	  		#muaRadios[0].click()

	  		banRadios = driver.find_elements(By.ID, Label3_str.get())
	  		banRadios[0].click()


	  		time.sleep(0.1)
	  		kikans=driver.find_elements(By.ID, "mgnMaturityCd_system_6m")
	  		kikans[0].click()
	  		qtys=driver.find_elements(By.NAME, "orderValue")
	  		qtys[0].send_keys(qtyStr.get())

	  		prices=driver.find_elements(By.NAME, "marketOrderPrice")
	  		#prices[0].send_keys("1000")

	  		#id=priceMarket name =marketOrderKbn id= marketOrderKbn
	  		#<input type="radio" name="marketOrderKbn" value="1" onclick="calcValueAmuont();" id="priceMarket">
	  		prices=driver.find_elements(By.ID, "priceMarket")
	  		prices[0].click()

				#<div id="yori_table_update_ask_1">
					#<div id="yori_table_update_bid_1">

	  		password=driver.find_elements(By.NAME, "password")
	  		password[0].send_keys("2701")


	  		#find price
	  		priceID="yori_table_update_ask_1"
	  		if Label3_str.get()=="sell":
	  			priceID="yori_table_update_bid_1"
	  		buyPrice=driver.find_elements(By.ID, priceID)
	  		buychild=buyPrice[0].find_elements(By.TAG_NAME, "a")
	  		buychild[0].click()


	  		#password  accountCd
	  		normals=driver.find_elements(By.ID, "general")
	  		normals[0].click()
	  		#ormit_checkbox

	  		normals=driver.find_elements(By.ID, "ormit_checkbox")
	  		normals[0].click()
	  		
	  		submit=driver.find_elements(By.ID, "ormit_sbm")
	  		submit[0].click()
	  		time.sleep(0.1)
	  		print(f"url buy { driver.current_url}")
	  		#id=ormit_sbm
	  		#orderValue	

	  		#mgnMaturityCd_system_6m

	  	#for k in range(len(MuaRefs)):
	  	#	print(f" {k} html {MuaRefs[k].get_attribute('innerHTML')}    ")
	  	#driver.back()
	  	time.sleep(1)
	  	Label3_str.set("OK")
	  	print(driver.title)
	  	#driver.get(href)
	  	#driver.back()
	  AllPrices=AddNewPrice(AllPrices,test)
	  i=i+1
	  dt_now = datetime.datetime.now()
	  now=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
	  print(f"======{now}======")
	#print(AllPrices)
	#print(AllChecks)
	print(f"========")

def select_combo(event):
	global listbox
	global user_name
	global Label1_str
	global Label2_str
	global Label3_str
	global AllChecks
	if len(test)>0:
		x=listbox.current()
		user_name.set(test[1][listbox.current()])
		Label1_str.set(test[2][listbox.current()])
		
	if len(AllChecks) > 0:
		Label2_str.set(''.join(AllChecks[listbox.current()][-20:-1]))
	if len(AllPrices)>0:
		Label1_str.set(f"{test[2][x]} ({max(AllPrices[x])}-{min(AllPrices[x])})")
def MuaBan(buycode):
	global Label3_str
	global webdriver
	global test
	global session
	buyurl=   f"https://member.rakuten-sec.co.jp/app/ord_jp_stk_new.do;BV_SessionID={session}?eventType=init&dscrCd={buycode}&marketCd=1&tradeType=3&ordInit=1"
	driver.get(buyurl)
	time.sleep(0.1)
	banRadios = driver.find_elements(By.ID, Label3_str.get())
	banRadios[0].click()
	time.sleep(0.1)
	kikans=driver.find_elements(By.ID, "mgnMaturityCd_system_6m")
	kikans[0].click()
	qtys=driver.find_elements(By.NAME, "orderValue")
	qtys[0].send_keys(qtyStr.get())
	prices=driver.find_elements(By.NAME, "marketOrderPrice")
		#prices[0].send_keys("1000")
	
			#id=priceMarket name =marketOrderKbn id= marketOrderKbn
			#<input type="radio" name="marketOrderKbn" value="1" onclick="calcValueAmuont();" id="priceMarket">
		#prices=driver.find_elements(By.ID, "priceMarket")
		#prices[0].click()
	
				#<div id="yori_table_update_ask_1">
					#<div id="yori_table_update_bid_1">
	
	password=driver.find_elements(By.NAME, "password")
	password[0].send_keys("2701")
			#find price
	priceID="yori_table_update_ask_1"
	if Label3_str.get()=="sell":
		priceID="yori_table_update_bid_1"
	buyPrice=driver.find_elements(By.ID, priceID)
	buychild=buyPrice[0].find_elements(By.TAG_NAME, "a")
	buychild[0].click()
	
		#password  accountCd
	normals=driver.find_elements(By.ID, "general")
	normals[0].click()
		#ormit_checkbox
	normals=driver.find_elements(By.ID, "ormit_checkbox")
	normals[0].click()
		
	submit=driver.find_elements(By.ID, "ormit_sbm")
	submit[0].click()
	time.sleep(0.1)
	print(f"url buy { driver.current_url}")
  		#id=ormit_sbm


def startForm():
	global root
	global listbox
	global qtyStr
	root = tk.Tk()
	root.title("Greeter")
	global user_name 
	user_name= tk.StringVar()
	qtyStr=tk.StringVar()
	qtyStr.set("100")
	global Label1_str 
	Label1_str= tk.StringVar()
	global Label2_str 
	global Label3_str 
	Label2_str= tk.StringVar()
	Label3_str= tk.StringVar()

	Label1_str.set("label1")
	Label2_str.set("label2")
	Label3_str.set("label3")

	main = ttk.Frame(root, padding=(20, 10, 20, 0))
	main.grid()

	root.columnconfigure(0, weight=1)
	root.rowconfigure(1, weight=1)
	
	name_entry = ttk.Entry(main, width=15, textvariable=user_name)
	name_entry.grid(row=0, column=1)
	name_entry.focus()

	listbox = ttk.Combobox(main)
	listbox.grid(row=0, column=0, padx=(0, 10))
	listbox.bind('<<ComboboxSelected>>', select_combo)	
	Label1 = ttk.Label(main, textvariable=Label1_str)
	Label1.grid(row=1, column=0, columnspan=1, sticky="W", pady=(10, 0))




	Label2 = ttk.Label(main, textvariable=Label2_str)
	Label2.grid(row=1, column=1, columnspan=1, sticky="W", pady=(10, 0))

	Label3 = ttk.Label(main, textvariable=Label3_str)
	Label3.grid(row=2, column=0, columnspan=1, sticky="W", pady=(10, 0))
	qty_entry = ttk.Entry(main, width=10, textvariable=qtyStr)
	qty_entry.grid(row=2, column=1)

	buttons = ttk.Frame(main, padding=(0, 10))
	buttons.grid(row=3, column=0, columnspan=2, sticky="EW")

	# buttons.columnconfigure(0, weight=1)
	# buttons.columnconfigure(1, weight=1)

	buttons.columnconfigure((0, 1), weight=1)
	start_button = ttk.Button(buttons, text="Mua", command=Mua)
	start_button.grid(row=0, column=0, sticky="EW")

	ban_button = ttk.Button(buttons, text="Ban", command=Ban)
	ban_button.grid(row=0, column=1, sticky="EW")

	quit_button = ttk.Button(buttons, text="Quit", command=root.destroy)
	quit_button.grid(row=0, column=2, sticky="EW")

	root.bind("<Return>", greet)
	root.bind("KP_Enter", greet)
	thread1 = threading.Thread(target=start)
	thread1.start()

	root.mainloop()

def Mua():
	global Label3_str
	Label3_str.set("buy")
def Ban():
	global Label3_str
	Label3_str.set("sell")	

def greet(*args):
    #greeting_message.set(f"Hello, {name or 'World'}!")
    thread1 = threading.Thread(target=start)
    thread1.start()

AllPrices=[]
AllChecks=[]
hrefElements=[]
test=[]
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options	)
startForm()	
