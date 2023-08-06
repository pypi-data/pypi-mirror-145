"""Main CLI for advent-of-code helper tool"""
from typing import List

import click

from .cache_file import delete_input
from .config_file import add_to_json, delete_from_json, get_all_session, list_from_json
from .server_action import download_input
from .utils import get_current_year, get_day


@click.group(help="CLI tool to perform action related to advent-of-code")
def main():
    pass


@main.group(help="perform action related to config file")
def config():
    pass


@config.command(help="add session to config")
@click.argument("name")
@click.argument("session_value")
def add(name: str, session_value: str):
    data_list = {name: session_value}
    add_to_json(**data_list)


@config.command("list", help="list all session present in config")
def list_config_session():
    list_from_json()


@config.command("remove", help="remove session from config")
@click.argument("name")
def remove_config_data(name: str):
    delete_from_json(name)


@main.command(help="download solution from advent-of-code server")
@click.option(
    "--year",
    "-y",
    "years",
    multiple=True,
    help="Pass input download year [default: latest year of problem]",
)
@click.option(
    "--day",
    "-d",
    "days",
    multiple=True,
    help="Pass input download day [default: latest problem day or day 1 of old year]",
)
@click.option(
    "--session",
    "-s",
    "sessions",
    multiple=True,
    help="Pass session name or use all session as default",
)
def download(years: List[int], days: List[int], sessions: List[int]):
    if not years:
        years = [get_current_year()]
    if not days:
        days = [get_day()]
    if not sessions:
        sessions = get_all_session()
    for year in years:
        for day in days:
            for session in sessions:
                download_input(year, day, session)


@main.command("remove", help="delete a input file from cache folder")
@click.option(
    "--year",
    "-y",
    "years",
    multiple=True,
    help="Year from which input is to be delete default all",
)
@click.option(
    "--day",
    "-d",
    "days",
    multiple=True,
    help="Day from which input file is to be delete default all day",
)
@click.option(
    "--session",
    "-s",
    "sessions",
    multiple=True,
    help="Session from which input file is to be deleted default all session",
)
def remove_cache(years: List[int], days: List[int], sessions: List[int]):
    if not years:
        years = list(range(2015, get_current_year() + 1))
    if not days:
        days = list(range(1, 26))
    if not sessions:
        sessions = get_all_session()
    for year in years:
        for day in days:
            for session in sessions:
                delete_input(year, day, session)
