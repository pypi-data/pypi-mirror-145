import threading
from multiprocessing import Process
from time import sleep

from selenium.common.exceptions import WebDriverException, TimeoutException, ElementNotInteractableException, \
    NoSuchElementException

from exceptions import ManualAnalysisNeededException
from exceptions import RenewalRequestNeededException
from exceptions import RetryException
from exceptions import SiteNotResolvableException
from input.input_management import InputManager
from model.backend_information import BackendInformation
from model.login_path_information import LoginPathInformation
from model.process_type import ProcessType
from model.ssodetection.search_engine import SearchEngine
from processes.process_helper import ProcessHelper
from processes.ssoanalysis import startpage_search, duck_duck_go_search
from processes.ssoanalysis.duck_duck_go_search import DuckDuckGoChangedSiteException
from processes.ssoanalysis.sso_detection_service import SSODetectionService
from processes.ssoanalysis.startpage_search import StartPageException
from services.driver_manager import DriverManager
from services.rest_client import RestClient


def thread_process(counter, site, backend_info: BackendInformation, process_type: ProcessType, search_engines,
                   analysis_run_id):
    success = False
    rest_client = None
    chromedriver = None
    cause = "Unknown"
    try:
        rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        print("Received site " + site.base_page + " to analyse. Starting chromedriver...")
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 0, "Starting chromedriver")
        chromedriver = DriverManager.generate_driver()
        if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 10, "Resolving site")
            test_resolve = ProcessHelper.resolve_tld1(chromedriver, site.base_page)
            if test_resolve is None:
                raise SiteNotResolvableException()
        del chromedriver.requests

        print("Checking sso support for " + site.base_page + " (id:" + str(site.index) + "|trancoID:" + str(
            rest_client.get_tranco_id_for_site(site.base_page)) + ") [" + str(counter) + "]")
        found_logins = []
        if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
            try:
                if search_engines.__contains__(SearchEngine.DUCKDUCKGO):
                    rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 15,
                                                            "Identifying login pages by DuckDuckGo")
                    found_logins.append({'engine': "DUCKDUCKGO",
                                         'site': duck_duck_go_search.get_duckduckgo_login_page(chromedriver,
                                                                                               site.base_page)})
                elif search_engines.__contains__(SearchEngine.STARTPAGE):
                    rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 20,
                                                            "Identifying login pages by Startpage")
                    found_logins.append({'engine': "STARTPAGE",
                                         'site': startpage_search.get_startpage_login_page(chromedriver,
                                                                                           site.base_page)})
                else:
                    raise Exception("Unknown search engine!")
                latest_login_infos = []
                for f_login in found_logins:
                    latest_login_infos.append(
                        LoginPathInformation(site, -1, f_login['site'], [], True, False, None))
            except (DuckDuckGoChangedSiteException, StartPageException) as err:
                print(err)
                input("Something unexpected happened. Waiting for user input")
                return
        else:
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 20,
                                                    "Loading login page from brain")
            latest_login_infos = [rest_client.get_latest_login_location_for_page_by_page_id(site.index)]
        # Finished Login Gathering
        results = []
        steps = 60 / len(latest_login_infos)
        last_progress = 20
        for latest_login_info in latest_login_infos:
            already_analysed_login_page = False
            for result in results:
                if result["info"].loginPath == latest_login_info.loginPath:
                    results.append(
                        {"ids": result["ids"], "info": latest_login_info, "screen": result["screen"]})
                    already_analysed_login_page = True
                    break
            if already_analysed_login_page:
                last_progress += steps
                continue
            try:
                last_progress += steps / 6
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, last_progress,
                                                        "Preparing analysis of " + latest_login_info.loginPath)
                DriverManager.prepare_webpage_with_steps_to_reproduce(chromedriver, latest_login_info, True)
            except (ElementNotInteractableException, NoSuchElementException):
                if handle_preparation_error(process_type, site.index, site.base_page, rest_client):
                    raise RenewalRequestNeededException()
            last_progress = last_progress + steps / 6
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, last_progress,
                                                    "Taking screenshot of " + latest_login_info.loginPath)
            screen = wait_and_gather_screenshot_if_necessary(chromedriver, process_type)

            # No update necessary because it will happen next in the callback

            def progress_callback(step: int, max: int, status: str):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page,
                                                        last_progress + ((steps / 1.5) / max * step), status)

            ids = gather_sso_support(latest_login_info, chromedriver, rest_client, process_type, progress_callback)
            last_progress = last_progress + steps / 1.5
            results.append({"ids": ids, "info": latest_login_info, "screen": screen})
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 90, "Uploading results")
        success = save_supported_sso_provider(site, results, found_logins, chromedriver.har, process_type, rest_client,
                                              analysis_run_id)
        print("Successfully saved!" if success else "Could not save site")
    except RenewalRequestNeededException:
        print("Sending renewal request")
        rest_client.create_renew_login_location_request(site.index)
        return
    except TimeoutException as err:
        cause = "Timout: " + err.__class__.__name__
        print("Timeout reached: " + err.msg)
    except WebDriverException as err:
        cause = "Webdriver problem: " + err.__class__.__name__
        print("Could not finish analysing (" + err.msg + ")!")
    except ManualAnalysisNeededException as err:
        cause = "Unknown - manual analysis needed"
        print("Could not finish analysing (" + str(err) + ")!.")
    except SiteNotResolvableException:
        cause = "Not resolvable"
        print("Could not resolve site!")
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


# Returns if the current site should be skipped
def handle_preparation_error(process_type, page_index, base_page, rest_client):
    print("Site preparation for " + base_page + " failed!")
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION:
        print("We will send a renewal request and skip this site!")
        handle_fail = 'y'
    elif process_type == ProcessType.MANUAL_SSO_DETECTION:
        handle_fail = InputManager.get_input_from_gui_with_specific_answer_values(
            "Do you want to send a renew request and skip this page or continue anyway?", ['y', 'n'])
    else:
        raise TypeError(process_type.__str__() + " should not land in this part of the code!")
    return handle_fail == 'y'


def wait_and_gather_screenshot_if_necessary(chromedriver, process_type):
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        print("Sleeping 5 sec to get best results in screenshot")
        sleep(5)
        print("Taking screenshot...")
        return chromedriver.get_screenshot_as_png()
    elif process_type == ProcessType.AUTOMATIC_SSO_DETECTION:
        print("Waiting 5 sec...")
        sleep(5)
    return None


def gather_sso_support(latest_login_info, chromedriver, rest_client, process_type, progress_callback=None):
    print("Starting SSO Detection algorithm")
    service = SSODetectionService(rest_client.get_known_sso_provider())
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION or process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        results = service.automatic_sso_detection(chromedriver, latest_login_info, progress_callback)
    else:
        results = service.manual_sso_detection()
    return results


def save_supported_sso_provider(site, results, found_logins, har, process_type, rest_client, analysis_run_id):
    ids = []
    already_used_engines = []
    for result in results:
        for found_login in found_logins:
            if result['info'].loginPath == found_login['site'] and not already_used_engines.__contains__(
                    found_login['engine']):
                result['info'].loginPath = "<<" + found_login['engine'] + ">>" + found_login['site']
                already_used_engines.append(found_login['engine'])
        for id in result['ids']:
            if not ids.__contains__(id):
                ids.append(id)
    if ids.__contains__(9999) and len(ids) > 1:
        ids.remove(9999)
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        print("Saving login pages (" + str(
            len(results)) + ") and the following sso support for " + site.base_page + ": " + str(ids))
        return rest_client.save_analysed_supported_sso_provider(site.base_page, ids, analysis_run_id,
                                                                results, har)
    else:
        print("Saving the following sso support for " + site.base_page + ": " + str(ids))
        return rest_client.save_analysed_supported_sso_provider(site.base_page, ids, analysis_run_id,
                                                                None, har)


class SSODetectionProcess:

    def __init__(self, backend_info: BackendInformation, analysis_run_id: int, process_type: ProcessType,
                 search_engines: list = None):
        if not [ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE, ProcessType.AUTOMATIC_SSO_DETECTION,
                ProcessType.MANUAL_SSO_DETECTION].__contains__(process_type):
            raise TypeError(process_type + " is not supported for single sign on analysis!")
        self.backend_info = backend_info
        self.rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        self.search_engines = search_engines
        self.analysis_run_id = analysis_run_id
        self.process_type = process_type

    def start_process(self, running_check: threading.Event = None):
        print("Starting process")
        counter = 0
        while running_check is None or running_check.is_set():
            try:
                site = self.get_next_page_to_analyse()
                if site is None:
                    break
            except RetryException:
                continue
            counter += 1
            p = Process(target=thread_process, args=(
                counter, site, self.backend_info, self.process_type, self.search_engines, self.analysis_run_id))
            p.start()
            p.join()
            print("Process finished")
        if running_check is not None and not running_check.is_set():
            print("Process was stopped by brain")
        else:
            print("No more sites left. Finished work here!")

    def finish(self):
        try:
            print("Quitting (analysis id: " + str(self.analysis_run_id) + ")")
        except WebDriverException:
            pass

    def get_next_page_to_analyse(self):
        return self.rest_client.get_next_ssodetection_page_to_analyse_for_run(self.analysis_run_id)
