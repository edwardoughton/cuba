import pytest
from cuba.energy import assess_energy#, calc_emissions


def test_assess_energy(setup_region, setup_option, setup_global_parameters,
    setup_country_parameters, setup_timesteps, setup_tech_lut, setup_on_grid_mix):

    setup_region[0]['new_sites'] = 1

    # {'scenario': 'high_25_25_25', 'strategy': '5G_nsa_fiber_baseline_baseline_baseline_baseline_baseline',
    # 'confidence': 50, 'decile': 7, 'asset': 'equipment', 'quantity': 452.5, 'cost_per_unit': 40000,
    # 'total_cost': 18100000.0, 'build_type': 'upgraded', 'ownership': 'mno'}

    regions = [
        {
            'GID_0': 'CHL',
            'GID_id': 'a',
            'geotype': 'urban',
            'decile': 1,
            'population_total': 1000,
            'population_km2': 500,
            'total_sites': 10,
            'total_upgraded_sites': 5,
            'total_new_sites': 5,
            'on_grid_perc': 50,
            'grid_other_perc': 50,
            'phones_on_network': 750,
            'population_with_phones': 1000,
            'phones_on_network_to_total_phones_ratio': 0.75,
        },
    ]

    assets = {1: [
        {
        'scenario': 'low_20_20_20',
        'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        'confidence': 50,
        'GID_id':  'a',
        'asset': 'equipment',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        'scenario': 'low_20_20_20',
        'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        'confidence': 50,
        'GID_id':  'a',
        'asset': 'backhaul_wireless_small',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        'scenario': 'low_20_20_20',
        'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        'confidence': 50,
        'GID_id':  'a',
        'asset': 'backhaul_wireless_medium',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        'scenario': 'low_20_20_20',
        'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        'confidence': 50,
        'GID_id':  'a',
        'asset': 'backhaul_wireless_large',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
    ]
    }

    energy_demand = {
        'equipment_kwh': 1,
        'core_node_kwh': 1,
        'regional_node_kwh': 1,
        'wireless_small_kwh': 1,
        'wireless_medium_kwh': 1,
        'wireless_large_kwh': 1,
    }

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets,
        {'strategy': '3G_epc_wireless_baseline_baseline_baseline_baseline','scenario': 'r'},
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    for item in results:

        if not item == 'new':
            continue

        ##(1*24*365) = 1 kWh*24 hours*365 days with a 50%/50% split of on/off grid power
        assert results[0]['mno_equipment_annual_demand_kWh'] == (1 * 24 * 365) * 0.5
        assert results[0]['mno_wireless_backhaul_annual_demand_kwh'] == (3 * 24 * 365) * 0.5
        assert results[0]['mno_energy_annual_demand_kwh'] == (
            (((1 * 24 * 365) * 0.5)) + (((3 * 24 * 365)) * 0.5)
        )

        assert results[0]['total_equipment_annual_demand_kWh'] == (((1 * 24 * 365) * 0.5) *3)

    regions = [
        {
            'GID_0': 'CHL',
            'GID_id': 'a',
            'geotype': 'urban',
            'decile': 1,
            'population_total': 1000,
            'population_km2': 500,
            'total_sites': 10,
            'total_upgraded_sites': 5,
            'total_new_sites': 5,
            'on_grid_perc': 100,
            'grid_other_perc': 0,
            'phones_on_network': 750,
            'population_with_phones': 1000,
            'phones_on_network_to_total_phones_ratio': 0.75,
            'asset_type': 'new',
        },
        {
            'GID_0': 'CHL',
            'GID_id': 'a',
            'geotype': 'urban',
            'decile': 1,
            'population_total': 1000,
            'population_km2': 500,
            'total_sites': 10,
            'total_upgraded_sites': 5,
            'total_new_sites': 5,
            'on_grid_perc': 0,
            'grid_other_perc': 100,
            'phones_on_network': 750,
            'population_with_phones': 1000,
            'phones_on_network_to_total_phones_ratio': 0.75,
            'asset_type': 'new',
        },
    ]

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets, setup_option,
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    for region in results:

        if not region['asset_type'] == 'new':
            continue

        ## number of assets: 4, kwh per asset: 1
        if region['grid_type_perc'] == 100 and region['grid_type'] == 'on_grid':
            assert region['mno_energy_annual_demand_kwh'] == (((1 * 24 * 365) * 4) * 1) 
        ## number of assets: 4, kwh per asset: 1, MNOs: 3
        if region['grid_type_perc'] == 100 and region['grid_type'] == 'on_grid':
            assert region['total_energy_annual_demand_kwh'] == (((1 * 24 * 365) * 4) * 1) * 3
        ## number of assets: 4, kwh per asset: 1, MNOs: 3
        if region['grid_type_perc'] == 100 and region['grid_type'] == 'off_grid':
            assert region['total_energy_annual_demand_kwh'] == (((1 * 24 * 365) * 4) * 1) * 3

    setup_timesteps = [
        2020,
        2021,
    ]

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets, setup_option,
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand
    ) # should produce 8 results, 2 regions, 2 grid types over 2 timesteps

    total_energy = 0

    for region in results:
        total_energy += region['total_energy_annual_demand_kwh']

    assert total_energy == (((1 * 24 * 365) * 4) * 1) * 4 * 3


def test_assess_energy_sharing(setup_region, setup_option, setup_global_parameters,
    setup_country_parameters, setup_timesteps, setup_tech_lut, setup_on_grid_mix):

    setup_region[0]['new_sites'] = 1

    regions = [
        {
            'GID_0': 'CHL',
            'GID_id': 'a',
            'geotype': 'urban',
            'decile': 1,
            'population_total': 1000,
            'population_km2': 500,
            'total_sites': 10,
            'total_upgraded_sites': 5,
            'total_new_sites': 5,
            'on_grid_perc': 50,
            'grid_other_perc': 50,
            'phones_on_network': 750,
            'population_with_phones': 1000,
            'phones_on_network_to_total_phones_ratio': 0.75,
        },
    ]

    assets = {1:[
        {
        # 'scenario': 'low_20_20_20',
        # 'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        # 'confidence': 50,
        'GID_id':  'a',
        'asset': 'equipment',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        # 'scenario': 'low_20_20_20',
        # 'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        # 'confidence': 50,
        'GID_id':  'a',
        'asset': 'regional_node',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        # 'scenario': 'low_20_20_20',
        # 'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        # 'confidence': 50,
        'GID_id':  'a',
        'asset': 'core_node',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        # 'scenario': 'low_20_20_20',
        # 'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        # 'confidence': 50,
        'GID_id':  'a',
        'asset': 'backhaul_wireless_small',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        # 'scenario': 'low_20_20_20',
        # 'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        # 'confidence': 50,
        'GID_id':  'a',
        'asset': 'backhaul_wireless_medium',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
        {
        # 'scenario': 'low_20_20_20',
        # 'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
        # 'confidence': 50,
        'GID_id':  'a',
        'asset': 'backhaul_wireless_large',
        'quantity': 1,
        'decile': 1,
        'asset_type': 'new',
        },
    ],
    }

    energy_demand = {
        'equipment_kwh': 1,
        'core_node_kwh': 1,
        'regional_node_kwh': 1,
        'wireless_small_kwh': 1,
        'wireless_medium_kwh': 1,
        'wireless_large_kwh': 1,
    }

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets,
        {'strategy': '3G_epc_wireless_baseline_baseline_baseline_baseline','scenario': 'r'},
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    for item in results:
        if item['asset_type'] == 'new':
            ##(1*24*365) = 1 kWh*24 hours*365 days with a 50%/50% split of on/off grid power
            ## 4380 = 24 * 365 * .5
            assert round(results[0]['mno_equipment_annual_demand_kWh']) == round((1 * 24 * 365) * 0.5)   #4,380
            assert round(results[0]['mno_energy_annual_demand_kwh']) == round((1 * 24 * 365) * 0.5) * 6  #26,280
            # assert round(results[0]['total_equipment_annual_demand_kWh']) == round((((1 * 24 * 365) * 0.5) *3)) #13140

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets,
        {'strategy': '3G_epc_wireless_passive_baseline_baseline_baseline','scenario': 'r'},
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    assert round(results[0]['mno_equipment_annual_demand_kWh']) == round((1 * 24 * 365) * 0.5) #4,380
    assert round(results[0]['mno_energy_annual_demand_kwh']) == round((1 * 24 * 365) * 0.5) * 6 #26,280
    assert round(results[0]['total_equipment_annual_demand_kWh']) == round(((1 * 24 * 365) * 0.5) * 3) #13140

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets,
        {'strategy': '3G_epc_wireless_active_baseline_baseline_baseline','scenario': 'r'},
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    assert round(results[0]['mno_equipment_annual_demand_kWh']) == round((1 * 24 * 365) * 0.5 * .33333) #1458
    assert round(results[0]['mno_energy_annual_demand_kwh']) == round((((1 * 24 * 365) * 0.5) * .33333) * 6) #8751
    assert round(results[0]['total_equipment_annual_demand_kWh']) == round((((1 * 24 * 365) * 0.5) * .33333) * 3)  #4380

    regions = [
        {
            'GID_0': 'CHL',
            'GID_id': 'a',
            'geotype': 'rural',
            'decile': 1,
            'population_total': 1000,
            'population_km2': 500,
            'total_sites': 10,
            'total_upgraded_sites': 5,
            'total_new_sites': 5,
            'on_grid_perc': 50,
            'grid_other_perc': 50,
            'phones_on_network': 750,
            'population_with_phones': 1000,
            'phones_on_network_to_total_phones_ratio': 0.75,
        },
    ]
    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets,
        {'strategy': '3G_epc_wireless_srn_baseline_baseline_baseline_baseline','scenario': 'r'},
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    # (1 * 24 * 365) *.5 * .3333 (divide by one single SRN)
    assert round(results[0]['mno_equipment_annual_demand_kWh']) == round(((1 * 24 * 365) * .5) * .3333) #1,460
    assert round(results[0]['mno_energy_annual_demand_kwh']) == round((((1 * 24 * 365) * 0.5) * .33333) * 6) #8,760
    assert round(results[0]['total_equipment_annual_demand_kWh']) == round((((1 * 24 * 365) * 0.5) * .33333) * 3) #4380

    regions[0]['geotype'] = 'urban'

    results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets,
        {'strategy': '3G_epc_wireless_srn_baseline_baseline_baseline_baseline','scenario': 'r'},
        setup_global_parameters, setup_country_parameters,
        setup_timesteps, energy_demand)

    assert round(results[0]['mno_equipment_annual_demand_kWh']) == round((((1 * 24 * 365) *.5) * 1)) #4380
    assert round(results[0]['mno_energy_annual_demand_kwh']) == round((((1 * 24 * 365) * 0.5) * 1) * 6) #26,280
    assert round(results[0]['total_equipment_annual_demand_kWh']) == round((((1 * 24 * 365) * 0.5)) * 3) #5,840

    # regions = [
    #     {
    #         'GID_0': 'CHL',
    #         'GID_id': 'a',
    #         'geotype': 'urban',
    #         'decile': 1,
    #         'population_total': 1000,
    #         'population_km2': 500,
    #         'total_sites': 10,
    #         'total_upgraded_sites': 5,
    #         'total_new_sites': 5,
    #         'on_grid_perc': 100,
    #         'grid_other_perc': 0,
    #         'phones_on_network': 750,
    #         'population_with_phones': 1000,
    #         'phones_on_network_to_total_phones_ratio': 0.75,
    #         'asset_type': 'existing',
    #     },
    #     {
    #         'GID_0': 'CHL',
    #         'GID_id': 'a',
    #         'geotype': 'urban',
    #         'decile': 1,
    #         'population_total': 1000,
    #         'population_km2': 500,
    #         'total_sites': 10,
    #         'total_upgraded_sites': 5,
    #         'total_new_sites': 5,
    #         'on_grid_perc': 0,
    #         'grid_other_perc': 100,
    #         'phones_on_network': 750,
    #         'population_with_phones': 1000,
    #         'phones_on_network_to_total_phones_ratio': 0.75,
    #         'asset_type': 'new',
    #     },
    # ]

    # assets = {1: [
    #     {
    #     'scenario': 'low_20_20_20',
    #     'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
    #     'confidence': 50,
    #     'GID_id':  'a',
    #     'asset': 'equipment',
    #     'quantity': 1,
    #     'decile': 1,
    #     'asset_type': 'existing',
    #     },
    #     {
    #     'scenario': 'low_20_20_20',
    #     'strategy': '3G_umts_wireless_baseline_baseline_baseline_baseline',
    #     'confidence': 50,
    #     'GID_id':  'a',
    #     'asset': 'equipment',
    #     'quantity': 1,
    #     'decile': 1,
    #     'asset_type': 'new',
    #     },
    # ]
    # }

    # results = assess_energy({'income': 'HIC','wb_region': 'SSA'}, regions, assets, setup_option,
    #     setup_global_parameters, setup_country_parameters,
    #     setup_timesteps, energy_demand)

    # for region in results:
    #     print(region['asset_type'], region['total_sites'], 
    #           region['grid_type'], region['mno_equipment_annual_demand_kWh'])

    # assert results == 0