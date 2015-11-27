from selenium import webdriver
import json
import time


def get_days(driver):
    driver.get("http://w1.c1.rada.gov.ua/pls/radan_gs09/ns_h1")
    print("Getting days")
    time.sleep(4)
    voting_days = driver.find_elements_by_xpath('//li[@style="background-color:#FFFFAE;"]/a[@href]')
    voting_days = [elem.get_attribute("href") for elem in voting_days]
    return voting_days


def get_laws_from_page(driver, day_link):
    print("   loading law page, getting nums and links")
    driver.get(day_link)
    time.sleep(1)
    laws = driver.find_elements_by_xpath('//div[@class="nomer"]/a')
    law_numbers = [elem.get_attribute("text") for elem in laws if elem.get_attribute("text") != '\xa0']
    law_links = [elem.get_attribute("href") for elem in laws if elem.get_attribute("text") != '\xa0']
    return zip(law_numbers, law_links)


def get_needed_columns(driver):
    print("   getting needed columns")
    trails = []
    for row in driver.find_elements_by_xpath("//div[@id='Data_gol']/*[@id='list_g']/ul/li"):
        time.sleep(1)
        print("   looping through trail rows info")
        try:
            row_id = row.find_element_by_xpath(".//div[@class='fr_nomer']").get_attribute("innerHTML")
            row_id = row_id.replace(".", "")
            date = row.find_element_by_xpath(".//div[@class='fr_data']").text  # 'fr_data'
            descr = row.find_element_by_xpath(".//div[@class='fr_nazva']").text
            descr = descr.split("\n")[0]
            votes = row.find_element_by_xpath(".//div[@class='fr_nazva']//center").text
            rishennya = votes.split("-")[-1].split(" ", 1)[1]
            trails.append((row_id, date, descr, rishennya))
        except:
            print("   Error\n Row: \n {0}".format(row.text))

    trails_table = []
    for elem in trails:
        if "Поіменне голосування про проект" in elem[2]:
            trails_table.append(elem)
    needed_columns = [item[0] for item in trails_table]
    print("\tneeded columns:", needed_columns)
    return needed_columns


def get_dep_list(driver):
    print("   getting deps list")
    deps = driver.find_elements_by_xpath("//table[@class='tab_gol']/tbody/tr/td[2]") # deputies
    dep_list = [elem.get_attribute("innerHTML") for elem in deps]
    return dep_list


def get_all_column_numbers(driver):
    print("   getting ALL column numbers")
    headings = driver.find_elements_by_xpath("//*[@id='list_g']/ul/table[1]/tbody/tr[1]")[0].text
    if headings:
        columns = headings.split(" ", 2)[2].split(" ")
        print("   All columns:", columns)
    return columns


def get_golosuv_info(driver, needed_columns, columns, dep_list):
    print("   --> getting voting data")
    golosuvannya = dict()
    golosuvannya['deputies'] = dep_list
    intesection_needed = set(columns) & set(needed_columns)
    if not bool(intesection_needed):
        print(" ! got no real votings")
    for count in intesection_needed:
        i = int(count) + 2
        votes = driver.find_elements_by_xpath("//table[@class='tab_gol']/tbody//td[%i]"%(i))
        colored_votes = []
        for vote in votes:
            # get element by color
            # 1 = za
            # 2 = proty
            # 3 = utrymavsya
            # 4 = ne golosuvav
            # 5 = vidsutiij
            color = vote.get_attribute("style").replace("color: ", "").replace(";", "").replace("Yellow", "3").replace("green", "1").replace("red", "2")
            if not color:
                if vote.text == '•':
                    color = "4"
                else:
                    color = "5"
            colored_votes.append(color)
        golosuvannya[count] = colored_votes
    return golosuvannya


if __name__ == "__main__":
    driver = webdriver.Firefox()
    voting_days = get_days(driver)
    # import ipdb; ipdb.set_trace()

    for day_link in voting_days:
        laws = get_laws_from_page(driver, day_link)
        for law_num, law_link in laws:
            print("Getting law number {0} page".format(law_num))
            url = law_link + "#ui-tabs-2"
            driver.get(url)
            time.sleep(2)
            try:
                # click 'details'
                driver.find_element_by_xpath(".//div[@class='vid_d']/p[@id='name_input']").click()
                time.sleep(1)

                needed_columns = get_needed_columns(driver)
                dep_list = get_dep_list(driver)
                columns = get_all_column_numbers(driver)
                golosuvannya = get_golosuv_info(driver, needed_columns, columns, dep_list)

                with open('data/law_{0}.json'.format(law_num), 'w') as out:
                    out.write(json.dumps(golosuvannya, indent=2))

            except ElementNotVisibleException as e:
                print("   No 'details' button!", e)

            except Exception as err:
                print(" ! Smth failed in law {0}, error: {1}".format(law_num, err))
