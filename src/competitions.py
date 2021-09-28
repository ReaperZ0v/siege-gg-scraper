from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd 
import requests
import json 
import os 


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

    def map_picks(self, export='dataframe'):
        map_frame = {
            "map": [map.text.strip() for map in self.soup_object.find_all("h4", class_="map__name my-0 mr-4")],
            "rounds": [round.text.strip() for round in self.soup_object.find_all("strong", class_="ml-auto text-center")]
        }

        if export == 'dataframe':
            return pd.DataFrame(map_frame)

        elif export == "csv":
            if os.path.exists("exports"):
                self.fetch_log()[0].to_csv(f"exports/map_export_{datetime.now()}.csv")
                return True

            else:
                os.mkdir("exports")
                self.fetch_log()[0].to_csv(f"exports/map_export_{datetime.now()}.csv")
                return True 

        elif export == 'json':
            return json.dumps(pd.DataFrame(map_frame), indent=4)


sgcomp = SiegeCompetition("318-polish-masters-2021")
sgcomp.map_picks()



    



