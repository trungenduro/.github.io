from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    options=options
)


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



element = driver.find_element(By.CLASS_NAME, "pcm-gl-g-header-text-search")
#検索テキストボックスに"Selenium"を入力
#element.send_keys("4565")
#element.send_keys(Keys.ENTER)
#pcm-gl-nav-02__button
cur_url = driver.current_url
print(cur_url)
#pcm-gl-nav-01__button
#pcm-gl-nav-01__button-inner  pcm-gl-nav-02__button
element = driver.find_element(By.CLASS_NAME, "pcm-gl-nav-01__button-inner")
href = element.get_attribute('href')
print("koku ")
print(href)
element.click()

time.sleep(0.1)
#//pcm-gl-nav-02__button
element = driver.find_element(By.CLASS_NAME, "pcm-gl-nav-02__button")

elements = driver.find_elements(By.CLASS_NAME, "pcm-gl-nav-02__button")

href = element.get_attribute('href')


print("list ")

elements[1].click()
time.sleep(0.1)

elements = driver.find_elements(By.CLASS_NAME, "cell-05")
print(len(elements))
i=0
prices=[]
for i in range(len(elements)):
	e1 = elements[i].find_element(By.CLASS_NAME, "mbody")	
	print(e1.text)
	if i%2==0:
		if "↓" in e1.text or "↑" in e1.text: 				
			prices.append(float( e1.text.replace(",","").split(' ')[0]))
		

print(prices)

elements = driver.find_elements(By.CLASS_NAME, "align-C")
print(len(elements))
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

print(codes)
print(names)
print(prices)
for x in range(len(names)):
	print(f"{x}  {names[x]}  {prices[x]}")
