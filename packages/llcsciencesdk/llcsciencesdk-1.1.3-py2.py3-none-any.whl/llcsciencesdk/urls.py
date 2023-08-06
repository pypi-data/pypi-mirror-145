from collections import namedtuple

ApiUrls = namedtuple(
    "ApiUrls",
    [
        "AUTH_URL",
        "GET_MODEL_INPUT_URL",
        "GET_OLD_MODEL_INPUT_URL",
        "GET_MODEL_INPUT_FAST_TRACK",
        "GET_MODEL_INPUT_CALIBRATE_FAST_TRACK",
        "GET_MODEL_INPUT_DENSITY_ANALYSES_FAST_TRACK",
        "GET_PLANTING_DESIGN_DETAIL",
        "GET_PLANTING_DESIGN_LIST",
    ],
)


def make_urls(environment):
    BASE_API_URL = "https://internal-landlifecompany.appspot.com"

    if environment == "staging":
        BASE_API_URL = "https://staging-dot-internal-landlifecompany.ue.r.appspot.com"

    if environment == "local":
        BASE_API_URL = "http://127.0.0.1:8000"

    return ApiUrls(
        AUTH_URL=f"{BASE_API_URL}/api/v1/token/",
        GET_MODEL_INPUT_FAST_TRACK=f"{BASE_API_URL}/sciencemodel/fasttrackinput/model_input_fast_track/",
        GET_MODEL_INPUT_CALIBRATE_FAST_TRACK=f"{BASE_API_URL}/sciencemodel/fasttrackinput/model_input_calibrate_fast_track/",
        GET_MODEL_INPUT_DENSITY_ANALYSES_FAST_TRACK=f"{BASE_API_URL}/sciencemodel/fasttrackinput/model_input_density_analyses_fast_track/",
        GET_PLANTING_DESIGN_DETAIL=f"{BASE_API_URL}/plantingdesign/api/detail/",
        GET_PLANTING_DESIGN_LIST=f"{BASE_API_URL}/plantingdesign/api/list",
        # START LEGACY ENDPOINTS -----------
        GET_MODEL_INPUT_URL=f"{BASE_API_URL}/sciencemodel/fasttrackinput/planting_design_config/",
        GET_OLD_MODEL_INPUT_URL=f"{BASE_API_URL}/api/v1/llcmodel/model_input?model_run_ids"
        # END LEGACY ENDPOINTS -------------
    )
