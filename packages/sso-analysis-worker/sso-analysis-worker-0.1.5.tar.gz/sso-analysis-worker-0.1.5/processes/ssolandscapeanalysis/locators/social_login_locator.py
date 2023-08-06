from time import sleep

from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from exceptions import ManualAnalysisNeededException
from logmgmt import logger
from processes.ssolandscapeanalysis.locators.generic_text_locator import GenericTextLocator
from processes.ssolandscapeanalysis.locators.locator_helper import LocatorHelper
from services.driver_manager import DriverManager


class SocialLoginLocator:
    def __init__(self, social_login_text, exclude_urls_starts_with, valid_login_urls,
                 must_have_texts_in_valid_login_urls, extra_texts):
        self.exclude_urls_starts_with = exclude_urls_starts_with

        self.extra_texts = extra_texts
        self.valid_login_urls = valid_login_urls
        self.must_have_texts_in_valid_login_urls = must_have_texts_in_valid_login_urls
        self.text_locator = GenericTextLocator(social_login_text, extra_texts)
        self.additional_xpath_searches_for_high_valid_found = []

    def add_xpath_for_high_valid_found_elements(self, xpath_text):
        self.additional_xpath_searches_for_high_valid_found.append(xpath_text)

    def reload_elements(self, driver, item, current_elements, high_validity):
        from services.driver_manager import DriverManager
        DriverManager.prepare_webpage_with_steps_to_reproduce(driver, item)
        sleep(5)
        logger.info("Site reloaded, elements must be reloaded!")
        if not high_validity:
            new_elements = self.text_locator.locate_low_validity_elements(driver)
        else:
            new_elements = self.text_locator.locate_high_validity(driver)
        if len(new_elements) != len(current_elements):
            logger.warning("WARNING! Count of elements changed. Can not analyse automatic anymore. Aborting...")
        return new_elements

    def locate_login(self, driver, item) -> tuple:
        if LocatorHelper.current_url_excluded(driver, self.exclude_urls_starts_with):
            return False,
        high_validity_elements = self.text_locator.locate_high_validity(driver)
        if len(high_validity_elements) > 0:
            check = self.check_found_elements(driver, high_validity_elements, item, True)
            if check[0]:
                return check
        for xpath in self.additional_xpath_searches_for_high_valid_found:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el is not None:
                    check = self.check_found_elements(driver, [el], item, True)
                    if check[0]:
                        return check
            except NoSuchElementException:
                pass
        sleep(5)
        low_validity_elements = self.text_locator.locate_low_validity_elements(driver)
        if len(low_validity_elements) > 0:
            return self.check_found_elements(driver, low_validity_elements, item, False)
        return False,

    def check_found_elements(self, driver, elements, item, high_validity) -> tuple:
        base_url_checks = driver.current_url
        logger.info("Possible elements found. Will test them (" + str(len(elements)) + ")")
        counter = 0
        stale_element_reference_execption_thrown = False
        while counter < len(elements):
            logger.info("Checking element #" + str(counter + 1) + " from " + str(len(elements)))
            try:
                element_coordinates = elements[counter].location
                high_validity_element_found = LocatorHelper.click_url_check_location(driver, elements[
                    counter], self.valid_login_urls, self.must_have_texts_in_valid_login_urls)
            except (ElementNotInteractableException, ElementClickInterceptedException):
                logger.warning("Element was still not clickable!")
                counter += 1
                continue
            except StaleElementReferenceException:
                if not stale_element_reference_execption_thrown:
                    logger.info("Site seems to have changed without url changed. Reloading elements and try again...")
                    stale_element_reference_execption_thrown = True
                    elements = self.reload_elements(driver, item, elements, high_validity)
                    continue
                else:
                    logger.error("Reload doesn't worked... Manual analysis needed")
                    raise ManualAnalysisNeededException("Could not handle StaleElementReferenceException")
            except WebDriverException as err:
                logger.error(err.msg)
                raise ManualAnalysisNeededException(err.msg)
            if high_validity_element_found:
                logger.info("Found login redirect from low validity element! Reloading the page...")
                DriverManager.prepare_webpage_with_steps_to_reproduce(driver, item)
                return True, element_coordinates
            if driver.current_url != base_url_checks:
                logger.info("Click changed base page. Must reload site..")
                elements = self.reload_elements(driver, item, elements, high_validity)
            counter += 1
            stale_element_reference_execption_thrown = False
        return False,
