# Produce scripts to run dsarch commands for publishing to RDA
# Other information relevant to publishhing workflow is here:
# https://docs.google.com/document/d/1LB4F0hv713h4B_ABcXuUBgALcTufx_qGA1Rye5WKV3o/
# Authors: Teagan King, Adam Phillips

# DO THESE STEPS BEFORE RUNNING THIS SCRIPT:
# module load conda
# conda activate /glade/work/rdadata/conda-envs/pg-casper
import os

# SET PARAMETERS
dset = "d651028"
name = "CESM1-CAM5-DPLE" # This name will be used in combination with the child dataset keys on the RDA webpage

readme = "" # set to empty string if readme does not exist to be added to Documentation Tab
#readme = "README.md" # if README does exist, add name of file here

# TODO: eventually we'd like to include these features
# print_out_only = True # True = only print commands, False = execute command (batch job?)
# overwrite = True # This will ideally eventually be set to avoid overwriting existing files;
# warning: for now, please only use this tool if files with the same name do not yet exist
# commands to run certain script portions and not others

scratch_dir = "/glade/campaign/collections/rda/scratch/tking/"+dset+"/" # PLEASE CHANGE TO YOUR USERNAME!
if not os.path.exists(scratch_dir):
    os.mkdir(scratch_dir)

# This should be a dictionary of all child datasets.
# The key is concatenated with the name to provide the displayed name on RDA.
# The corresponding values are a list of [component, frequency, ensemble member].
# The corresponding values should also be the same as the names used in the directory structure
child_datasets = {'FOSI Ice Daily': ['ice','daily','FOSI'],
                  'FOSI Ice Monthly': ['ice','monthly','FOSI'],
                  'FOSI Ocean Daily': ['ocn','daily','FOSI'],
                  'FOSI Ocean Monthly': ['ocn','monthly','FOSI'],
                  'FOSI Ocean Yearly': ['ocn','yearly','FOSI'],
                  'Atmosphere 6-Hourly': ['atm','6-hourly',''],
                  'Atmosphere Daily': ['atm','daily',''],
                  'Atmosphere Monthly': ['atm','monthly',''],
                  'Ice Daily': ['ice','daily',''],
                  'Ice Monthly': ['ice','monthly',''],
                  'Land Daily': ['lnd','daily',''],
                  'Land Monthly': ['lnd','monthly',''],
                  'Ocean 5-Daily': ['ocn','5-daily',''],
                  'Ocean Monthly': ['ocn','daily',''],
                  'Ocean Yearly': ['ocn','yearly',''],
                  'River Runoff Daily': ['rof','daily',''],
                  'River Runoff Monthly': ['rof','monthly',''],
                 }
#--------------------------------------------------------------------------------------------------
# determine unique dataset numbers corresponding with each child dataset
for child in child_datasets:
    if child_datasets[child][2]=='FOSI':  # You may need to edit this bit to get unique numbers for every ensemble member # TODO could probably automate that
        ens_number = '1'
    elif child_datasets[child][2]=='':
        ens_number = '2'
    else:
        print(f"Warning: ens_number {child_datasets[child][2]} not found")

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
    else:
        print("Warning: comp_number not found")
    if child_datasets[child][1]=='daily':
        freq_number = '1'
    elif child_datasets[child][1]=='monthly':
        freq_number = '2'
    elif child_datasets[child][1]=='yearly':
        freq_number = '3'
    elif child_datasets[child][1]=='6-hourly':
        freq_number = '4'
    elif child_datasets[child][1]=='5-daily':
        freq_number = '5'
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
