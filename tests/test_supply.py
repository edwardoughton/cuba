import pytest
from cucumber.demand import estimate_demand
from cucumber.supply import (estimate_supply, find_site_density,
    estimate_site_upgrades, estimate_backhaul_upgrades)

def test_find_site_density(
    setup_country,
    setup_deciles,
    setup_capacity_lut
    ):

    setup_deciles[0]['demand_mbps_km2'] = 0.005
    #test demand being larger than max capacity
    answer = find_site_density(
        setup_country,
        setup_deciles[0],
        setup_capacity_lut
    )

    assert answer == 0.01

    setup_deciles[0]['demand_mbps_km2'] = 250
    answer = find_site_density(
        setup_country,
        setup_deciles[0],
        setup_capacity_lut
    )

    assert round(answer, 1) == 0.5

    setup_deciles[0]['demand_mbps_km2'] = 120
    answer = find_site_density(
        setup_country,
        setup_deciles[0],
        setup_capacity_lut
    )

    assert round(answer, 1) == .3


def test_estimate_site_upgrades(
        setup_country,
        setup_deciles
    ):

    #100 non-4G sites in total required. Hence 100 upgraded, with 0 new.  
    setup_deciles[0]['total_existing_sites'] = 100
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '4G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 100
    assert answer['total_new_sites'] == 0

    #100 4G sites in total required. 50 already exist. 50 to upgrade.  
    setup_deciles[0]['total_existing_sites'] = 200
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '4G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 50
    assert answer['total_new_sites'] == 0

    #100 4G sites in total required. 50 already exist. 50 to upgrade.  
    setup_deciles[0]['total_existing_sites'] = 0
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '4G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 0
    assert answer['total_new_sites'] == 100

    #100 4G sites in total required. 0 already exist. 100 new.  
    setup_deciles[0]['total_existing_sites'] = 0
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '4G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 0
    assert answer['total_new_sites'] == 100

    #150 4G sites in total required. 50 exist, 50 upgraded, 50 new.  
    setup_deciles[0]['total_existing_sites'] = 100
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_required_sites'] = 150
    setup_deciles[0]['generation'] = '4G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 50
    assert answer['total_new_sites'] == 50

    #100 4G sites in total required. 0 exist, 10 upgraded, 90 new.  
    setup_deciles[0]['total_existing_sites'] = 10
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '4G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 10
    assert answer['total_new_sites'] == 90

    #100 non-5G sites in total required. Hence 100 upgraded, with 0 new.  
    setup_deciles[0]['total_existing_sites'] = 100
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '5G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 100
    assert answer['total_new_sites'] == 0

    #100 5G sites in total required. 50 already exist. 50 to upgrade.  
    setup_deciles[0]['total_existing_sites'] = 200
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '5G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 100
    assert answer['total_new_sites'] == 0

    #100 5G sites in total required. 50 already exist. 50 to upgrade.  
    setup_deciles[0]['total_existing_sites'] = 0
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '5G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 0
    assert answer['total_new_sites'] == 100

    #100 5G sites in total required. 0 already exist. 100 new.  
    setup_deciles[0]['total_existing_sites'] = 0
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '5G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 0
    assert answer['total_new_sites'] == 100

    #150 5G sites in total required. 50 exist, 50 upgraded, 50 new.  
    setup_deciles[0]['total_existing_sites'] = 100
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_required_sites'] = 150
    setup_deciles[0]['generation'] = '5G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 100
    assert answer['total_new_sites'] == 50

    #100 5G sites in total required. 0 exist, 10 upgraded, 90 new.  
    setup_deciles[0]['total_existing_sites'] = 10
    setup_deciles[0]['total_existing_sites_4G'] = 0
    setup_deciles[0]['total_required_sites'] = 100
    setup_deciles[0]['generation'] = '5G'
    answer = estimate_site_upgrades({}, setup_deciles[0])
    assert answer['total_upgraded_sites'] == 10
    assert answer['total_new_sites'] == 90


def test_estimate_supply(
        setup_country,
        setup_deciles,
        setup_capacity_lut
    ):
    setup_deciles[0]['demand_mbps_km2'] = 5000
    setup_deciles[1]['demand_mbps_km2'] = 5000

    #total sites across all operators
    setup_deciles[0]['total_estimated_sites'] = 100
    setup_deciles[0]['total_estimated_sites_4G'] = 0
    setup_deciles[0]['backhaul_fiber'] = 0
    setup_deciles[0]['backhaul_copper'] = 0
    setup_deciles[0]['backhaul_wireless'] = 0
    setup_deciles[0]['backhaul_satellite'] = 0

    answer = estimate_supply(
        setup_country,
        setup_deciles,
        setup_capacity_lut
    )
    print(answer)
    assert round(answer[0]['total_required_sites'], 1) == 4630
    assert round(answer[1]['total_required_sites'], 1) == 5264


def test_estimate_backhaul_upgrades(
    setup_country,
    setup_deciles,
    ):

    setup_deciles[0]['backhaul'] = 'fiber'
    setup_deciles[0]['total_existing_sites'] = 50
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_new_sites'] = 50
    setup_deciles[0]['total_upgraded_sites'] = 50
    setup_deciles[0]['backhaul_fiber'] = 20
    setup_deciles[0]['backhaul_copper'] = 20
    setup_deciles[0]['backhaul_wireless'] = 50
    setup_deciles[0]['backhaul_satellite'] = 10
    answer = estimate_backhaul_upgrades(setup_country, setup_deciles[0])
    assert answer['backhaul_new'] == 80

    setup_deciles[0]['backhaul'] = 'wireless'
    setup_deciles[0]['total_existing_sites'] = 50
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_new_sites'] = 50
    setup_deciles[0]['total_upgraded_sites'] = 50
    setup_deciles[0]['backhaul_fiber'] = 20
    setup_deciles[0]['backhaul_wireless'] = 50
    answer = estimate_backhaul_upgrades(setup_country, setup_deciles[0])
    assert answer['backhaul_new'] == 30

    setup_deciles[0]['backhaul'] = 'wireless'
    setup_deciles[0]['total_existing_sites'] = 50
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_new_sites'] = 50
    setup_deciles[0]['total_upgraded_sites'] = 50
    setup_deciles[0]['backhaul_fiber'] = 100
    setup_deciles[0]['backhaul_wireless'] = 50
    answer = estimate_backhaul_upgrades(setup_country, setup_deciles[0])
    assert answer['backhaul_new'] == 0

    setup_deciles[0]['backhaul'] = 'wireless'
    setup_deciles[0]['total_existing_sites'] = 50
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_new_sites'] = 50
    setup_deciles[0]['total_upgraded_sites'] = 50
    setup_deciles[0]['backhaul_fiber'] = 0
    setup_deciles[0]['backhaul_wireless'] = 100
    answer = estimate_backhaul_upgrades(setup_country, setup_deciles[0])
    assert answer['backhaul_new'] == 0

    setup_deciles[0]['backhaul'] = 'wireless'
    setup_deciles[0]['total_existing_sites'] = 50
    setup_deciles[0]['total_existing_sites_4G'] = 50
    setup_deciles[0]['total_new_sites'] = 50
    setup_deciles[0]['total_upgraded_sites'] = 50
    setup_deciles[0]['backhaul_fiber'] = 0
    setup_deciles[0]['backhaul_wireless'] = 100
    answer = estimate_backhaul_upgrades(setup_country, setup_deciles[0])
    assert answer['backhaul_new'] == 0



 
