################################################################################
##                                                                            ##
##    CONTAINS: Script to check contents of output file from proton selection ##
##              being run over Bern Module Data.                              ##
##                                                                            ##
################################################################################

import h5py, glob, argparse
import numpy as np
import matplotlib.pyplot as plt

data_file = 'test_out.h5'#'test_two_tracks_allowed_pid.h5'#'test_out.h5'
data_h5 = h5py.File(data_file,'r')

print('FILE KEYS:', list(data_h5.keys()),'\n')
print('HIGH PURITY SEL KEYS:',list(data_h5['high_purity_sel'].keys()),'\n')
print('Proton Selection Event Summ Saved values:',list(data_h5['high_purity_sel']['protons']['sel_reco']['data'].dtype.names),'\n')

sel_mask = (data_h5['high_purity_sel']['protons']['sel_reco']['data']['sel'] == True)
ntracks_mask = (data_h5['high_purity_sel']['protons']['sel_reco']['data']['ntracks'] >= 1) & (data_h5['high_purity_sel']['protons']['sel_reco']['data']['ntracks'] <= 3)
event_mask = np.isin(data_h5['high_purity_sel']['protons']['sel_reco']['data']['event_id'], [7980, 10541, 1579, 3153, 3029])
pid_muon_mask = (data_h5['high_purity_sel']['protons']['sel_reco']['data']['pid_muon_proton'] < 0.)
pid_mip_mask = (data_h5['high_purity_sel']['protons']['sel_reco']['data']['pid_mip_proton'] < 0.)
print('Number of selected events:',len(data_h5['high_purity_sel']['protons']['sel_reco']['data'][sel_mask]),'\n')
print('Selected Events:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][sel_mask]['event_id'],'\n')
print('Number of tracks in Selected Events:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][sel_mask]['ntracks'],'\n')
print('Proton Log Likelihood Means:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][sel_mask]['proton_loglikelihood_mean'],'\n')
print('Muon Log Likelihood Means:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][sel_mask]['muon_loglikelihood_mean'],'\n')
print('MIP Log Likelihood Means:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][sel_mask]['mip_loglikelihood_mean'],'\n')
print('1-3 Tracks in FID (no sel):',data_h5['high_purity_sel']['protons']['sel_reco']['data'][ntracks_mask]['event_id'],'\n')
print('PID score muon proton:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][event_mask]['pid_muon_proton'],'\n')
print('PID score mip proton:',data_h5['high_purity_sel']['protons']['sel_reco']['data'][event_mask]['pid_mip_proton'],'\n')
print('PID muon proton', data_h5['high_purity_sel']['protons']['sel_reco']['data'][pid_muon_mask]['pid_muon_proton'],'\n')
print('PID mip proton', data_h5['high_purity_sel']['protons']['sel_reco']['data'][pid_mip_mask]['pid_mip_proton'],'\n')

