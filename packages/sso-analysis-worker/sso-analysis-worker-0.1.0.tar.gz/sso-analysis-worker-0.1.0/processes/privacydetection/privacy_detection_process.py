import threading
import time
from multiprocessing import Process

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from exceptions import ConfigInvalidException
from exceptions import RetryException
from exceptions import SiteNotResolvableException
from model.backend_information import BackendInformation
from model.process_type import ProcessType
from model.privacydetection.privacy_detection_type import PrivacyDetectionType
from processes.process_helper import ProcessHelper
from processes.privacydetection.privacy_detection_provider import PrivacyDetectionProvider
from services.driver_manager import DriverManager
from services.rest_client import RestClient


def process_function(site, backend_info: BackendInformation, counter: int,
                     privacy_detection_type: PrivacyDetectionType, analysis_run_id: int, config_directory):
    success = False
    rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
    chromedriver = None
    cause = "Unknown"
    try:
        print("Received site " + site.base_page + " to analyse.")
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 0, "Starting chromedriver")
        chromedriver = DriverManager.generate_driver(config_directory)
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 15, "Checking config")
        if not ProcessHelper.check_log_in_state(chromedriver):
            raise ConfigInvalidException()
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 30, "Resolving site")
        test_resolve = ProcessHelper.resolve_tld1(chromedriver, site.base_page)
        if test_resolve is None:
            raise SiteNotResolvableException()
        del chromedriver.requests
        print("Performing privacy detection actions for " + site.base_page + " (id:" + str(
            site.index) + "|trancoID:" + str(
            rest_client.get_tranco_id_for_site(site.base_page)) + ") [" + str(counter) + "]")
        print("Opening site")
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 45, "Opening page")
        chromedriver.get(site.base_page)
        if privacy_detection_type == PrivacyDetectionType.CONSENT_GIVEN_INTERACTION:
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 60, "Performing click actions")
            time.sleep(5)
            PrivacyDetectionProcess.find_clickable_element_without_url_change(chromedriver)
            time.sleep(1)
            print("Performing key actions")
            chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(1)
            chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
            time.sleep(1)
            chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 75, "Taking screenshot")
        print("Waiting 5 seconds")
        time.sleep(10)
        print("Taking screenshot")
        screen = chromedriver.get_screenshot_as_png()
        print("Saving HAR and Screenshot for analysis")
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 90, "Uploading results")
        success = rest_client.save_privacy_detection(site.base_page, analysis_run_id, screen, chromedriver.har)
    except TimeoutException as err:
        cause = "Timout: " + err.__class__.__name__
        print("Timeout reached: " + err.msg)
    except SiteNotResolvableException:
        cause = "Not resolvable"
        print("Could not resolve site!")
    except WebDriverException as err:
        cause = "Webdriver problem: " + err.__class__.__name__
        print("Could not finish analysing (" + err.msg + ")!")
    except ConfigInvalidException:
        cause = "Invalid config"
        print("Config is invalid! Could not find exactly one logged in profile (see log before)")
        # TODO maybe notify brain to stop analysis till user looked into it?
        if rest_client.unregister_page_in_work(analysis_run_id, site.base_page):
            print("Unregistered page at brain.")
            success = True
        else:
            print("Failed unregistering page at brain")
    except KeyboardInterrupt as err:
        print("Received interrupt. Will deregister current page:")
        print("Done") if rest_client.unregister_page_in_work(analysis_run_id, site.base_page) else print("Failed!")
        success = True
        raise err
    except Exception as err:
        cause = "Unknown error: " + err.__class__.__name__
        print("Unknown error! This should be managed explicitly " + str(err))
    finally:
        if not success:
            rest_client.unregister_page_in_work_and_block_for_time(analysis_run_id, site.base_page, cause)
        if chromedriver is not None:
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
            del chromedriver.requests, chromedriver


class PrivacyDetectionProcess:
    def __init__(self, backend_info, analysis_run_id, process_type, privacy_detection_type, config_directory):
        if process_type is not ProcessType.PRIVACY_DETECTION:
            raise TypeError(process_type + " is not supported for privacy analysis!")
        self.backend_info = backend_info
        self.rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        self.privacy_detection_type = privacy_detection_type
        self.analysis_run_id = analysis_run_id
        self.process_type = process_type
        self.config_directory = config_directory

    def start_process(self, running_check: threading.Event = None):
        print("Starting process")
        counter = 0
        while running_check is None or running_check.is_set():
            try:
                site = self.rest_client.get_next_privacy_detection_page_to_analyse_for_run(self.analysis_run_id)
                if site is None:
                    break
            except RetryException:
                continue
            counter += 1
            p = Process(target=process_function,
                        args=(site, self.backend_info, counter, self.privacy_detection_type, self.analysis_run_id,
                              self.config_directory))
            p.start()
            p.join()
            print("Process finished")
        if running_check is not None and not running_check.is_set():
            print("Process was stopped by brain")
        else:
            print("No more sites left. Finished work here!")

    def finish(self):
        pass

    @staticmethod
    def load_privacy_detection_provider(provider_name):
        return PrivacyDetectionProvider[provider_name]

    @staticmethod
    def find_clickable_element_without_url_change(chromedriver):
        tags = ['body', 'div', 'p']
        for tag in tags:
            elements = chromedriver.find_elements(By.TAG_NAME, tag)
            el_count = len(elements)
            current_el = 0
            print("Checking " + tag + " elements for ability to click (count: " + str(len(elements)) + ")")
            while current_el < len(elements) and current_el < el_count:
                el = elements[current_el]
                current_el += 1
                try:
                    url_before_click = chromedriver.current_url
                    el.click()
                    time.sleep(1)
                    if url_before_click != chromedriver.current_url:
                        print("Url changed. Reloading page and retrying")
                        chromedriver.get(url_before_click)
                        elements = chromedriver.find_elements(By.TAG_NAME, tag)
                    else:
                        print("Click action performed without url change! Found an valid element.")
                        return el
                except WebDriverException:
                    pass
        print("We did not find any valid element. Forcing an exception!")
        el = chromedriver.find_element(By.TAG_NAME, 'body')  # Force an exception
        el.click()
        return el
