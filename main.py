import os
import sys
import urllib
import click
from ir_webstats.client import iRWebStats

irw = iRWebStats()


@click.command()
@click.argument("club")
@click.argument("year", type=int)
@click.option("--quarter", type=int)
@click.option("--tops", default=3, type=int)
@click.option("--user", prompt="Username")
@click.password_option(confirmation_prompt=False)
def ir_clubchamp(club, year, quarter=None, tops=3, user=None, password=None):
    if hasattr(sys, "frozen"):
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.path.dirname(sys.executable), "cacert.pem")
    irw.login(user, password)
    if not irw.logged:
        click.echo (
            "Couldn't log in to iRacing Membersite. Please check your credentials")
    else:
        champs = acquire_champ_list(club, year, quarter, tops)
        print_champs(champs)


def acquire_champ_list(club, year, quarter=None, tops=3):
    champs = []
    for club_id in irw.CLUBS:
        if irw.CLUBS[club_id]["shortclubname"] == club:
            club_id = irw.CLUBS[club_id]["id"]
            break
    else:
        raise KeyError("Club ID not found for {}".format(club))

    seasons2process = irw.all_seasons()
    if year:
        seasons2process = [s for s in seasons2process if s["year"] == year]
    if quarter:
        seasons2process = [s for s in seasons2process if s["quarter"] == quarter]
    with click.progressbar(seasons2process, label="Requesting Series Stats") as seasons:
        for season in seasons:
            if not season["isOfficial"]:
                continue
            for carclass in season["carclasses"]:
                class_id = int(carclass["id"])
                if class_id in [0]:
                    continue
#                click.echo("Getting results for {} ({})".format(season["seriesshortname"], season["seasonid"]))
                try:
                    resp = irw.season_standings(season["seasonid"], class_id)
                except Exception as exc:
#                    click.echo("- Error {}".format(exc))
                    continue
                standings = resp[0]
                for i, driver in enumerate(standings[:tops]):
                    if driver["clubid"] == club_id:
                        pos = i+1
                        champs.append((pos, driver, season, carclass))
    return champs


def print_champs(champs):
    seasons = {}
    for champ in champs:
        seasonchamps = seasons.setdefault(champ[2]["seasonshortname"], [])
        seasonchamps.append(champ)
    for season_name in sorted(seasons):
        click.echo(season_name)
        seasonchamps = seasons[season_name]
        for pos, driver, season, carclass in sorted(seasonchamps, key=lambda x: x[0]):
            driver_name = urllib.parse.unquote(driver["displayname"])
            driver_name = driver_name.replace("+", " ")
            if season["multiclass"]:
                series_name = "{} ({})".format(season["seriesname"], carclass["shortname"])
            else:
                series_name = season["seriesname"]
            if pos == 1:
                pos_text = "Champion"
            elif pos == 2:
                pos_text = "2nd Place"
            elif pos == 3:
                pos_text = "3rd Place"
            else:
                pos_text = "{}th Place".format(pos)
            click.echo("{0:28} {1:9} - {2}".format(driver_name, pos_text, series_name))
        click.echo()


if __name__ == '__main__':
    click.echo("= iRacing Club Champions =")
    click.echo()
    ir_clubchamp()