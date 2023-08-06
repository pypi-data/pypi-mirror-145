"""Initializes the project"""
from colorama import init
from rich.console import Console

import kiraak.config

from woocommerce import API
from kiraak.config import Auth
# This is the console that helps us print tables, etc.
console = Console()

# Initializes coloring in the terminal
init()

VERSION = "3.0.0"
wc_api = API(
    url="https://rgbsocial.redgreenbluemix.com/",
    consumer_key=Auth.WOOCOMMERCE_CONSUMER_KEY,
    consumer_secret=Auth.WOOCOMMERCE_CONSUMER_SECRET,
    wp_api=True,
    version="wc/v3",
)
