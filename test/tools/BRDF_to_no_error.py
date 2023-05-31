# coding: utf-8
"""
This code takes a BRDF-file with error columns and delete these error columns.
We need it for the test purposes.
"""

import core

# parameters
input_file = "../files/NH4-Jarosite_geo_corr_last.txt"
output_prefix = "_no_err"

# data_reading
data_reading_result = core.data_reading(input_file)
"""
data_reading_result has the next structure:
    [0] : file_header (list of str), 
    [1] : file_data (list of lists of floats)
    [2] : file_separator (str)
    [3] : accuracy_array (list of ints)
"""

output_data = ""
# header
for i, v in enumerate(data_reading_result[0]):
    if i != 5:
        output_data = output_data + v
    else:
        header_list = v.split(data_reading_result[2])
        for j, item in enumerate(header_list):
            if j == 0 or j % 2 != 0:
                output_data = output_data + item + (data_reading_result[2] if j != (len(header_list) - 2) else "")
# data
for line_number, line_value in enumerate(data_reading_result[1]): # data_reading_result[1] has indexes [line][column]
    for column_number, column_value in enumerate(line_value):
        if column_number == 0 or column_number % 2 != 0:
            output_data = output_data + f"{column_value:.{data_reading_result[3][column_number]}f}" + data_reading_result[2]
    output_data = output_data + "\n"
# saving
file_name = input_file[:input_file.rfind(".")] + f"{output_prefix}.txt"
with open(file_name, 'w+') as file_output:
    file_output.write(output_data)
