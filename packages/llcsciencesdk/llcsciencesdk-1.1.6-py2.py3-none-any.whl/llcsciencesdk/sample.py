from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk(environment="production")
llc_api.login("username", "password")

# model_input = llc_api.get_model_input_fast_track_json(46)
# model_input = llc_api.get_model_input_fast_track(46)
# model_input = llc_api.get_model_input_calibrate_fast_track_json(46)
# model_input = llc_api.get_model_input_calibrate_fast_track(46)
# model_input = llc_api.get_model_input_density_analyses_fast_track_json(46)
# model_input = llc_api.get_model_input_density_analyses_fast_track_json(46)
# model_input = llc_api.get_model_inputs_as_df(46, legacy_parameters=True)
planting_detail = llc_api.get_planting_design_detail(10)
planting_list = llc_api.get_planting_design_list()
