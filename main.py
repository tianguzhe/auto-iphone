import json
import time
import urllib

import requests
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

with open('config.yml', 'r') as file:
    prime_service = yaml.safe_load(file)


def loop_func(func, second):
    while True:
        func()
        time.sleep(second)


def pz(driver):
    # 4.4 你是否有智能手机要折抵 【此处我选择了-没有旧机折扣】
    element_old = driver.find_element(By.XPATH, '//*[@id="noTradeIn"]')
    driver.execute_script("arguments[0].click();", element_old)
    driver.implicitly_wait(10)

    # 4.5 Applecare 【此处我选择了-无Applecare】
    element_care = driver.find_element(By.XPATH,
                                       '//*[@id="iphone14plus_ac_iup_noapplecare"]')
    driver.execute_script("arguments[0].click();", element_care)
    driver.implicitly_wait(10)

    time.sleep(0.5)

    # 4.6 添加到购物袋
    element_car = driver.find_element(By.XPATH,
                                      '//span[@class="add-to-cart "]/button')
    element_car.click()
    driver.implicitly_wait(10)


def add(driver):
    # 5 页面跳转查看购物袋
    element_check = driver.find_element(By.XPATH,
                                        '//*[@value="proceed"]')
    driver.execute_script("arguments[0].click();", element_check)
    driver.implicitly_wait(10)

    # 6 结账
    element_check_out = driver.find_element(By.XPATH,
                                            '//*[@id="shoppingCart.actions.navCheckout"]')
    driver.execute_script("arguments[0].click();", element_check_out)
    driver.implicitly_wait(10)

    # 同意授权
    element_check_a = driver.find_element(By.ID, 'signIn.consentOverlay.dataHandleByApple_label')
    driver.execute_script("arguments[0].click();", element_check_a)
    driver.implicitly_wait(10)

    element_check_b = driver.find_element(By.ID, 'signIn.consentOverlay.dataOutSideMyCountry')
    driver.execute_script("arguments[0].click();", element_check_b)
    driver.implicitly_wait(10)

    element_check_c = driver.find_element(By.ID, 'consent-overlay-accept-button')
    driver.execute_script("arguments[0].click();", element_check_c)
    driver.implicitly_wait(10)


def login(driver):
    element_username = driver.find_element(By.ID, 'signIn.customerLogin.appleId')
    element_username.send_keys(prime_service['apple']['id'])
    driver.implicitly_wait(10)

    # 7.2 输入密码
    element_password = driver.find_element(By.ID, 'signIn.customerLogin.password')
    element_password.send_keys(prime_service['apple']['pwd'])
    driver.implicitly_wait(10)

    # 7.3 点击登录
    element_login = driver.find_element(By.ID, 'signin-submit-button')
    element_login.click()
    driver.implicitly_wait(10)


def other(driver):
    # 自提
    element_want_order = driver.find_element(By.ID,
                                             'fulfillmentOptionButtonGroup1')
    driver.execute_script("arguments[0].click();", element_want_order)
    driver.implicitly_wait(10)

    # 8.2 点击显示此地附近的零售店
    element_selectdistrict = driver.find_element(By.XPATH,
                                                 '//*[@data-autom="fulfillment-pickup-store-search-button"]')
    element_selectdistrict.click()
    driver.implicitly_wait(10)

    # 广西壮族自治区
    # 南宁
    # 青秀区

    # 8.3 点击广西壮族自治区
    element_province = driver.find_element(By.XPATH,
                                           f'//button[contains(text(),{prime_service["address"]["province"]})]')
    element_province.click()
    driver.implicitly_wait(10)

    # 8.4 点击南宁
    element_city = driver.find_element(By.XPATH,
                                       f'//button[contains(text(),{prime_service["address"]["city"]})]')
    element_city.click()
    driver.implicitly_wait(10)

    # 8.5 点击青秀区
    element_area = driver.find_element(By.XPATH,
                                       f'//button[contains(text(),{prime_service["address"]["area"]})]')
    element_area.click()
    driver.implicitly_wait(20)

    # 8.6 选择取货零售店 【此处我选择了-Apple 武汉】
    element_pickupTab = driver.find_element(By.XPATH,
                                            '//ul[contains(@class, "rt-storelocator-store-group")]/li[1]/input')
    driver.execute_script("arguments[0].click();", element_pickupTab)
    driver.implicitly_wait(20)

    # # 8.7 选择取货时间 【根据时间自己定】
    # element_pickup_time = driver.find_element(By.XPATH,
    #                                           '//*[@value="11"]')
    # driver.execute_script("arguments[0].click();", element_pickup_time)
    # driver.implicitly_wait(10)

    # 8.8 选择取货时间段 【此处我选择了-默认第一个时间段】
    element_time_quantum = driver.find_element(By.ID,
                                               'checkout.fulfillment.pickupTab.pickup.timeSlot.dateTimeSlots.timeSlotValue')
    Select(element_time_quantum).select_by_index(2)
    driver.implicitly_wait(15)

    # 8.9 继续填写取货详情
    element_checkout = driver.find_element(By.ID,
                                           'rs-checkout-continue-button-bottom')
    driver.implicitly_wait(15)
    element_checkout.click()
    driver.implicitly_wait(10)

    # 9.1 请填写收件人姓氏
    lastName = driver.find_element(By.ID, 'checkout.pickupContact.selfPickupContact.selfContact.address.lastName')
    lastName.send_keys(prime_service['info']['lastname'])
    driver.implicitly_wait(10)

    # 9.2 请填写收件人名字
    firstName = driver.find_element(By.ID,
                                    'checkout.pickupContact.selfPickupContact.selfContact.address.firstName')
    firstName.send_keys(prime_service['info']['firstname'])
    driver.implicitly_wait(10)

    # 9.3 请填写收件人邮箱
    emailAddress = driver.find_element(By.ID,
                                       'checkout.pickupContact.selfPickupContact.selfContact.address.emailAddress')
    emailAddress.send_keys(prime_service['info']['email'])
    driver.implicitly_wait(10)

    # 9.4 请填写收件人手机号
    fullDaytimePhone = driver.find_element(By.ID,
                                           'checkout.pickupContact.selfPickupContact.selfContact.address.fullDaytimePhone')
    fullDaytimePhone.send_keys(prime_service['info']['phone'])
    driver.implicitly_wait(10)

    # 9.5 请填写身份证后4位
    nationalIdSelf = driver.find_element(By.ID,
                                         'checkout.pickupContact.selfPickupContact.nationalIdSelf.nationalIdSelf')
    nationalIdSelf.send_keys(prime_service['info']['card'])
    driver.implicitly_wait(10)

    # 9.6 开发票
    nationalIdSelf = driver.find_element(By.ID,
                                         'checkout.pickupContact.eFapiaoSelector.selectFapiao-e_personal')
    driver.execute_script("arguments[0].click();", nationalIdSelf)
    driver.implicitly_wait(10)

    # 9.7 检查订单
    element_checkoutPay = driver.find_element(By.ID,
                                              'rs-checkout-continue-button-bottom')
    driver.execute_script("arguments[0].click();", element_checkoutPay)
    driver.implicitly_wait(10)

    # checkout.billing.billingoptions.alipay_label
    # checkout.billing.billingoptions.wechat_label

    # 10 立即下单 【此处我选择了-支付宝】
    element_billingOptions = driver.find_element(By.ID,
                                                 'checkout.billing.billingoptions.alipay_label')
    driver.execute_script("arguments[0].click();", element_billingOptions)
    driver.implicitly_wait(10)

    # 11.1 确定
    element_orderPay = driver.find_element(By.ID,
                                           'rs-checkout-continue-button-bottom')
    element_orderPay.click()
    driver.implicitly_wait(15)

    # 12 确认订单
    element_endPay = driver.find_element(By.ID,
                                         'rs-checkout-continue-button-bottom')
    element_endPay.click()
    driver.implicitly_wait(15)


def checkStatus():
    a = f'{prime_service["address"]["province"]} {prime_service["address"]["city"]} {prime_service["address"]["area"]}'

    response = requests.get(
        f"https://www.apple.com.cn/shop/fulfillment-messages?pl=true&mts.0=regular&parts.0={prime_service['iphone']['type']}&location={urllib.parse.quote(a)}")

    store = json.loads(response.text).get('body').get('content').get('pickupMessage').get('stores')[0]

    print(
        f'门店: {store.get("storeName")}, 型号: {store.get("partsAvailability").get(prime_service["iphone"]["type"]).get("messageTypes").get("regular").get("storePickupProductTitle")}, 状态: {store.get("partsAvailability").get(prime_service["iphone"]["type"]).get("pickupSearchQuote")}')

    return [store.get("storeName"),
            store.get("partsAvailability").get(prime_service['iphone']['type']).get("messageTypes").get("regular").get(
                "storePickupProductTitle"),
            store.get("partsAvailability").get(prime_service['iphone']['type']).get("pickupSearchQuote")]


def run():
    c = checkStatus()
    if c[2] != '暂无供应':
        url = f"https://www.apple.com.cn/shop/buy-iphone/{prime_service['iphone']['standard']}/{prime_service['iphone']['type']}"
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)

        pz(driver)
        while url == driver.current_url:
            pz(driver)
        add(driver)
        login(driver)
        other(driver)

        time.sleep(10)


if __name__ == '__main__':
    loop_func(run, 5)
