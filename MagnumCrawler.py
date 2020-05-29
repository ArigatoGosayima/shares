from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import csv
from datetime import datetime
import re
import time


def main():
    print('Enter the number with respect to the site you wish to scrape')
    print('1 - Facebook')
    print('2 - Craigs list')
    print('3 - offer up')
    print('4 - Let go')
    site = input()
    site = int(site)
    if site == 1:
        facebookcrawler()
    elif site == 2:
        craigscrawler()
    elif site == 3:
        offerupcrawler()
    elif site == 4:
        letgocrawler()
    else:
        print('Restart the program and enter a value between 1 and 4')

def letgocrawler():
    PROXY = '190.112.194.246:1212'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.letgo.com/en-us/c/cars/page/1?distance=100&latitude=30.267153000000015&longitude=-97.7430608")

    timeout = 2
    try:
        element_present = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")

    with open('letgo.csv', 'a', newline='') as fil:
        e = csv.writer(fil, delimiter=',')
        e.writerows([['NO', 'Item URL', 'Seller', 'Price', 'Title', 'Location', 'Make', 'Model', 'Year',
                      'Car Description', 'Condition', 'Posted Date', 'Seller Full Address', 'Seller phone number',
                      'Seller Website', 'Seller Description', 'Opens at', 'Images', 'Scrap Time',
                      'KBB site search ( https://www.kbb.com/car-prices/)  need to search item via Make Model value and get url']])

    sn = 0

    for l in range(120):
        try:
            driver.get('https://www.letgo.com/en-us/c/cars/page/' + str(
                l + 1) + '?distance=100&latitude=30.267153000000015&longitude=-97.7430608')
        except:
            continue

        timeout = 3
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        pageList = []
        for page in range(40):
            try:
                button = driver.find_element_by_xpath(
                    '/html/body/div/main/div[3]/div/div[2]/div[6]/div/div[1]/div[2]/div/div/div[' + str(
                        page + 1) + ']/div/div/div/div[2]/div[1]/p[1]/a')
                pageList.append(button.get_attribute('href'))
            except:
                continue

        for k in range(len(pageList)):

            url = pageList[k]
            try:
                driver.get(url)
            except:
                c = 0

            timeout = 2

            try:
                element_present = EC.presence_of_element_located((By.ID, 'main'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            finally:
                print("Page loaded")

            row = []
            sn = sn + 1
            row.append(sn)
            row.append(url)

            try:
                code_soup = driver.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[3]/div/section/div[1]/div/div/div/div[1]/div/div[2]/p')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:

                code_soup = driver.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/span')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("$0")

            try:
                code_soup = driver.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[2]/h1')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:
                code_soup = driver.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/img')
                if code_soup:
                    code_soup = code_soup.get_attribute('src')
                    row.append(code_soup)
                    location = code_soup
            except:
                row.append("")

            try:
                code_soup = driver.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[3]/div[1]/a')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")
            try:
                code_soup = driver.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[3]/div[2]/a')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")
            try:
                code_soup = driver.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[3]/div[3]/a')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:
                code_soup = driver.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[5]/p')
                if code_soup:
                    body1 = code_soup.text
                    row.append(code_soup.text)
            except:
                row.append("")
            row.append("")

            try:
                code_soup = driver.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[1]/div[1]/span/span')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:
                row.append(location)
            except:
                row.append("")

            try:
                regex = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
                if (re.search(regex, body1)):
                    phone = re.findall(regex, body1)
                    separator = ', '
                    data = separator.join(phone)
                    row.append(data)
                else:
                    row.append("")
            except:
                row.append("")

            row.append("")
            row.append("")
            row.append("")
            image = ""

            for q in range(24):
                try:
                    code_soup = driver.find_element_by_xpath(
                        '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[' + str(
                            q + 1) + ']')
                    if code_soup:
                        code_soup = code_soup.get_attribute('src')
                        image = image + code_soup + ", "
                except:
                    break

            row.append(image)
            try:
                now = datetime.now()
                date = now.strftime("%Y-%m-%d %H:%M:%S")
                row.append(date)
            except:
                row.append("")

            row.append("")
            print(k)

            with open('letgo.csv', 'a', newline='', encoding="utf-8") as fil:
                e = csv.writer(fil, delimiter=',')
                e.writerows([row])


def offerupcrawler():
    PROXY = '190.112.194.246:1212'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://offerup.com/explore/sck/tx/austin/cars-trucks/")

    timeout = 2
    try:
        element_present = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")

    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/button').click()
    time.sleep(5)

    urlarray = []

    for i in range(800):
        for j in range(4):

            try:
                button = driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[' + str(j + 1) + ']/a[' + str(i + 1) + ']')
                urlarray.append(button.get_attribute('href'))
            except:
                time.sleep(15)
                try:
                    button = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[' + str(j + 1) + ']/a[' + str(
                            i + 1) + ']')
                    urlarray.append(button.get_attribute('href'))
                    print("EX")

                except:
                    time.sleep(5)
                    try:
                        button = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[' + str(j + 1) + ']/a[' + str(
                                i + 1) + ']')
                        urlarray.append(button.get_attribute('href'))
                        print("EX")

                    except:
                        i = 4000000
                        break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    print("Complete")
    print(len(urlarray))

    with open('offerup.csv', 'a', newline='') as fil:
        e = csv.writer(fil, delimiter=',')
        e.writerows([['NO', 'Item URL', 'Seller', 'Price', 'Title', 'Location', 'Make', 'Model', 'Year',
                      'Car Description', 'Condition', 'Posted Date', 'Seller Full Address', 'Seller phone number',
                      'Seller Website', 'Seller Description', 'Opens at', 'Images', 'Scrap Time',
                      'KBB site search ( https://www.kbb.com/car-prices/)  need to search item via Make Model value and get url']])
    linkno = len(urlarray)
    for k in range(linkno):

        url = urlarray[k]
        try:
            driver.get(url)
        except:
            c = 0

        timeout = 2

        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print(".")
        finally:
            print("Page loaded")

        row = []
        row.append(k + 1)
        row.append(url)

        try:
            code_soup = driver.find_element_by_xpath(
                '//*[@id="react-container"]/div/div[5]/div[1]/div[6]/div[1]/a/div[2]/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")

        try:

            code_soup = driver.find_element_by_xpath(
                '//*[@id="react-container"]/div/div[5]/div[1]/div[1]/div/span/span/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("$0")

        try:
            code_soup = driver.find_element_by_xpath('//*[@id="react-container"]/div/div[5]/div[1]/div[1]/h1')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")

        try:
            code_soup = driver.find_element_by_xpath('//*[@id="react-container"]/div/div[5]/div[1]/div[4]/div/a')
            if code_soup:
                row.append(code_soup.text)
                location = code_soup.text
        except:
            row.append("")

        row.append("")
        row.append("")
        row.append("")

        try:
            code_soup = driver.find_element_by_xpath(
                '//*[@id="react-container"]/div/div[5]/div[1]/div[7]/span/span[1]/div')

            if code_soup:
                body1 = code_soup.text
                row.append(code_soup.text)
        except:
            row.append("")

        try:
            code_soup = driver.find_element_by_xpath(
                '//*[@id="react-container"]/div/div[5]/div[1]/div[7]/span/span/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")

        try:
            code_soup = driver.find_element_by_xpath('//*[@id="react-container"]/div/div[5]/div[1]/div[5]')
            if code_soup:
                s = code_soup.text
                s = s.replace(' in Cars & trucks', '')
                row.append(s)
        except:
            row.append("")

        try:
            row.append(location)
        except:
            row.append("")

        try:
            regex = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
            if (re.search(regex, body1)):
                phone = re.findall(regex, body1)
                separator = ', '
                data = separator.join(phone)
                row.append(data)
                print(data)
            else:
                row.append("")
        except:
            row.append("")

        row.append("")
        row.append("")
        row.append("")

        try:
            code_soup = driver.find_element_by_xpath('//*[@id="react-container"]/div/div[4]/div/table/tbody/tr/td/img')
            if code_soup:
                code_soup = code_soup.get_attribute('src')
                image = code_soup
                row.append(image)
        except:
            row.append("")

        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            row.append(date)
        except:
            row.append("")

        print(k)

        with open('offerup.csv', 'a', newline='', encoding="utf-8") as fil:
            e = csv.writer(fil, delimiter=',')
            e.writerows([row])


def craigscrawler():
    PROXY = '190.112.194.246:1212'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://austin.craigslist.org/d/cars-trucks/search/cta")

    timeout = 2

    try:
        element_present = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")

    button = driver.find_element_by_xpath('//*[@id="sortable-results"]/ul/li[1]/p/a')
    url = button.get_attribute('href')

    with open('craigslist.csv', 'a', newline='') as fil:
        e = csv.writer(fil, delimiter=',')
        e.writerows([['NO', 'Item URL', 'Seller', 'Price', 'Title', 'Location', 'Make', 'Model', 'Year',
                      'Car Description', 'Condition', 'Posted Date', 'Seller Full Address', 'Seller phone number',
                      'Seller Website', 'Seller Description', 'Opens at', 'Images']])

    for k in range(1, 10):
        try:
            driver.get(url)
        except:
            c = 0
        timeout = 1

        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print(".")
        finally:
            print("Page loaded")

        try:
            code_soup = driver.find_element_by_xpath('/html/body/section/section/header/div[2]/div/button').click()
            timeout = 1
            try:
                element_present = EC.presence_of_element_located((By.ID, 'main'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print(".")
            finally:
                print("Page loaded")
        except:
            x = 0

        row = []
        row.append(k)
        row.append(url)

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/section/section/header/div[2]/div/div[1]/aside/ul/li[1]/p')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")

        try:

            code_soup = driver.find_element_by_xpath('/html/body/section/section/h2/span/span[2]')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("$0")

        try:
            code_soup = driver.find_element_by_xpath('//*[@id="titletextonly"]')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
        try:
            code_soup = driver.find_element_by_xpath('/html/body/section/section/section/div[1]/div/p/small/a')
            if code_soup:
                code_soup = code_soup.get_attribute('href')
                row.append(code_soup)
                location = code_soup
        except:
            row.append("")

        row.append("")

        try:
            code_soup = driver.find_element_by_xpath('/html/body/section/section/section/div[1]/p[1]/span/b')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
        row.append("")
        try:
            code_soup = driver.find_element_by_xpath('//*[@id="postingbody"]')
            if code_soup:
                body1 = code_soup.text
                row.append(code_soup.text)
        except:
            row.append("")
        try:
            code_soup = driver.find_element_by_xpath('/html/body/section/section/section/div[1]/p[2]/span[1]')
            if code_soup:
                condition = code_soup.text
            if ("VIN:" in condition or "fuel:" in condition):
                code_soup = driver.find_element_by_xpath('/html/body/section/section/section/div[1]/p[2]/span[2]')
                if code_soup:
                    row.append(code_soup.text)
            else:
                row.append(condition)
        except:
            row.append("")
        try:
            code_soup = driver.find_element_by_xpath('//*[@id="display-date"]/time')
            if code_soup:
                code_soup = code_soup.get_attribute('datetime')
                row.append(code_soup)
        except:
            row.append("")
        try:
            row.append(location)
        except:
            row.append("")

        try:
            regex = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
            if (re.search(regex, body1)):
                phone = re.findall(regex, body1)
                separator = ', '
                data = separator.join(phone)
                row.append(data)
                print(data)
            else:
                row.append("")
        except:
            row.append("")

        row.append("")
        row.append("")
        row.append("")
        image = ""

        for q in range(24):
            try:
                code_soup = driver.find_element_by_xpath(
                    '/html/body/section/section/section/figure/div[2]/a[' + str(q + 1) + ']')
                if code_soup:
                    code_soup = code_soup.get_attribute('href')
                    image = image + code_soup + ", "
            except:
                break

        row.append(image)

        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            row.append(date)
        except:
            row.append("")
        print(k)
        with open('craigslist.csv', 'a', newline='', encoding="utf-8") as fil:
            e = csv.writer(fil, delimiter=',')
            e.writerows([row])
        button = driver.find_element_by_xpath('/html/body/section/section/header/div[1]/div/a[3]')
        url = button.get_attribute('href')


def facebookcrawler():
    PROXY = '190.112.194.246:1212'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.facebook.com/marketplace/108276955864187/vehicles/?sort=CREATION_TIME_DESCEND")

    timeout = 4
    try:
        element_present = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")

    urla = []

    for i in range(30):
        try:
            button = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[3]/div/div/div[' + str(
                    i + 1) + ']/div/span/div/a')
            urla.append(button.get_attribute('href'))

        except:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                button = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[3]/div/div/div[' + str(
                        i + 1) + ']/div/span/div/a')
                urla.append(button.get_attribute('href'))
                print("EX")
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
                try:
                    button = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[3]/div/div/div[' + str(
                            i + 1) + ']/div/span/div/a')
                    urla.append(button.get_attribute('href'))
                    print("EX")
                except:
                    c = 0

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    print("Complete")

    print(len(urla))

    with open('facebook.csv', 'a', newline='') as fil:
        e = csv.writer(fil, delimiter=',')
        e.writerows([['NO', 'Item URL', 'Seller', 'Price', 'Title', 'Location', 'Make', 'Model', 'Year',
                      'Car Description', 'Condition', 'Posted Date', 'Seller Full Address', 'Seller phone number',
                      'Seller Website', 'Seller Description', 'Opens at', 'Images']])
    linkno = len(urla)
    print(linkno)
    for k in range(linkno):

        url = urla[k]
        driver.get(url)

        timeout = 2

        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print(".")
        finally:
            print("Page loaded")

        row = []
        row.append(k + 1)
        row.append(url)
        new = 0

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[7]/div[2]/div[2]/div/div/div[2]/div/div/div/div/span/span')
            if code_soup:
                row.append(code_soup.text)

        except:
            row.append("")
            new = new + 1

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/span')
            if code_soup:
                row.append(code_soup.text)

        except:
            row.append("")
            new = new + 1
        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[1]/span')
            if code_soup:
                row.append(code_soup.text)

        except:
            row.append("")
            new = new + 1

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/span/a/span')
            if code_soup:
                row.append(code_soup.text)
                location = code_soup.text
        except:
            row.append("")
            new = new + 1

        row.append("")

        row.append("")

        row.append("")

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[5]/div[2]/div')
            if code_soup:
                body1 = code_soup.text
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        row.append("")

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/span/span/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[3]/div/div/div[2]/div/div/div/div/span/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[4]/div/div/div[2]/div/div/div/div/span/span/a')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[5]/div[2]/div/div/div/span/div/span').click()

            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[5]/div[2]/div/div/div/span')
            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        try:
            code_soup = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[5]/div/div/div[2]/div/div/div/div[1]/span/span')

            if code_soup:
                row.append(code_soup.text)
        except:
            row.append("")
            new = new + 1

        image = ""

        for q in range(24):
            try:
                code_soup = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[' + str(
                        q + 1) + ']/div/div/img')
                if code_soup:
                    code_soup = code_soup.get_attribute('src')
                    image = image + code_soup + ", "
            except:
                xq = 0

        row.append(image)

        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            row.append(date)
        except:
            row.append("")

        print(row)

        with open('facebook.csv', 'a', newline='', encoding="utf-8") as fil:
            e = csv.writer(fil, delimiter=',')
            e.writerows([row])

main()
