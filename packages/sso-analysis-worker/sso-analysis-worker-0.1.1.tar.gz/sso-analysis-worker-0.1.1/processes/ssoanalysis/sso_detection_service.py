from exceptions import RenewalRequestNeededException
from input.input_management import InputManager
from processes.ssoanalysis.locators.social_login_information import SocialLoginInformation
from processes.ssoanalysis.locators.social_login_locator import SocialLoginLocator


class SSODetectionService:

    def __init__(self, known_sso_providers):
        self.known_sso_providers = known_sso_providers
        self.provider_ids = {
            'google': self.find_id_for_provider("google"),
            'facebook': self.find_id_for_provider("facebook"),
            'apple': self.find_id_for_provider("apple"),
            'none': self.find_id_for_provider("none")
        }
        self.locators = {
            'google': self.load_social_login_locater("Google"),
            'facebook': self.load_social_login_locater("Facebook"),
            'apple': self.load_social_login_locater("Apple"),
        }

    def automatic_sso_detection(self, chromedriver, latest_login_info, progress_callback=None):
        ids = []
        progress_callback(1, 3, "Identifying Google SSO Support for " + latest_login_info.loginPath)
        print("--- Google ---")
        google_locate_result = self.locators['google'].locate_login(chromedriver, latest_login_info)
        if google_locate_result:
            ids.append(self.provider_ids['google'])
        progress_callback(2, 3, "Identifying Facebook SSO Support for " + latest_login_info.loginPath)
        print("--- Facebook ---")
        facebook_locate_result = self.locators['facebook'].locate_login(chromedriver, latest_login_info)
        if facebook_locate_result:
            ids.append(self.provider_ids['facebook'])
        progress_callback(3, 3, "Identifying Apple SSO Support for " + latest_login_info.loginPath)
        print("--- Apple ---")
        apple_locate_result = self.locators['apple'].locate_login(chromedriver, latest_login_info)
        if apple_locate_result:
            ids.append(self.provider_ids['apple'])
        if len(ids) == 0:
            ids.append(self.provider_ids['none'])
        return ids

    def manual_sso_detection(self):
        supported_sso = []
        inp = ""
        while inp != "Finish" and inp != "None" and inp != "Skip" and inp != "Send Renewal Request":
            valid = self.create_valid_inputs_from_already_gathered_sso(supported_sso)
            if len(supported_sso) == 0:
                valid.append("Skip")
                valid.append("Send Renewal Request")
            if len(supported_sso) > 0:
                valid.append("Finish")
                valid.append("Reset")
            inp = InputManager.get_input_from_gui_with_specific_answer_values("Input", valid, False)
            if inp == "Reset":
                supported_sso.clear()
            if inp == "Send Renewal Request":
                raise RenewalRequestNeededException()
            elif inp != "Finish":
                supported_sso.append(inp)
            if inp == "Finish" or inp == "None" or inp == "Skip":
                savable_sso_providers = []
                for supported_sso_provider in supported_sso:
                    for backend_sso_provider in self.known_sso_providers:
                        if backend_sso_provider[1].startswith(supported_sso_provider):
                            savable_sso_providers.append(backend_sso_provider)
                text = ""
                ids = []
                for save_sso_provider in savable_sso_providers:
                    text += " " + save_sso_provider[1]
                    ids.append(save_sso_provider[0])
                if len(ids) > 1 or ids[0] != 9999:
                    if InputManager.get_input_from_gui_with_specific_answer_values(
                            "Saving:" + text + ". Correct?", ["y", "n"], False) == "n":
                        print("Restarting gathering process...")
                        supported_sso.clear()
                        inp = ""
                    else:
                        return ids
                else:
                    return ids

    def create_valid_inputs_from_already_gathered_sso(self, supported_sso):
        valid_inputs_raw = InputManager.create_supported_sso_user_inputs(self.known_sso_providers)
        return_list = []
        for inp in valid_inputs_raw:
            # inp_to_check = inp[0][0:1].upper() + inp[0][1:len(inp)]
            inp_to_check = inp[1]
            if inp_to_check not in supported_sso:
                if inp[1].lower() != "none" or len(supported_sso) == 0:
                    return_list.append(inp[1])  # Change this to 0 and change commented line above for short form
        return return_list

    def find_id_for_provider(self, provider_name):
        for sso in self.known_sso_providers:
            if sso[1].lower() == provider_name.lower():
                return sso[0]
        raise Exception("Unknown provider")

    @staticmethod
    def load_social_login_locater(social_login_name):
        return SocialLoginLocator(SocialLoginInformation[social_login_name]["name"],
                                  SocialLoginInformation[social_login_name]["exclude_url_starts_with"],
                                  SocialLoginInformation[social_login_name]["valid_login_urls"],
                                  SocialLoginInformation[social_login_name]["must_have_texts_in_valid_login_urls"],
                                  SocialLoginInformation[social_login_name]["extra_texts"], )
