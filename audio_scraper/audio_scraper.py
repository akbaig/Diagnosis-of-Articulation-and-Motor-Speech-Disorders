from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as SE
from webdriver_manager.firefox import GeckoDriverManager
import urllib.request
import time
import random

options = Options()
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "none"
# fp = webdriver.FirefoxProfile()
# fp.set_preference("browser.download.folderList",2)
# fp.set_preference("browser.download.manager.showWhenStarting",False)
# fp.set_preference("browser.download.dir", os.getcwd())
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options, desired_capabilities=caps)
list = [('User-agent', 'Mozilla/5.0')]
opener = urllib.request.build_opener()
opener.addheaders = list
urllib.request.install_opener(opener)

f = open("words.txt", "r")
for x in f:
    word = x.split()[0]
    driver.get(f"https://dictionary.cambridge.org/search/direct/?datasetsearch=english&q={word}")
    uk_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'uk')))
    #uk_element = driver.find_element_by_class_name("uk")
    #audio_element = uk_element.find_element_by_tag_name("source")
    audio_element = WebDriverWait(uk_element, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'source')))
    link = audio_element.get_attribute("src")
    try:
        urllib.request.urlretrieve(link, word+".mp3")
    except:
        urllib.request.urlretrieve(link, word+".mp3")
    print(f"Downloaded {word}.mp3")
    #time.sleep(random.randint(2, 5))
    driver.execute_script("window.open()")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    

driver.quit()
f.close()
