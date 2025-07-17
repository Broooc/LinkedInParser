import bs4
import time
import csv

with open("data.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(
        ("LinkedIn", "Name", "Email")
    )

def parse(driver, url2):
    email_count = 0
    contact_count = 0
    driver.get(url2)
    time.sleep(5)
    page = driver.page_source
    soup = bs4.BeautifulSoup(page, 'html.parser')
    list = soup.find_all('a', {"aria-hidden" : "false", "class" : "scale-down"})
    url_list = []
    for i in list:
        url_list.append(i["href"])
    time.sleep(3)
    try:
        for i in url_list:
            email_info = None
            contact_count += 1
            driver.get(i)
            time.sleep(3)
            info_url = driver.current_url + "overlay/contact-info/"
            time.sleep(1)
            driver.get(info_url)
            contacts = driver.page_source
            soup_contacts = bs4.BeautifulSoup(contacts, 'html.parser')
            name = soup_contacts.find('h1', {"id" : "pv-contact-info"})
            if (name != None):
                name = name.get_text().strip()
            print(name)
            email_elem = soup_contacts.find_all('a', href=lambda h: h and h.startswith('mailto:'), class_="link-without-visited-state", attrs={"rel":"noopener noreferrer", "target":"_blank"})
            linkedin = soup_contacts.find('h3', class_="pv-contact-info__header t-16 t-black t-bold").findNext('div').findChild('a')["href"]
            print(linkedin)
            for item in email_elem:
                email_info = item["href"].strip('mailto:')
            if email_info != None:
                email = email_info
            else:
                email = None
            if email_info == None:
                print('Email missing')
            else:
                email_count += 1
                print(f'Email: {email}')
            with open ("data.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [linkedin, name, email]
                )
    except Exception as ex:
        print(ex)
        print("Сталася помилка\n\n")
    print(f"Емейлів знайдено на сторінці: {email_count}\n\nРезультатів на сторінці: {contact_count}\n\n")
    return email_count, contact_count