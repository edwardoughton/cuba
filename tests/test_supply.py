import pytest
from cuba.demand import estimate_demand
from cuba.supply import (estimate_supply, find_site_density,
    estimate_site_upgrades, estimate_backhaul_upgrades)


def test_find_site_density(
    setup_country,
    setup_region,
    setup_option,
    setup_global_parameters,
    setup_timesteps,
    setup_penetration_lut,
    setup_costs,
    setup_lookup,
    setup_ci,
    setup_infra_sharing_assets,
    setup_cost_types
    ):

    #test demand being larger than max capacity
    answer = find_site_density(
        setup_country,
        {'demand_mbps_km2': 100000,
        'geotype': 'urban'},
        setup_option,
        setup_global_parameters,
        setup_lookup,
        setup_ci,
    )

    assert answer == 2

    answer = find_site_density(
        setup_country,
        {'demand_mbps_km2': 0.005,
        'geotype': 'urban'},
        setup_option,
        setup_global_parameters,
        setup_lookup,
        setup_ci
    )

    assert answer == 0.01

    answer = find_site_density(
        setup_country,
        {'demand_mbps_km2': 250,
        'geotype': 'urban'},
        setup_option,
        setup_global_parameters,
        setup_lookup,
        setup_ci
    )

    assert round(answer, 1) == 0.3

    answer = find_site_density(
        setup_country,
        {'demand_mbps_km2': 120,
        'geotype': 'urban'},
        setup_option,
        setup_global_parameters,
        setup_lookup,
        setup_ci
    )

    assert round(answer, 1) == .2


def test_estimate_site_upgrades(
    setup_region,
    setup_option,
    setup_country_parameters,
    ):

    #total sites across all opterators
    setup_region[0]['total_estimated_sites'] = 100
    setup_region[0]['total_estimated_sites_4G'] = 0
    setup_region[0]['total_sites_required'] = 100

    #100 sites in total across two operators, hence 50 existing sites for this MNO
    answer = estimate_site_upgrades(
        setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline',
        {'networks': {'baseline_urban': 2}}
    )

    assert answer['existing_mno_sites'] == 50
    assert answer['new_mno_sites'] == 50
    assert answer['upgraded_mno_sites'] == 50

    #total sites across all operators
    setup_region[0]['total_estimated_sites'] = 200
    setup_region[0]['total_estimated_sites_4G'] = 50
    setup_region[0]['total_sites_required'] = 100

    #200 sites in total across two operators, hence 100 existing sites for this MNO
    #100 sites required, hence no new sites or no new upgrades
    answer = estimate_site_upgrades(setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline',
        {'networks': {'baseline_urban': 2}}
    )

    assert answer['existing_mno_sites'] == 100
    assert answer['new_mno_sites'] == 0
    assert answer['upgraded_mno_sites'] == 75

    #total sites across all operators
    setup_region[0]['total_estimated_sites'] = 0
    setup_region[0]['total_estimated_sites_4G'] = 0
    setup_region[0]['total_sites_required'] = 100

    #100 sites in total across two operators, hence 50 existing sites for this MNO
    answer = estimate_site_upgrades(setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline',
        {'networks': {'baseline_urban': 2}}
    )

    assert answer['existing_mno_sites'] == 0
    assert answer['new_mno_sites'] == 100
    assert answer['upgraded_mno_sites'] == 0

    #total sites across all operators
    setup_region[0]['total_estimated_sites'] = 100
    setup_region[0]['total_estimated_sites_4G'] = 0
    setup_region[0]['total_sites_required'] = 100

    #100 sites in total across two operators, hence 50 existing sites for this MNO
    answer = estimate_site_upgrades(setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline',
        {'networks': {'baseline_urban': 10}}
    )

    assert answer['existing_mno_sites'] == 10
    assert answer['new_mno_sites'] == 90
    assert answer['upgraded_mno_sites'] == 10

    #total sites across all operators
    setup_region[0]['total_estimated_sites'] = 100
    setup_region[0]['total_estimated_sites_4G'] = 50
    setup_region[0]['total_sites_required'] = 100

    #100 sites in total across two operators
    #Hence 50 existing sites for this MNO (all techs, 2G-4G)
    #However, 50 total are 4G, which means 25 for this MNO
    #So we need to upgrade
    answer = estimate_site_upgrades(setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline',
        {'networks': {'baseline_urban': 2}}
    )
    #the MNO has 50 current sites for all techs (of which 25 are 4G)
    assert answer['existing_mno_sites'] == 50
    #the MNO then builds 50 new sites
    assert answer['new_mno_sites'] == 50
    #and upgrades 25 (totalling the 100 required)
    assert answer['upgraded_mno_sites'] == 25

    #total sites across all operators
    setup_region[0]['total_estimated_sites'] = 100
    setup_region[0]['total_estimated_sites_4G'] = 100
    setup_region[0]['total_sites_required'] = 50

    #100 sites in total across two operators, hence 50 existing sites for this MNO
    answer = estimate_site_upgrades(setup_region[0],
        '5g_nsa_wireless_baseline_baseline_baseline_baseline',
        {'networks': {'baseline_urban': 2}}
    )

    assert answer['new_mno_sites'] == 0
    assert answer['upgraded_mno_sites'] == 50


def test_estimate_supply(
    setup_country,
    setup_region,
    setup_lookup,
    setup_option,
    setup_global_parameters,
    setup_country_parameters,
    setup_costs,
    setup_ci,
    setup_infra_sharing_assets,
    setup_cost_types,
    ):

    #total sites across all operators
    setup_region[0]['total_estimated_sites'] = 100
    setup_region[0]['total_estimated_sites_4G'] = 0
    setup_region[0]['backhaul_fiber'] = 0
    setup_region[0]['backhaul_copper'] = 0
    setup_region[0]['backhaul_wireless'] = 0
    setup_region[0]['backhaul_satellite'] = 0

    answer = estimate_supply(
        setup_country,
        setup_region,
        setup_lookup,
        setup_option,
        setup_global_parameters,
        setup_country_parameters,
        setup_costs,
        setup_ci,
        setup_infra_sharing_assets,
        setup_cost_types,
    )

    assert round(answer[0][0]['mno_site_density'], 1) == 2#0.9


def test_estimate_backhaul_upgrades(
    setup_region, setup_country_parameters
    ):

    setup_region[0]['new_mno_sites'] = 50
    setup_region[0]['upgraded_mno_sites'] = 50

    setup_region[0]['backhaul_fiber'] = 20
    setup_region[0]['backhaul_copper'] = 20
    setup_region[0]['backhaul_wireless'] = 50
    setup_region[0]['backhaul_satellite'] = 10

    answer = estimate_backhaul_upgrades(
        setup_region[0],
        '4G_epc_fiber_baseline_baseline_baseline_baseline',
        setup_country_parameters
    )

    assert answer['backhaul_new'] == 94

    answer = estimate_backhaul_upgrades(
        setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline',
        setup_country_parameters
    )

    assert answer['backhaul_new'] == 77

    setup_region[0]['backhaul_fiber'] = 300

    answer = estimate_backhaul_upgrades(
        setup_region[0],
        '4G_epc_fiber_baseline_baseline_baseline_baseline',
        setup_country_parameters
    )

    assert answer['backhaul_new'] == 0

    setup_region[0]['backhaul_fiber'] = 0
    setup_region[0]['backhaul_wireless'] = 300

    answer = estimate_backhaul_upgrades(
        setup_region[0],
        '4G_epc_wireless_baseline_baseline_baseline_baseline',
        setup_country_parameters
    )

    assert answer['backhaul_new'] == 0
