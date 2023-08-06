from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By

startpage_url = "https://startpage.com/"
startpage_search_input_xpath = "/html/body/div[2]/section[1]/div[3]/div[2]/div/form/input[1]"
startpage_search_button_xpath = "/html/body/div[2]/section[1]/div[3]/div[2]/div/form/button[2]"
startpage_first_search_result_xpath = "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/section[3]/div[1]/div[1]/div[2]/a"
startpage_family_filter_check_xpath = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div/form/button/span"
startpage_family_filter_button_xpath = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div/form/button"


class StartPageException(Exception):
    pass


def get_startpage_login_page(driver, base_page, max_tries=3):
    print("Searching over startpage")
    counter = 1
    while counter <= max_tries:
        counter += 1
        try:
            print("Opening startpage and search for page")
            driver.get(startpage_url)
            search_input = driver.find_element(By.XPATH, startpage_search_input_xpath)
            search_input.send_keys(base_page + " login")
            driver.find_element(By.XPATH, startpage_search_button_xpath).click()
            print("Taking first result")
            el = None
            try:
                el = driver.find_element(By.XPATH, startpage_first_search_result_xpath)
            except NoSuchElementException as e:
                print("Could not find any search result element. Checking if family search is the problem")
                fel = driver.find_element(By.XPATH, startpage_family_filter_check_xpath)
                class_attr = fel.get_attribute("class")
                if class_attr is not None and 'active' in class_attr.split():
                    print("Found active family search. Will retry with disabled")
                    driver.find_element(By.XPATH, startpage_family_filter_button_xpath).click()
                    try:
                        el = driver.find_element(By.XPATH, startpage_first_search_result_xpath)
                    except NoSuchElementException:
                        pass
            if el is None:
                print("We could not find first link of DuckDuckGos search results! Please check if the site changed!")
                raise StartPageException()
            login_page = el.get_attribute("href")
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
