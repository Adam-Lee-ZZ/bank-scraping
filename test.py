from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import csv
import sys

def get_building(location):

    if not re.match(pattern=r'^["Hong Kong","Islands","Kowloon","New Territories"]-*-*',
                                string=location):
        print('Please enter the location in "Region-District-Else" form.')
        sys.exit()
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
    url = 'https://www.hkbea-cyberbanking.com/ibk/loan/property/valuation/pub/input'
    driver.get(url)

    location = location.split("-")
    
    order = {0:"area",1:"district",2:"building"}

    for i in range(3):

        p = driver.find_element(By.NAME, f'formBean.{order[i]}').text
        p_list = p.split('\n      \n       \n       \n         ')
        if location[i] in p_list:
            driver.find_element(By.NAME, f'formBean.{order[i]}').send_keys(location[i])
        else:
            print(f'Not leagle {order[i]}.')
            sys.exit()
    
    return driver, location


def getvalue(driver: webdriver,loc):

    data = []

    floor = driver.find_element(By.NAME, 'formBean.floor').text
    floor_list = floor.split('\n      \n       \n       \n         ')
    time.sleep(0.5)
    flat_list = ['A','B','C']

    for i in range(len(floor_list)):
        for j in range(len(flat_list)):
            if floor_list[i]!='     Please Select\n     ':    
                driver_p = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
                driver_p.get('https://www.hkbea-cyberbanking.com/ibk/loan/property/valuation/pub/input')
                driver_p.find_element(By.NAME, f'formBean.area').send_keys(loc[0])
                driver_p.find_element(By.NAME, f'formBean.district').send_keys(loc[1])
                driver_p.find_element(By.NAME, f'formBean.building').send_keys(loc[2])
                driver_p.find_element(By.NAME, f'formBean.floor').send_keys(floor_list[i])
                driver_p.find_element(By.NAME, f'formBean.flat').send_keys(flat_list[j])
                time.sleep(1)
                driver.find_element(By.NAME, 'formBean.floor')

                submit_button = driver_p.find_element(By.CLASS_NAME, 'btn01Short')
                submit_button.click()

                submit_button = driver_p.find_element(By.CLASS_NAME, 'btn01Short')
                submit_button.click()
                page_source = driver_p.page_source
                pattern = r'HK\$\s*([\d,]+\.\d{2})'

                # 搜索匹配的内容
                match = re.search(pattern, page_source)

                if match:
                    price = match.group(1)
                    data.append({'location':f'九龙深水埗-順怡閣,{i}樓{j}戶','price':price})
                else:
                    continue

                driver_p.quit()
    return data
            

driver,loc = get_building(sys.argv[1])
data = getvalue(driver,loc)
with open('output.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['location', 'price'])
        writer.writeheader()
        writer.writerows(data)
