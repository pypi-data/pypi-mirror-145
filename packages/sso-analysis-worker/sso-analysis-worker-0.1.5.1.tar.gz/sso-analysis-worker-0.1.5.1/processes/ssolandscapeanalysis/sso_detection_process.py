import threading
from multiprocessing import Process
from time import sleep

from selenium.common.exceptions import WebDriverException, TimeoutException, ElementNotInteractableException, \
    NoSuchElementException

from logmgmt import logger
from exceptions import ManualAnalysisNeededException, WebDriverInitialisationException
from exceptions import RenewalRequestNeededException
from exceptions import RetryException
from exceptions import SiteNotResolvableException
from input.input_management import InputManager
from model.backend_information import BackendInformation
from model.login_path_information import LoginPathInformation
from model.process_type import ProcessType
from model.ssodetection.search_engine import SearchEngine
from processes.process_helper import ProcessHelper
from processes.ssolandscapeanalysis import startpage_search, duck_duck_go_search, bing_search
from processes.ssolandscapeanalysis.sso_detection_service import SSODetectionService
from services.driver_manager import DriverManager
from services.rest_client import RestClient


def thread_process(counter, site, backend_info: BackendInformation, process_type: ProcessType, search_engines,
                   analysis_run_id):
    success = False
    rest_client = None
    chromedriver = None
    cause = "Unknown"
    site_no_proto = ProcessHelper.remove_protocol_if_existent(site.base_page)
    try:
        rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        known_sso_provider = rest_client.get_known_sso_provider()
        logger.info("Received site " + site.base_page + " to analyse. Starting chromedriver...")
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 0, "Starting chromedriver")
        chromedriver = None
        if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
            chromedriver = DriverManager.generate_driver()
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 5, "Resolving site")
            test_resolve = ProcessHelper.resolve_tld1(chromedriver, site.base_page)
            if test_resolve is None:
                raise SiteNotResolvableException()

        logger.info("Checking sso support for " + site.base_page + " (id:" + str(site.index) + "|trancoID:" + str(
            rest_client.get_tranco_id_for_site(site.base_page)) + ") [" + str(counter) + "]")
        login_candidates = []
        if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
            if chromedriver is None:
                chromedriver = DriverManager.generate_driver()
            for se in search_engines:
                if not [e for e in SearchEngine].__contains__(se):
                    raise Exception("Unknown search engine!")
            if search_engines.__contains__(SearchEngine.DUCKDUCKGO):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 10,
                                                        "Identifying login pages by DuckDuckGo")
                login_candidates_ddg = duck_duck_go_search.get_duckduckgo_login_pages(chromedriver, site_no_proto,
                                                                                      count_of_results=3)
                for lc in login_candidates_ddg:
                    login_candidates.append({'engine': "DUCKDUCKGO", 'site': lc})
            if search_engines.__contains__(SearchEngine.STARTPAGE):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 15,
                                                        "Identifying login pages by Startpage")
                login_candidates_sp = startpage_search.get_startpage_login_pages(chromedriver, site_no_proto,
                                                                                 count_of_results=3)
                for lc in login_candidates_sp:
                    login_candidates.append({'engine': "STARTPAGE", 'site': lc})
            if search_engines.__contains__(SearchEngine.BING):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 20,
                                                        "Identifying login pages by Bing")
                login_candidates_bing = bing_search.get_bing_login_pages(chromedriver, site_no_proto,
                                                                         count_of_results=3)
                for fc in login_candidates_bing:
                    login_candidates.append({'engine': "BING", 'site': fc})
            latest_login_infos = []
            for f_login in login_candidates:
                latest_login_infos.append(
                    LoginPathInformation(site, -1, f_login['site'], [], True, False, None, {'se': f_login['engine']}))
        else:
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 20,
                                                    "Loading login page from brain")
            latest_login_infos = [rest_client.get_latest_login_location_for_page_by_page_id(site.index)]
        # Finished Login Gathering
        if chromedriver is not None:
            logger.info("Preparations are finished. Closing chrome instance which was started for preparation.")
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
        results = []
        steps = 60 / len(latest_login_infos)
        last_progress = 20
        har_files = []
        for latest_login_info in latest_login_infos:
            logger.info("Starting analysis for " + latest_login_info.loginPath)
            already_analysed_login_page = False
            for result in results:
                if result["info"].loginPath == latest_login_info.loginPath:
                    results.append({"ids": result["ids"], "info": latest_login_info, "screen": result["screen"]})
                    already_analysed_login_page = True
                    break
            if already_analysed_login_page:
                last_progress += steps
                continue
            logger.info("Starting chrome instance to analyse " + latest_login_info.loginPath)
            chromedriver = DriverManager.generate_driver()
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

            # No status update necessary because it will happen next in the callback

            def progress_callback(step: int, max: int, status: str):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page,
                                                        last_progress + ((steps / 1.5) / max * step), status)

            search_for_google = not ProcessHelper.contain_results_provider(results, "google", known_sso_provider)
            if not search_for_google:
                logger.info("Google SSO Support already found. Skipping it in analysis")
            search_for_facebook = not ProcessHelper.contain_results_provider(results, "facebook", known_sso_provider)
            if not search_for_facebook:
                logger.info("Facebook SSO Support already found. Skipping it in analysis")
            search_for_apple = not ProcessHelper.contain_results_provider(results, "apple", known_sso_provider)
            if not search_for_apple:
                logger.info("Apple SSO Support already found. Skipping it in analysis")

            ids = gather_sso_support(known_sso_provider, latest_login_info, chromedriver, process_type,
                                     search_for_google, search_for_facebook, search_for_apple, progress_callback)
            logger.info("Analysis finished for " + latest_login_info.loginPath +
                        ". Exporting har and stopping chromedriver")
            har_files.append(chromedriver.har)
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
            last_progress = last_progress + steps / 1.5
            results.append({"ids": ids, "info": latest_login_info, "screen": screen})
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 90, "Uploading results")
        success = save_supported_sso_provider(site, results, login_candidates, har_files, process_type,
                                              rest_client, analysis_run_id)
        logger.info("Successfully saved!" if success else "Could not save site")
    except RenewalRequestNeededException:
        logger.error("Sending renewal request")
        rest_client.create_renew_login_location_request(site.index)
        return
    except TimeoutException as err:
        cause = "Timout: " + err.__class__.__name__
        logger.error("Timeout reached: " + err.msg)
    except WebDriverException as err:
        cause = "Webdriver problem: " + err.__class__.__name__
        logger.error("Could not finish analysing (" + err.msg + ")!")
    except ManualAnalysisNeededException as err:
        cause = "Unknown - manual analysis needed"
        logger.error("Could not finish analysing (" + str(err) + ")!.")
    except SiteNotResolvableException:
        cause = "Not resolvable"
        logger.error("Could not resolve site!")
    except KeyboardInterrupt as err:
        logger.info("Received interrupt. Will deregister current page:")
        logger.info("Done") if rest_client.unregister_page_in_work(analysis_run_id, site.base_page) \
            else logger.error("Failed!")
        success = True
        raise err
    except WebDriverInitialisationException as e:
        logger.error(e)
        logger.error(
            "Webdriver could not be initialized (" + e.thrown_exception.__class__.__name__ + "). This client looks broken. Exit with error code")
        try:
            rest_client.unregister_page_in_work(analysis_run_id, site.base_page)
            rest_client.update_latest_activity("ERROR!")
            success = True
        except Exception:
            pass
        exit(75)
    except Exception as err:
        cause = "Unknown error: " + err.__class__.__name__
        logger.error("Unknown error! This should be managed explicitly " + str(err))
    finally:
        if not success:
            rest_client.unregister_page_in_work_and_block_for_time(analysis_run_id, site.base_page, cause)
        if chromedriver is not None:
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
            del chromedriver.requests, chromedriver


# Returns if the current site should be skipped
def handle_preparation_error(process_type, page_index, base_page, rest_client):
    logger.error("Site preparation for " + base_page + " failed!")
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION:
        logger.error("We will send a renewal request and skip this site!")
        handle_fail = 'y'
    elif process_type == ProcessType.MANUAL_SSO_DETECTION:
        handle_fail = InputManager.get_input_from_gui_with_specific_answer_values(
            "Do you want to send a renew request and skip this page or continue anyway?", ['y', 'n'])
    else:
        raise TypeError(process_type.__str__() + " should not land in this part of the code!")
    return handle_fail == 'y'


def wait_and_gather_screenshot_if_necessary(chromedriver, process_type):
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        logger.info("Sleeping 10 sec to get best results in screenshot")
        sleep(10)
        logger.info("Taking screenshot...")
        return chromedriver.get_screenshot_as_png()
    elif process_type == ProcessType.AUTOMATIC_SSO_DETECTION:
        logger.info("Waiting 10 sec...")
        sleep(10)
    return None


def gather_sso_support(known_sso_provider, latest_login_info, chromedriver, process_type, google=True, facebook=True,
                       apple=True, progress_callback=None):
    logger.info("Starting SSO Detection algorithm")
    service = SSODetectionService(known_sso_provider)
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION or process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        results = service.automatic_sso_detection(chromedriver, latest_login_info, progress_callback, google, facebook,
                                                  apple)
    else:
        results = service.manual_sso_detection()
    return results


def save_supported_sso_provider(site, results, found_logins, har_files, process_type, rest_client, analysis_run_id):
    ids = []
    for result in results:
        if result['info'].other_information.__contains__("se"):
            result['info'].loginPath = "<<" + result['info'].other_information['se'] + ">>" + result['info'].loginPath
        for id_container in result['ids']:
            id_already_exists = False
            for already_existing_id in ids:
                if id_container[0] == already_existing_id[0]:
                    id_already_exists = True
                    break
            if not id_already_exists:
                ids.append(id_container)

    if ids.__contains__((9999,)) and len(ids) > 1:
        ids.remove((9999,))
    if len(ids) == 0:
        ids.append((9999,))
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        logger.info("Saving login candidates (" + str(
            len(results)) + ") and the following sso support for " + site.base_page + ": " + str(ids))
        return rest_client.save_analysed_supported_sso_provider(site.base_page, ids, analysis_run_id,
                                                                results, har_files)
    else:
        logger.info("Saving the following sso support for " + site.base_page + ": " + str(ids))
        return rest_client.save_analysed_supported_sso_provider(site.base_page, ids, analysis_run_id,
                                                                None, har_files)


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

    def start_process(self, running_check: threading.Event = None, no_error_check: threading.Event = None):
        logger.info("Starting process")
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
            if p.exitcode == 75:
                logger.error("Client looks broken! Quitting!")
                if no_error_check is not None:
                    no_error_check.clear()
                exit(75)
            logger.info("Process finished")
        if running_check is not None and not running_check.is_set():
            logger.info("Process was stopped by brain")
        else:
            logger.info("No more sites left. Finished work here!")

    def finish(self):
        try:
            logger.info("Quitting (analysis id: " + str(self.analysis_run_id) + ")")
        except WebDriverException:
            pass

    def get_next_page_to_analyse(self):
        return self.rest_client.get_next_ssodetection_page_to_analyse_for_run(self.analysis_run_id)
