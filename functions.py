import matplotlib.pyplot as plt
import numpy as np
import sys
from math import pi, pow, tan, radians, sqrt, log, exp
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


def calc_bp_dh_charge(bp_burden, bp_spacing, bp_height,
                      bp_dh_subdrilling, bp_dh_stemming, bp_dh_diameter,
                      expl_density):
    ''' Calculates drillhole and charge parameters - drillhole length, charge length, explosive mass, specific charge
    Изчислява конструкцията на заряда за взривен сондаж - дължина на сондажа, дължина на зярада, количество ВВ,
    и относ. разход на ВВ '''

    bp_dh_length = bp_dh_subdrilling + bp_height
    bp_dh_exp_length = bp_dh_length - bp_dh_stemming
    bp_dh_exp_mass = expl_density * bp_dh_exp_length * (bp_dh_diameter ** 2) * pi / 4 / 1000
    bp_dh_spec_charge = bp_dh_exp_mass / (bp_burden * bp_spacing * bp_height)
    bp_dh_charge_dict = {"DH length, m": bp_dh_length, "DH charge length, m": bp_dh_exp_length,
                         "DH charge mass, kg": bp_dh_exp_mass, "DH spec. charge, kg/m³": bp_dh_spec_charge}

    return bp_dh_charge_dict


def calc_bp_total(bp_height, bp_width, bp_length, bp_slope_angle,
                  bp_burden, bp_spacing, bp_dh_length, bp_dh_exp_mass):
    ''' Calculates overall blast panel charging parameters - rows, drillholes per row, total drillhole count,
    total drillhole length, total rock volume and total explsoive mass
    Изчислява общите параметри за взривяваното поле - брой редове, брой сондажи в ред, брой сондажи,
    общ обем пробивни работи, обем взривявана скална маса и общо количество ВВ '''

    bp_dh_rows_cnt = (bp_width - 3) // bp_burden + 1
    bp_dh_per_row_cnt = bp_length // bp_spacing + 1
    bp_total_dh_cnt = bp_dh_rows_cnt * bp_dh_per_row_cnt
    bp_total_dh_length = bp_total_dh_cnt * bp_dh_length
    bp_total_volume = bp_height * (bp_width * bp_length + 1 / tan(radians(bp_slope_angle)))
    bp_total_exp_mass = bp_dh_exp_mass * bp_total_dh_cnt
    bp_total_pf = bp_total_exp_mass / bp_total_volume
    bp_total_dict = {"Rows": bp_dh_rows_cnt, "DHs per row": bp_dh_per_row_cnt,
                     "Total DH count": bp_total_dh_cnt, "Total DH length, m": bp_total_dh_length,
                     "Total rock volume, m³": bp_total_volume, "Total explosive mass, kg": bp_total_exp_mass,
                     "Overall powder factor, kg/m³": bp_total_pf}

    return bp_total_dict


def calc_x50(bp_dh_exp_mass, bp_dh_spec_charge, rm_rock_factor, expl_rws):
    ''' Calculates and returns the value of the Median rock fragment size (X50) based on the original formula by Cunningham
    Изчислява и връща стойността на средния размер скален къс (X50) на базата на първоначалната формула на Cunningham '''

    x50 = rm_rock_factor * \
          pow(bp_dh_spec_charge, -0.8) * \
          pow(bp_dh_exp_mass, (1 / 6)) * \
          pow((115 / expl_rws), (19 / 30))

    return x50 * 10


def calc_uniformity_idx(bp_burden, bp_spacing, bp_dh_diameter, bp_dh_exp_length, bp_dh_dev, bp_height, bp_dh_pattern):
    ''' Calculates and returns the value of the Uniformity index value based on original formula, proposed by Cunningham
    Изчислява и връща стойността индекса на еднородост по първоначалната формула на Cunningham'''

    p = 1  # Pattern type coefficient (Коефициент, отчитащ вида на мрежата)
    if bp_dh_pattern == "staggered":
        p = 1.1
    elif bp_dh_pattern == "regular":
        p = 1

    n = (2.2 - 14 * bp_burden / bp_dh_diameter) * \
        sqrt(0.5 + 0.5 * bp_spacing / bp_burden) * \
        (1 - bp_dh_dev / bp_burden) * \
        (bp_dh_exp_length / bp_height) * p

    return n


def calc_uniformity_idx_mod(bp_burden, bp_spacing, 
                            bp_dh_diameter, bp_dh_exp_length, bp_dh_dev, 
                            bp_height, rm_rock_factor, c_n = 1):
    '''Calculates and returns the value of the Uniformity index value based on updated formula, proposed by Cunningham
    Изчислява и връща стойността индекс на еднородост по обновената формула на Cunningham'''
    
    n = sqrt(2 - 30 * bp_burden / bp_dh_diameter) * \
        sqrt(0.5 + 0.5 * bp_spacing / bp_burden) * \
        (1 - bp_dh_dev / bp_burden) * \
        pow((bp_dh_exp_length / bp_height), 0.3) * c_n
    
    return n


def kuz_ram_model(n, x50, x):
    ''' Returns the percent passing value for a rock fragment size, based on the Rosin-Rammler distribution
    Връща стойността на процента преминал материал при даден размер скален къс на базата на разпределението на
    Rosin-Rammler '''

    x_c = x50 / pow(0.693, 1 / n)
    p = 1 - 1 / exp(pow((x / x_c), n))

    return 100*p


def plot_kuz_ram_result(crusher_feed, x50, uniformity_idx, f_colour = "tab:blue", f_label = "Old uniformity model"):
    ''' Plots the CDF of the rock fragments for the Kuz-Ram model 
    Чертае кумулативната плътност на разпределението на скалните късове по модела Kuz-Ram '''

    x = np.arange(0, crusher_feed + 1000, 10)

    kuz_ram_model_vectorized = np.vectorize(kuz_ram_model)
    y = kuz_ram_model_vectorized(uniformity_idx, x50, x)

    plt.scatter(crusher_feed, kuz_ram_model(uniformity_idx, x50, crusher_feed), c = f_colour)
    x_const = np.linspace(0, crusher_feed + 1, 1000)
    y_const = np.linspace(0, kuz_ram_model(uniformity_idx, x50, crusher_feed), 1000)
    
    plt.axvline(crusher_feed, color = 'black', linestyle = 'dashed', linewidth = 2)
    plt.plot(x_const, [kuz_ram_model(uniformity_idx, x50, crusher_feed)] * 1000, color='black', linestyle="--")
    
    plt.plot(x, y, label = f_label)
    plt.xlabel("Rock fragment size, mm")
    plt.ylabel("Passing, %")

    plt.xlim(0, crusher_feed + 1000)
    plt.ylim(0, 101)


def set_fill_factor(x50):
    ''' Returns loader bucket fill factor depening on Median rock fragment size (X50)
    Връща коефициента на напълване на кофата на база на среден размер на скалните късове (X50) '''
    
    return -0.0022 * x50/10 + 0.8833


def calc_truck_tr_t(loader_bucket_vol, rm_density, rm_swell_factor, loader_bucket_fill_factor, truck_cap_t):
    truck_tr_t = 0

    while True:
        if truck_tr_t + loader_bucket_vol * rm_density / rm_swell_factor * loader_bucket_fill_factor <= truck_cap_t:
            truck_tr_t += loader_bucket_vol * rm_density / rm_swell_factor * loader_bucket_fill_factor
        else:
            break

    return truck_tr_t


def calc_drilling(bp_total_dh_length, drill_h_rate, drill_h_costs):
    ''' Returns Drilling costs
    Връща разходите за пробивни работи '''
    
    costs = bp_total_dh_length * drill_h_costs / drill_h_rate / 1000
    time = bp_total_dh_length / drill_h_rate
    drilling_result_dict = {"Costs": costs, "Time": time}
    
    return drilling_result_dict


def calc_blasting(bp_total_exp_mass, expl_price):
    '''Returns Blasting costs
    Връща разходите за взривяване'''
    
    costs = bp_total_exp_mass * expl_price / 1000
    blasting_result_dict = {"Costs": costs, "Time": "Not included in project"}
    
    return blasting_result_dict


def calc_loading(bp_total_volume, loader_h_prod, loader_h_costs):
    ''' Returns Loading costs
    Връща разходите за изкопно-товарни работи '''
    
    costs = bp_total_volume * loader_h_costs / loader_h_prod / 1000
    time = bp_total_volume / loader_h_prod
    loading_result_dict = {"Costs": costs, "Time": time}
    
    return loading_result_dict


def calc_hauling(bp_total_volume, truck_h_prod, truck_h_costs, rm_density):
    # Returns Hauling costs
    # Връща разходите за транспортиране
    
    costs = bp_total_volume * rm_density * truck_h_costs / truck_h_prod / 1000
    time = bp_total_volume * rm_density / truck_h_prod
    hauling_result_dict = {"Costs": costs, "Time": time}
    
    return hauling_result_dict


def pareto_chart(total_costs_dict):

    sorted_total_costs = dict(sorted(total_costs_dict.items(), key=lambda x: x[1], reverse=True))

    cumulative_counts = []
    cumulative_sum = 0
    for count in sorted_total_costs.values():
        cumulative_sum += count
        cumulative_counts.append(cumulative_sum)

    total = sum(sorted_total_costs.values())
    cumulative_percentage = [(count / total) * 100 for count in cumulative_counts]
    
    fig, ax = plt.subplots()

    ax.bar(range(len(sorted_total_costs)), sorted_total_costs.values(), align='center')
    plt.xticks(range(len(sorted_total_costs)), sorted_total_costs.keys())
    
    ax2 = ax.twinx()
    
    ax2.plot(range(len(sorted_total_costs)), cumulative_percentage, color='r', marker='o')
    ax2.set_ylim([0, 102])

    ax.set_xlabel('Types of mining costs')
    ax.set_ylabel('Operational costs, kEUR')
    ax2.set_ylabel("Cumulative Percentage, %")
    plt.title('Pareto Chart for mining cost')

    plt.show()
    
    
def mining_ops(bp_burden, bp_spacing, bp_dh_subdrilling, bp_dh_stemming):
    # Caluclates total mining costs, based on blast deisng parameters and global variables for mining equipment, prices, 
    # rockmass properties and blast panel features
    
    charge =  calc_bp_dh_charge(bp_burden, bp_spacing, bp_height, 
                                bp_dh_subdrilling, bp_dh_stemming, bp_dh_diameter, expl_density)
    bp_dh_length = charge["DH length, m"]
    bp_dh_exp_length = charge["DH charge length, m"]
    bp_dh_exp_mass = charge["DH charge mass, kg"]
    bp_dh_spec_charge = charge["DH spec. charge, kg/m³"]
    
    bp_total = calc_bp_total(bp_height, bp_width, bp_length, bp_slope_angle, 
                             bp_burden, bp_spacing, bp_dh_length, bp_dh_exp_mass)
    bp_dh_rows_cnt = bp_total["Rows"]
    bp_dh_per_row_cnt = bp_total["DHs per row"]
    bp_total_dh_cnt = bp_total["Total DH count"]
    bp_total_dh_length = bp_total["Total DH length, m"]
    bp_total_volume = bp_total["Total rock volume, m³"]
    bp_total_exp_mass = bp_total["Total explosive mass, kg"]
    
    frag_uniformity_idx_mod = calc_uniformity_idx_mod(bp_burden, bp_spacing, 
                                                      bp_dh_diameter, bp_dh_exp_length, bp_dh_dev, bp_height, rm_rock_factor)
    frag_x50 = calc_x50(bp_dh_exp_mass, bp_dh_spec_charge, rm_rock_factor, expl_rws)
    frag_oversize = 100 - kuz_ram_model(frag_uniformity_idx_mod, frag_x50, 1000)
    
    loader_fill_factor = set_fill_factor(frag_x50)
    loader_h_prod = 3600 / loader_s_cycle * loader_fill_factor * loader_bucket_vol / rm_swell_factor

    truck_tr_t = calc_truck_tr_t(loader_bucket_vol, rm_density, rm_swell_factor, loader_fill_factor, truck_cap_t)
    truck_h_prod =  truck_tr_t * (60 / truck_min_haul)
    
    costs_drilling = calc_drilling(bp_total_dh_length, drill_h_rate, drill_h_costs)["Costs"]
    costs_blasting = calc_blasting(bp_total_exp_mass, expl_price)["Costs"]
    costs_loading = calc_loading(bp_total_volume, loader_h_prod, loader_h_costs)["Costs"]
    costs_hauling = calc_hauling(bp_total_volume, truck_h_prod, truck_h_costs)["Costs"]
    costs_total = costs_drilling + costs_blasting + costs_loading + costs_hauling
    
    result_dict = {"Burden, m": bp_burden,
                   "Spacing, m": bp_spacing,
                   "Stemming, m": bp_dh_stemming,
                   "Subdrilling, m": bp_dh_subdrilling,
                   "DH length, m": bp_dh_length,
                   "DH expl. mass, kg": bp_dh_exp_mass,
                   "DH spec. charge, kg/m³": bp_dh_spec_charge,
                   "Rows": bp_dh_rows_cnt,
                   "Holes per row": bp_dh_per_row_cnt,
                   "Total number of drillholes": bp_total_dh_cnt,
                   "Total drillhole length, m": bp_total_dh_length,
                   "Total explosive mass, kg": bp_total_exp_mass,
                   "Drilling costs, kEUR": costs_drilling,
                   "Blasting costs, kEUR": costs_blasting, 
                   "Loading costs, kEUR": costs_loading, 
                   "Haul costs, kEUR": costs_hauling, 
                   "Total costs, kEUR": costs_total, 
                   "X50, mm": frag_x50, 
                   "Uniformity index": frag_uniformity_idx_mod, 
                   "Oversize, %": frag_oversize}
    
    return result_dict