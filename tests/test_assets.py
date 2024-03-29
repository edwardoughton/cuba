import pytest
import math
from cuba.assets import (
    estimate_assets,
    upgrade_sites,
    greenfield_sites,
    existing_sites,
    # estimate_core_assets,
    get_backhaul_dist,
    # regional_net_assets,
    # core_net_assets,
    calc_assets,
    estimate_backhaul_type
)

def test_estimate_assets(setup_country, setup_region, setup_costs,
    setup_global_parameters, setup_country_parameters,
    setup_core_lut):
    """
    Integration test.

    """
    setup_region[0]['sites_4G'] = 0
    setup_region[0]['existing_mno_sites'] = 0
    setup_region[0]['new_mno_sites'] = 1
    setup_region[0]['upgraded_mno_sites'] = 0
    setup_region[0]['site_density'] = 0.5
    setup_region[0]['backhaul_new'] = 0
    setup_region[0]['scenario'] = 'S1_50_50_50'
    setup_region[0]['strategy'] = '3G_epc_wireless_baseline_baseline_baseline_baseline'
    setup_region[0]['confidence'] = [50]

    results = estimate_assets(
        setup_country,
        setup_region[0],
        {'scenario': '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline',
        'strategy': '3G_epc_wireless_baseline_baseline_baseline_baseline'},
        setup_costs,
        setup_global_parameters,
        setup_country_parameters,
    )

    for result in results:

        if result['asset'] == 'equipment':
            assert result['cost_per_unit'] == setup_costs['equipment']
        if result['asset'] == 'core_node':
            assert result['quantity'] == 2

    setup_region[0]['area_km2'] = 5000
    setup_region[0]['sites_4G'] = 0
    setup_region[0]['existing_mno_sites'] = 1
    setup_region[0]['new_mno_sites'] = 10
    setup_region[0]['upgraded_mno_sites'] = 0
    setup_region[0]['site_density'] = 0.5
    setup_region[0]['backhaul_new'] = 10
    setup_region[0]['scenario'] = 'S1_50_50_50'
    setup_region[0]['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['confidence'] = [50]

    results = estimate_assets(
        setup_country,
        setup_region[0],
        {'scenario': 'S1_50_50_50',
        'strategy': '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'},
        setup_costs,
        setup_global_parameters,
        setup_country_parameters,
    )
    total_cost_new = 0
    for result in results:

        cost = result['cost_per_unit'] * result['quantity'] #* result['backhaul_units']
        if 'backhaul' in result['asset']:
            cost = cost * result['backhaul_units']
        if 'existing' == result['build_type']:
            continue

        total_cost_new += cost

    assert total_cost_new == 4705600

    setup_region[0]['area_km2'] = 100
    setup_region[0]['sites_4G'] = 0
    setup_region[0]['existing_mno_sites'] = 1
    setup_region[0]['new_mno_sites'] = 10
    setup_region[0]['upgraded_mno_sites'] = 0
    setup_region[0]['site_density'] = 0.5
    setup_region[0]['backhaul_new'] = 10
    setup_region[0]['scenario'] = 'S1_50_50_50'
    setup_region[0]['strategy'] = '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['confidence'] = [50]

    results = estimate_assets(
        setup_country,
        setup_region[0],
        {'scenario': 'S1_50_50_50',
        'strategy': '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'},
        setup_costs,
        setup_global_parameters,
        setup_country_parameters,
    )
    total_cost_new = 0
    for result in results:

        cost = result['cost_per_unit'] * result['quantity']
        if 'backhaul' in result['asset']:
            cost = cost * result['backhaul_units']
        if 'existing' == result['build_type']:
            continue

        total_cost_new += cost

    assert total_cost_new == 1270000


def test_upgrade_site(setup_country, setup_region):
    """
    Unit test.

    """
    setup_region[0]['existing_mno_sites'] = 0

    cost_structure = upgrade_sites(10, setup_country, setup_region[0])

    assert cost_structure['equipment'] == 10
    assert cost_structure['installation'] == 10
    assert cost_structure['site_rental'] == 10
    assert cost_structure['operation_and_maintenance'] == 10
    assert cost_structure['backhaul']['quantity'] == 10
    assert cost_structure['backhaul']['backhaul_dist_m'] == 707.0#1414


def test_greenfield_site(setup_country, setup_region):
    """
    Unit test.

    """
    setup_region[0]['existing_mno_sites'] = 0

    cost_structure = greenfield_sites(10, setup_country, setup_region[0])

    assert cost_structure['equipment'] == 10
    assert cost_structure['site_build'] == 10
    assert cost_structure['installation'] == 10
    assert cost_structure['site_rental'] == 10
    assert cost_structure['operation_and_maintenance'] == 10
    assert cost_structure['backhaul']['quantity'] == 10
    assert cost_structure['backhaul']['backhaul_dist_m'] == 707.0#1414


def test_existing_site(setup_country, setup_region):
    """
    Unit test.

    """
    setup_region[0]['existing_mno_sites'] = 5

    cost_structure = greenfield_sites(5, setup_country, setup_region[0])

    assert cost_structure['equipment'] == 5
    assert cost_structure['site_build'] == 5
    assert cost_structure['installation'] == 5
    assert cost_structure['site_rental'] == 5
    assert cost_structure['operation_and_maintenance'] == 5
    assert cost_structure['backhaul']['quantity'] == 5
    assert round(cost_structure['backhaul']['backhaul_dist_m']) == 408


def test_calc_assets(setup_region, setup_option, setup_costs):
    """
    Unit test.

    """
    setup_region[0]['scenario'] = 'test'
    setup_region[0]['confidence'] = 'test'
    setup_region[0]['backhaul_new'] = 5
    setup_region[0]['backhaul_existing'] = 5

    asset_structure = {
        'equipment': 10,
        'installation': 10,
        'site_rental': 10,
        'operation_and_maintenance': 10,
        'backhaul': {
            'quantity': 10,
            'backhaul_dist_m': 2000
        }
    }

    setup_option['strategy'] = '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['strategy'] = '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'

    assets = calc_assets(setup_region[0], setup_option, asset_structure,
        setup_costs, 'upgraded')

    for asset in assets:
        if asset['asset'] == 'equipment':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 40000
            assert asset['total_cost'] == 10*40000
        if asset['asset'].startswith('backhaul'):
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 10000
            assert asset['backhaul_units'] == 1
            assert asset['total_cost'] == 10*10000

    setup_option['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'

    assets = calc_assets(setup_region[0], setup_option, asset_structure,
        setup_costs, 'upgraded')

    for asset in assets:
        if asset['asset'] == 'equipment':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 40000
            assert asset['total_cost'] == 10*40000
        if asset['asset'].startswith('backhaul'):
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 10
            assert asset['backhaul_units'] == 2000
            assert asset['total_cost'] == 10*10*2000

    setup_region[0]['strategy'] = '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'

    asset_structure = {
        'equipment': 10,
        'site_build': 10,
        'installation': 10,
        'site_rental': 10,
        'operation_and_maintenance': 10,
        'backhaul': {
            'quantity': 10,
            'backhaul_dist_m': 2000
        }
    }

    assets = calc_assets(setup_region[0], setup_option, asset_structure,
        setup_costs, 'new')

    for asset in assets:

        if asset['asset'] == 'equipment':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 40000
            assert asset['total_cost'] == 10*40000
        if asset['asset'] == 'installation':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 30000
            assert asset['total_cost'] == 10*30000
        if asset['asset'] == 'site_rental_urban':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 9600
            assert asset['total_cost'] == 10*9600
        if asset['asset'] == 'operation_and_maintenance':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 7400
            assert asset['total_cost'] == 10*7400
        if asset['asset'] == 'backhaul_wireless_small':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 10000
            assert asset['total_cost'] == 10*10000

    setup_option['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'

    assets = calc_assets(setup_region[0], setup_option, asset_structure,
        setup_costs, 'new')

    for asset in assets:
        if asset['asset'].startswith('backhaul'):
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 10
            assert asset['backhaul_units'] == 2000
            assert asset['total_cost'] == 10*10*2000


    asset_structure = {
        'site_rental': 10,
        'operation_and_maintenance': 10,
    }

    setup_option['strategy'] = '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['strategy'] = '4G_epc_wireless_baseline_baseline_baseline_baseline_baseline_baseline'

    assets = calc_assets(setup_region[0], setup_option, asset_structure,
        setup_costs, 'existing')

    for asset in assets:
        if asset['asset'].startswith('site_rental'):
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 9600
            assert asset['total_cost'] == 10*9600
        if asset['asset'] == 'operation_and_maintenance':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 7400
            assert asset['total_cost'] == 10*7400

    setup_option['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'
    setup_region[0]['strategy'] = '4G_epc_fiber_baseline_baseline_baseline_baseline_baseline_baseline'

    assets = calc_assets(setup_region[0], setup_option, asset_structure,
        setup_costs, 'existing')

    assert len(assets) == 2

    for asset in assets:
        if asset['asset'] == 'equipment':
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 40000
            assert asset['total_cost'] == 10*40000
        if asset['asset'].startswith('backhaul'):
            assert asset['quantity'] == 10
            assert asset['cost_per_unit'] == 10
            assert asset['backhaul_units'] == 2000
            assert asset['total_cost'] == 10*10*2000


def test_get_backhaul_dist(setup_country, setup_region):

    setup_region[0]['existing_mno_sites'] = 15
    assert get_backhaul_dist(setup_country, setup_region[0]) == 250

    setup_region[0]['existing_mno_sites'] = 0
    assert get_backhaul_dist(setup_country, setup_region[0]) == 707


def test_estimate_backhaul_type():

    assert estimate_backhaul_type('wireless', 10000, 'rural') == (1, 'wireless_small')

    assert estimate_backhaul_type('wireless', 20000, 'rural') == (1, 'wireless_medium')

    assert estimate_backhaul_type('wireless', 35000, 'rural') == (1, 'wireless_large')

    assert estimate_backhaul_type('wireless', 90000, 'rural') == (2, 'wireless_large')

    assert estimate_backhaul_type('fiber', 10000, 'rural') == (10000, 'fiber_rural_m')

    assert estimate_backhaul_type('', 10000, 'rural') == (0, 'Backhaul tech not recognized')
