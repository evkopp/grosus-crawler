from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://w1.c1.rada.gov.ua/pls/radan_gs09/ns_h1")
voting_days = driver.find_elements_by_xpath('//li[@style="background-color:#FFFFAE;"]/a[@href]')
voting_days = [elem.get_attribute("href") for elem in voting_days]

for link in voting_days:
    driver.get(link)
    laws = driver.find_elements_by_xpath('//div[@class="nomer"]/a')
    law_numbers = [elem.get_attribute("text") for elem in laws if elem.get_attribute("text") != '\xa0']
    law_links = [elem.get_attribute("href") for elem in laws if elem.get_attribute("text") != '\xa0']

    for link in law_links:
        url = link + "#ui-tabs-2"
        driver.get(url)
        voting_list = driver.find_elements_by_xpath('//div[@class="fr_nazva"]/a')
        voting_names = [elem.get_attribute("text") for elem in voting_list]
        voting_urls = [elem.get_attribute("href") for elem in voting_list]
        expand = driver.find_elements_by_xpath("//div[@class='vid_d']/p[@id='name_input']")
        expand[0].click()

        trials = driver.find_elements_by_xpath('//div[@class="block_pd"]')
        for elem in trials:
            trail_numbers = [elem.get_attribute("innerHTML") for elem in trials_num]


        trials_num = driver.find_elements_by_xpath('//div[@class="fr_nomer"]')
        trail_numbers = [elem.get_attribute("innerHTML") for elem in trials_num]
        trail_numbers = [elem for elem in trail_numbers if '-' not in elem]
        trail_names = [elem.get_attribute("text") for elem in trials if 'про проект Закону' in elem.get_attribute("text")]


