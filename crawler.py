from selenium import webdriver

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

        trails = []
        for row in driver.find_elements_by_xpath("//div[@id='Data_gol']/*[@id='list_g']/ul/li"):
            try:
                row_id = row.find_element_by_xpath(".//div[@class='fr_nomer']").get_attribute("innerHTML")
                row_id = int(row_id.replace(".", ""))
                date = row.find_element_by_xpath(".//div[@class='fr_data']").text  # 'fr_data'
                descr = row.find_element_by_xpath(".//div[@class='fr_nazva']").text
                descr = descr.split("\n")[0]
                votes = row.find_element_by_xpath(".//div[@class='fr_nazva']//center").text
                rishennya = votes.split("-")[-1].split(" ", 1)[1]
                trails.append((row_id, date, descr, rishennya))
            except:
                print("Error\n Row: \n {0}".format(row.text))

        trails_table = []
        for elem in trails:
            if "Поіменне голосування про проект Закону" in elem[2]:
                trails_table.append(elem)


# [num for num, law in zip(nums, laws) if "x" in law]
# ".//*[@id='list_g']"
deps = driver.find_elements_by_xpath("//table[@class='tab_gol']/tbody/tr/td[2]") # deputies
dep_list = [elem.get_attribute("innerHTML") for elem in deps]
votes = driver.find_elements_by_xpath("//table[@class='tab_gol']/tbody//td[3]")
colored_votes = []
for vote in votes:
    #get element by color
    color = vote.get_attribute("style").replace("color: ", "").replace(";", "")
    if not color:  # this means '-' is  in the cell
        if vote.text == '•':
            color = 'didnotvote'
        else:
            color = 'absent'
    
    colored_votes.append(color)
    # if votes[elem].find_elements_by_xpath("//tr[elem]/td[@style='color:Yellow;']"):
    #     votes[elem] = "utrymavsya"
    # elif votes[elem].find_elements_by_xpath("//tr[elem]/td[@style='color:green;']"):
    #     votes[elem] = "za"
    # elif votes[elem].find_elements_by_xpath("//tr[elem]/td[@style='color:red;']"):
    #     votes[elem] = "proty"
    # else:
    #     votes[elem] = "vidsutniiy"
dep_list = [elem.get_attribute("innerHTML") for elem in deps]

for i in range(len(trails_table)):
    count = trails_table[i][0]

if votes[2].find_elements_by_xpath("//tr[2]/td[@style='color:Yellow;']"):
    elem = "utrymavsya"