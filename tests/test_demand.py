import pytest
from cucumber.demand import estimate_demand, get_per_user_capacity

def test_estimate_demand(
    setup_country,
    setup_deciles,
    ):
    """
    Integration test.

    """
    answer = estimate_demand(
        setup_country, setup_deciles
    )

    assert answer[0]['population_with_smartphones'] == (
        answer[0]['population_total'] * 
        setup_country['smartphone_penetration']
    )

    answer2 = round(
        (answer[0]['population_with_smartphones'] * 0.59) / 
        answer[0]['area_km2']
    )
    assert round(answer[0]['demand_mbps_km2']) == answer2


def test_get_per_user_capacity(setup_country, setup_deciles):
    """
    Unit test.

    """
    answer1 = get_per_user_capacity(setup_country, 'urban', setup_deciles[0])
    answer2 = (
        (int(setup_deciles[0]['capacity']) / 30) * 
        (int(setup_country['traffic_in_the_busy_hour_perc']) / 100) * 1000 * 8 / 3600
    )
    assert round(answer1, 2) == round(answer2, 2)

    answer1 = get_per_user_capacity(setup_country, 'suburban', setup_deciles[0])
    answer2 = (
        (int(setup_deciles[0]['capacity']) / 30) * 
        (int(setup_country['traffic_in_the_busy_hour_perc']) / 100) * 1000 * 8 / 3600
    )
    assert round(answer1, 2) == round(answer2, 2)

    answer1 = get_per_user_capacity(setup_country, 'rural', setup_deciles[0])
    answer2 = (
        (int(setup_deciles[0]['capacity']) / 30) * 
        (int(setup_country['traffic_in_the_busy_hour_perc']) / 100) * 1000 * 8 / 3600
    )
    assert round(answer1, 2) == round(answer2, 2)
