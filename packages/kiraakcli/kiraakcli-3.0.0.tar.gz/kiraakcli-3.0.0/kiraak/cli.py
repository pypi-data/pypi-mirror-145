"""Main CLI application"""
import json

import click

from kiraak.config import API, Auth
from kiraak.main import main
from kiraak.get_catalog import download_catalog
from kiraak import VERSION
import kiraak.sync

@click.group()
@click.version_option(VERSION)
def cli():
    """Kiraak CLI"""

@cli.command()
def add() -> None:
    """Add orders using the Kiraak API"""
    main()

@cli.command()
def clear() -> None:
    "Clear login data and credentials"
    Auth.CONF_FILE.unlink()
    API.TOKEN_FILE.unlink()

@cli.command()
def catalog() -> None:
    "Download the current catalog from Kiraak"
    download_catalog()

@cli.command()
@click.option("--once", is_flag=True)
@click.option("--time-gap", default=300, type=int)
def sync(once, time_gap) -> None:
    """Synchronizes the catalog"""
    kiraak.sync.main(once, time_gap)
    