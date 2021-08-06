from matches import SiegeMatch
import pandas as pd 
import unittest
import json 


class TestSiegeMatch(unittest.TestCase):
    def test_json_export_match(self):
        sg_match_object = SiegeMatch('6124-japan-league-apac-sengoku-vs-guts-gaming')
        self.assertIsInstance(sg_match_object.get_match_log(export='json'), str)

    def test_json_export_stat(self):
        sg_match_object = SiegeMatch('6124-japan-league-apac-sengoku-vs-guts-gaming')
        self.assertIsInstance(sg_match_object.get_player_stats(export='json'), str)

if __name__ == "__main__":
    unittest.main()