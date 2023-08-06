from multiprocessing import Process

from selenium.common.exceptions import TimeoutException, WebDriverException

from exceptions import ManualAnalysisNeededException
from exceptions import RenewalRequestNeededException
from model.login_path_information import LoginPathInformation
from model.page_information import PageInformation
from processes.ssoanalysis.sso_detection_service import SSODetectionService
from services import file_service
from services.driver_manager import DriverManager


def thread_process(site, sso_detection_service, local_run_results):
    try:
        site = site.replace("\n", "")
        if not site.startswith("https://") and not site.startswith("http://"):
            site = "https://" + site
        print("Analyzing site " + site)
        chromedriver = DriverManager.generate_driver()
        chromedriver.get(site)
        ids = sso_detection_service.automatic_sso_detection(
            chromedriver, LoginPathInformation(PageInformation(-1, site), -1, site, [], True, False, None))
        file_service.save_to_file(local_run_results, site, ids)
        chromedriver.close()
        chromedriver.quit()
    except (RenewalRequestNeededException, TimeoutException, WebDriverException,
            ManualAnalysisNeededException) as err:
        print("Problems while analysing website " + site + "! Skipping...", err)
    except KeyboardInterrupt as err:
        print("Received interrupt")
        raise err
    except Exception as err:
        print("Unknown error! This should be managed explicitly " + str(err))


class LocalSSODetectionProcess:

    def __init__(self, local_run_sites: str, local_run_results: str):
        self.local_run_sites = local_run_sites
        self.local_run_results = local_run_results
        self.sso_detection_service = SSODetectionService(
            [[1, "Google"], [2, "Facebook"], [3, "Apple"], [9998, "Others"], [9999, "None"]])

    def start_process(self):
        counter = 0
        while (site := file_service.read_line_from_file(self.local_run_sites, counter)) is not None:
            p = Process(target=thread_process, args=(site, self.sso_detection_service, self.local_run_results))
            p.start()
            p.join()
            counter += 1
            print("Process finished")
        print("No more sites left!")
