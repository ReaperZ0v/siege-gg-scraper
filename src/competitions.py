from bs4 import BeautifulSoup
import pandas as pd 
import requests
import json 


class SiegeCompetition:
    def __init__(self, league_id):
        """
        [the competition league to get insights/data scraped from]
        Args:
            league_id ([str]): [example: 318-polish-masters-2021]
        """
        self.league_id = league_id.lower()
        self.match_page_resp = requests.get(f"https://siege.gg/competitions/{self.league_id}")
        self.soup_object = BeautifulSoup(self.match_page_resp.text, "lxml")

    def participating_teams(self):
        return pd.Series([
            team.text.strip() for team in self.soup_object.find_all("div", class_="col-6 col-md-4 col-lg-3 px-2 mb-3 col--has-trunk overflow-visible")
        ])

    



