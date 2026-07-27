import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
APPLICATION_CATEGORY_ID = int(os.getenv("APPLICATION_CATEGORY_ID"))
APPLICATION_STAFF_ROLE_ID = int(os.getenv("APPLICATION_STAFF_ROLE_ID"))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID"))
EMBASSY_CATEGORY_ID = int(os.getenv("EMBASSY_CATEGORY_ID"))
EMBASSY_STAFF_ROLE_ID = int(os.getenv("EMBASSY_STAFF_ROLE_ID"))
ERIFY_CHANNEL = os.getenv(
    "VERIFY_CHANNEL"
)

INFO_CHANNEL = os.getenv(
    "INFO_CHANNEL"
)

APPLY_CHANNEL = os.getenv(
    "APPLY_CHANNEL"
)

LOCUTUS_USER = os.getenv(
    "LOCUTUS_USER"
)

FA_CONTACT = os.getenv(
    "FA_CONTACT"
)

WELCOME_LOGO = os.getenv(
    "WELCOME_LOGO"
)

WELCOME_BANNER = os.getenv(
    "WELCOME_BANNER"
)
