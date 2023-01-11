import os.path
import time
import urllib.request as req

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == "__main__":
    opt = Options()
    # opt.add_argument("--no-sandbox")
    # opt.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)

    wait = WebDriverWait(driver, 20)
    header = ['Title', 'Type', 'Date', 'Language', 'Lok Sabha Number', 'Session Number', 'Appears in Collection', 'Filename', 'FileSize']
    driver.get("https://eparlib.nic.in/handle/123456789/796090/browse?page-token=207d0e1f9bbc&page-token-value=36cf3ef399f0aadcbd18c480ec1d23e1&type=loksabhanumber&submit_browse=Lok+Sabha+Number")

    for i in range(1, 17):
        data = []
        total = f'/html/body/main/div/div[3]/div[3]/div[2]/ul/li[{i}]/span'
        file_num = int(driver.find_element(by=By.XPATH, value=total).get_attribute('innerText'))

        num = f"/html/body/main/div/div[3]/div[3]/div[2]/ul/li[{i}]/a"
        wait.until(ec.visibility_of_element_located((By.XPATH, num)))
        driver.find_element(by=By.XPATH, value=num).click()

        ctr = 2
        for j in range(1, file_num + 1):

            view = f'/html/body/main/div/div[3]/div[2]/table/tbody/tr[{ctr}]/td[4]/a'
            wait.until(ec.visibility_of_element_located((By.XPATH, view)))
            driver.find_element(by=By.XPATH, value=view).click()

            title = '/html/body/main/div/div[3]/table/tbody/tr[1]/td[2]'
            _type = '/html/body/main/div/div[3]/table/tbody/tr[2]/td[2]'
            date = '/html/body/main/div/div[3]/table/tbody/tr[3]/td[2]'
            lang = '/html/body/main/div/div[3]/table/tbody/tr[4]/td[2]'
            lok_num = '/html/body/main/div/div[3]/table/tbody/tr[5]/td[2]'
            ses_num = '/html/body/main/div/div[3]/table/tbody/tr[6]/td[2]'
            app_col = '/html/body/main/div/div[3]/table/tbody/tr[7]/td[2]/a'

            filename = '/html/body/main/div/div[3]/div[1]/table/tbody/tr[2]/td[1]/a'
            file_size = '/html/body/main/div/div[3]/div[1]/table/tbody/tr[2]/td[2]'

            file_link = '/html/body/main/div/div[3]/div[1]/table/tbody/tr[2]/td[4]/a'

            wait.until(ec.visibility_of_element_located((By.XPATH, title)))

            row = [driver.find_element(by=By.XPATH, value=title).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=_type).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=date).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=lang).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=lok_num).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=ses_num).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=app_col).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=filename).get_attribute('innerText'),
                   driver.find_element(by=By.XPATH, value=file_size).get_attribute('innerText')]
            print(row)
            data.append(row)
            response = req.urlopen(driver.find_element(by=By.XPATH, value=file_link).get_attribute('href'))
            file = open(f"{driver.find_element(by=By.XPATH, value=filename).get_attribute('innerText')}", "wb")
            file.write(response.read())
            file.close()
            driver.back()
            ctr += 1
            if j % 20 == 0:
                if j == 20:
                    _next = "/html/body/main/div/div[3]/div[2]/div[2]/a"
                else:
                    _next = "/html/body/main/div/div[3]/div[2]/div[2]/a[2]"
                wait.until(ec.visibility_of_element_located((By.XPATH, _next)))
                driver.find_element(by=By.XPATH, value=_next).click()
                ctr = 2
                if os.path.exists(f"Result-{i}.csv"):
                    df = pd.DataFrame(data)
                    df.to_csv(f"Result-{i}.csv", index=False, mode='a+', header=False)

                else:
                    df = pd.DataFrame(data, columns=header)
                    df.to_csv(f"Result-{i}.csv", index=False, mode='a+')
                data = []
        driver.back()

