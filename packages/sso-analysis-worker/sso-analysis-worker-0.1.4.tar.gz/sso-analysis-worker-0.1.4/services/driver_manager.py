import json
import os
import tempfile
from os.path import exists
from time import sleep, time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from services import crx_downloader
from services.xpath_manager import XPathManager

extensions_folder = tempfile.tempdir + "/ssoworker/Extensions"
if not os.path.exists(extensions_folder):
    os.makedirs(extensions_folder)


class DriverManager:
    extensions = [
        ["idontcareaboutcookies",
         "https://chrome.google.com/webstore/detail/i-dont-care-about-cookies/fihnjjcciajhdojfnbdddfaoknhalnja"]
    ]

    if not exists(extensions_folder):
        os.mkdir(extensions_folder)

    @staticmethod
    def prepare_webpage_with_steps_to_reproduce(driver, current_item, throw_exception_if_element_not_found=False):
        driver.get(current_item.loginPath)
        for step in current_item.additionalSteps:
            sleep(1)
            if step.additionalStepType == "@cookie":
                DriverManager.set_cookie(driver, step.additionalStepValue.split(" ")[0],
                                         step.additionalStepValue.split(" ")[1])
            elif step.additionalStepType == "@wait":
                sleep(int(step.additionalStepValue))
            else:
                DriverManager.execute_driver_step(driver,
                                                  XPathManager.get_xpath_for_input_type(
                                                      step.additionalStepType + ":" + step.additionalStepValue),
                                                  throw_exception_if_element_not_found)

    @staticmethod
    def generate_driver(config_directory=None):
        print(extensions_folder)
        options = webdriver.ChromeOptions()
        options.set_capability("unexpectedAlertBehaviour", "accept")
        options.set_capability("unhandledPromptBehavior", "accept")
        if config_directory is not None:
            options.add_argument("--user-data-dir=" + config_directory.name + "/chrome_profile")
            extensions_file = open(config_directory.name + "/extensions.json")
            extensions_meta_info = json.load(extensions_file)
            for extension in extensions_meta_info['extensions']['packed']:
                options.add_extension(config_directory.name + "/" + extension)
            unpacked_extensions_string = ""
            for extension in extensions_meta_info['extensions']['unpacked']:
                unpacked_extensions_string += config_directory.name + "/" + extension + ","
            options.add_argument("--load-extension=" + unpacked_extensions_string)

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        DriverManager.download_extensions()

        for filename in os.listdir(extensions_folder):
            if filename.endswith(".crx"):
                options.add_extension(extensions_folder + "/" + filename)

        selenium_wire_options = {
            'enable_har': True  # Capture HAR data, retrieve with driver.har
        }

        print("Starting driver")
        driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager(log_level=0).install(),
                                  seleniumwire_options=selenium_wire_options)
        driver.implicitly_wait(1)
        driver.set_page_load_timeout(180)

        print("Activate stealth for driver")
        stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine", fix_hairline=True)
        driver.set_window_position(0, 0)
        driver.set_window_size(1920, 1080)

        return driver

    @staticmethod
    def download_extensions():
        realpath = extensions_folder + "/"
        for ext in DriverManager.extensions:
            path = realpath + ext[0]
            skip = False
            for f in os.listdir(realpath):
                if f.startswith(ext[0]):
                    time_diff = int(time()) - int((os.path.getmtime(realpath + f)))
                    if time_diff > 3600:
                        print("File exists but is older than a hour. Redownloading it")
                        os.remove(realpath + f)
                    else:
                        print("Extension exists and is not older than a hour. Skipping download.")
                        skip = True
                    break
            if not skip:
                crx_downloader.download(ext[1], path)

    @staticmethod
    def set_cookie(driver, name, value):
        driver.add_cookie({"name": name, "value": value})
        driver.refresh()

    @staticmethod
    def execute_driver_step(driver, xpath_input, throw_exception_if_element_not_found=False):
        el = DriverManager.find_element(driver, xpath_input)
        if el is not None:
            el.click()
        elif throw_exception_if_element_not_found:
            raise NoSuchElementException()

    @staticmethod
    def find_element(driver, xpath_input):
        elements = driver.find_elements(By.XPATH, xpath_input)
        if len(elements) == 0:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_input)))
            except TimeoutException:
                pass
            except Exception as err:
                print("ERROR: Unknown exception! ")
                print(err)
            elements = driver.find_elements(By.XPATH, xpath_input)
        if len(elements) == 0:
            print("Couldn't find element for " + xpath_input)
            el = None
        elif len(elements) == 1:
            el = elements[0]
        else:
            foundWithoutScriptEntries = 0
            for element in elements:
                if element.tag_name != "script":
                    if foundWithoutScriptEntries == 0:
                        el = element
                    foundWithoutScriptEntries += 1
            if foundWithoutScriptEntries > 1:
                print("WARNING: Found more than one element for users input. Taking the first one")
        return el
