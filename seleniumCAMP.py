from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
options = webdriver.chrome.options.Options()
options.add_argument('headless')
driver = webdriver.Chrome()


driver.get('https://kouan-motosuko.com/reserve/Reserve/input/?type=camp')


time.sleep(0.1)
checkinday="19"
checkoutday = str(int(checkinday) + 1 )
checkindates = driver.find_elements(By.TAG_NAME, "td")
plan_detail_nos=driver.find_elements(By.ID,"plan_detail_no");
plan_detail_no= Select(plan_detail_nos[0])

for checkin in checkindates:
	
	if(checkin.text.split(' ')[0].strip()==checkinday and len(checkin.text) > 10):
		plan_detail_nos=checkin.find_elements(By.ID,"plan_detail_no");
		plan_detail_no= Select(plan_detail_nos[0])
		print(f"  checkin date={checkin.text.split(' ')[0]}     {len(checkin.text)}   splitlen= {len(checkin.text.split(' '))}    =={checkin.text} ")

optOK=""
if len(plan_detail_no.options) >1:
	for k in range(1,len(plan_detail_no.options)):
		opt = plan_detail_no.options[k]
		optval = plan_detail_no.options[k].get_attribute('value')				
		if( "disabled" not in optval):
			print(f"  ok {opt.get_attribute('value')}")
			optOK = optval
			break

if optOK!="":
	plan_detail_no.select_by_value(optOK)


checkout_date=driver.find_element(By.ID,"checkout_date");
checkout_date.send_keys("05/17/2024")
datepicker=driver.find_elements(By.CLASS_NAME,"ui-datepicker-calendar");
nexts=driver.find_elements(By.CLASS_NAME,"ui-datepicker-next.ui-corner-all");


months=driver.find_elements(By.CLASS_NAME,"ui-datepicker-month");
print(f"  months =  {months[0].text}  ")
nexts[0].click()

nexts=driver.find_elements(By.CLASS_NAME,"ui-datepicker-next.ui-corner-all");
nexts[0].click()



datepicker=driver.find_elements(By.CLASS_NAME,"ui-datepicker-calendar");
cells = datepicker[0].find_elements(By.TAG_NAME, "td")
print(f"  datepicker =  {len(datepicker)}  next= {len(nexts)}  cells={len(cells) }")

#checkoutday
for cell in cells:
	print(f"  cell {cell.text}")
	if cell.text.strip() == checkoutday:
		cell.click()

#checkout_date.send_keys(Keys.TAB)
time.sleep(10)


	