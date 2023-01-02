"""
Assessment Module

Written by Ed Oughton.

Winter 2020

"""

def assess(country, regions, option, global_parameters, country_parameters, timesteps):
    """
    For each region, assess the viability level.

    Parameters
    ----------
    country : dict
        Country information.
    regions : dataframe
        Geopandas dataframe of all regions.
    option : dict
        Contains the scenario and strategy. The strategy string controls
        the strategy variants being testes in the model and is defined based
        on the type of technology generation, core and backhaul, and the level
        of sharing, subsidy, spectrum and tax.
    global_parameters : dict
        All global model parameters.
    country_parameters : dict
        All country specific parameters.

    Returns
    -------
    output : list of dicts
        Contains all output data.

    """
    interim = []

    strategy = option['strategy']
    available_for_cross_subsidy = 0

    for region in regions:

        # add administration cost
        region = get_administration_cost(region, country_parameters,
            global_parameters, timesteps)

        # npv spectrum cost
        region['spectrum_cost'] = get_spectrum_costs(region, option['strategy'],
            global_parameters, country_parameters)

        #tax on investment
        region['tax'] = calculate_tax(region, strategy, country_parameters)

        #profit margin value calculated on all costs + taxes
        region['profit_margin'] = calculate_profit(region, country_parameters)

        region['total_mno_cost'] = (
            region['network_cost'] +
            region['administration'] +
            region['spectrum_cost'] +
            region['tax'] +
            region['profit_margin']
        )

        #avoid zero division
        if region['total_mno_cost'] > 0 and region['smartphones_on_network'] > 0:
            region['cost_per_sp_user'] = (
                region['total_mno_cost'] / region['smartphones_on_network'])
        else:
            region['cost_per_sp_user'] = 0

        region = allocate_available_excess(region)
        available_for_cross_subsidy += region['available_cross_subsidy']

        interim.append(region)

    interim = sorted(interim, key=lambda k: k['deficit'], reverse=False)

    intermediate_regions = []

    for region in interim:

        region, available_for_cross_subsidy = estimate_subsidies(
            region, available_for_cross_subsidy)

        intermediate_regions.append(region)

    output = calculate_total_market_costs(
        intermediate_regions, option, country_parameters)

    return output


def get_administration_cost(region, country_parameters, global_parameters, timesteps):
    """
    There is an annual administration cost to deploying and operating all assets.

    Parameters
    ----------
    regions : list of dicts
        Data for all regions (one dict per region).
    country_parameters : dict
        All country specific parameters.

    Returns
    -------
    region : dict
        Contains all regional data.

    """
    annual_cost = (
        region['network_cost'] *
        (country_parameters['financials']['administration_percentage_of_network_cost'] /
        100))

    costs = []

    for timestep in timesteps:

        timestep = timestep - 2020

        discounted_cost = discount_admin_cost(annual_cost, timestep, global_parameters)

        costs.append(discounted_cost)

    region['administration'] = sum(costs)

    return region


def allocate_available_excess(region):
    """
    Allocate available excess capital (if any).

    """
    difference = region['total_mno_revenue'] - region['total_mno_cost']

    if difference > 0:
        region['available_cross_subsidy'] = difference
        region['deficit'] = 0
    else:
        region['available_cross_subsidy'] = 0
        region['deficit'] = abs(difference)

    return region


def get_spectrum_costs(region, strategy, global_parameters, country_parameters):
    """
    Calculate spectrum costs.

    """
    population = int(round(region['population_total']))
    frequencies = {
        '3G': [
            {
                'frequency': 1900,
                'bandwidth': '2x10',
                # 'status': 'active',
            },
        ],
        '4G': [
            {
                'frequency': 850,
                'bandwidth': '2x10',
                # 'status': 'active',
            },
            {
                'frequency': 1700,
                'bandwidth': '2x10',
                # 'status': 'active',
            },
        ],
        '5G': [
            {
                'frequency': 700,
                'bandwidth': '2x10',
                # 'status': 'inactive',
            },
            {
                'frequency': 3500,
                'bandwidth': ' 1x40',
                # 'status': 'inactive',
            },
        ]
    }
    # frequencies = country_parameters['frequencies']
    generation = strategy.split('_')[0]
    frequencies = frequencies[generation]

    spectrum_cost = strategy.split('_')[5]

    coverage_spectrum_cost = 'spectrum_coverage_baseline_usd_mhz_pop'
    capacity_spectrum_cost = 'spectrum_capacity_baseline_usd_mhz_pop'

    coverage_cost_usd_mhz_pop = country_parameters['financials'][coverage_spectrum_cost]
    capacity_cost_usd_mhz_pop = country_parameters['financials'][capacity_spectrum_cost]

    if spectrum_cost == 'low':
        coverage_cost_usd_mhz_pop = (coverage_cost_usd_mhz_pop *
            (country_parameters['financials']['spectrum_cost_low'] /100))
        capacity_cost_usd_mhz_pop = (capacity_cost_usd_mhz_pop *
            (country_parameters['financials']['spectrum_cost_low'] /100))

    if spectrum_cost == 'high':
        coverage_cost_usd_mhz_pop = (coverage_cost_usd_mhz_pop *
            (country_parameters['financials']['spectrum_cost_high'] / 100))
        capacity_cost_usd_mhz_pop = (capacity_cost_usd_mhz_pop *
            (country_parameters['financials']['spectrum_cost_high'] / 100))

    all_costs = []

    for frequency in frequencies:

        # if frequency['status'] == 'active':
        #     continue

        channel_number = int(frequency['bandwidth'].split('x')[0])
        channel_bandwidth = int(frequency['bandwidth'].split('x')[1])
        bandwidth_total = channel_number * channel_bandwidth

        if frequency['frequency'] < 1000:
            cost = (
                coverage_cost_usd_mhz_pop * bandwidth_total *
                population)
            all_costs.append(cost)
        else:
            cost = (
                capacity_cost_usd_mhz_pop * bandwidth_total *
                population)
            all_costs.append(cost)

    return sum(all_costs)


def calculate_tax(region, strategy, country_parameters):
    """
    Calculate tax.

    """
    tax_rate = strategy.split('_')[6]
    tax_rate = 'tax_{}'.format(tax_rate)

    tax_rate = country_parameters['financials'][tax_rate]

    investment = region['network_cost']

    tax = investment * (tax_rate / 100)

    return tax


def calculate_profit(region, country_parameters):
    """
    Estimate npv profit.

    This is treated as the Net Operating Profit After
    Taxes Margin (NOPAT).

    NOPAT ranges from ~5-15% depending on the context:
    https://static1.squarespace.com/static/54922abde4b0afbec1351c14/t/583c49c8bebafb758437374e

    """
    investment = (
        region['network_cost'] +
        region['administration'] +
        region['spectrum_cost'] +
        region['tax']
    )

    profit = investment * (country_parameters['financials']['profit_margin'] / 100)

    return profit


def estimate_subsidies(region, available_for_cross_subsidy):
    """
    Estimates either the contribution to cross-subsidies, or the
    quantity of subsidy required.

    Parameters
    ----------
    region : Dict
        Contains all variable for a single region.
    available_for_cross_subsidy : int
        The amount of capital available for cross-subsidization.

    Returns
    -------
    region : Dict
        Contains all variable for a single region.
    available_for_cross_subsidy : int
        The amount of capital available for cross-subsidization.

    """
    if region['deficit'] > 0:

        if available_for_cross_subsidy >= region['deficit']:
            region['used_cross_subsidy'] = region['deficit']
            available_for_cross_subsidy -= region['deficit']
        elif 0 < available_for_cross_subsidy < region['deficit']:
            region['used_cross_subsidy'] = available_for_cross_subsidy
            available_for_cross_subsidy = 0
        else:
            region['used_cross_subsidy'] = 0

    else:
        region['used_cross_subsidy'] = 0

    required_state_subsidy = (region['total_mno_cost'] -
        (region['total_mno_revenue'] + region['used_cross_subsidy']))

    if required_state_subsidy > 0:
        region['required_state_subsidy'] = required_state_subsidy
    else:
        region['required_state_subsidy'] = 0

    return region, available_for_cross_subsidy


def discount_admin_cost(cost, timestep, global_parameters):
    """
    Discount admin cost based on return period.
    192,744 = 23,773 / (1 + 0.05) ** (0:9)

    Parameters
    ----------
    cost : float
        Annual admin network running cost.
    timestep : int
        Time period (year) to discount against.
    global_parameters : dict
        All global model parameters.
    Returns
    -------
    discounted_cost : float
        The discounted admin cost over the desired time period.
    """
    discount_rate = global_parameters['discount_rate'] / 100

    discounted_cost = cost / (1 + discount_rate) ** timestep

    return discounted_cost


def calculate_total_market_costs(regions, option, country_parameters):
    """
    Calculate the costs for all Mobile Network Operators (MNOs).
    """
    output = []

    # generation_core_backhaul_sharing_networks_spectrum_tax
    network_strategy = option['strategy'].split('_')[4]

    for region in regions:

        geotype = region['geotype'].split(' ')[0]

        net_handle = network_strategy + '_' + geotype
        networks = country_parameters['networks'][net_handle]

        ms = 100 / networks

        region['total_phones'] = calc(region, 'phones_on_network', ms)
        region['total_smartphones'] = calc(region, 'smartphones_on_network', ms)
        region['total_market_revenue'] = calc(region, 'total_mno_revenue', ms)
        region['total_sites'] = calc(region, 'existing_mno_sites', ms)
        region['total_upgraded_sites'] = calc(region, 'upgraded_mno_sites', ms)
        region['total_new_sites'] = calc(region, 'new_mno_sites', ms)
        region['total_ran'] = calc(region, 'ran', ms)
        region['total_backhaul_fronthaul'] = calc(region, 'backhaul_fronthaul', ms)
        region['total_civils'] = calc(region, 'civils', ms)
        region['total_core_network'] = calc(region, 'core_network', ms)
        region['total_network_cost'] = calc(region, 'network_cost', ms)
        region['total_administration'] = calc(region, 'administration', ms)
        region['total_spectrum_cost'] = calc(region, 'spectrum_cost', ms)
        region['total_tax'] = calc(region, 'tax', ms)
        region['total_profit_margin'] = calc(region, 'profit_margin', ms)
        region['total_market_cost'] = calc(region, 'total_mno_cost', ms)
        region['total_available_cross_subsidy'] = calc(region, 'available_cross_subsidy', ms)
        region['total_deficit'] = calc(region, 'deficit', ms)
        region['total_used_cross_subsidy'] = calc(region, 'used_cross_subsidy', ms)
        region['total_required_state_subsidy'] = calc(region, 'required_state_subsidy', ms)

        output.append(region)

    return output


def calc(region, metric, ms):
    """

    """
    if metric in region:

        value = region[metric]

        if value == 0 or region['phones_on_network'] == 0:
            return 0

        value_per_user = value / region['phones_on_network']

        return round(value_per_user * region['population_with_phones'])

    else:

        return 0
