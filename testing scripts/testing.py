import time
from selenium import webdriver
from threading import Thread
from selenium.webdriver.chrome.options import Options

def login(driver, EMAIL, PASSWORD, ROLE):
    driver.get('https://pitcher-275100.wl.r.appspot.com/users/login/')
    email = driver.find_elements_by_name('email')[0]
    email.send_keys(EMAIL)
    password = driver.find_elements_by_name('password')[0]
    password.send_keys(PASSWORD)
    role = driver.find_elements_by_name('role')
    for _ in role:
        if(_.get_attribute("value")==ROLE):
            _.click()
    submit = driver.find_elements_by_name('loginform')[0].find_elements_by_tag_name("input")[-1]
    submit.click()
def logout(driver, ROLE):
    driver.get('https://pitcher-275100.wl.r.appspot.com/{}/logout/'.format(ROLE))

def work(e, p, r):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options = chrome_options)
    driver.maximize_window()
    login(driver, e, p, r)
    time.sleep(5)
    driver.refresh()
    logout(driver, r)
    time.sleep(5)
    driver.refresh()
    time.sleep(2)
    driver.close()

PASSWORD = "Password@1234"
param = [
    ['mn@gmail.com', PASSWORD, 'pitcher'],
    ['in@gmail.com', PASSWORD, 'investor'],
    ['co@gmail.com', PASSWORD, 'contributor'],
    ['mn@gmail.com', PASSWORD, 'pitcher'],
    ['in@gmail.com', PASSWORD, 'investor'],
    ['co@gmail.com', PASSWORD, 'contributor'],
    ['mn@gmail.com', PASSWORD, 'pitcher'],
    ['in@gmail.com', PASSWORD, 'investor'],
    ['co@gmail.com', PASSWORD, 'contributor'],
    ['mn@gmail.com', PASSWORD, 'pitcher'],
    ['in@gmail.com', PASSWORD, 'investor'],
    ['co@gmail.com', PASSWORD, 'contributor'],
]
browers, i = [], 0

for e,p,r in param:
    t = Thread(target=work, args=(e, p, r,), name=i)
    i += 1
    t.start()
    browers.append(t)
    
for b in browers:
    b.join()