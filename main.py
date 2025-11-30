import json
from jinja2 import Template
import os

from src.api.gmail import send_html
from src.api.basketball_reference import BBRefAPI
from src.preprocess.preprocess import get_top_k_players


# Load config
with open("config.json", "r") as f:
    config = json.load(f)

with open("utils/tm_map.json", "r") as f:
    tm_map = json.load(f)

# Initialize Basketball Reference API
bbref_api = BBRefAPI()
stats = bbref_api.get_table("leagues/NBA_2026_per_game.html")
stats = stats[stats["Team"] == config["favorite_team"]]

top_5_scorers = get_top_k_players(stats, "PTS", 5)


data = {
    "top_5_scorers": top_5_scorers,
}

with open("templates/email.html") as f:
    email_template = Template(f.read())

report_html = email_template.render(
    team_name=tm_map[config["favorite_team"]],
    top_5_scorers_table=top_5_scorers.to_html(index=False, border=0),
)

os.makedirs("outputs", exist_ok=True)
with open("outputs/report.html", "w") as f:
    f.write(report_html)
