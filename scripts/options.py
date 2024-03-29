"""
Options consisting of scenarios and strategies.

Country parameters consist of those parameters which are specific
to each country.

Written by Ed Oughton, based on work from the pytal and podis repositories.

April 2021

#strategy is defined based on generation_core_backhaul_sharing_networks_spectrum_tax_power

generation: technology generation, so 3G or 4G
core: type of core data transport network, eg. evolved packet core (4G)
backhaul: type of backhaul, so fiber or wireless
sharing: the type of infrastructure sharing, active, passive etc..
network: relates to the number of networks, as defined in country parameters
spectrum: type of spectrum strategy, so baseline, high or low
tax: type of taxation strategy, so baseline, high or low

"""


def generate_tech_options():
    """
    Generate technology strategy options.

    """
    output = []

    scenarios = [
                'low_40_40_40', 'baseline_40_40_40','high_40_40_40',
                'low_30_30_30','baseline_30_30_30', 'high_30_30_30',
                'low_20_20_20', 'baseline_20_20_20', 'high_20_20_20',
                ]
    generation_core_types = ['4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline']
    networks_types = ['baseline']
    spectrum_types = ['baseline']
    tax_types = ['baseline']
    power_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    for power in power_types:
                                        strategy = '{}_{}_{}_{}_{}_{}_{}'.format(
                                            generation_core_type,
                                            backhaul,
                                            sharing,
                                            network,
                                            spectrum,
                                            tax,
                                            power
                                        )
                                        output.append({
                                            'scenario': scenario,
                                            'strategy': strategy
                                        })

    return output


def generate_business_model_options():
    """
    Generate business model strategy options.

    """
    output = []

    scenarios = [
                'low_40_40_40', 'baseline_40_40_40', 'high_40_40_40',
                'low_30_30_30', 'baseline_30_30_30', 'high_30_30_30',
                'low_20_20_20', 'baseline_20_20_20', 'high_20_20_20',
                ]
    generation_core_types = ['4G_epc']
    backhaul_types = ['wireless']
    sharing_types = ['baseline', 'passive', 'active', 'srn']
    networks_types = ['baseline']
    spectrum_types = ['baseline']
    tax_types = ['baseline']
    power_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    for power in power_types:
                                        strategy = '{}_{}_{}_{}_{}_{}_{}'.format(
                                            generation_core_type,
                                            backhaul,
                                            sharing,
                                            network,
                                            spectrum,
                                            tax,
                                            power
                                        )
                                        output.append({
                                            'scenario': scenario,
                                            'strategy': strategy
                                        })

    return output


def generate_policy_options():
    """
    Generate policy strategy options.

    """
    output = []

    scenarios = ['low_40_40_40', 'baseline_40_40_40','high_40_40_40',
                'low_30_30_30', 'baseline_30_30_30','high_30_30_30',
                'low_20_20_20', 'baseline_20_20_20', 'high_20_20_20',
                ]
    generation_core_types = ['4G_epc']
    backhaul_types = ['wireless']
    sharing_types = ['baseline']
    networks_types = ['baseline']
    spectrum_types = ['baseline', 'low', 'high']
    tax_types = ['baseline', 'low', 'high']
    power_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    for power in power_types:
                                        strategy = '{}_{}_{}_{}_{}_{}_{}'.format(
                                            generation_core_type,
                                            backhaul,
                                            sharing,
                                            network,
                                            spectrum,
                                            tax,
                                            power
                                        )
                                        output.append({
                                            'scenario': scenario,
                                            'strategy': strategy
                                        })

    return output


def generate_mixed_options():
    """
    Generate policy strategy options.

    """
    output = []

    scenarios = ['low_40_40_40', 'baseline_40_40_40','high_40_40_40',
                'low_30_30_30', 'baseline_30_30_30','high_30_30_30',
                'low_20_20_20', 'baseline_20_20_20', 'high_20_20_20',
                ]
    generation_core_types = ['4G_epc']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline', 'srn']
    networks_types = ['baseline']
    spectrum_types = ['baseline', 'low']
    tax_types = ['baseline', 'low']
    power_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    for power in power_types:
                                        strategy = '{}_{}_{}_{}_{}_{}_{}'.format(
                                            generation_core_type,
                                            backhaul,
                                            sharing,
                                            network,
                                            spectrum,
                                            tax,
                                            power
                                        )
                                        output.append({
                                            'scenario': scenario,
                                            'strategy': strategy
                                        })

    return output


def generate_power_options():
    """
    Generate energy strategy options.

    """
    output = []

    scenarios = ['low_40_40_40', 'baseline_40_40_40','high_40_40_40',
                'low_30_30_30', 'baseline_30_30_30','high_30_30_30',
                'low_20_20_20', 'baseline_20_20_20', 'high_20_20_20',
                ]
    generation_core_types = ['4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline']
    networks_types = ['baseline']
    spectrum_types = ['baseline']
    tax_types = ['baseline']
    power_types = ['baseline', 'renewable']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    for power in power_types:
                                        strategy = '{}_{}_{}_{}_{}_{}_{}'.format(
                                            generation_core_type,
                                            backhaul,
                                            sharing,
                                            network,
                                            spectrum,
                                            tax,
                                            power
                                        )
                                        output.append({
                                            'scenario': scenario,
                                            'strategy': strategy
                                        })

    return output


def business_model_power_options():
    """
    Generate energy strategy options.

    """
    output = []

    scenarios = ['low_40_40_40', 'baseline_40_40_40','high_40_40_40',
                'low_30_30_30', 'baseline_30_30_30','high_30_30_30',
                'low_20_20_20', 'baseline_20_20_20', 'high_20_20_20',
                ]
    generation_core_types = ['4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline', 'passive', 'active', 'srn']
    networks_types = ['baseline']
    spectrum_types = ['baseline']
    tax_types = ['baseline']
    power_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    for power in power_types:
                                        strategy = '{}_{}_{}_{}_{}_{}_{}'.format(
                                            generation_core_type,
                                            backhaul,
                                            sharing,
                                            network,
                                            spectrum,
                                            tax,
                                            power
                                        )
                                        output.append({
                                            'scenario': scenario,
                                            'strategy': strategy
                                        })

    return output


OPTIONS = {
    'technology_options': generate_tech_options(),
    'business_model_options': generate_business_model_options(),
    'policy_options': generate_policy_options(),
    'mixed_options': generate_mixed_options(),
    'power_options': generate_power_options(),
    'business_model_power_options': business_model_power_options(),
}


COSTS = {
    #all costs in $USD
    'equipment': 40000,
    'site_build': 30000,
    'installation': 30000,
    'operation_and_maintenance': 7400,
    'power': 3000,
    'site_rental_urban': 10000,
    'site_rental_suburban': 5000,
    'site_rental_rural': 3000,
    'fiber_urban_m': 20,
    'fiber_suburban_m': 12,
    'fiber_rural_m': 7,
    'wireless_small': 40000,
    'wireless_medium': 40000,
    'wireless_large': 80000,
}


GLOBAL_PARAMETERS = {
    'traffic_in_the_busy_hour_perc': 20,
    'return_period': 10,
    'discount_rate': 5,
    'opex_percentage_of_capex': 10,
    'core_perc_of_ran': 10,
    'confidence': [50],
    'tdd_dl_to_ul': '80:20',
    }


INFRA_SHARING_ASSETS = {
    'baseline': [],
    'passive': [
        'site_build',
        'installation',
        'site_rental',
        'backhaul',
        'backhaul_fiber_urban_m',
        'backhaul_fiber_suburban_m',
        'backhaul_fiber_rural_m',
        'backhaul_wireless_small',
        'backhaul_wireless_medium',
        'backhaul_wireless_large',
    ],
    'active': [
        'equipment',
        'site_build',
        'installation',
        'site_rental',
        'operation_and_maintenance',
        'power',
        'backhaul',
        'backhaul_fiber_urban_m',
        'backhaul_fiber_suburban_m',
        'backhaul_fiber_rural_m',
        'backhaul_wireless_small',
        'backhaul_wireless_medium',
        'backhaul_wireless_large',
    ],
    'srn': [
        'equipment',
        'site_build',
        'installation',
        'site_rental',
        'operation_and_maintenance',
        'power',
        'backhaul',
        'backhaul_fiber_urban_m',
        'backhaul_fiber_suburban_m',
        'backhaul_fiber_rural_m',
        'backhaul_wireless_small',
        'backhaul_wireless_medium',
        'backhaul_wireless_large',
    ],
}


COST_TYPES = {
    'equipment': 'capex',
    'site_build': 'capex',
    'installation': 'capex',
    'site_rental': 'opex',
    'site_rental_urban': 'opex',
    'site_rental_suburban': 'opex',
    'site_rental_rural': 'opex',
    'operation_and_maintenance': 'opex',
    'backhaul': 'capex_and_opex',
    'backhaul_fiber_urban_m': 'capex_and_opex',
    'backhaul_fiber_suburban_m': 'capex_and_opex',
    'backhaul_fiber_rural_m': 'capex_and_opex',
    'backhaul_wireless_small': 'capex_and_opex',
    'backhaul_wireless_medium': 'capex_and_opex',
    'backhaul_wireless_large': 'capex_and_opex',
    'regional_node': 'capex_and_opex',
    'regional_edge': 'capex_and_opex',
    'core_node': 'capex_and_opex',
    'core_edge': 'capex_and_opex',
}


ENERGY_DEMAND = {
    #all values in kwh per hour
    #roughly 5 kwh per site
    'equipment_kwh': 0.249,
    'wireless_small_kwh': .06, 
    'wireless_medium_kwh': .06,
    'wireless_large_kwh': .06,
    'core_node_kwh': 0,
    'regional_node_kwh': 0,
    #https://blog.wirelessmoves.com/2019/08/cell-site-power-consumption.html
    #https://www.gsma.com/mobilefordevelopment/wp-content/uploads/2015/01/140617-GSMA-report-draft-vF-KR-v7.pdf
}


TECH_LUT = {
    'oil': {
        'carbon_per_kWh': 0.5, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.00009, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.007, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.002, #kgs of PM10 per kWh
    },
    'gas': {
        'carbon_per_kWh': 0.5, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.00009, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.007, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.002, #kgs of PM10 per kWh
    },
    'coal': {
        'carbon_per_kWh': 1, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.0001, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.01, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.01, #kgs of PM10 per kWh
    },
    'nuclear': {
        'carbon_per_kWh': 0.5, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.00009, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.007, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.002, #kgs of PM10 per kWh
    },
    'hydro': {
        'carbon_per_kWh': 0.01, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.0000009, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.00007, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.00002, #kgs of PM10 per kWh
    },
    'diesel': {
        'carbon_per_kWh': 0.5, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.00009, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.007, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.002, #kgs of PM10 per kWh
    },
    'renewables': {
        'carbon_per_kWh': 0.1, #kgs of carbon per kWh
        'nitrogen_oxide_per_kWh':0.000001, #kgs of nitrogen oxide (NOx) per kWh
        'sulpher_dioxide_per_kWh': 0.0001, #kgs of sulpher dioxide (SO2) per kWh
        'pm10_per_kWh': 0.00001, #kgs of PM10 per kWh
    }
}
