from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://w1.c1.rada.gov.ua/pls/radan_gs09/ns_h1")
voting_days = driver.find_elements_by_xpath('//li[@style="background-color:#FFFFAE;"]/a[@href]')
voting_days = [elem.get_attribute("href") for elem in voting_days]

for link in voting_days:
    driver.get(link)
    laws = driver.find_elements_by_xpath('//div[@class="nomer"]/a')
    law_numbers = [elem.get_attribute("text") for elem in laws]
    law_links = [elem.get_attribute("href") for elem in law_numbers if elem.get_attribute("text") != '\xa0']

    for link in law_links:
        url4 = url3 + "#ui-tabs-2"
        url4.replace(" ", "")
        driver.get(link)
        voting_list = driver.find_elements_by_xpath('//div[@class="fr_nazva"]/a/text()')
        voting_l = driver.find_elements_by_xpath('//div[@class="fr_nazva"]/a')
