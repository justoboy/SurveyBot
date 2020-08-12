'''
Created on Feb 10, 2019

@author: justo
'''
import time
from selenium import webdriver

def StartChromeProxy(proxy,chrome_options=webdriver.ChromeOptions()):
    chrome_options.add_argument('--proxy-server='+proxy)
    chrome = webdriver.Chrome(options=chrome_options)
    return chrome

def GetProxies(amount=1):
    proxies = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    chrome = webdriver.Chrome(options=options)
    chrome.get('https://www.us-proxy.org/')
    while chrome.page_source == '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body></body></html>':
        print('Waiting for internet')
        time.sleep(1)
        chrome.refresh()
    while amount > 0:
        if amount > 20:
            data = chrome.find_element_by_id("proxylisttable").find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for row in data:
                columns = row.find_elements_by_tag_name('td')
                proxies.append(columns[0].text+':'+columns[1].text)
            amount -= 20
            chrome.find_element_by_id('proxylisttable_next').find_element_by_tag_name('a').click()
        else:
            data = chrome.find_element_by_id("proxylisttable").find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for i in range(amount):
                columns = data[i].find_elements_by_tag_name('td')
                proxies.append(columns[0].text+':'+columns[1].text)
            amount = 0
    chrome.quit()
    return proxies