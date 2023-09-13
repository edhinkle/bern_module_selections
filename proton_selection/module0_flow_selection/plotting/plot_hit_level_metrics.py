################################################################################
##                                                                            ##
##    CONTAINS: Script to create plots describing data/MC metrics             ##
##              events using a dictionary                                     ##
##                                                                            ##
################################################################################

import matplotlib.pyplot as plt
import numpy as np

def plot_hit_level_metrics(d, is_mc):

    if is_mc:
        mc_title = '[Simulation]'
        sample_type = "MC"
    else:
        mc_title = '[Data]'
        sample_type = "Data"

    # PLOT: total charge
    fig0, ax0 = plt.subplots(figsize=(8,4))
    data0tot = np.array([d[key]['total_charge']/1000. for key in d.keys()])
    counts0tot, bins0tot = np.histogram(data0tot, bins=np.linspace(0,20,21))
    ax0.hist(bins0tot[:-1], bins=bins0tot, weights = counts0tot)
    ax0.set_xlabel('Total Charge [V]')
    ax0.set_ylabel('Count / V')
    ax0.set_title(r'Total Charge '+mc_title)
    plt.savefig(sample_type+"_selected_events_total_charge.png")
    plt.close(fig0)

    return