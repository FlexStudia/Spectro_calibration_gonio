# coding: utf-8

"""
    To run the test (with activated virtual environment):
        cd test
        python -m pytest
"""

# IMPORTS
import filecmp
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import core


# TESTS
# data_reading
def test_data_reading_recular_case(): # NaN are not included
    result = core.data_reading('files/data_reading.txt')
    assert len(result) == 4
    assert result[0] == ['some text here\n', 'column1 column2 column3\n']
    assert list(result[1]) == [[400.000000, 0.670180, 0.005378], [410.000000, 0.751126, 0.003947], [420.000000, 0.670180, 0.005378], [430.000000, 0.751126, 0.003947]]
    assert result[2] == "\t"
    assert result[3] == [6, 6, 6]


def test_data_reading_comma_separator(): # NaN are in the beginning, the separator is a ','
    result = core.data_reading('files/data_reading_comma.txt')
    assert len(result) == 4
    assert result[0] == []
    assert list(result[1]) == [[450.0, 0.670180, 0.005378], [460.0, 0.751126, 0.003947], [470.0, 0.670180, 0.005378], [480.0, 0.751126, 0.003947]]
    assert result[2] == ","
    assert result[3] == [6, 6, 6]


def test_data_reading_disparate_data(): # NaN are not only in the beginning, a differnt separator, some variable accuracy, text in the beggining
    result = core.data_reading('files/data_reading_special.txt')
    assert len(result) == 4
    assert result[0] == ['text\n', '25\t\t\t\n', 'Some text is here\n', 'Incidence\t0\t0\n', 'Emergence\t-70\t-60\n', 'Azimuth\t0\t0\n', 'column1 column2 column3\n']
    assert list(result[1]) == [[392.51, 0.6702, 0.006], [492.52, 0.7511, 0.004], [592.58, 0.6702, 0.005], [692.57, 0.7511, 0.004]]
    assert result[2] == ",  "
    assert result[3] == [2, 4, 3]


def test_data_reading_start_different_separators(): # an exception
    result = core.data_reading('files/data_reading_problem_separator.txt')
    assert result == "In the data there is text. Or the separator is not homogeneous."


def test_data_reading_start_text_in_data(): # an exception
    result = core.data_reading('files/data_reading_problem_text_in_data.txt')
    assert result == "In the data there is some text."


def test_data_reading_empty_file(): # an exception
    result = core.data_reading('files/data_reading_problem_empty.txt')
    assert result == "The file separator was not found."


# p_array_verif
def test_p_array_verif_regular_case():
    p_array = [670, 990, 1590]
    result = core.p_array_verif(p_array)
    assert result == "Ok"


def test_p_array_verif_non_zeros():
    p_array = [670, 990, 0]
    result = core.p_array_verif(p_array)
    assert result == "p values must be non-zero"


def test_p_array_verif_negative():
    p_array = [670, 990, -250]
    result = core.p_array_verif(p_array)
    assert result == "p values must be positive"


def test_p_array_verif_non_increasing():
    p_array = [670, 400, 990, 1590]
    result = core.p_array_verif(p_array)
    assert result == "p values must be increasing"


# points_to_p_intervals
def test_points_to_p_intervals_regular_case():
    p_array = [670, 990, 1590]
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    result = core.points_to_p_intervals(file_data, p_array)
    assert result == [(0, 27), (28, 59), (60, 119), (120, 329)]


def test_points_to_p_intervals_not_found():
    p_array = [670, 998, 1590]
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    result = core.points_to_p_intervals(file_data, p_array)
    assert result == "998 was not found among the wavelengths"


def test_points_to_p_intervals_empty():
    p_array = []
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    result = core.points_to_p_intervals(file_data, p_array)
    assert result == "at least one breakpoint is required"


# points_to_ref_intervals
def test_points_to_ref_intervals_regular_case():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 990
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == [False, False, True, False]


def test_points_to_ref_intervals_0():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 0
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == [True, False, False, False]


def test_points_to_ref_intervals_file_first_wlth():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 400
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == [True, False, False, False]


def test_points_to_ref_intervals_first():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 670
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == [False, True, False, False]


def test_points_to_ref_intervals_last():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 1590
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == [False, False, False, True]


def test_points_to_ref_intervals_not_in_the_data():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 390
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == "390 was not found among the wavelengths"


def test_points_to_ref_intervals_not_in_the_p_array():
    file_data = core.data_reading("files/points_to_intervals.txt")[1]
    p_intervals_list = [(0, 27), (28, 59), (60, 119), (120, 329)] # p_array = [670, 990, 1590]
    ref_p = 660
    result = core.points_to_ref_intervals(file_data, p_intervals_list, ref_p)
    assert result == "the reference p-value is not inside the list of p-values"


# f_calc
def test_f_calc_left():
    result = core.f_calc((440, 0.820929), (450, 0.826875), (460, 0.839151), (470, 0.846049), "left")
    assert result == 1.0070543039207178


def test_f_calc_right():
    result = core.f_calc((440, 0.820929), (450, 0.826875), (460, 0.839151), (470, 0.846049), "right")
    assert result == 0.992995110697354


# adjust_data
def test_adjust_data_demo_last():
    input_file = "files/demo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    assert adjusted_data[1].tolist() == [[1.0283743495559157, 1.0260465049965217, 1.025058162401424, 1]]
    assert adjusted_data[0][0] == [400, 0.6891959215853836, 0.0055305972519117145]
    assert adjusted_data[0][1] == [500, 0.8821816803973962, 0.00025915033608809077]
    assert adjusted_data[0][2] == [600, 0.868283201063148, 0.00028794481787565635]
    assert adjusted_data[0][3] == [660, 0.7147993577662771, 0.00027766107438009725]
    assert adjusted_data[0][4] == [670, 0.6903353603646916, 0.0003074839305172188]
    assert adjusted_data[0][5] == [680, 0.6687555649801279, 0.0007531181346674469]
    assert adjusted_data[0][6] == [690, 0.6500599716125862, 0.00036732464878875474]
    assert adjusted_data[0][7] == [800, 0.44745580268946816, 0.00039092371840367476]
    assert adjusted_data[0][8] == [900, 0.28437597118532093, 0.00010568279001464174]
    assert adjusted_data[0][9] == [980, 0.28390809397904254, 7.695348787473912e-05]
    assert adjusted_data[0][10] == [990, 0.2879589255807688, 0.00013133395263955478]
    assert adjusted_data[0][11] == [1000, 0.2922543326822699, 0.0007974952503483078]
    assert adjusted_data[0][12] == [1010, 0.2967943152835459, 0.0007821193779122864]
    assert adjusted_data[0][13] == [1200, 0.31868545739979065, 0.00023371326102752466]
    assert adjusted_data[0][14] == [1300, 0.37166661358167064, 0.0002326882028651232]
    assert adjusted_data[0][15] == [1400, 0.4646383638533174, 0.0005576316403463746]
    assert adjusted_data[0][16] == [1500, 0.2733225334808781, 0.0002439638426515389]
    assert adjusted_data[0][17] == [1580, 0.23214799721353768, 0.00042437407923418945]
    assert adjusted_data[0][18] == [1590, 0.2311526657378459, 0.00024498890081394033]
    assert adjusted_data[0][19] == [1600, 0.231508, 0.000257]
    assert adjusted_data[0][20] == [1610, 0.233214, 0.000355]
    assert adjusted_data[0][21] == [1700, 0.274384, 0.000182]
    assert adjusted_data[0][22] == [1800, 0.331339, 0.000262]
    assert adjusted_data[0][23] == [1900, 0.27726, 0.000203]
    assert adjusted_data[0][24] == [2000, 0.076533, 0.000373]


def test_adjust_data_demo_second():
    input_file = "files/demo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[1]
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    assert adjusted_data[1].tolist() == [[1.0032351209678902, 1.0009641819667896, 1, 0.9755543994277167]]
    assert adjusted_data[0][0] == [400, 0.6723481133702607, 0.005395398480565314]
    assert adjusted_data[0][1] == [500, 0.8606162194062159, 0.00025281525048390834]
    assert adjusted_data[0][2] == [600, 0.8470574967463349, 0.00028090583387100927]
    assert adjusted_data[0][3] == [660, 0.6973256581769982, 0.00027087348266133037]
    assert adjusted_data[0][4] == [670, 0.673459697884293, 0.0002999673011693992]
    assert adjusted_data[0][5] == [680, 0.6524074335581321, 0.0007347077095636235]
    assert adjusted_data[0][6] == [690, 0.6341688651985152, 0.00035834517714411067]
    assert adjusted_data[0][7] == [800, 0.43651747686317105, 0.0003813673533293468]
    assert adjusted_data[0][8] == [900, 0.2774242297813695, 0.00010309931074257933]
    assert adjusted_data[0][9] == [980, 0.2769677901143926, 7.507231364750921e-05]
    assert adjusted_data[0][10] == [990, 0.2809195967047975, 0.00012812341529174908]
    assert adjusted_data[0][11] == [1000, 0.28511, 0.000778]
    assert adjusted_data[0][12] == [1010, 0.289539, 0.000763]
    assert adjusted_data[0][13] == [1200, 0.310895, 0.000228]
    assert adjusted_data[0][14] == [1300, 0.362581, 0.000227]
    assert adjusted_data[0][15] == [1400, 0.45328, 0.000544]
    assert adjusted_data[0][16] == [1500, 0.266641, 0.000238]
    assert adjusted_data[0][17] == [1580, 0.226473, 0.000414]
    assert adjusted_data[0][18] == [1590, 0.225502, 0.000239]
    assert adjusted_data[0][19] == [1600, 0.22584864790271184, 0.0002507174806529232]
    assert adjusted_data[0][20] == [1610, 0.22751294370813552, 0.00034632181179683946]
    assert adjusted_data[0][21] == [1700, 0.26767651833257466, 0.00017755090069584444]
    assert adjusted_data[0][22] == [1800, 0.32323921915198023, 0.0002555952526500618]
    assert adjusted_data[0][23] == [1900, 0.27048221278532875, 0.0001980375430838265]
    assert adjusted_data[0][24] == [2000, 0.07466210485140144, 0.00036388179098653835]


def test_adjust_data_demo_first():
    input_file = "files/demo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[0]
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    assert adjusted_data[1].tolist() == [[1.0022687515118056, 1, 0.9990367467845902, 0.9746146935156611]]
    assert adjusted_data[0][0] == [400, 0.6717004718881818, 0.00539020134563049]
    assert adjusted_data[0][1] == [500, 0.8597872280656388, 0.000252571725380975]
    assert adjusted_data[0][2] == [600, 0.8462415658889568, 0.00028063525042330557]
    assert adjusted_data[0][3] == [660, 0.6966539569945712, 0.0002706125629081875]
    assert adjusted_data[0][4] == [670, 0.672810985664857, 0.0002996783567020299]
    assert adjusted_data[0][5] == [680, 0.651779, 0.000734]
    assert adjusted_data[0][6] == [690, 0.633558, 0.000358]
    assert adjusted_data[0][7] == [800, 0.436097, 0.000381]
    assert adjusted_data[0][8] == [900, 0.277157, 0.000103]
    assert adjusted_data[0][9] == [980, 0.276701, 0.000075]
    assert adjusted_data[0][10] == [990, 0.280649, 0.000128]
    assert adjusted_data[0][11] == [1000, 0.2848353668757545, 0.0007772505889984112]
    assert adjusted_data[0][12] == [1010, 0.28926010062726343, 0.0007622650377966424]
    assert adjusted_data[0][13] == [1200, 0.3105955293915951, 0.00022778037826688658]
    assert adjusted_data[0][14] == [1300, 0.36223174268590347, 0.00022678134152010198]
    assert adjusted_data[0][15] == [1400, 0.45284337658251905, 0.0005434759902508171]
    assert adjusted_data[0][16] == [1500, 0.26638415719938996, 0.00023777074573473248]
    assert adjusted_data[0][17] == [1580, 0.2262548491545465, 0.0004136012131688203]
    assert adjusted_data[0][18] == [1590, 0.22528478447341868, 0.00023876978248151706]
    assert adjusted_data[0][19] == [1600, 0.22563109846642365, 0.0002504759762335249]
    assert adjusted_data[0][20] == [1610, 0.22729379113356138, 0.0003459882161980597]
    assert adjusted_data[0][21] == [1700, 0.26741867806560116, 0.00017737987421985032]
    assert adjusted_data[0][22] == [1800, 0.3229278579347856, 0.00025534904970110324]
    assert adjusted_data[0][23] == [1900, 0.2702216699241522, 0.00019784678278367921]
    assert adjusted_data[0][24] == [2000, 0.07459018633883409, 0.0003635312806813416]


def test_adjust_data_demo_0():
    input_file = "files/demo.txt"
    p_array = [670, 990, 1590]
    ref_p = 0
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    assert adjusted_data[1].tolist() == [[1, 0.9977363840702571, 0.9967753112901698, 0.9724085401700572]]
    assert adjusted_data[0][0] == [400, 0.67018, 0.005378]
    assert adjusted_data[0][1] == [500, 0.857841, 0.000252]
    assert adjusted_data[0][2] == [600, 0.844326, 0.00028]
    assert adjusted_data[0][3] == [660, 0.695077, 0.00027]
    assert adjusted_data[0][4] == [670, 0.671288, 0.000299]
    assert adjusted_data[0][5] == [680, 0.6503036226729281, 0.0007323385059075687]
    assert adjusted_data[0][6] == [690, 0.632123868018784, 0.000357189625497152]
    assert adjusted_data[0][7] == [800, 0.4351098438838869, 0.00038013756233076795]
    assert adjusted_data[0][8] == [900, 0.27652962299976025, 0.00010276684755923648]
    assert adjusted_data[0][9] == [980, 0.2760746552086242, 7.483022880526927e-05]
    assert adjusted_data[0][10] == [990, 0.28001371845293355, 0.0001277102571609929]
    assert adjusted_data[0][11] == [1000, 0.2841906090019403, 0.0007754911921837522]
    assert adjusted_data[0][12] == [1010, 0.2886053268556445, 0.0007605395625143996]
    assert adjusted_data[0][13] == [1200, 0.30989246040355733, 0.00022726477097415873]
    assert adjusted_data[0][14] == [1300, 0.36141178914290106, 0.00022626799566286855]
    assert adjusted_data[0][15] == [1400, 0.4518183131016082, 0.0005422457693418524]
    assert adjusted_data[0][16] == [1500, 0.2657811657777222, 0.00023723252408706043]
    assert adjusted_data[0][17] == [1580, 0.22574269507381864, 0.0004126649788741303]
    assert adjusted_data[0][18] == [1590, 0.2247748262465559, 0.0002382292993983506]
    assert adjusted_data[0][19] == [1600, 0.2251203563176896, 0.0002499089948237047]
    assert adjusted_data[0][20] == [1610, 0.22677928528721972, 0.00034520503176037033]
    assert adjusted_data[0][21] == [1700, 0.266813344886021, 0.00017697835431095042]
    assert adjusted_data[0][22] == [1800, 0.32219687329140656, 0.000254771037524555]
    assert adjusted_data[0][23] == [1900, 0.2696099918475501, 0.0001973989336545216]
    assert adjusted_data[0][24] == [2000, 0.07442134280483499, 0.00036270838548343136]


# full test with the error columns
def test_f_array_calc_simple_0():
    input_file = "files/NH4-Jarosite_i0e20a0_c.txt.txt"
    p_array = [670, 990, 1590]
    ref_p = 0
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_corr.txt", "files/NH4-Jarosite_i0e20a0_c.txt_corr_0.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_log.txt", "files/NH4-Jarosite_i0e20a0_c.txt_log_0.txt")
    assert f_result == True


def test_full_simple_between():
    input_file = "files/NH4-Jarosite_i0e20a0_c.txt.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[1]
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_corr.txt", "files/NH4-Jarosite_i0e20a0_c.txt_corr_between.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_log.txt", "files/NH4-Jarosite_i0e20a0_c.txt_log_between.txt")
    assert f_result == True


def test_full_simple_last():
    input_file = "files/NH4-Jarosite_i0e20a0_c.txt.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 2
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_corr.txt", "files/NH4-Jarosite_i0e20a0_c.txt_corr_last.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_log.txt", "files/NH4-Jarosite_i0e20a0_c.txt_log_last.txt")
    assert f_result == True


def test_full_complet_0():
    input_file = "files/Phillipsite_powder_32-80_MF_VfNfc48.txt"
    p_array = [678, 998, 1598]
    ref_p = 0
    refl_cln = 4
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_corr.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_corr_0.txt")
    assert data_result == True
    f_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_log.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_log_0.txt")
    assert f_result == True


def test_full_complet_between():
    input_file = "files/Phillipsite_powder_32-80_MF_VfNfc48.txt"
    p_array = [678, 998, 1598]
    ref_p = p_array[1]
    refl_cln = 4
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_corr.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_corr_between.txt")
    assert data_result == True
    f_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_log.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_log_between.txt")
    assert f_result == True


def test_full_complet_last():
    input_file = "files/Phillipsite_powder_32-80_MF_VfNfc48.txt"
    p_array = [678, 998, 1598]
    ref_p = p_array[2]
    refl_cln = 4
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_corr.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_corr_last.txt")
    assert data_result == True
    f_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_log.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_log_last.txt")
    assert f_result == True


def test_full_BRDF_0():
    input_file = "files/NH4-Jarosite_geo.txt"
    p_array = [670, 990, 1590]
    ref_p = 0
    refl_cln = 'brdf'
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_geo_corr.txt", "files/NH4-Jarosite_geo_corr_0.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_geo_log.txt", "files/NH4-Jarosite_geo_log_0.txt")
    assert f_result == True


def test_full_BRDF_between():
    input_file = "files/NH4-Jarosite_geo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[1]
    refl_cln = 'brdf'
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_geo_corr.txt", "files/NH4-Jarosite_geo_corr_between.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_geo_log.txt", "files/NH4-Jarosite_geo_log_between.txt")
    assert f_result == True


def test_full_BRDF_last():
    input_file = "files/NH4-Jarosite_geo.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 'brdf'
    is_there_the_error_column = True
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_geo_corr.txt", "files/NH4-Jarosite_geo_corr_last.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_geo_log.txt", "files/NH4-Jarosite_geo_log_last.txt")
    assert f_result == True


# full test without any error column
def test_f_array_calc_simple_0_no_err():
    input_file = "files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"
    p_array = [670, 990, 1590]
    ref_p = 0
    refl_cln = 2
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_no_err_corr.txt", "files/NH4-Jarosite_i0e20a0_c.txt_corr_0_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_no_err_log.txt", "files/NH4-Jarosite_i0e20a0_c.txt_log_0_no_err.txt")
    assert f_result == True


def test_full_simple_between_no_err():
    input_file = "files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[1]
    refl_cln = 2
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_no_err_corr.txt", "files/NH4-Jarosite_i0e20a0_c.txt_corr_between_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_no_err_log.txt", "files/NH4-Jarosite_i0e20a0_c.txt_log_between_no_err.txt")
    assert f_result == True


def test_full_simple_last_no_err():
    input_file = "files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 2
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_no_err_corr.txt", "files/NH4-Jarosite_i0e20a0_c.txt_corr_last_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_i0e20a0_c.txt_no_err_log.txt", "files/NH4-Jarosite_i0e20a0_c.txt_log_last_no_err.txt")
    assert f_result == True


def test_full_complet_0_no_err():
    input_file = "files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"
    p_array = [678, 998, 1598]
    ref_p = 0
    refl_cln = 4
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_no_err_corr.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_corr_0_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_no_err_log.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_log_0_no_err.txt")
    assert f_result == True


def test_full_complet_between_no_err():
    input_file = "files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"
    p_array = [678, 998, 1598]
    ref_p = p_array[1]
    refl_cln = 4
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_no_err_corr.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_corr_between_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_no_err_log.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_log_between_no_err.txt")
    assert f_result == True


def test_full_complet_last_no_err():
    input_file = "files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"
    p_array = [678, 998, 1598]
    ref_p = p_array[2]
    refl_cln = 4
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_no_err_corr.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_corr_last_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("Phillipsite_powder_32-80_MF_VfNfc48_no_err_log.txt", "files/Phillipsite_powder_32-80_MF_VfNfc48_log_last_no_err.txt")
    assert f_result == True


def test_full_BRDF_0_no_err():
    input_file = "files/NH4-Jarosite_geo_no_err.txt"
    p_array = [670, 990, 1590]
    ref_p = 0
    refl_cln = 'brdf'
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_geo_no_err_corr.txt", "files/NH4-Jarosite_geo_corr_0_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_geo_no_err_log.txt", "files/NH4-Jarosite_geo_log_0_no_err.txt")
    assert f_result == True


def test_full_BRDF_between_no_err():
    input_file = "files/NH4-Jarosite_geo_no_err.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[1]
    refl_cln = 'brdf'
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_geo_no_err_corr.txt", "files/NH4-Jarosite_geo_corr_between_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_geo_no_err_log.txt", "files/NH4-Jarosite_geo_log_between_no_err.txt")
    assert f_result == True


def test_full_BRDF_last_no_err():
    input_file = "files/NH4-Jarosite_geo_no_err.txt"
    p_array = [670, 990, 1590]
    ref_p = p_array[2]
    refl_cln = 'brdf'
    is_there_the_error_column = False
    data_reading_result = core.data_reading(input_file)
    p_intrvals = core.points_to_p_intervals(data_reading_result[1], p_array)
    ref_intervals = core.points_to_ref_intervals(data_reading_result[1], p_intrvals, ref_p)
    adjusted_data = core.adjust_data(data_reading_result[1], refl_cln, p_intrvals, ref_intervals, is_there_the_error_column)
    core.data_export(input_file, data_reading_result[0], adjusted_data[0], data_reading_result[2], data_reading_result[3])
    core.f_export(input_file, data_reading_result[0], adjusted_data[1], data_reading_result[2], p_intrvals, data_reading_result[1])
    data_result = filecmp.cmp("NH4-Jarosite_geo_no_err_corr.txt", "files/NH4-Jarosite_geo_corr_last_no_err.txt")
    assert data_result == True
    f_result = filecmp.cmp("NH4-Jarosite_geo_no_err_log.txt", "files/NH4-Jarosite_geo_log_last_no_err.txt")
    assert f_result == True
