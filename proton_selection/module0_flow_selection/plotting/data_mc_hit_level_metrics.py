################################################################################
##                                                                            ##
##    CONTAINS: Script to plot contents in output file from proton selection  ##
##              being run over Bern Module Data.                              ##
##                                                                            ##
################################################################################

import h5py, glob, argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../../../common')
import file_parsing
from plot_hit_level_metrics import plot_hit_level_metrics 

def main(file_dir, is_mc):

    # initialize plotting datasets
    hit_level_dict = dict()

    if is_mc:
        sample_type = 'MC'
    else:
        sample_type = 'data'


    for file in glob.glob(file_dir+'/*.h5'): # Loop over files files

        f = h5py.File(file,'r')

        # Prepare datasets for plotting
        events = f['charge/events/data']
        tracks = f['combined/tracklets/data']
        tracks_ref = f['charge/events/ref/combined/tracklets/ref']
        tracks_region = f['charge/events/ref/combined/tracklets/ref_region']
        hits_trk_ref = f['combined/tracklets/ref/charge/hits/ref']
        hits_trk_region = f['combined/tracklets/ref/charge/hits/ref_region']
        hits_drift = f['combined/hit_drift/data']
        hits = f['charge/hits/data']
        hits_ref = f['charge/events/ref/charge/hits/ref']
        hits_region = f['charge/events/ref/charge/hits/ref_region']
        if not is_mc:
            charge_hits = f['combined/q_calib_el/data']
            charge_hits_ref = f['charge/events/ref/combined/q_calib_el/ref']
            charge_hits_region = f['charge/events/ref/combined/q_calib_el/ref_region']
        else:
            charge_hits = hits
            charge_hits_ref = hits_ref
            charge_hits_region = hits_region
        ext_trigs = f['charge/ext_trigs/data']
        ext_trigs_ref = f['charge/events/ref/charge/ext_trigs/ref']
        ext_trigs_region = f['charge/events/ref/charge/ext_trigs/ref_region']
        #print(sim_h5.keys(),'\n')
        sel_reco = f['high_purity_sel']['protons']['sel_reco']['data']
        if is_mc:
            sel_truth = f['high_purity_sel']['protons']['sel_reco']['data']
        
        print("File:", file)
        sel_mask = (sel_reco['sel'] == True)
        sel_event_ids = sel_reco[sel_mask]['event_id']
        print("Selected Event Ids:", sel_event_ids)
        if is_mc:
            sel_truth_mask = (sel_truth['sel'] == True)
            sel_truth_protons = sel_truth[sel_mask]['proton']
            sel_truth_sel = sel_truth[sel_truth_mask]['event_id']
            sel_pdg_mask = (sel_truth[sel_truth_mask]['pdg_id'] != 0)
            sel_truth_pdg = sel_truth[sel_truth_mask]['pdg_id'][sel_pdg_mask]
            print("Selected Proton?:", sel_truth_protons)
            print("Selected True?:", sel_truth_sel)
            print("Selected PDG IDs:", sel_truth_pdg)
            for event in sel_event_ids:
                event_sel_mask = f['high_purity_sel']['protons']['sel_truth']['data']['event_id'] == event
                zero_mask = f['high_purity_sel']['protons']['sel_truth']['data'][event_sel_mask]['pdg_id'] != 0.
                print('Selected event true PID:', f['high_purity_sel']['protons']['sel_truth']['data'][event_sel_mask]['pdg_id'][zero_mask], "| Event ID:", event)

        ### partition file by selected events
        sel_event_mask = np.isin(events['id'], sel_event_ids)
        #print("Events:", events[sel_event_mask])
        for event_id in sel_event_ids:

            charge_hit_ref = charge_hits_ref[charge_hits_region[int(event_id),'start']:charge_hits_region[int(event_id),'stop']]
            charge_hit_ref = np.sort(charge_hit_ref[charge_hit_ref[:,0] == event_id, 1])
            charge_hits_data = charge_hits[charge_hit_ref]['q']

            hit_level_dict[(file, event_id)]=dict(
                total_charge=int(sum(charge_hits_data))
            )
        
    ## Save all Python dictionaries to JSON files
    file_parsing.save_dict_to_json(hit_level_dict, sample_type+"hit_level_dict", True)


    # PLOT: Signal Event Info      
    plot_hit_level_metrics(hit_level_dict, is_mc)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--file_dir', default=None, required=True, type=str, \
                        help='''string corresponding to the path of the directory containing processed files for plotting''')
    parser.add_argument('-mc', '--is_mc', default=False, required=True, type=bool, \
                        help='''bool corresponding to whether files are simulation (MC) or data''')
    args = parser.parse_args()
    main(**vars(args))