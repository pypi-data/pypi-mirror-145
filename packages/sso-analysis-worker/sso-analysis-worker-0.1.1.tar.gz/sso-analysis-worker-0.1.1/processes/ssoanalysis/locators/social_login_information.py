SocialLoginInformation = {
    "Google": {
        "name": "Google",
        "valid_login_urls": ["https://accounts.google.com/"],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["accounts.google.", "google.", "developers.googleblog.com/", "pki.goog"],
        "extra_texts": ["ورود با حساب گوگل"]
    },
    "Facebook": {
        "name": "Facebook",
        "valid_login_urls": ["https://m.facebook.com/login", "https://facebook.com/login",
                             "https://www.facebook.com/login"],
        "must_have_texts_in_valid_login_urls": [["client_id", "app_id"]],
        "exclude_url_starts_with": ["facebook."],
        "extra_texts": []
    },
    "Apple": {
        "name": "Apple",
        "valid_login_urls": ["https://appleid.apple.com/"],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["apple.", "appleid.apple.", "secure.apple.", "secure2.apple.",
                                    "secure2.store.apple."],
        "extra_texts": []
    }
}
