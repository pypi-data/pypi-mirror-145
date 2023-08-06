import time

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import exceptions
from logmgmt import logger

bing_url = 'https://bing.com'


def test_search(driver: WebDriver) -> bool:
    driver.get(bing_url)
    try:
        search_field = driver.find_element(By.ID, 'sb_form_q')
        search_field.send_keys("test")
        search_field.submit()
        time.sleep(2)
        return len(driver.find_elements(By.CSS_SELECTOR, 'li.b_algo > h2 > a')) > 0
    except NoSuchElementException:
        return False


def get_bing_login_pages(driver: WebDriver, base_page, count_of_results=1, login_search_term="login", max_tries=3,
                         include_just_sub_domains=True) -> list:
    logger.info("Starting Bing search")
    search_term = base_page + " " + login_search_term
    if include_just_sub_domains:
        search_term += " site:" + base_page
    logger.info("Searching Bing with term \"" + search_term + "\"")
    counter = 1
    while counter <= max_tries:
        counter += 1
        try:
            driver.get(bing_url)
            search_field = driver.find_element(By.ID, 'sb_form_q')
            search_field.send_keys(search_term)
            search_field.submit()
            time.sleep(2)
            logger.info("Taking first " + str(count_of_results) + " result(s)")
            links = []
            while len(links) < count_of_results:
                selected = driver.find_elements(By.CSS_SELECTOR, 'li.b_algo > h2 > a')
                if len(selected) == 0:
                    if len(links) == 0:
                        logger.info("We could not find first link of Bing search results! "
                                    "Checking if test search is working!")
                        if not test_search(driver):
                            raise exceptions.BingHasChangedException()
                        logger.info("Looks like no links are found by Bing for the original request.")
                        if counter <= max_tries:
                            logger.info("Retrying getting results")
                            raise exceptions.RetryException()
                        logger.info("Returning empty list")
                        return links
                    return links
                link_counter = 0
                while len(links) < count_of_results and link_counter < len(selected):
                    link = selected[link_counter].get_attribute('href')
                    logger.info("Got " + link)
                    links.append(link)
                    link_counter += 1

                if len(links) < count_of_results:
                    time.sleep(5)
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.sb_bp')
                    if next_buttons:
                        driver.execute_script("arguments[0].click();", next_buttons[-1])
                        time.sleep(2)
                    else:
                        break
                else:
                    break
            return links
        except NoSuchElementException:
            raise exceptions.BingHasChangedException()
        except WebDriverException as e:
            logger.error(e)
            logger.error("We got an unknown Webdriverexception. Please manage this!")
        except exceptions.BingHasChangedException as e:
            raise e
        except exceptions.RetryException:
            logger.info("Retrying (attempt: " + str(counter) + ")")
            continue
        except Exception as e:
            logger.error(e)
            logger.error("We got an unknown Exception. Please manage this!")

        if counter <= max_tries:
            logger.info("Retrying (attempt: " + str(counter) + ")")
            continue
    raise exceptions.BingHasChangedException()

# if __name__ == "__main__":
#    driver = DriverManager.generate_driver()
#    print(get_bing_login_pages(driver, "google.com", count_of_results=3))
#    driver.quit()
