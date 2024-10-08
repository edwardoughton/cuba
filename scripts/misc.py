"""


"""
import os
import pandas as pd
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']


def find_country_list(continent_list):
    """
    This function produces country information by continent.
    Parameters
    ----------
    continent_list : list
        Contains the name of the desired continent, e.g. ['Africa']
    Returns
    -------
    countries : list of dicts
        Contains all desired country information for countries in
        the stated continent.
    """
    glob_info_path = os.path.join(BASE_PATH, 'global_information.csv')
    countries = pd.read_csv(glob_info_path, encoding = "ISO-8859-1")

    if len(continent_list) > 0:
        data = countries.loc[countries['continent'].isin(continent_list)]
    else:
        data = countries

    output = []

    for index, country in data.iterrows():

        # if not country['iso3'] == 'CAN':
        #     continue
        if country['ignore'] == 1:
            continue
        
        # if country['iea_classification'] == 'North America':
        #     iea_classification = 'NA'
        # else:
        #     iea_classification = country['iea_classification']

        output.append({
            'country_name': country['country'],
            'iso3': country['iso3'],
            'iso2': country['iso2'],
            'regional_level': country['gid_region'],
            'continent2': country['continent2'],
            'income': country['income'],
            'wb_region': country['wb_region'],
            'adb_region': country['adb_region'],
            'iea_classification': country['iea_classification'],
            'operators': country['operators'],
            # 'subs_growth_low': float(country['subs_growth_low']),
            # 'subs_growth_baseline': float(country['subs_growth_baseline']),
            # 'subs_growth_high': float(country['subs_growth_high']),
            # 'smartphone_penetration': float(country['smartphone_penetration']),
            # 'sp_growth_low': float(country['sp_growth_low']),
            # 'sp_growth_baseline': float(country['sp_growth_baseline']),
            # 'sp_growth_high': float(country['sp_growth_high']),
            # 'backhaul_fiber_perc': int(country['backhaul_fiber_perc']),
        })

    return output
