# Produce scripts to run dsarch commands for publishing to RDA
# Other information relevant to publishhing workflow is here:
# https://docs.google.com/document/d/1LB4F0hv713h4B_ABcXuUBgALcTufx_qGA1Rye5WKV3o/
# Authors: Teagan King, Adam Phillips

# DO THESE STEPS BEFORE RUNNING THIS SCRIPT:
# module load conda
# conda activate /glade/work/rdadata/conda-envs/pg-casper
import os

# TODO: eventually we'd like to include these features
# print_out_only = True # True = only print commands, False = execute command (batch job?)
# overwrite = True # This will ideally eventually be set to avoid overwriting existing files;
# warning: for now, please only use this tool if files with the same name do not yet exist
# commands to run certain script portions and not others

###############################################################################################################################
# SET PARAMETERS - UPDATE THIS SECTION!
dset = "d6510##"  # UPDATE # to be dataset number
name = "SOMETHING-LIKE-CESM1-CAM5-DPLE" # This name will be used in combination with the child dataset keys on the RDA webpage

readme = "" # set to empty string if readme does not exist to be added to Documentation Tab
#readme = "README.md" # if README does exist, add name of file here

username = 'tking' # PLEASE CHANGE TO YOUR USERNAME!

# UPDATE THESE VALUES WITH THE FORMAT THAT IS USED IN DIRECTORY STRUCTURE
# Note that it's okay to have some that are not used that are defined here; if they're not defined, it'll cause issues later...
ensemble_name='' # eg, 'FOSI'
day_freq_name = 'daily' # could change to 'day_1'
month_freq_name = 'monthly'  # could change to 'month_1'
hour6_freq_name = 'hourly6'  # could change to '6-hourly'
yearly_freq_name = 'yearly' # could change to 'annual'

# THIS SHOULD BE A DICTIONARY OF ALL CHILD DATASETS. IT NEEDS UPDATING FOR EACH DATASET
# The key (eg Atmoshperic daily) is concatenated with the name (eg CESM1-CAM5-DPLE) to provide the displayed name on RDA (eg CESM1-CAM5-DPLE Atmospheric daily).
# The corresponding values are a list of [component, frequency, ensemble member].
child_datasets = {ensemble_name+' Ice '+day_freq_name: ['ice',day_freq_name,ensemble_name],
                  ensemble_name+' Ice '+month_freq_name: ['ice',month_freq_name,ensemble_name],
                  'Atmosphere '+hour6_freq_name: ['atm',hour6_freq_name,''],  # ensemble member can be empty string if ensemble members are not relevant
                  'Atmosphere '+day_freq_name: ['atm',day_freq_name,''],
                  'Atmosphere '+month_freq_name: ['atm',month_freq_name,''],
                  'Ice '+day_freq_name: ['ice',day_freq_name,''],
                  'Ice '+month_freq_name: ['ice',month_freq_name,''],
                  'Land '+day_freq_name: ['lnd',day_freq_name,''],
                  'Land '+month_freq_name: ['lnd',month_freq_name,''],
                  'Ocean '+month_freq_name: ['ocn',month_freq_name,''],
                  'Ocean '+yearly_freq_name: ['ocn',yearly_freq_name,''],
                  'River Runoff '+day_freq_name: ['rof',day_freq_name,''],
                  'River Runoff '+month_freq_name: ['rof',month_freq_name,''],
                 }

ovewrite_child_dataset_with_ensembles = False  # Change to True if you want to use this feature!
ensemble_members_list=['....001', '.....002', '...003']

# DUPLICATE DRAFT DICTIONARY FOR EACH ENSEMBLE MEMBER IN THE ABOVE LIST IF ovewrite_child_dataset_with_ensembles is True
child_datasets_overwrite = {}
if ovewrite_child_dataset_with_ensembles:
    for base_key, base_val in child_datasets_pre_ensemble.items():
        for ensemble_member in ensemble_members_list:
            new_key = f"{base_key} {ensemble_member}"
            new_val = base_val[:-1] + [ensemble_member]  # Replace last item ('' placeholder)
            child_datasets_overwrite[new_key] = new_val
    child_datasets = child_datsets_overwrite

# USERS PROBABLY DON'T NEED TO EDIT ANYTHING BELOW THIS LINE
#############################################################################################################################
#--------------------------------------------------------------------------------------------------
scratch_dir = "/glade/campaign/collections/rda/scratch/"+username+"/"+dset+"/"
if not os.path.exists(scratch_dir):
    os.mkdir(scratch_dir)

# determine unique dataset numbers corresponding with each child dataset
for child in child_datasets:
    if ensemble_name == '':
        ens_number = ''
    if child_datasets[child][2][-3:]=='001':
        ens_number = '1'
    elif child_datasets[child][2][-3:]=='002':
        ens_number = '2'
    elif child_datasets[child][2][-3:]=='003':
        ens_number = '3'
    elif child_datasets[child][2][-3:]=='004':
        ens_number = '4'
    elif child_datasets[child][2][-3:]=='005':
        ens_number = '5'
    elif child_datasets[child][2][-3:]=='006':
        ens_number = '6'
    elif child_datasets[child][2][-3:]=='007':
        ens_number = '7'
    elif child_datasets[child][2][-3:]=='008':
        ens_number = '8'
    elif child_datasets[child][2][-3:]=='009':
        ens_number = '9'
    elif child_datasets[child][2][-3:]=='010':
        ens_number = '10'
    else:
        print(f"Warning: ens_number {child_datasets[child][2][-3:]} not found")
    
    if child_datasets[child][0]=='atm':
        comp_number = '1'
    elif child_datasets[child][0]=='ocn':
        comp_number = '2'
    elif child_datasets[child][0]=='lnd':
        comp_number = '3'
    elif child_datasets[child][0]=='ice':
        comp_number = '4'
    elif child_datasets[child][0]=='rof':
        comp_number = '5'
    elif child_datasets[child][0]=='glc':
        comp_number = '6'
    else:
        print("Warning: comp_number not found")
    if child_datasets[child][1]==day_freq_name:
        freq_number = '1'
    elif child_datasets[child][1]==month_freq_name:
        freq_number = '2'
    elif child_datasets[child][1]==yearly_freq_name:
        freq_number = '3'
    elif child_datasets[child][1]==hour6_freq_name:
        freq_number = '4'
    # IF YOU ADDED MORE FREQUENCY OPTIONS, INCLUDE THEM HERE
    else:
         print(f"Warning: freq_number {child_datasets[child][1]} not found")

    # include unique child number in dictionary of child datasets
    child_number = ens_number+comp_number+freq_number
    child_datasets[child].append(child_number)

#---------------------------------------------------------------------------------------------------
# produce <dataset>.gp file
# EXAMPLE:
#     Dataset<=>d651008
#     GroupIndex<:>GroupName<:>ParentIndex<:>Title<:>GroupPattern<:>BackupFlag<:>SavedPath<:>WebPath<:>
#     111<:>1_atm_6h<:>0<:> BRCP60 Member 1 Atmosphere 6-Hourly Files <:><:>P<:><:><:>
#     112<:>1_atm_d<:>0<:> BRCP60 Member 1 Atmosphere Daily Files <:><:>P<:><:><:>
#     113<:>1_atm_m<:>0<:> BRCP60 Member 1 Atmosphere Monthly Files <:><:>P<:><:><:>

with open(scratch_dir+dset+".gp", "w") as file:
    file.write("Dataset<=>{}\n".format(dset))
    file.write("GroupIndex<:>GroupName<:>ParentIndex<:>Title<:>GroupPattern<:>BackupFlag<:>SavedPath<:>WebPath<:>\n")
    for child in child_datasets:
        comp=child_datasets[child][0]
        freq=child_datasets[child][1]
        ens=child_datasets[child][2]
        number=child_datasets[child][3]
        file.write(f"{number}<:>{ens} {comp}_{freq}<:>0<:>{name} {child} Files<:><:>P<:><:><:>\n")

#--------------------------------------------------------------------------------------------------
# produce files (eg d651008.111) to hold list of files
# EXAMPLE:
#     Dataset<=>d651008
#     echo 'WebFile<:>'
for child in child_datasets:
    with open(scratch_dir+dset+"."+child_datasets[child][3], "w") as file:
        file.write(f"Dataset<=>{dset}\n")
        file.write("WebFile<:>\n")

#--------------------------------------------------------------------------------------------------
# produce list of find commands, to run from data directory eg
# EXAMPLE
#     find b.e13.BRCP60C5.ne120_t12.cesm-ihesp-hires1.0.46-2006-2100.010/atm/proc/tseries/hour_6/ -type f | awk '{print $1"<:>"}' >> /glade/campaign/collections/rda/scratch/tking/d651008/1011
#     find b.e13.BRCP60C5.ne120_t12.cesm-ihesp-hires1.0.46-2006-2100.010/atm/proc/tseries/day_1/ -type f | awk '{print $1"<:>"}' >> /glade/campaign/collections/rda/scratch/tking/d651008/1012
#     find b.e13.BRCP60C5.ne120_t12.cesm-ihesp-hires1.0.46-2006-2100.010/atm/proc/tseries/month_1/ -type f | awk '{print $1"<:>"}' >> /glade/campaign/collections/rda/scratch/tking/d651008/1013
#     add list of files to files above
with open(scratch_dir+"find_commands", "w") as file:
    for child in child_datasets:
        comp=child_datasets[child][0]
        freq=child_datasets[child][1]
        ens=child_datasets[child][2]
        number=child_datasets[child][3]
        file.write(f"find {ens}/{comp}/proc/tseries/{freq}/ -type f | awk '"+"{print $1"+'"'+"<:>"+'"'+"}'"+f" >> {scratch_dir}{dset}"+'.'+f"{number}\n")

#--------------------------------------------------------------------------------------------------
# produce list of dsarch commands to run from scratch directory as well as a few one-time commands to run
# EXAMPLE:
#     dsarch d651008 sw  -GI 1011 -LC G -IF d651008.1011 &
#     dsarch d651008 sw  -GI 1012 -LC G -IF d651008.1012 &
#     dsarch d651008 sw  -GI 1013 -LC G -IF d651008.1013 &
with open(scratch_dir+"dsarch_commands", "w") as file:
    # set up dataset groups (once per dataset)
    file.write(f"dsarch {dset} sg -IF {dset}.gp\n")
    # set dataset to published (once per dataset)
    file.write(f"dsarch {dset} sd -UD P\n")
    if readme != "":
        file.write(f"dsarch {dset} ah -ht D -df text -LF {readme}\n")
    for child in child_datasets:
        number=child_datasets[child][3]
        file.write(f"dsarch {dset} sw  -GI {number} -LC G -IF {dset}.{number} &\n")
