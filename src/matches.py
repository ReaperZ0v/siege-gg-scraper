from bs4 import BeautifulSoup
from datetime import date, datetime
import pandas as pd 
import requests
import json 
import sys
import os 


class SiegeMatch:
    def __init__(self, match_id):
        """
        [the match to get insights/data scraped from]
        Args:
            match_id ([str]): [example: 6124-japan-league-apac-sengoku-vs-guts-gaming]
        """
        self.match_id = match_id.lower()
        self.match_page_resp = requests.get(f"https://siege.gg/matches/{self.match_id}")
        self.soup_object = BeautifulSoup(self.match_page_resp.text, "lxml")

    def remove_non(self, val):
        if val is None:
            return 'No Further Data'

        else:
            return val 

    def fetch_log(self):
        match_log_pre_frame = {
            "round": [rnd.text.strip() for rnd in self.soup_object.find_all("li", class_="log__line log__line--round")],
            "multi_kill_attack": [mk.text.strip() for mk in self.soup_object.find_all("li", class_="log__line log__line--multikill log__line--attack")],
            "multi_kill_defend": [dfd.text.strip() for dfd in self.soup_object.find_all("li", class_="log__line log__line--multikill log__line--defend")],
            "plant": [pl.text.strip() for pl in self.soup_object.find_all("li", class_="log__line log__line--plant log__line--attack")],
            "result": [res.text.strip() for res in self.soup_object.find_all("li", class_="log__line log__line--plant log__line--attack")]
        }

        data_frame = pd.DataFrame.from_dict(match_log_pre_frame, orient='index').T
        for col_ in data_frame.columns:
            data_frame[col_] = data_frame[col_].apply(self.remove_non)
        
        return (data_frame, match_log_pre_frame)

    def get_match_log(self, export='dataframe'):
        """[Scrape the entier game log of a match]

        Args:
            export (str, optional): [dataframe, csv, json]. Defaults to 'dataframe'.
        """
        if export == 'dataframe':
            return self.fetch_log()

        elif export == 'csv':
            if os.path.exists("exports"):
                self.fetch_log()[0].to_csv(f"exports/log_export_{datetime.now()}.csv")
                return True

            else:
                os.mkdir("exports")
                self.fetch_log()[0].to_csv(f"exports/log_export_{datetime.now()}.csv")
                return True 

        elif export == 'json':
            return json.dumps(self.fetch_log()[1], indent=4)

    def get_player_stats(self, export='dataframe'):
        clean_kill_ratio = lambda val: val.replace(val[5:], "").split('-')[0]
        clean_death_ratio = lambda val: val.replace(val[5:], "").split('-')[1]

        stats_pre_frame = {
            "name": [n.text.strip() for n in self.soup_object.find_all("td", class_="team--a sp__player js-heatmap-ignore")],
            "rating": [r.text.strip() for r in self.soup_object.find_all("td", class_="sp__rating")],
            "K/D_ratio": [kd.text.strip() for kd in self.soup_object.find_all("td", class_="sp__kills text-nowrap")],
            "entry": [en.text.strip() for en in self.soup_object.find_all("td", class_="sp__ok text-nowrap")],
            "plant": [pl.text.strip() for pl in self.soup_object.find_all("td", class_="sp__plant")]
        }
        stats_dataframe = pd.DataFrame(stats_pre_frame)

        stats_dataframe['kills'] = stats_dataframe["K/D_ratio"].apply(clean_kill_ratio)
        stats_dataframe['deaths'] = stats_dataframe["K/D_ratio"].apply(clean_death_ratio)

        stats_dataframe.drop("K/D_ratio", axis=1, inplace=True)

        if export == 'dataframe':
            return stats_dataframe

        elif export == "csv":
            if os.path.exists("exports"):
                self.fetch_log()[0].to_csv(f"exports/stats_export_{datetime.now()}.csv")
                return True

            else:
                os.mkdir("exports")
                self.fetch_log()[0].to_csv(f"exports/stats_export_{datetime.now()}.csv")
                return True 

        elif export == 'json':
            return json.dumps(stats_pre_frame, indent=4)
            



        

