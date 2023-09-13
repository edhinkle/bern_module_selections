################################################################################
##                                                                            ##
##    CONTAINS: Everything needed to run module0_evd.py.                      ##
##              Change data file and geometry file as needed. Can also change ##
##              charge threshold if desired.                                  ##
##                                                                            ##
################################################################################


import module0_evd

# File paths based on NERSC locations
file = '/global/cfs/cdirs/dune/www/data/Module1/reco/charge_only/events_2022_02_11_00_05_25_CET.gz.h5'
mc_file = '/global/cfs/cdirs/dune/www/data/Module1/sim/cosmics/reco/larndsim.30624.reco.h5'
geometry = '/global/cfs/cdirs/dune/www/data/Module1/TPC12/module1_layout-2.3.16.yaml'
test_evd = module0_evd.EventDisplay(filename=file, geometry_file=geometry, is_mc=False)