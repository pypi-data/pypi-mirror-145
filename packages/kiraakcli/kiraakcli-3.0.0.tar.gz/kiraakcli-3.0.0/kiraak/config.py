"""Initializes configuration variables for the project"""
import json
import logging
import os
import pathlib
import platform
from getpass import getpass

import requests
import urllib3
# from dotenv import load_dotenv
from rich.logging import RichHandler

# load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)
logging.captureWarnings(True)

# Set up project wide request session
session = requests.Session()
session.verify = False

FLAT_RE = r"^(?P<block>[A-N])( |-)?(?P<flat>((0?[1-9]0|1[0-2]0|1[5-9]0|200|14A|14B)[1-4]))$"


class Auth:
    """Class for the configurations of the app"""

    if platform.system() in ["Linux", "Darwin"]:
        CONF_FILE = pathlib.Path(os.path.expanduser("~/.config/kiraakapi/conf.json"))
    else:
        CONF_FILE = pathlib.Path(os.path.expandvars("%APPDATA%/kiraakapi/conf.json"))
    if CONF_FILE.exists():
        with CONF_FILE.open("r") as f:
            data = json.load(f)
        WOOCOMMERCE_CONSUMER_KEY = data.get("WOOCOMMERCE_CONSUMER_KEY")
        WOOCOMMERCE_CONSUMER_SECRET = data.get("WOOCOMMERCE_CONSUMER_SECRET")
        MOBILE, PASSWORD = data.get("mobile"), data.get("password")
    else:
        MOBILE = input("Enter your mobile number: ")
        PASSWORD = getpass("Enter your password: ")
        WOOCOMMERCE_CONSUMER_KEY = input("Enter your Woocommerce API Consumer Key: ")
        WOOCOMMERCE_CONSUMER_SECRET = input(
            "Enter your Woocommerce API Consumer Secret: "
        )
        CONF_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONF_FILE.touch()
        with open(CONF_FILE, "w+") as f:
            json.dump(
                {
                    "mobile": MOBILE,
                    "password": PASSWORD,
                    "WOOCOMMERCE_CONSUMER_KEY": WOOCOMMERCE_CONSUMER_KEY,
                    "WOOCOMMERCE_CONSUMER_SECRET": WOOCOMMERCE_CONSUMER_SECRET,
                },
                f,
            )


class API:
    """Class for constant API routes"""

    LOGIN = "https://kiraak.tech/api/partner/login"
    CUSTOMERS = "https://kiraak.tech/api/partner/viewMyCustomers"
    ACTIVE_ANALYTICS = "https://kiraak.tech/api/partner/getActiveAnalytics"
    MONTHLY_ANALYTICS = "https://kiraak.tech/api/partner/getMonthlyAnalytics"
    SUMMARY_ANALYTICS = "https://kiraak.tech/api/partner/getSummaryAnalytics"
    CATALOG = (
        "https://kiraak.tech/api/admin/getActicePriceList"  # Misspelled on purpose
    )
    ACTIVE_ORDERS = (
        "https://kiraak.tech/api/partner/getAllCustomerOrdersByStatus/active"
    )
    ADD_CUSTOMER = "https://kiraak.tech/api/partner/createCustomer"
    CUSTOMER_DATA = "https://kiraak.tech/api/partner/viewCustomer/{id}"
    CUSTOMER_ACTIVE_ORDER = (
        "https://kiraak.tech/api/partner/viewCustomerActiveOrder/{id}/regular"
    )
    CANCEL_ORDER = "https://kiraak.tech/api/psartner/updateOrderStatus/{id}"
    ADD_ORDER = "https://kiraak.tech/api/partner/createOrder"
    UPDATE_ORDER = "https://kiraak.tech/api/partner/updateOrder/{id}"

    if platform.system() in ["Linux", "Darwin"]:
        TOKEN_FILE = pathlib.Path(os.path.expanduser("~/.config/kiraakapi/auth.json"))
    else:
        TOKEN_FILE = pathlib.Path(
            os.path.expandvars("%APPDATA%/Roaming/kiraakapi/auth.json")
        )
    if not TOKEN_FILE.exists():
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.touch()
