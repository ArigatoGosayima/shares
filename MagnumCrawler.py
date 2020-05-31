from random import randrange

from bs4 import BeautifulSoup
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
        maxim = input('How many pages do you want to scrape: ')
        facebookcrawler(maxim)
    elif site == 2:
        maxim = input('How many pages do you want to scrape: ')
        craigscrawler(maxim)
    elif site == 3:
        maxim = input('How many pages in multiples of 3 do you want to scrape: ')
        offerupcrawler(maxim)
    elif site == 4:
        maxim = input('How many pages in multiples of 40 do you want to scrape: ')
        letgocrawler(maxim)
    else:
        print('Restart the program and enter a value between 1 and 4')

def letgocrawler(maxim):
    pcounter = 0
    counter = 0
    user_agent = 'Mozilla/5.0 (Ubuntu; Desktop) WebKit/<webkitVersion>'
    with open('magnumproxylist.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            pcounter += 1
    with open('magnummain.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            counter += 1
    ai = randrange(0, counter)
    with open('magnummain.txt', 'r', encoding='UTF-8') as proxylist:
        for i, line in enumerate(proxylist):
            if i == ai:
                PROXY = line
            else:
                pass
    print('MAIN PROXY: ' + PROXY)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=%s' %user_agent)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.letgo.com/en-us/c/cars/page/1?distance=100&latitude=30.267153000000015&longitude=-97.7430608")

    timeout = 6
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div[2]/header/div/div[4]/button'))
        WebDriverWait(driver, timeout).until(element_present)
        print("Page loaded")
    except TimeoutException:
        print("Timed out waiting for page to load")

    with open('letgo.csv', 'a', newline='') as fil:
        e = csv.writer(fil, delimiter=',')
        e.writerows([['NO', 'Item URL', 'Seller', 'Price', 'Title', 'Location', 'Make', 'Model', 'Year',
                      'Car Description', 'Condition', 'Posted Date', 'Seller Full Address', 'Seller phone number',
                      'Seller Website', 'Seller Description', 'Opens at', 'Images', 'Scrap Time',
                      'KBB site search ( https://www.kbb.com/car-prices/)  need to search item via Make Model value and get url']])

    sn = 0

    for l in range(int(maxim) + 1):
        try:
            driver.get('https://www.letgo.com/en-us/c/cars/page/' + str(
                l + 1) + '?distance=100&latitude=30.267153000000015&longitude=-97.7430608')
        except:
            continue

        timeout = 6
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div[2]/header/div/div[4]/button'))
            WebDriverWait(driver, timeout).until(element_present)
            print("Page loaded")
        except TimeoutException:
            driver.get('https://www.letgo.com/en-us/c/cars/page/' + str(
                l + 1) + '?distance=100&latitude=30.267153000000015&longitude=-97.7430608')
            try:
                element_present = EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/main/div[2]/header/div/div[4]/button'))
                WebDriverWait(driver, timeout).until(element_present)
                print("Page loaded")
            except TimeoutException:
                driver.get('https://www.letgo.com/en-us/c/cars/page/' + str(
                    l + 1) + '?distance=100&latitude=30.267153000000015&longitude=-97.7430608')
                try:
                    element_present = EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app"]/main/div[2]/header/div/div[4]/button'))
                    WebDriverWait(driver, timeout).until(element_present)
                    print("Page loaded")
                except TimeoutException:
                    driver.get('https://www.letgo.com/en-us/c/cars/page/' + str(
                        l + 1) + '?distance=100&latitude=30.267153000000015&longitude=-97.7430608')
                    try:
                        element_present = EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="app"]/main/div[2]/header/div/div[4]/button'))
                        WebDriverWait(driver, timeout).until(element_present)
                        print("Page loaded")
                    except TimeoutException:
                        print('Page did not load')
                        continue

        pageList = []
        for page in range(40):
            try:
                button = driver.find_element_by_xpath(
                    '/html/body/div/main/div[3]/div/div[2]/div[6]/div/div[1]/div[2]/div/div/div[' + str(
                        page + 1) + ']/div/div/div/div[2]/div[1]/p[1]/a')
                pageList.append(button.get_attribute('href'))
            except:
                continue
        print(len(pageList))
        for k in range(len(pageList)):
            a = randrange(0, pcounter)
            with open('magnumproxylist.txt', 'r', encoding='UTF-8') as proxylist:
                for i, line in enumerate(proxylist):
                    if i == a:
                        PROXY = line
                    else:
                        pass
            print('On a proxy: ' + PROXY)
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server=%s' % PROXY)
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('user-agent=' + user_agent)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver1 = webdriver.Chrome(options=options)
            url = pageList[k]
            try:
                driver1.get(url)
            except:
                c = 0

            timeout = 2

            try:
                element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div[1]/header/div/div[1]/a'))
                WebDriverWait(driver1, timeout).until(element_present)
                print("Page loaded")
            except TimeoutException:
                driver1.get(url)
                try:
                    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div[1]/header/div/div[1]/a'))
                    WebDriverWait(driver1, timeout).until(element_present)
                    print("Page loaded")
                except TimeoutException:
                    driver1.get(url)
                    try:
                        element_present = EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="app"]/main/div[1]/header/div/div[1]/a'))
                        WebDriverWait(driver1, timeout).until(element_present)
                        print("Page loaded")
                    except TimeoutException:
                        print('page did not load')
                        continue

            row = []
            sn = sn + 1
            row.append(sn)
            row.append(url)

            try:
                code_soup = driver1.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[3]/div/section/div[1]/div/div/div/div[1]/div/div[2]/p')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:

                code_soup = driver1.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/span')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("$0")

            try:
                code_soup = driver1.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[2]/h1')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:
                code_soup = driver1.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/img')
                if code_soup:
                    code_soup = code_soup.get_attribute('src')
                    row.append(code_soup)
                    location = code_soup
            except:
                row.append("")

            try:
                code_soup = driver1.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[3]/div[1]/a')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")
            try:
                code_soup = driver1.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[3]/div[2]/a')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")
            try:
                code_soup = driver1.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[3]/div[3]/a')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            try:
                code_soup = driver1.find_element_by_xpath(
                    '//*[@id="app"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[5]/p')
                if code_soup:
                    body1 = code_soup.text
                    row.append(code_soup.text)
            except:
                row.append("")
            row.append("")

            try:
                code_soup = driver1.find_element_by_xpath(
                    '/html/body/div/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[4]/div/div[1]/div[1]/span/span')
                if code_soup:
                    row.append(code_soup.text)
            except:
                row.append("")

            row.append("")#location is empty

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
                    code_soup = driver1.find_element_by_xpath(
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
            driver1.close()


def offerupcrawler(maxim):
    counter = 0
    with open('magnummain.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            counter += 1
    ai = randrange(0, counter)
    with open('magnummain.txt', 'r', encoding='UTF-8') as proxylist:
        for i, line in enumerate(proxylist):
            if i == ai:
                PROXY = line
            else:
                pass
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get("https://offerup.com/explore/sck/tx/austin/cars-trucks/")

    timeout = 6
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body'))
        WebDriverWait(driver, timeout).until(element_present)
        print("Page loaded")
    except TimeoutException:
        time.sleep(6)
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body'))
            WebDriverWait(driver, timeout).until(element_present)
            print("Page loaded")
        except:
            print("Timed out waiting for page to load")
            driver.close()
    time.sleep(6)
    urlarray = []
    if int(maxim) <= 4:
        calc = int(maxim)
    else:
        calc = int(maxim) - int(maxim) % 4
    for i in range(calc):
        for j in range(4):

            try:
                button = driver.find_element_by_xpath(
                    '//*[@id="db-item-list"]/div[' + str(j + 1) + ']/a[' + str(i + 1) + ']')
                urlarray.append(button.get_attribute('href'))
            except:
                time.sleep(5)
                try:
                    button = driver.find_element_by_xpath(
                        '//*[@id="db-item-list"]/div[' + str(j + 1) + ']/a[' + str(
                            i + 1) + ']')
                    urlarray.append(button.get_attribute('href'))
                    print("EX")

                except:
                    time.sleep(5)
                    try:
                        button = driver.find_element_by_xpath(
                            '//*[@id="db-item-list"]/div[' + str(j + 1) + ']/a[' + str(
                                i + 1) + ']')
                        urlarray.append(button.get_attribute('href'))
                        print("EX")

                    except:
                        i = 4000000
                        continue

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
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body'))
            WebDriverWait(driver, timeout).until(element_present)
            print("Page loaded")
        except TimeoutException:
            print("Check your internet speed")
            continue

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


def craigscrawler(maxim):
    counter = 0
    with open('magnummain.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            counter += 1
    ai = randrange(0, counter)
    with open('magnummain.txt', 'r', encoding='UTF-8') as proxylist:
        for i, line in enumerate(proxylist):
            if i == ai:
                PROXY = line
            else:
                pass
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=%s' % user_agent)
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

    for k in range(1, int(maxim) + 1):
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
            driver.find_element_by_xpath('/html/body/section/section/header/div[2]/div/button').click()
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


def facebookcrawler(maxim):
    counter = 0
    with open('magnummain.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            counter += 1
    ai = randrange(0, counter)
    with open('magnummain.txt', 'r', encoding='UTF-8') as proxylist:
        for i, line in enumerate(proxylist):
            if i == ai:
                PROXY = line
            else:
                pass
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.facebook.com/marketplace/108276955864187/vehicles/?exact=false")
    timeout = 7
    #time.sleep(1000)
    try:
        element_present = EC.presence_of_element_located((By.ID, 'js_1'))
        WebDriverWait(driver, timeout).until(element_present)
        print('Page loaded')
    except TimeoutException:
        driver.save_screenshot('b.png')
        print("Timed out waiting for page to load")
        driver.close()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)


    urla = []
    cat = driver.find_element_by_id('js_1')
    cat = cat.get_attribute('innerHTML')
    cat = BeautifulSoup(cat)
    n = 0

    for link in cat.find_all('a'):
        if n == 0:
            n += 1
            continue
        else:
            if n <= int(maxim):
                link = link.get('href')
                if str(link)[0:18] == '/marketplace/item/':
                    urla.append('https://www.facebook.com' + link)
                    n += 1
                else:
                    pass
            else:
                break
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
        driver.save_screenshot('a.png')
        timeout = 2

        try:
            element_present = EC.presence_of_element_located((By.XPATH, 'html/body'))
            WebDriverWait(driver, timeout).until(element_present)
            print("Page loaded")
        except TimeoutException:
            print("Didnt load")
            continue


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
                pass

        row.append(image)

        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            row.append(date)
        except:
            row.append("")

        with open('facebook.csv', 'a', newline='', encoding="utf-8") as fil:
            e = csv.writer(fil, delimiter=',')
            e.writerows([row])

main()
