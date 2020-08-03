import time

from selenium import webdriver

tel = []
PROXY = '200.35.154.13:1212'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('user-agent=%s' % user_agent)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=options)
fin = []
with open('inter.txt', 'r', encoding='UTF-8')as innie:
    for n, thing in enumerate(innie):
        if thing[:5] != 'https':
            continue
        if n > 2500 and n <= 5000:
            print(thing)
            driver.get(thing)
            try:
                b = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/button')
                b.click()

                c = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div[2]/div/a/span/span')
                tel.append(c.text)
                print(c.text)
            except:
                pass

with open('final.txt', 'a+', encoding='UTF-8')as outed:
    for thing in tel:
        outed.writelines(thing + '\n')