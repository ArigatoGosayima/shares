import time

from selenium import webdriver

tel = []
PROXY = '200.35.154.13:1212'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('user-agent=%s' % user_agent)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

driver.get('https://www.avito.ma/fr/marrakech/electorm%C3%A9nager_et_vaisselle/climat_9000_41397868.htm')
try:
    b = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/button')
    b.click()

    c = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div[2]/div/a/span/span')
    tel.append(c.text)
    print(c.text)
except:
    pass
