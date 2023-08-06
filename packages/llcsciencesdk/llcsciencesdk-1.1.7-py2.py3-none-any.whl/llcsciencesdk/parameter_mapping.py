new_and_old_parameter_mapping = {
    "BEFD": "ratio_Sh2St",
    "CF": "cnc_CWd",
    "max_dRdsCr_dt": "max_d_RdsCn_dt",
    "max_RdsCr": "max_RdsCn",
    "MxCAI": "max_CAI",
    "R": "ratio_Rt2Sh",
    "WD": "dns_Wd",
    "C_CncWd": "cnc_CWd",
    "DnsWd": "dns_Wd",
    "max_dVlmSt_dt": "max_d_VlmSt_dt",
    "Mrt1": "mrt_default_1",
    "ratio_St2Sh": "ratio_Sh2St",
    "SelfThin0": "mrt_selfthin_1",
    "SelfThin1": "mrt_selfthin_2",
}

old_and_new_parameters_mapping = {
    'ratio_Sh2St': 'BEFD',
    'cnc_CWd': 'CF',
    'max_d_RdsCn_dt': 'max_dRdsCr_dt',
    'max_RdsCn': 'max_RdsCr',
    'max_CAI': 'MxCAI',
    'ratio_Rt2Sh': 'R',
    'dns_Wd': 'WD',
    'max_d_VlmSt_dt': 'max_d_VlmSt_dt',
    'mrt_default_1': 'Mrt1',
    'mrt_selfthin_1': 'SelfThin0',
    'mrt_selfthin_2': 'SelfThin1'
}


def update_legacy_parameter(parameter_name):
    if parameter_name in old_and_new_parameters_mapping.keys():
        return old_and_new_parameters_mapping[parameter_name]
    else:
        return parameter_name
