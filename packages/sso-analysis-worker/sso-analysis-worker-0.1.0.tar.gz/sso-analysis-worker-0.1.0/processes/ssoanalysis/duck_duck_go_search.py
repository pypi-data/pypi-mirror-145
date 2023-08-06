from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

duckduckgo_url = "https://duckduckgo.com/?q="


class DuckDuckGoChangedSiteException(Exception):
    pass


def get_duckduckgo_login_page(driver, base_page, login_search_term="login", max_tries=3):
    url = duckduckgo_url + base_page + "+" + login_search_term
    print("Searching in duckduckgo")
    counter = 1
    while counter <= max_tries:
        counter += 1
        try:
            print("Opening DuckDuckGo")
            driver.get(url)
            print("Taking first result")
            el = driver.find_element(By.XPATH, '//*[@id="r1-0"]/div/h2/a[1]')
            if el is None:
                print("We could not find first link of DuckDuckGos search results! Please check if the site changed!")
                raise DuckDuckGoChangedSiteException()
            login_page = el.get_attribute("href")
            print("Got " + login_page)
            return login_page
        except WebDriverException as e:
            print(e)
            print("We got an unknown Webdriverexception. Please manage this!")
        except Exception as e:
            print(e)
            print("We got an unknown Exception. Please manage this!")

        if counter <= max_tries:
            print("Retrying (attempt: " + str(counter) + ")")
            continue
    return False
