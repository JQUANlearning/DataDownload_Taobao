from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime


# 登录设置，避开淘宝的登录检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# option.add_argument('--headless')
web = webdriver.Chrome(options=option)
web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
   "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
})


try:
    # 打开生意参谋页面
    web.get('https://sycm.taobao.com/cc/item_rank')
    print(datetime.datetime.now())
    time.sleep(3)
    # 寻找并切进淘宝登录内嵌页面
    iframe = web.find_element(By.TAG_NAME, 'iframe')
    web.switch_to.frame(iframe)
    # 登录淘宝
    web.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys('帅强家具旗舰店:推广01')
    web.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys('shuaiqiang888')
    web.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()
    # 等待页面刷新
    try:
        WebDriverWait(web, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'oui-card-header-wrapper')))
    finally:
        pass
    # 以下两步下载“生意参谋-品类”数据
    # 寻找“日”与“下载”按钮，下载数据
    web.find_element(By.XPATH, '//*[@class="oui-date-picker-particle-button"]/button[4]').click()
    WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="anticon anticon-download oui-canary-icon oui-canary-icon-download"]'))).click()
    # 寻找“<”与“下载”按钮，下载数据（通过修改while循环的条件来确定下载几天数据）
    i = 0
    while i < 6:
        i += 1
        web.find_element(By.XPATH, '//*[@class="oui-date-picker-particle-button"]/button[8]').click()
        time.sleep(1)
        WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="anticon anticon-download oui-canary-icon oui-canary-icon-download"]'))).click()
    # 下载“生意参谋-自助分析”数据

except Exception as e:
    # 抛出报错信息
    print('str Error:')
    print(str(e))
    error_msg = repr(e)
    print('repr Error')
finally:
    time.sleep(10)
    print('---关闭浏览器---')
    web.close()
    web.quit()
    print(datetime.datetime.now())
