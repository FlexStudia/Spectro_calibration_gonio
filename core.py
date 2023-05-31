# coding: utf-8

"""
    Documentation
        Main links:
            * Forge: https://gricad-gitlab.univ-grenoble-alpes.fr/gonios-ipag/logiciels-gonios/-/issues/47

"""

# IMPORT
import re
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys


def data_reading(file_name):
    """
    Reads the input text file and separates the data
    :param file_name: file name with its path and extension
    :return: set of data chunks: file_header (list of str), file_data (list of lists of floats), file_separator (str), accuracy_array (list of ints)
    """
    try:
        # read the file
        file_content = []
        with open(file_name, "r", encoding="utf8") as file:
            file_content = file.readlines()
        # header, separator, body
        file_header = []
        file_separator = ""
        file_body = []
        body_started = False
        for index, line in enumerate(file_content):
            data_pattern = re.search(r'^(\d+\.?\d*)[ *\,*\t*]+\w', line)
            if data_pattern:
                if line.strip().lower().find('nan') == -1:
                    if not file_separator:
                        separator_pattern = re.findall(r'\d{1,}\.{0,1}\d{0,}', line.strip())
                        file_separator = line.strip()[len(separator_pattern[0]):line.strip().find(separator_pattern[1])]
                    if len(line.split(file_separator)) > 1:
                        file_body.append(line.strip())
                        body_started = True
            else:
                if body_started:
                    return "In the data there is some text."
                else:
                    file_header.append(line)
        if not file_separator:
            return "The file separator was not found."
        # accuracy
        accuracy_array = []
        for element in file_body[0].split(file_separator):
            if element.find(".") != -1:
                accuracy_array.append(len(element) - element.find(".") - 1)
            else:
                accuracy_array.append(0)
        # data
        file_data = np.zeros(len(file_body), dtype='object')
        index = 0
        for i, element in enumerate(file_body):
            temp_array = []
            for item in element.split(file_separator):
                try:
                    temp_array.append(float(item))
                except:
                    return "In the data there is text. Or the separator is not homogeneous."
            file_data[index] = temp_array
            index = index + 1
        return file_header, file_data, file_separator, accuracy_array
    except Exception as e:
        return str(e)


def p_array_verif(p_array):
    """
    Checks that all values of p are non-zero, positive, non-equal and increasing.
    :param p_array: list of p values
    :return: "Ok" or ValueError message
    """
    try:
        for i in range(len(p_array)):
            if p_array[i] == 0:
                return "p values must be non-zero"
            if p_array[i] < 0:
                return "p values must be positive"
            if i != 0 and p_array[i - 1] >= p_array[i]:
                return "p values must be increasing"
        return "Ok"
    except Exception as e:
        return str(e)


def points_to_p_intervals(file_data, p_list):
    """
    Searches for breakpoints (p_list) in the original spectral data (file_data) and returns line numbers pairs limiting the intervals between breakpoints.
    :param file_data: initial spectral data
    :param p_list: list of break points
    :return: list of tuples of line numbers limiting the intervals between breakpoints
    """
    try:
        if len(p_list) == 0:
            return "at least one breakpoint is required"
        interv_array_pnts = []
        p_previous = 0
        for i in range(0, len(p_list)):
            not_inside = True
            for j in range(0, len(file_data)):
                if file_data[j][0] == p_list[i]:
                    not_inside = False
                    interv_array_pnts.append((p_previous, j))
                    p_previous = j + 1
                    if i == len(p_list) - 1:
                        interv_array_pnts.append((j + 1, len(file_data) - 1))
                    break
            if not_inside:
                return f"{p_list[i]} was not found among the wavelengths"
        return interv_array_pnts
    except Exception as e:
        return str(e)


def points_to_ref_intervals(file_data, p_intervals_list, ref_p):
    """
    Transforms a list of points into a list of reference intervals
    :param p_list: list of break points
    :param ref_p: the lowest point of the reference intervals
    :return: list of reference intervals where True is used when an interval is the reference interval and False is used when it is not
    """
    try:
        ref_index = -1
        if ref_p == 0:
            ref_index = 0
        else:
            for i in range(0, len(file_data)):
                if file_data[i][0] == ref_p:
                    ref_index = i
                    break
            if ref_index == -1:
                return f"{ref_p} was not found among the wavelengths"
        ref_inside = False
        interv_array_refs = []
        if ref_index == 0:
            ref_inside = True
            interv_array_refs.append(True)
        else:
            interv_array_refs.append(False)
        for i in range(1, len(p_intervals_list)):
            if ref_index == p_intervals_list[i][0] - 1:
                interv_array_refs.append(True)
                ref_inside = True
            else:
                interv_array_refs.append(False)
        if not ref_inside:
            return "the reference p-value is not inside the list of p-values"
        return interv_array_refs
    except Exception as e:
        return str(e)


def f_calc(point_before_break, break_point, point_after_break_1, point_after_break_2, direction):
    """
    Calculates the multiplicative correction factor of tangent adjustment
    All points are tuples of wavelength and reflectance.
    :param point_before_break: wavelength and reflectance of the point just before the break point
    :param break_point: wavelength and reflectance of the break point
    :param point_after_break_1: wavelength and reflectance of the first point after the break point
    :param point_after_break_2: wavelength and reflectance of the second point after the break point
    :param direction: can be "left" or "right" to reference the position of the interval in relation to the reference interval
    :return:
    """
    try:
        # y (reflectance) value for the first point after the break
        p2_1 = point_after_break_1[1]
        # y (reflectance) value for the second point after the break
        p2_2 = point_after_break_2[1]
        # y (reflectance) value for the break point
        p1_n = break_point[1]
        # y (reflectance) value for the point before the break
        p1_n_1 = point_before_break[1]
        # x (wavelength) value for the first point after the break
        x2_1 = point_after_break_1[0]
        # x (wavelength) value for the second point after the break
        x2_2 = point_after_break_2[0]
        # x (wavelength) value for the break point
        x1_n = break_point[0]
        # x (wavelength) value for the point before the break
        x1_n_1 = point_before_break[0]
        f = (p2_1/(x2_1 - x1_n) - (p2_2 - p2_1)/(2*(x2_2 - x2_1)))/((p1_n - p1_n_1)/(2*(x1_n - x1_n_1)) + p1_n/(x2_1 - x1_n))
    except Exception as e:
        return str(e)
    if direction == "left":
        return f
    elif direction == "right":
        return 1 / f
    else:
        return "direction value must me left of right"


def adjust_data(file_data, column, interv_pnts, interv_refs, error_ajust=True):
    """
    Adjustes data
    :param file_data: the initial data
    :param column: the column with the data to adjust
    :param interv_pnts: points_to_p_intervals() result
    :param interv_refs: points_to_ref_intervals() result
    :param error_ajust: to adjust or not the error (in the column + 1)
    :return:set of two lists: the adjusted data and the grating f-coefficients
    """
    # BRDF
    try:
        adjusted_data = copy.deepcopy(file_data)
        ref_index = -1
        for i in range(0, len(interv_refs)):
            if interv_refs[i]:
                ref_index = i
                break
        if type(column) != str:
            start = column
            stop = column + 1
            step = 1
            f_array = np.zeros((1, len(interv_refs)))
            f_array[0][ref_index] = 1
        elif column.lower() == "brdf":
            start = 2
            stop = len(file_data[0]) + 1
            if error_ajust:
                step = 2
            else:
                step = 1
            f_array = np.zeros((int((stop - start) / step), len(interv_refs)))
            for i in range(0, int((stop - start) / step)):
                f_array[i][ref_index] = 1
        else:
            return "Column must be a number or brdf"
        k = 0
        for clmn in range(start, stop, step):
            # left
            for i in range(ref_index, 0, -1):
                break_point = [0] * 2
                break_point[0] = adjusted_data[interv_pnts[i - 1][1]][0]
                break_point[1] = adjusted_data[interv_pnts[i - 1][1]][clmn - 1]
                point_before_break = [0] * 2
                point_before_break[0] = adjusted_data[interv_pnts[i - 1][1] - 1][0]
                point_before_break[1] = adjusted_data[interv_pnts[i - 1][1] - 1][clmn - 1]
                point_after_break_1 = [0] * 2
                point_after_break_1[0] = adjusted_data[interv_pnts[i][0]][0]
                point_after_break_1[1] = adjusted_data[interv_pnts[i][0]][clmn - 1]
                point_after_break_2 = [0] * 2
                point_after_break_2[0] = adjusted_data[interv_pnts[i][0] + 1][0]
                point_after_break_2[1] = adjusted_data[interv_pnts[i][0] + 1][clmn - 1]
                f = f_calc(point_before_break, break_point, point_after_break_1, point_after_break_2, "left")
                f_array[k][i - 1] = f
                for j in range(0, len(file_data)):
                    if j >= interv_pnts[i - 1][0] and j <= interv_pnts[i - 1][1]:
                        adjusted_data[j][clmn - 1] = adjusted_data[j][clmn - 1] * f
                        if error_ajust:
                            adjusted_data[j][clmn] = adjusted_data[j][clmn] * f
            # right
            for i in range(ref_index, len(interv_refs) - 1):
                break_point = [0] * 2
                break_point[0] = adjusted_data[interv_pnts[i][1]][0]
                break_point[1] = adjusted_data[interv_pnts[i][1]][clmn - 1]
                point_before_break = [0] * 2
                point_before_break[0] = adjusted_data[interv_pnts[i][1] - 1][0]
                point_before_break[1] = adjusted_data[interv_pnts[i][1] - 1][clmn - 1]
                point_after_break_1 = [0] * 2
                point_after_break_1[0] = adjusted_data[interv_pnts[i + 1][0]][0]
                point_after_break_1[1] = adjusted_data[interv_pnts[i + 1][0]][clmn - 1]
                point_after_break_2 = [0] * 2
                point_after_break_2[0] = adjusted_data[interv_pnts[i + 1][0] + 1][0]
                point_after_break_2[1] = adjusted_data[interv_pnts[i + 1][0] + 1][clmn - 1]
                f = f_calc(point_before_break, break_point, point_after_break_1, point_after_break_2, "right")
                f_array[k][i + 1] = f
                for j in range(0, len(file_data)):
                    if j >= interv_pnts[i + 1][0] and j <= interv_pnts[i + 1][1]:
                        adjusted_data[j][clmn - 1] = adjusted_data[j][clmn - 1] * f
                        if error_ajust:
                            adjusted_data[j][clmn] = adjusted_data[j][clmn] * f
            k = k + 1
        return adjusted_data, f_array
    except Exception as e:
        return str(e)


def data_export(input_file_name, file_header, data_array, file_separator, accuracy_array):
    """
    Saves the adjusted data
    :param input_file_name: the name of initial file
    :param file_header: the header from the initial file
    :param data_array: the adjusted data
    :param file_separator: the separator from the initial file
    :param accuracy_array: the accuracy from the initial file
    :return: None
    """
    file_str = ""
    for item in file_header:
        file_str = file_str + item
    for line in data_array:
        for i in range(0, len(line)):
            pass
            file_str = file_str + f'{line[i]:.{accuracy_array[i]}f}' + file_separator
        file_str = file_str + "\n"
    with open(input_file_name[input_file_name.rfind("/") + 1:input_file_name.rfind(".")] + "_corr.txt", "w+", encoding="utf8") as s_file:
        s_file.write(file_str)


def f_export(input_file_name, file_header, f_array, file_separator, interv_pnts, file_data):
    """
    Saves the adjustment factors
    :param input_file_name: the name of initial file
    :param file_header: the header from the initial file
    :param f_array: the adjustment factors
    :param file_separator: the separator from the initial file
    :param interv_pnts: line numbers pairs limiting the intervals between breakpoints
    :param file_data: the initial data
    :return: None
    """
    data_header = f'Adjustment factors of the gratings in {input_file_name[input_file_name.rfind("/") + 1:]}\n'
    data_header = data_header + 'Gratings' + file_separator + 'Wavelengths_nm' + file_separator
    if len(f_array) == 1:
        data_header = data_header + "Factors\n"
    else:
        for i, v in enumerate(file_header[5].split(file_separator)):
            if "Refl" in v:
                data_header = data_header + f"f_{v[v.rfind('_') + 1:].strip()}" + file_separator
        data_header = data_header[0:-1]
        data_header = data_header + "\n"
    for i in range(len(f_array[0])):
        data_header = data_header + f'grating_{i + 1}' + file_separator + f'{file_data[interv_pnts[i][0]][0]}-{file_data[interv_pnts[i][1]][0]}' + file_separator
        for j in range(0, len(f_array)):
            data_header = data_header + f'{f_array[j][i]:.6f}' + ("" if j == len(f_array) - 1 else file_separator)
        data_header = data_header + "\n"
    # save
    with open(input_file_name[input_file_name.rfind("/") + 1:input_file_name.rfind(".")] + "_log.txt", 'w+') as file_output:
        file_output.write(data_header)


# PLOT
def data_plot(file_data, calc_data, column_number, file_name):
    """
    Plots the graph for the selected column of the initial and corrected data
    :param file_data: list with the initial data
    :param calc_data: list with the corrected data
    :param column_number: selected column
    :param file_name: the name of the initial file
    :return: None
    """
    fig, ax = plt.subplots()
    fig.suptitle(f'{file_name}, column {column_number}')
    wlth_array = []
    refl_array = []
    for line in file_data:
        wlth_array.append(float(line[0]))
        refl_array.append(float(line[column_number - 1]))
    ax.plot(wlth_array, refl_array, label='initial')
    wlth_array = []
    refl_array = []
    for line in calc_data:
        wlth_array.append(float(line[0]))
        refl_array.append(float(line[column_number - 1]))
    ax.plot(wlth_array, refl_array, label='calculated')
    plt.legend()
    ax.set_xlabel(f'Wavelength')
    ax.set_ylabel('Reflectance')
    plt.show()


def demo_f():
    """
    Demo for the program
    :return: prints, plots and saves the data
    """
    # INPUT examples
    input_file = "resources/NH4-Jarosite_geo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 'brdf'
    column_to_plot = 2
    is_there_the_error_column = True

    """input_file = "resources/Phillipsite_powder_32-80_MF_VfNfc48.txt"
    p_array = [678, 998, 1598]
    ref_p = p_array[2]
    refl_cln = 4
    is_there_the_error_column = True"""

    """input_file = "resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e20a0_c.txt.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 2
    is_there_the_error_column = True"""

    """input_file = "test/files/demo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 2
    is_there_the_error_column = True"""

    # CALCS
    data_reading_result = data_reading(input_file)
    if type(data_reading_result) == str:
        print(data_reading_result)
    file_header = data_reading_result[0]
    initial_data = data_reading_result[1]
    file_separator = data_reading_result[2]
    accuracy_array = data_reading_result[3]
    verif_p = p_array_verif(p_array)
    if verif_p == "Ok":
        p_intrvals = points_to_p_intervals(initial_data, p_array)
        if type(p_intrvals) == str:
            print("points_to_p_intervals error: ", p_intrvals)
        else:
            ref_intervals = points_to_ref_intervals(initial_data, p_intrvals, ref_p)
            if type(ref_intervals) == str:
                print("points_to_ref_intervals: ", ref_intervals)
            else:
                adjusted_data = adjust_data(initial_data, refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
                if type(adjusted_data) == str:
                    print("adjust_data error: ", adjusted_data)
                else:
                    # result printing:
                    print("f-factor array:", adjusted_data[1], "\n")
                    print("adjusted data array:", adjusted_data[0], "\n")
                    # plot the initial and the adjusted data
                    if refl_cln == "brdf":
                        data_plot(initial_data, adjusted_data[0], column_to_plot, input_file)
                    else:
                        data_plot(initial_data, adjusted_data[0], refl_cln, input_file)
                    # adjusted data export
                    data_export(input_file, file_header, adjusted_data[0], file_separator, accuracy_array)
                    f_export(input_file, file_header, adjusted_data[1], file_separator, p_intrvals, initial_data)
    else:
        print(verif_p)


#demo_f()
