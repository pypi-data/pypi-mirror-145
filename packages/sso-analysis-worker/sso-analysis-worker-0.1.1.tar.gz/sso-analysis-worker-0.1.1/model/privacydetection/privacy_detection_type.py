from enum import Enum


class PrivacyDetectionType(Enum):
    NO_CONSENT_GIVEN = 1,
    CONSENT_GIVEN = 2,
    CONSENT_GIVEN_INTERACTION = 3
