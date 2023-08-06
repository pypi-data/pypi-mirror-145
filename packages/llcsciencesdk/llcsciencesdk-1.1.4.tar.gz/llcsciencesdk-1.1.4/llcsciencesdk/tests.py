import unittest
from llcsciencesdk.llc_api import ScienceSdk

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"


class TestAPI(unittest.TestCase):
    """
    Very primitive test case. You need to provide a USERNAME and PASSWORD in order to run. It is meant as a quick
    sanity check when refactoring. Need to develop more robust testing as this grows.
    """

    def setUp(self):
        self.llc_api = ScienceSdk(environment="production")
        self.llc_api.login(USERNAME, PASSWORD)

    def test_api(self):
        """
        Very basic test.
        """
        self.assertIsInstance(self.llc_api.get_model_input_fast_track_json(46), dict)
        self.assertIsInstance(self.llc_api.get_model_input_fast_track(46), dict)
        self.assertIsInstance(self.llc_api.get_model_input_calibrate_fast_track_json(46), dict)
        self.assertIsInstance(self.llc_api.get_model_input_calibrate_fast_track(46), dict)
        self.assertIsInstance(self.llc_api.get_model_input_density_analyses_fast_track_json(46), dict)
        self.assertIsInstance(self.llc_api.get_model_input_density_analyses_fast_track(46), dict)
        self.assertIsInstance(self.llc_api.get_model_inputs_as_df(46), tuple)
        self.assertIsInstance(self.llc_api.get_planting_design_detail(10), dict)
        self.assertIsInstance(self.llc_api.get_planting_design_list(), list)
