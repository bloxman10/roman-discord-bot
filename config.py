import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
APPLICATION_CATEGORY_ID = int(os.getenv("APPLICATION_CATEGORY_ID"))
APPLICATION_STAFF_ROLE_ID = int(os.getenv("APPLICATION_STAFF_ROLE_ID"))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID"))
EMBASSY_CATEGORY_ID = int(os.getenv("EMBASSY_CATEGORY_ID"))
EMBASSY_STAFF_ROLE_ID = int(os.getenv("EMBASSY_STAFF_ROLE_ID"))