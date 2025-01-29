import os

dataset_number = 'd651028'
rda_dir = '/glade/campaign/collections/rda/data'
data_dir = os.path.join(rda_dir,dataset_number)
file_with_duplicates = 'list_of_vars_containing_duplicates.txt'
clean_file = 'clean_list_of_vars.txt'

components=['atm', 'ocn', 'lnd', 'ice', 'rof']
frequencies=['daily', 'hourly6', 'annual',  'daily5', 'monthly']

def write_directory_contents(data_dir, output_file, components, frequencies):
    """Writes the contents of a directory to a text file."""

    with open(output_file, "w") as f:
        for component in components:
            for frequency in frequencies:
                try:
                    for entry in os.listdir(os.path.join(data_dir,'CESM1-DPLE',component,'proc','tseries',frequency)):
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
  
