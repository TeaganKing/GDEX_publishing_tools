import os

dataset_number = 'd651038'
rda_dir = '/glade/campaign/collections/rda/data'
data_dir = os.path.join(rda_dir,dataset_number)
file_with_duplicates = 'list_of_vars_containing_duplicates.txt'
clean_file = 'clean_list_of_vars.txt'
var_in_name = True # some datasets have variables listed in file names; others variables are directories

components=['atm', 'lnd', 'ice']  # Take out whatever components/frequencies don't exist, or clean up generated text files
frequencies=['day_1', 'month_1']

def write_directory_contents(data_dir, output_file, components, frequencies):
    """Writes the contents of a directory to a text file."""

    with open(output_file, "w") as f:
        for component in components:
            for frequency in frequencies:
                try:
                    f.write(component + ' ' + frequency + "\n")
                    for entry in os.listdir(os.path.join(data_dir,'f.c6.F1850.f19_f19.paleo_ppe.sst_m04k.ens251',component,'proc','tseries',frequency)):
                        if var_in_name:
                            if '.h0.' in entry:
                                entry = entry.split('.h0.')[1].split('.00')[0]
                            if '.h1.' in entry:
                                entry = entry.split('.h1.')[1].split('.00')[0]
                            if '.clm2.' in entry:
                                entry = entry.split('.clm2.')[1].split('.00')[0]
                            if '.h.' in entry:
                                entry = entry.split('.h.')[1].split('.00')[0]
                            else:
                                print("WARNING: MAKE SURE THIS ENTRY IS PROCESSED CORRECTLY:" + entry)
                        f.write(entry + "\n")
                except:
                    continue

def remove_duplicates(input_file, output_file):
    """Removes duplicate lines from a text file."""

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        seen_lines = set()
        for line in infile:
            if line not in seen_lines:
                outfile.write(line)
                seen_lines.add(line)

if __name__ == '__main__':
    write_directory_contents(data_dir, file_with_duplicates, components, frequencies)
    remove_duplicates(file_with_duplicates, clean_file)
  
