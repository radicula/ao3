"""
Little script to help process the output from ao3-stats
into something I can use in R

(ggplot is pretty)

Requires the file path as a command line argument.
"""

import csv
import json
import sys

def main():
    filepath = sys.argv[1]
    with open(filepath, 'r') as input_file:
        data = json.load(input_file)
    keys = data[0].keys()
    newfile = filepath.split('.')[0] + '.csv'
    with open(newfile, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


main()



