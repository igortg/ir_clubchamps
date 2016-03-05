#-*- coding: utf8
from __future__ import unicode_literals
from collections import namedtuple
import click
from irclub.irclubstats import ClubStats, unquote_string
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('irclub', 'templates'))


Driver = namedtuple("Driver", ["name", "position", "points"])
clubstats = ClubStats()


@click.command()
@click.option("--user", prompt="Username")
@click.password_option(confirmation_prompt=False)
def fetch(user, password):
    clubstats.login(user, password)

    champs = [
        "Blancpain Sprint Series",
        "NASCAR iRacing Class A Fixed",
        "NASCAR iRacing Class C Fixed",
    ]

    standings_list = [fetch_drivers(champ) for champ in champs]
    template = env.get_template("cover.html")

    with open("cover.html", "w") as cover_file:
        cover_file.write(template.render(standings_list=standings_list))


def fetch_drivers(series_name):
    drivers_data = clubstats.fetch_season_standings(series_name, "Brazil")
    drivers = []
    for data in drivers_data:
        driver = Driver(
            name=unquote_string(data["displayname"]),
            position=data["pos"],
            points=data["points"]
        )
        drivers.append(driver)
    return drivers


fetch()