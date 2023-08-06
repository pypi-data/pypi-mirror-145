import base64
import json

import requests

from exceptions import RetryException
from services.rest_helper import RestHelper
from input.input_management import InputManager
from model.process_type import ProcessType


class RestClient:
    # region Path Variables
    # region Global, Tranco, Misc Paths
    path_check_token = "/rest/global/validateToken"
    path_tranco_entries_between = "/rest/tranco/between"
    path_get_tranco_id_for_site = "/rest/tranco/idforsite"
    path_known_sso_providers = "/rest/knownproviders/all"
    path_file_upload_login_path_detection = "/rest/files/loginlocationdetection"
    # endregion
    # region Login Page Locations Paths
    path_next_page_of_tranco_domains_with_no_login_path_detection = "/rest/loginlocation/getNextNotAnalysedPage"
    path_next_page_to_renew_login_path_information = "/rest/loginlocation/getNextPageToRenew"
    path_next_broken_page_to_renew_login_path_information = "/rest/loginlocation/getNextBrokenToRenew"
    path_latest_login_page_location = "/rest/loginlocation/latestForPage"
    path_latest_login_page_location_by_page_id = "/rest/loginlocation/latestForPageByPageId"
    path_additional_steps_for_login_path_location = "/rest/loginlocation/getAdditionalSteps"
    path_add_new_login_page_location = "/rest/loginlocation/addNew"
    path_create_login_location_renew_request = "/rest/loginlocation/generateRenewRequest"
    # endregion
    # region Analysis Runs Paths
    path_exists_analysis_run = "/rest/analysisrun/existsid"
    path_get_analysis_run_type = "/rest/analysisrun/type"
    path_analysis_run_additional_information = "/rest/analysisrun/additionalInformationForAnalysisRun"
    path_has_configuration = "/rest/analysisrun/hasConfiguration"
    path_get_configuration = "/rest/analysisrun/configuration"
    # endregion
    # region SSO Detection Paths
    path_get_ssodet_next_page_to_analyze = "/rest/ssodetection/nextPageToAnalyse"
    path_save_sso_analysis = "/rest/ssodetection/new"
    # endregion
    # region Currently in Work Paths
    path_unregister_currently_in_work_site_and_block = "/rest/currentlyinwork/unregisterCurrentlyInWorkAndBlockForTime"
    path_unregister_currently_in_work_site = "/rest/currentlyinwork/unregisterCurrentlyInWork"
    path_update_currently_in_work_site_progress = "/rest/currentlyinwork/reportProgress"
    # endregion
    # region Privacy Detection
    path_get_next_privacy_page_to_analyze = "/rest/privacy/nextPageToAnalyse"
    path_save_privacy_detection = "/rest/privacy/new"

    # endregion
    # region Daemon
    path_daemon_start = "/rest/daemon/wakeup"
    path_daemon_get_current_job = "/rest/daemon/job"
    path_daemon_stop = "/rest/daemon/stopped"
    path_daemon_ping = "/rest/daemon/ping"
    path_daemon_update_activity = "/rest/daemon/activity"

    # endregion
    # endregion
    def __init__(self, backend_url, backend_port, token=None):
        self.backend_url = backend_url
        self.port = backend_port
        self.url = self.backend_url + ":" + str(self.port)
        if token is not None:
            self.auth_bearer_header = {'Authorization': 'Bearer ' + token}
        else:
            self.auth_bearer_header = {}

    # region Global, Tranco, Misc
    def check_token(self, token):
        response = self.send_post_request(self.path_check_token, {'token': token})
        if response.status_code == 200 and response.text.startswith("valid"):
            return True
        print("Something went wrong while checking (" + str(response.status_code) + "): " + response.text)
        return False

    def get_list_of_tranco_domains(self, lower_bound, upper_bound):
        url = self.url + self.path_tranco_entries_between
        response = requests.get(url, params={'lower': lower_bound, 'upper': upper_bound},
                                headers=self.auth_bearer_header)
        if not response.status_code == 200:
            print("Something went wrong (code " + str(response.status_code) + "): " + response.text)
            return []
        return_list = []
        for entry in response.json():
            return_list.append(RestHelper.tranco_page_info_from_json(entry))
        return return_list

    def get_tranco_id_for_site(self, site):
        response = self.send_get_request(self.path_get_tranco_id_for_site, {'site': site})
        if response.status_code == 200 and response.text.isnumeric():
            return response.text
        print("Something went wrong")
        return "UNKNOWN"

    def get_known_sso_provider(self):
        response = self.send_get_request(self.path_known_sso_providers)
        return RestHelper.convert_json_to_list_of_sso_provider(response)

    # endregion

    # region Login Page Locations
    def get_next_broken_path_detection_to_renew(self):
        response = self.send_get_request(self.path_next_broken_page_to_renew_login_path_information)
        if len(response.text) == 0:
            return None
        return RestHelper.page_info_from_json(response.json())

    def get_next_login_path_detection_to_renew(self):
        response = self.send_get_request(self.path_next_page_to_renew_login_path_information)
        if len(response.text) == 0:
            return None
        return RestHelper.page_info_from_json(response.json())

    def get_next_page_of_tranco_domains_with_no_login_path_detection(self, lower_bound, upper_bound):
        response = self.send_get_request(self.path_next_page_of_tranco_domains_with_no_login_path_detection,
                                         {'lower': lower_bound, 'upper': upper_bound})
        if len(response.text) == 0:
            return None
        return RestHelper.page_info_from_json(response.json())

    def get_latest_login_location_for_page(self, base_page):
        response = self.send_get_request(self.path_latest_login_page_location, {'basepage': base_page})
        if response.content.__len__() == 0:
            return None
        return RestHelper.manual_login_page_location_from_json(response.json(), self)

    def get_latest_login_location_for_page_by_page_id(self, index):
        response = self.send_get_request(self.path_latest_login_page_location_by_page_id, {'basepageid': index})
        if response.content.__len__() == 0:
            return None
        return RestHelper.manual_login_page_location_from_json(response.json(), self)

    def save_login_page_location(self, basepage, loginPage, hasLogin, additionalStepsToShowLogin, broken,
                                 finding_strategy, har_content):
        additionalStepsData = []
        counter = 0
        if additionalStepsToShowLogin is not None:
            for addStep in additionalStepsToShowLogin:
                additionalStepsData.append(
                    {"additionalStepValue": InputManager.get_additional_step_value_from_user_input(addStep),
                     "additionalStepType": InputManager.get_additional_step_type_from_user_input(addStep),
                     "additionalStepOrderIndex": counter})
                counter += 1

        post_data = {'basepage': basepage, 'loginpage': loginPage, 'haslogin': hasLogin, 'broken': broken,
                     'additionalsteps': base64.b64encode(json.dumps(additionalStepsData).encode()),
                     'findingstrategy': finding_strategy.name}
        response = self.send_post_request(self.path_add_new_login_page_location, post_data)
        if response.status_code == 200 and response.text.isnumeric():
            print("Successfully saved login location!")
            if har_content is not None:
                print("Uploading HAR file...")
                if self.upload_har_files(response.text, har_content, ProcessType.LOGIN_PATH_DETECTION):
                    print("Uploading HAR file finished!")
            else:
                print("No HAR content was given. Not going to upload har file!")
            return response.text
        else:
            print("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def get_additional_steps_for_login_path_location(self, login_path_detection_id):
        response = self.send_get_request(self.path_additional_steps_for_login_path_location,
                                         {'loginpagelocationid': login_path_detection_id})
        return RestHelper.convert_json_to_list_of_additional_steps(response)

    def upload_har_files(self, saved_item_id, har_content, file_type):
        print("Uploading har content")
        if file_type == ProcessType.LOGIN_PATH_DETECTION:
            path = self.path_file_upload_login_path_detection
        else:
            raise Exception("Unknown har file type")
        response = self.send_post_file_request(path, {saved_item_id: base64.b64encode(har_content.encode("utf-8"))})
        if response.status_code == 200 and response.text == "success":
            print("File uploaded successfully!")
            return True
        else:
            print("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def create_renew_login_location_request(self, page_id):
        response = self.send_post_request(self.path_create_login_location_renew_request, {"pageid": page_id})
        if response.status_code == 200:
            if response.text == "created":
                print("Renew request created")
            elif response.text == "exists":
                print("Renew request already exists")
            else:
                print("Something went wrong!")
            return True
        else:
            print("Something went wrong (code " + str(response.status_code) + ")")
            return False

    # endregion

    # region SSO Detection
    def save_analysed_supported_sso_provider(self, trancosite, ids, analysis_session, results, har_content):
        post_data = {'analysisrunid': analysis_session, 'trancosite': trancosite,
                     'supportedproviderids': ids, "loginpages": []}
        if results is not None:
            for result in results:
                post_data['loginpages'].append(result['info'].loginPath)
        files = []
        if har_content is not None:
            files.append(('har', har_content))
        if results is not None:
            for result in results:
                files.append(('screenshot', result['screen']))
        if len(files) > 0:
            print("Upload size of files (har, screen, ...): " + str(len(str(files)) * 0.000001) + " MB")
        response = self.send_post_request_with_files(self.path_save_sso_analysis, post_data,
                                                     files)
        if response.status_code == 200 and response.text == "success":
            print("File uploaded successfully!")
            return True
        else:
            print("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def get_next_ssodetection_page_to_analyse_for_run(self, analysis_run_id):
        return self.get_next_page_to_analyse_for_run(self.path_get_ssodet_next_page_to_analyze, analysis_run_id)

    def get_search_engine_mode_for_run(self, run_id):
        return self.get_additional_analysis_run_information(run_id, "SEARCH_ENGINE")

    # endregion

    # region Privacy Detection
    def save_privacy_detection(self, trancosite, analysis_session, screenshot, har_content):
        post_data = {'analysisrunid': analysis_session, 'trancosite': trancosite}
        files = {}
        if har_content is not None:
            files['har'] = har_content
        if screenshot is not None:
            files['screenshot'] = screenshot
        response = self.send_post_request_with_files(self.path_save_privacy_detection, post_data,
                                                     files)
        if response.status_code == 200 and response.text == "success":
            print("Privacy detection with HAR and Screenshot uploaded was successful!")
            return True
        else:
            print("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def get_next_privacy_detection_page_to_analyse_for_run(self, analysis_run_id):
        return self.get_next_page_to_analyse_for_run(self.path_get_next_privacy_page_to_analyze, analysis_run_id)

    def get_privacy_detection_mode_for_run(self, run_id):
        return self.get_additional_analysis_run_information(run_id, "PRIVACY_DETECTION_TYPE")

    # endregion

    # region Currently in Work Pages
    def unregister_page_in_work_and_block_for_time(self, analysisrunid, basepage, cause="Unknown"):
        response = self.send_post_request(self.path_unregister_currently_in_work_site_and_block,
                                          {'analysisrunid': analysisrunid, 'basepage': basepage, 'cause': cause})
        if response.status_code == 200:
            return True
        print("Something went wrong (" + str(response.status_code) + ")!")
        return False

    def unregister_page_in_work(self, analysisrunid, basepage):
        response = self.send_post_request(self.path_unregister_currently_in_work_site,
                                          {'analysisrunid': analysisrunid, 'basepage': basepage})
        if response.status_code == 200:
            return True
        print("Something went wrong (" + str(response.status_code) + ")!")
        return False

    def update_progress_of_analysis(self, analysisrunid: int, basepage: str, percent: int, status: str):
        response = self.send_post_request(self.path_update_currently_in_work_site_progress,
                                          {'analysisrunid': analysisrunid, 'basepage': basepage,
                                           'percent': int(percent), 'status': status})
        if response.status_code == 200:
            return True
        print("Something went wrong updating progress status (" + str(response.status_code) + ")!")
        return False

    # endregion

    # region Analysis Runs
    def exists_analysis_session(self, analysis_run_id):
        response = self.send_get_request(self.path_exists_analysis_run,
                                         {'analysisrunid': analysis_run_id})
        return response.status_code == 200 and response.text == 'success'

    def get_analysis_run_type(self, analysis_run_id):
        response = self.send_get_request(self.path_get_analysis_run_type, {'analysisrunid': analysis_run_id})
        if response.status_code == 200 and response.text is not None and len(response.text) != 0:
            return response.text
        print("Something went wrong (code " + str(response.status_code) + ")")
        return None

    def get_configuration_for_run(self, analysis_run_id):
        response = self.send_get_request(self.path_has_configuration, {'analysisrunid': analysis_run_id})
        if response.status_code != 200 or response.text is None or response.text != "true":
            return None
        response = self.send_get_request(self.path_get_configuration, {'analysisrunid': analysis_run_id})
        if response.status_code != 200:
            return None
        return response.content

    # endregion

    # region Generic Methods
    def get_next_page_to_analyse_for_run(self, path, analysis_run_id):
        response = self.send_get_request(path, {'analysisrunid': analysis_run_id})
        if response.status_code == 200:
            if response.text is not None and len(response.text) != 0:
                return RestHelper.page_info_from_json(response.json())
            else:
                return None  # No more sites left!
        if response.status_code == 409:
            print("Server requested a retry")
            raise RetryException()
        print("Something went wrong (code " + str(response.status_code) + ")")
        return None

    def get_additional_analysis_run_information(self, analysis_run_id, key):
        response = self.send_get_request(self.path_analysis_run_additional_information,
                                         {'analysisrunid': analysis_run_id, 'key': key})
        if response.status_code == 200 and response.text is not None and len(response.text) != 0:
            return response.text
        print("Something went wrong (code " + str(response.status_code) + ")")
        return None

    # endregion

    # region DAEMON METHODS
    def get_notify_daemon_start_get_token(self, name, identifier):
        if name is None:
            response = self.send_post_request(self.path_daemon_start, {'identifier': identifier})
        else:
            response = self.send_post_request(self.path_daemon_start, {'name': name, 'identifier': identifier})
        if response.status_code == 200 and response.text is not None and len(response.text) != 0:
            return response.text
        elif response.status_code != 200:
            print("Something went wrong! (code: " + str(response.status_code) + ")")
        return None

    def get_job_for_daemon_client(self):
        response = self.send_get_request(self.path_daemon_get_current_job)
        if response.status_code == 200 and response.text is not None and len(
                response.text) != 0 and response.text.lstrip("-").isnumeric():
            return response.text
        return None

    def send_daemon_ping(self):
        self.send_get_request(self.path_daemon_ping)

    def update_latest_activity(self, activity: str):
        self.send_post_request(self.path_daemon_update_activity, {'activity': activity})

    # endregion

    # region REQUEST METHODS
    def send_get_request(self, path, parameters=None):
        if parameters is None:
            return requests.get(self.url + path, headers=self.auth_bearer_header, allow_redirects=False)
        else:
            return requests.get(self.url + path, params=parameters, headers=self.auth_bearer_header,
                                allow_redirects=False)

    def send_post_request(self, path, postdata):
        return requests.post(self.url + path, data=postdata, headers=self.auth_bearer_header, allow_redirects=False)

    def send_post_file_request(self, path, files):
        print("Size of fileupload: " + str(len(str(files)) * 0.000001) + " MB")
        return requests.post(self.url + path, files=files, headers=self.auth_bearer_header, allow_redirects=False)

    def send_post_request_with_files(self, path, postdata, files):
        return requests.post(self.url + path, data=postdata, files=files, headers=self.auth_bearer_header,
                             allow_redirects=False)
    # endregion
