import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from auth import password, email, url
from script import parse

def get_src(url1):
    s = Service(executable_path="chromedriver_mac64/chromedriver", service_args=["--disable-build-check"])
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=s, options=options)
    try:
        driver.get(url1)
        time.sleep(3)
        email_input = driver.find_element(By.XPATH,'//*[@id="username"]')
        email_input.clear()
        email_input.send_keys(email)
        pass_input = driver.find_element(By.XPATH, '//*[@id="password"]')
        pass_input.clear()
        pass_input.send_keys(password)
        button_confirm = driver.find_element(By.XPATH, '//button[@data-litms-control-urn="login-submit" and contains(@class, "btn__primary--large") and contains(@class, "from__button--floating")]')
        button_confirm.click()
        time.sleep(3)
        email_count_list = 0
        contact_count_list = 0
        for i in url_list:
            email_count, contact_count = parse(driver, i)
            email_count_list += email_count
            contact_count_list += contact_count
        # print(f"Всього результатів: {contact_count_list}\n\nЕмейлів знайдено: {email_count_list}")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


print("Enter the number of pages to parse:")
page_count = input()
if int(page_count) == 0:
    print("The value is not suitable")
else:
    print("Enter the page you would like to start your search from:")
    first_page = int(input())
    if first_page == 0 or int(page_count) < int(first_page):
        print("The value is not suitable")
    else:
        url_list = []
        for i in range(int(first_page), int(page_count)+int(first_page)):
            if i == 1:
                url_list.append(url)
            else:
                url_list.append(url+f"&page={i}")
        print(url_list)
        get_src('https://www.linkedin.com/login/uk')
