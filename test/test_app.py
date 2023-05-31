# coding: utf-8

"""
    To run the test (with activated virtual environment):
        cd test
        python -m pytest
"""

# IMPORTS
from PyQt5.QtWidgets import QApplication
import filecmp
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import app
# test QApp
test_app = QApplication(sys.argv)


# TESTS
# individual functions tests
def test_last_dir():
    win = app.DecalCorr()

    # exists
    str_path = "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev"
    result = win.last_dir(str_path)
    assert result == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev"

    # doesn't exist: 1 level
    str_path = "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/some_path"
    result = win.last_dir(str_path)
    assert result == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev"

    # doesn't exist: 3 level
    str_path = "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/some_path1/some_path2/some_path3"
    result = win.last_dir(str_path)
    assert result == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev"

    # doesn't exist: at all
    str_path = "Z:"
    result = win.last_dir(str_path)
    assert result == ""

    # doesn't exist: empty
    str_path = ""
    result = win.last_dir(str_path)
    assert result == ""


def test_file_ui():
    win = app.DecalCorr()

    # one file
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]
    win.file_select(str_paths)
    assert app.settings.value("data_dir") == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files"
    assert win.files == ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]
    assert win.ui.lbl_f.text() == "NH4-Jarosite_geo.txt"
    assert win.open_dir == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files"

    # a few files
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e20a0_c.txt.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e-20a0_c.txt.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e40a0_c.txt.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i60e20a0_c.txt.txt"]
    win.file_select(str_paths)
    assert app.settings.value("data_dir") == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c"
    assert win.files == ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e20a0_c.txt.txt",
                         "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e-20a0_c.txt.txt",
                         "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e40a0_c.txt.txt",
                         "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i60e20a0_c.txt.txt"]
    assert win.ui.lbl_f.text() == "4 files in NH4-Jarosite_iea0_c"
    assert win.open_dir == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c"



def test_file_dell():
    win = app.DecalCorr()

    # one file
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]
    win.file_select(str_paths)
    win.file_dell()
    assert app.settings.value("data_dir") == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files"
    assert win.files == ""
    assert win.ui.lbl_f.text() == "no file selected"
    assert win.open_dir == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files"

    # a few files
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e20a0_c.txt.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e-20a0_c.txt.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i0e40a0_c.txt.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c/NH4-Jarosite_i60e20a0_c.txt.txt"]
    win.file_select(str_paths)
    win.file_dell()
    assert app.settings.value("data_dir") == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c"
    assert win.files == ""
    assert win.ui.lbl_f.text() == "no file selected"
    assert win.open_dir == "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/resources/NH4-Jarosite_iea0_c"


"""
    Possible combinations:
        - one data file / a few data files
        - 4 types
        - free format for each of 3 other types
        - error column / no error column
        - breakpoints from a file or not (1 to 7 of them)
        - all possible reference ranges (from 2)
    What to compare:
        - exported result
        -exported log
    For the memory:
        unit_set = ('free format', 'BRDF data', 'full data', '3-col. data')
"""


# general tests
def test_general_test():
    win = app.DecalCorr()

    # one file, free format (BRDF, one column), error, file breakpoints, 7 points, ranges from 1 to 8
    # 71
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"] # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0) # free format
    win.ui.sb_refl_c.setValue(2) # column 2
    win.ui.chb_erro_c.setChecked(True) # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/71.txt") # 7 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p1_p2.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [True, False, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0029
    assert win.ui.dsb_p8.value() == 0.8643
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_err_71_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_err_71_log.txt")
    assert result == True

    # 72
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/72.txt")  # 7 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, True, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0115
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9385
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_72_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_72_log.txt")
    assert result == True

    # 73
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(6)  # column 6
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/73.txt")  # 7 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p2_p3.isChecked() == True
    assert win.ui.check_p6_p7.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9995
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p8.value() == 1.0101
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_6_err_73_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_6_err_73_log.txt")
    assert result == True

    # 74
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(8)  # column 8
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/74.txt")  # 7 points, range 4
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0211
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.8884
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_8_err_74_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_8_err_74_log.txt")
    assert result == True

    # 75
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(10)  # column 10
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/75.txt")  # 7 points, range 5
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1_p2.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0410
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p8.value() == 1.0205
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_10_err_75_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_10_err_75_log.txt")
    assert result == True

    # 76
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(12)  # column 12
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/76.txt")  # 7 points, range 6
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.1439
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9677
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_12_err_76_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_12_err_76_log.txt")
    assert result == True

    # 77
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(14)  # column 14
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/77.txt")  # 7 points, range 7
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p4_p5.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 2.7908
    assert win.ui.dsb_p7.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9659
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_14_err_77_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_14_err_77_log.txt")
    assert result == True

    # 78
    # set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(16)  # column 14
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/78.txt")  # 7 points, range 8
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p6_p7.isChecked() == False
    assert win.ui.check_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.1487
    assert win.ui.dsb_p4.value() == 1.0830
    assert win.ui.dsb_p8.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_16_err_78_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_16_err_78_log.txt")
    assert result == True

    # one file, free format (BRDF, one column), error, not file breakpoints, 6 points, ranges 1 to 7
    # 61
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(18)  # column 18
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 1
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)  # we set this manually as we bypass it
    win.ui.check_p1.setChecked(True)
    win.ui.check_p7.setChecked(False)  # we set this manually as we bypass check_toggle here
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [True, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9511
    assert win.ui.dsb_p7.value() == 0.9354
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_18_err_61_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_18_err_61_log.txt")
    assert result == True

    # 62
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(20)  # column 20
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 2
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p1.setChecked(False)
    win.ui.check_p1_p2.setChecked(True)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9949
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0900
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_20_err_62_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_20_err_62_log.txt")
    assert result == True

    # 63
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(22)  # column 22
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 3
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p1_p2.setChecked(False)
    win.ui.check_p2_p3.setChecked(True)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0053
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p7.value() == 0.9911
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_22_err_63_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_22_err_63_log.txt")
    assert result == True

    # 64
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(24)  # column 24
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 4
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p2_p3.setChecked(False)
    win.ui.check_p3_p4.setChecked(True)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0224
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0999
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_24_err_64_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_24_err_64_log.txt")
    assert result == True

    # 65
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(26)  # column 26
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 5
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p3_p4.setChecked(False)
    win.ui.check_p4_p5.setChecked(True)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0147
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p7.value() == 0.8594
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_26_err_65_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_26_err_65_log.txt")
    assert result == True

    # 66
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(28)  # column 28
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 6
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p4_p5.setChecked(False)
    win.ui.check_p5_p6.setChecked(True)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.8802
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0038
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_28_err_66_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_28_err_66_log.txt")
    assert result == True

    # 67
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(30)  # column 30
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 6 points, range 7
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(2830)
    win.ui.dsb_p_6.setValue(3170)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p5_p6.setChecked(False)
    win.ui.check_p6_p7.setChecked(True)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9487
    assert win.ui.dsb_p2.value() == 0.9110
    assert win.ui.dsb_p7.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_30_err_67_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_30_err_67_log.txt")
    assert result == True

    # one file, free format (BRDF, one column), no error, file breakpoints, 5 points, ranges 1 to 6
    # 51
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/51.txt")  # 5 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [True, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9874
    assert win.ui.dsb_p6.value() == 0.8600
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_51_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_51_log.txt")
    assert result == True

    # 52
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(3)  # column 3
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/52.txt")  # 5 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0115
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p6.value() == 0.9228
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_3_noerr_52_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_3_noerr_52_log.txt")
    assert result == True

    # 53
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/53.txt")  # 5 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p2_p3.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9995
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0259
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_53_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_53_log.txt")
    assert result == True

    # 54
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(5)  # column 5
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/54.txt")  # 5 points, range 4
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0211
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p6.value() == 0.8820
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_5_noerr_54_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_5_noerr_54_log.txt")
    assert result == True

    # 55
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(6)  # column 6
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/55.txt")  # 5 points, range 5
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1_p2.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0410
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0398
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_6_noerr_55_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_6_noerr_55_log.txt")
    assert result == True

    # 56
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(7)  # column 7
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/56.txt")  # 5 points, range 6
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.1439
    assert win.ui.dsb_p3.value() == 1.1842
    assert win.ui.dsb_p6.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_7_noerr_56_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_7_noerr_56_log.txt")
    assert result == True

    # one file, free format (BRDF, one column), no error, not file breakpoints, 4 points, range 1 to 5
    # 41
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(8)  # column 8
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 4 points, range 1
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(0)
    win.ui.dsb_p_6.setValue(0)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p1.setChecked(True)
    win.ui.check_p5_p6.setChecked(False)
    win.ui.check_p6_p7.setChecked(False)
    win.ui.check_p7.setChecked(False)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 0.9769
    assert win.ui.dsb_p5.value() == 0.9543
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_8_noerr_41_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_8_noerr_41_log.txt")
    assert result == True

    # 42
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(9)  # column 9
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 4 points, range 2
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(0)
    win.ui.dsb_p_6.setValue(0)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p1.setChecked(False)
    win.ui.check_p1_p2.setChecked(True)
    win.ui.check_p5_p6.setChecked(False)
    win.ui.check_p6_p7.setChecked(False)
    win.ui.check_p7.setChecked(False)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9995
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9419
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_9_noerr_42_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_9_noerr_42_log.txt")
    assert result == True

    # 43
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(10)  # column 10
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 4 points, range 3
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(0)
    win.ui.dsb_p_6.setValue(0)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p1_p2.setChecked(False)
    win.ui.check_p2_p3.setChecked(True)
    win.ui.check_p5_p6.setChecked(False)
    win.ui.check_p6_p7.setChecked(False)
    win.ui.check_p7.setChecked(False)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0966
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p5.value() == 1.0368
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_10_noerr_43_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_10_noerr_43_log.txt")
    assert result == True

    # 44
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(11)  # column 11
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 4 points, range 4
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(0)
    win.ui.dsb_p_6.setValue(0)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p2_p3.setChecked(False)
    win.ui.check_p3_p4.setChecked(True)
    win.ui.check_p5_p6.setChecked(False)
    win.ui.check_p6_p7.setChecked(False)
    win.ui.check_p7.setChecked(False)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0217
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p5.value() == 1.0001
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_11_noerr_44_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_11_noerr_44_log.txt")
    assert result == True

    # 45
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(12)  # column 12
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints set up
    # 4 points, range 5
    win.ui.dsb_p_1.setValue(670)
    win.ui.dsb_p_2.setValue(990)
    win.ui.dsb_p_3.setValue(1590)
    win.ui.dsb_p_4.setValue(2050)
    win.ui.dsb_p_5.setValue(0)
    win.ui.dsb_p_6.setValue(0)
    win.ui.dsb_p_7.setValue(0)
    win.ui.check_p3_p4.setChecked(False)
    win.ui.check_p4_p5.setChecked(True)
    win.ui.check_p5_p6.setChecked(False)
    win.ui.check_p6_p7.setChecked(False)
    win.ui.check_p7.setChecked(False)
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0231
    assert win.ui.dsb_p4.value() == 1.0011
    assert win.ui.dsb_p5.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_12_noerr_45_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_12_noerr_45_log.txt")
    assert result == True

    # one file, free format (full), error, file breakpoints, 3 points, ranges 1 to 4
    # 31
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/31.txt")  # 3 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0028
    assert win.ui.dsb_p4.value() == 1.0018
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_31_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_31_log.txt")
    assert result == True

    # 32
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/32.txt")  # 3 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9989
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_32_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_32_log.txt")
    assert result == True

    # 33
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/33.txt")  # 3 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p2_p3.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9989
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_33_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_33_log.txt")
    assert result == True

    # 34
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/34.txt")  # 3 points, range 4
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9982
    assert win.ui.dsb_p3.value() == 1.0011
    assert win.ui.dsb_p4.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_34_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_err_34_log.txt")
    assert result == True

    # one file, free format (full), no error, file breakpoints, 2 points, ranges 1 to 3
    # 21
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/21.txt")  # 2 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0028
    assert win.ui.dsb_p3.value() == 1.0028
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_21_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_21_log.txt")
    assert result == True

    # 22
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/22.txt")  # 2 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_22_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_22_log.txt")
    assert result == True

    # 23
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/23.txt")  # 2 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1_p2.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_23_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_4_noerr_23_log.txt")
    assert result == True

    # one file, free format (3 columns), error, file breakpoints, 1 point, ranges 1 to 2
    # 11
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/11.txt")  # 1 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p1_p2.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670]
    assert win.ref_intervals == [True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 0.9977
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_err_11_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_err_11_log.txt")
    assert result == True

    # 12
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/12.txt")  # 1 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670]
    assert win.ref_intervals == [False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_err_12_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_err_12_log.txt")
    assert result == True

    # one file, free format (3 columns), no error, file breakpoints, 2 points, ranges 1 to 3
    # 21
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/21.txt")  # 2 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p1_p2.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 0.9977
    assert win.ui.dsb_p3.value() == 0.9968
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_21_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_21_log.txt")
    assert result == True

    # 22
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/22.txt")  # 2 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p3.value() == 0.9990
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_22_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_22_log.txt")
    assert result == True

    # 23
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free format
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/23.txt")  # 2 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0032
    assert win.ui.dsb_p2.value() == 1.0010
    assert win.ui.dsb_p3.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_23_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/free_2_noerr_23_log.txt")
    assert result == True

    # one file, BRDF, error, file breakpoints, 3 points, ranges 1 to 4
    # 31
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/31.txt")  # 3 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0029
    assert win.ui.dsb_p4.value() == 0.9874
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_31_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_31_log.txt")
    assert result == True

    # 32
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/32.txt")  # 3 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9846
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_32_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_32_log.txt")
    assert result == True

    # 33
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/33.txt")  # 3 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9799
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9676
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_33_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_33_log.txt")
    assert result == True

    # 34
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/34.txt")  # 3 points, range 4
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0127
    assert win.ui.dsb_p3.value() == 1.0335
    assert win.ui.dsb_p4.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_34_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_err_34_log.txt")
    assert result == True

    # one file, BRDF, no error, file breakpoints, 4 points, ranges 1 to 5
    # 41
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/41.txt")  # 4 points, range 1
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0205
    assert win.ui.dsb_p5.value() == 0.9726
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_41_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_41_log.txt")
    assert result == True

    # 42
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/42.txt")  # 4 points, range 2
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9698
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_42_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_42_log.txt")
    assert result == True

    # 43
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/43.txt")  # 4 points, range 3
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p2_p3.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9799
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9530
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_43_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_43_log.txt")
    assert result == True

    # 44
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/44.txt")  # 4 points, range 4
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0127
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9850
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_44_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_44_log.txt")
    assert result == True

    # 45
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_geo_no_err.txt"]  # one file, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf format
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/45.txt")  # 4 points, range 5
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0282
    assert win.ui.dsb_p4.value() == 1.0153
    assert win.ui.dsb_p5.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_45_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/brdf_noerr_45_log.txt")
    assert result == True

    # one file, full, error, file breakpoints, 5 points, ranges 1 to 6
    # 51
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/51.txt")  # 5 points, range 1
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p4_p5.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 1.0018
    assert win.ui.dsb_p6.value() == 1.0779
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_51_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_51_log.txt")
    assert result == True

    # 52
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/52.txt")  # 5 points, range 2
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0749
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_52_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_52_log.txt")
    assert result == True

    # 53
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/53.txt")  # 5 points, range 3
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0749
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_53_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_53_log.txt")
    assert result == True

    # 54
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/54.txt")  # 5 points, range 4
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9982
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0760
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_54_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_54_log.txt")
    assert result == True

    # 55
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/55.txt")  # 5 points, range 5
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9984
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0762
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_55_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_55_log.txt")
    assert result == True

    # 56
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/56.txt")  # 5 points, range 6
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9277
    assert win.ui.dsb_p4.value() == 0.9293
    assert win.ui.dsb_p6.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_56_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_err_56_log.txt")
    assert result == True

    # one file, full, no error, file breakpoints, 6 points, ranges 1 to 7
    # 61
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/61.txt")  # 6 points, range 1
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p5_p6.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [True, False, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 1.0018
    assert win.ui.dsb_p7.value() == 1.1064
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_61_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_61_log.txt")
    assert result == True

    # 62
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/62.txt")  # 6 points, range 2
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, True, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1032
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_62_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_62_log.txt")
    assert result == True

    # 63
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/63.txt")  # 6 points, range 3
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1033
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_63_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_63_log.txt")
    assert result == True

    # 64
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/64.txt")  # 6 points, range 4
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9982
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1044
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_64_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_64_log.txt")
    assert result == True

    # 65
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/65.txt")  # 6 points, range 5
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9984
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1046
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_65_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_65_log.txt")
    assert result == True

    # 66
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/66.txt")  # 6 points, range 6
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9277
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0264
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_66_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_66_log.txt")
    assert result == True

    # 67
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/Phillipsite_powder_32-80_MF_VfNfc48_no_err.txt"]  # one file, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/67.txt")  # 6 points, range 7
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9039
    assert win.ui.dsb_p3.value() == 0.9064
    assert win.ui.dsb_p7.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_67_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/full_noerr_67_log.txt")
    assert result == True

    # one file, 3 columns, error, file breakpoints, 7 points, ranges 1 to 8
    # 71
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/71.txt")  # 7 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p6_p7.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [True, False, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 0.9968
    assert win.ui.dsb_p8.value() == 0.9833
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_71_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_71_log.txt")
    assert result == True

    # 72
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/72.txt")  # 7 points, range 2
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, True, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9855
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_72_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_72_log.txt")
    assert result == True

    # 73
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/73.txt")  # 7 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0032
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9864
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_73_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_73_log.txt")
    assert result == True

    # 74
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/74.txt")  # 7 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0284
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p8.value() == 1.0112
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_74_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_74_log.txt")
    assert result == True

    # 75
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/75.txt")  # 7 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0380
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p8.value() == 1.0207
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_75_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_75_log.txt")
    assert result == True

    # 76
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/76.txt")  # 7 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9983
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9816
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_76_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_76_log.txt")
    assert result == True

    # 77
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/77.txt")  # 7 points, range 7
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9906
    assert win.ui.dsb_p7.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9740
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_77_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_77_log.txt")
    assert result == True

    # 78
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/78.txt")  # 7 points, range 8
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0170
    assert win.ui.dsb_p4.value() == 0.9890
    assert win.ui.dsb_p8.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_78_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_err_78_log.txt")
    assert result == True

    # one file, 3 columns, no error, file breakpoints, 6 points, ranges 1 to 7
    # 61
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/61.txt")  # 6 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p4_p5.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [True, False, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9724
    assert win.ui.dsb_p7.value() == 1.0095
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_61_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_61_log.txt")
    assert result == True

    # 62
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/62.txt")  # 6 points, range 2
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p4_p5.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, True, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0118
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_62_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_62_log.txt")
    assert result == True

    # 63
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/63.txt")  # 6 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p2_p3.isChecked() == True
    assert win.ui.check_p4_p5.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0032
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0128
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_63_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_63_log.txt")
    assert result == True

    # 64
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/64.txt")  # 6 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p3_p4.isChecked() == True
    assert win.ui.check_p4_p5.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0284
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0382
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_64_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_64_log.txt")
    assert result == True

    # 65
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/65.txt")  # 6 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p3_p4.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0380
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0479
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_65_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_65_log.txt")
    assert result == True

    # 66
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/66.txt")  # 6 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p3_p4.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9983
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0078
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_66_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_66_log.txt")
    assert result == True

    # 67
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/NH4-Jarosite_i0e20a0_c.txt_no_err.txt"]  # one file, 3 columns
    win.ui.cb_f_type.setCurrentIndex(3)  # simple
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/67.txt")  # 6 points, range 7
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p3_p4.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9906
    assert win.ui.dsb_p4.value() == 0.9632
    assert win.ui.dsb_p7.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_67_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/log.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/simple_noerr_67_log.txt")
    assert result == True

    # a few files, free format (BRDF, one column), error, file breakpoints, 5 points, ranges 1 to 6
    # 51
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/51.txt")  # 5 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9874
    assert win.ui.dsb_p6.value() == 0.8600
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/51/5_cal-grating.txt")
    assert result == True

    # 52
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/52.txt")  # 5 points, range 2
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0115
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p6.value() == 0.9228
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/52/5_cal-grating.txt")
    assert result == True

    # 53
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(6)  # column 6
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/53.txt")  # 5 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p2_p3.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9995
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0259
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/53/5_cal-grating.txt")
    assert result == True

    # 54
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(8)  # column 8
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/54.txt")  # 5 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0211
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p6.value() == 0.8820
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/54/5_cal-grating.txt")
    assert result == True

    # 55
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(10)  # column 10
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/55.txt")  # 5 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0410
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0398
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/55/5_cal-grating.txt")
    assert result == True

    # 56
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(12)  # column 12
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/56.txt")  # 5 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p2_p3.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.1439
    assert win.ui.dsb_p3.value() == 1.1842
    assert win.ui.dsb_p6.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_err/56/5_cal-grating.txt")
    assert result == True

    # a few files, free format (BRDF, one column), no error, file breakpoints, 4 points, ranges 1 to 5
    # 41
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/41.txt")  # 4 points, range 1
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0205
    assert win.ui.dsb_p5.value() == 0.9726
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/41/5_cal-grating.txt")
    assert result == True

    # 42
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(3)  # column 3
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/42.txt")  # 4 points, range 2
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0115
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p5.value() == 1.0104
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/42/5_cal-grating.txt")
    assert result == True

    # 43
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/43.txt")  # 4 points, range 3
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1_p2.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9995
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9771
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/43/5_cal-grating.txt")
    assert result == True

    # 44
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(5)  # column 5
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/44.txt")  # 4 points, range 4
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1_p2.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0211
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9953
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/44/5_cal-grating.txt")
    assert result == True

    # 45
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(6)  # column 6
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/45.txt")  # 4 points, range 5
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1_p2.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0410
    assert win.ui.dsb_p3.value() == 1.0349
    assert win.ui.dsb_p5.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/freeBRDF_noerr/45/5_cal-grating.txt")
    assert result == True

    # a few files, free format (full), error, file breakpoints, 3 points, ranges 1 to 4
    # 31
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/31.txt")  # 3 points, range 1
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0028
    assert win.ui.dsb_p4.value() == 1.0018
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/31/5_cal-grating.txt")
    assert result == True

    # 32
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/32.txt")  # 3 points, range 2
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1_p2.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9989
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/32/5_cal-grating.txt")
    assert result == True

    # 33
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/33.txt")  # 3 points, range 3
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9989
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/33/5_cal-grating.txt")
    assert result == True

    # 34
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/34.txt")  # 3 points, range 4
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9982
    assert win.ui.dsb_p3.value() == 1.0011
    assert win.ui.dsb_p4.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/34/5_cal-grating.txt")
    assert result == True

    # a few files, free format (full), no error, file breakpoints, 2 points, ranges 1 to 3
    # 21
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/21.txt")  # 2 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p1_p2.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0028
    assert win.ui.dsb_p3.value() == 1.0028
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/21/5_cal-grating.txt")
    assert result == True

    # 22
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/22.txt")  # 2 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/22/5_cal-grating.txt")
    assert result == True

    # 23
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/23.txt")  # 2 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/23/5_cal-grating.txt")
    assert result == True

    # a few files, free format (3 columns), error, file breakpoints, 1 point, ranges 1 to 2
    # 11
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/11.txt")  # 1 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p1_p2.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670]
    assert win.ref_intervals == [True, False]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 0.9977
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/11/5_cal-grating.txt")
    assert result == True

    # 12
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/12.txt")  # 1 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670]
    assert win.ref_intervals == [False, True]
    assert win.reflectance_error == True
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/12/5_cal-grating.txt")
    assert result == True

    # a few files, free format (3 columns), no error, file breakpoints, 2 points, ranges 1 to 3
    # 21
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/21.txt")  # 2 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p1_p2.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 0.9977
    assert win.ui.dsb_p3.value() == 0.9968
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/21/5_cal-grating.txt")
    assert result == True

    # 22
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/22.txt")  # 2 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p3.value() == 0.9990
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/22/5_cal-grating.txt")
    assert result == True

    # 23
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(0)  # free
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/23.txt")  # 2 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990]
    assert win.ref_intervals == [False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "free format"
    assert win.ui.dsb_p1.value() == 1.0032
    assert win.ui.dsb_p2.value() == 1.0010
    assert win.ui.dsb_p3.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/23/5_cal-grating.txt")
    assert result == True

    # a few files, BRDF, error, file breakpoints, 3 points, ranges 1 to 4
    # 31
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/31.txt")  # 3 points, range 1
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p2_p3.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p2.value() == 1.0029
    assert win.ui.dsb_p4.value() == 0.9874
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/31/5_cal-grating.txt")
    assert result == True

    # 32
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/32.txt")  # 3 points, range 2
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9846
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/32/5_cal-grating.txt")
    assert result == True

    # 33
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/33.txt")  # 3 points, range 3
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9799
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p4.value() == 0.9676
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/33/5_cal-grating.txt")
    assert result == True

    # 34
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_err/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/34.txt")  # 3 points, range 4
    assert win.ui.dsb_p_1.value() == 670
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590]
    assert win.ref_intervals == [False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0127
    assert win.ui.dsb_p3.value() == 1.0335
    assert win.ui.dsb_p4.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_err/34/5_cal-grating.txt")
    assert result == True

    # a few files, BRDF, no error, file breakpoints, 4 points, ranges 1 o 5
    # 41
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/41.txt")  # 4 points, range 1
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0205
    assert win.ui.dsb_p5.value() == 0.9726
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/41/5_cal-grating.txt")
    assert result == True

    # 42
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/42.txt")  # 4 points, range 2
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9698
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/42/5_cal-grating.txt")
    assert result == True

    # 43
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/43.txt")  # 4 points, range 3
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 0.9799
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9530
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/43/5_cal-grating.txt")
    assert result == True

    # 44
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/44.txt")  # 4 points, range 4
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0127
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9850
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/44/5_cal-grating.txt")
    assert result == True

    # 45
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/BRDF_noerr/5.txt"]  # a few files, BRDF
    win.ui.cb_f_type.setCurrentIndex(1)  # BRDF
    win.ui.sb_refl_c.setValue(0)  # column 0
    win.ui.le_refl_c.setText("brdf format")  # brdf
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/45.txt")  # 4 points, range 5
    assert win.ui.dsb_p_2.value() == 990
    assert win.ui.dsb_p_4.value() == 2050
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050]
    assert win.ref_intervals == [False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "BRDF data"
    assert win.ui.dsb_p1.value() == 1.0282
    assert win.ui.dsb_p3.value() == 1.0493
    assert win.ui.dsb_p5.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/BRDF_noerr/45/5_cal-grating.txt")
    assert result == True

    # a few files, full, error, file breakpoints, 5 points, ranges 1 to 6
    # 51
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/51.txt")  # 5 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p4_p5.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 1.0028
    assert win.ui.dsb_p6.value() == 1.0779
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/51/5_cal-grating.txt")
    assert result == True

    # 52
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/52.txt")  # 5 points, range 2
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0749
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/52/5_cal-grating.txt")
    assert result == True

    # 53
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/53.txt")  # 5 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0749
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/53/5_cal-grating.txt")
    assert result == True

    # 54
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/54.txt")  # 5 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9982
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0760
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/54/5_cal-grating.txt")
    assert result == True

    # 55
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/55.txt")  # 5 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9984
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p6.value() == 1.0762
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/55/5_cal-grating.txt")
    assert result == True

    # 56
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_err/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/56.txt")  # 5 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_5.value() == 2830
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830]
    assert win.ref_intervals == [False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9277
    assert win.ui.dsb_p3.value() == 0.9303
    assert win.ui.dsb_p6.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_err/56/5_cal-grating.txt")
    assert result == True

    # a few files, full, no error, file breakpoints, 6 points, ranges 1 to 7
    # 61
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/61.txt")  # 6 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p5_p6.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [True, False, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p4.value() == 1.0018
    assert win.ui.dsb_p7.value() == 1.1064
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/61/5_cal-grating.txt")
    assert result == True

    # 62
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/62.txt")  # 6 points, range 2
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, True, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1032
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/62/5_cal-grating.txt")
    assert result == True

    # 63
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/63.txt")  # 6 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9972
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1033
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/63/5_cal-grating.txt")
    assert result == True

    # 64
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/64.txt")  # 6 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9982
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1044
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/64/5_cal-grating.txt")
    assert result == True

    # 65
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/65.txt")  # 6 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9984
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.1046
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/65/5_cal-grating.txt")
    assert result == True

    # 66
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/66.txt")  # 6 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9277
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0264
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/66/5_cal-grating.txt")
    assert result == True

    # 67
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/full_noerr/5.txt"]  # a few files, full
    win.ui.cb_f_type.setCurrentIndex(2)  # full
    win.ui.sb_refl_c.setValue(4)  # column 4
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/67.txt")  # 6 points, range 7
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "full data"
    assert win.ui.dsb_p1.value() == 0.9039
    assert win.ui.dsb_p3.value() == 0.9064
    assert win.ui.dsb_p7.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/full_noerr/67/5_cal-grating.txt")
    assert result == True

    # a few files, 3 columns, error, file breakpoints, 7 points, ranges 1 to 8
    # 71
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/71.txt")  # 7 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p6_p7.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [True, False, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p3.value() == 0.9968
    assert win.ui.dsb_p8.value() == 0.9833
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/71/5_cal-grating.txt")
    assert result == True

    # 72
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/72.txt")  # 7 points, range 2
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, True, False, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9855
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/72/5_cal-grating.txt")
    assert result == True

    # 73
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/73.txt")  # 7 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, True, False, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0032
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9864
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/73/5_cal-grating.txt")
    assert result == True

    # 74
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/74.txt")  # 7 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, True, False, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0284
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p8.value() == 1.0112
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/74/5_cal-grating.txt")
    assert result == True

    # 75
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/75.txt")  # 7 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, True, False, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0380
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p8.value() == 1.0207
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/75/5_cal-grating.txt")
    assert result == True

    # 76
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/76.txt")  # 7 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, True, False, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9983
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9816
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/76/5_cal-grating.txt")
    assert result == True

    # 77
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/77.txt")  # 7 points, range 7
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, False, True, False]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9906
    assert win.ui.dsb_p7.value() == 1.0000
    assert win.ui.dsb_p8.value() == 0.9740
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/77/5_cal-grating.txt")
    assert result == True

    # 78
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_err/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(True)  # error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/78.txt")  # 7 points, range 8
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_7.value() == 3880
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170, 3880]
    assert win.ref_intervals == [False, False, False, False, False, False, False, True]
    assert win.reflectance_error == True
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0170
    assert win.ui.dsb_p4.value() == 0.9890
    assert win.ui.dsb_p8.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_err/78/5_cal-grating.txt")
    assert result == True

    # a few files, 3 columns, no error, file breakpoints, 6 points, ranges 1 to 7
    # 61
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/61.txt")  # 6 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == True
    assert win.ui.check_p3_p4.isChecked() == False
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [True, False, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0000
    assert win.ui.dsb_p5.value() == 0.9634
    assert win.ui.dsb_p7.value() == 1.0095
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/61/5_cal-grating.txt")
    assert result == True

    # 62
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/62.txt")  # 6 points, range 1
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p1_p2.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, True, False, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0023
    assert win.ui.dsb_p2.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0118
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/62/5_cal-grating.txt")
    assert result == True

    # 63
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/63.txt")  # 6 points, range 3
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p2_p3.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, True, False, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0032
    assert win.ui.dsb_p3.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0128
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/63/5_cal-grating.txt")
    assert result == True

    # 64
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/64.txt")  # 6 points, range 4
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p3_p4.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, True, False, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0284
    assert win.ui.dsb_p4.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0382
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/64/5_cal-grating.txt")
    assert result == True

    # 65
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/65.txt")  # 6 points, range 5
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p4_p5.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, True, False, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 1.0380
    assert win.ui.dsb_p5.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0479
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/65/5_cal-grating.txt")
    assert result == True

    # 66
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/66.txt")  # 6 points, range 6
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p5_p6.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, True, False]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9983
    assert win.ui.dsb_p6.value() == 1.0000
    assert win.ui.dsb_p7.value() == 1.0078
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/66/5_cal-grating.txt")
    assert result == True

    # 67
    # data set up
    str_paths = ["C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/1.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/2.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/3.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/4.txt",
                 "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/a_few_files/simple_noerr/5.txt"]  # a few files, simple
    win.ui.cb_f_type.setCurrentIndex(3)  # full
    win.ui.sb_refl_c.setValue(2)  # column 2
    win.ui.le_refl_c.setText("")
    win.ui.chb_erro_c.setChecked(False)  # no error
    # data read
    win.file_select(str_paths)
    assert win.files == str_paths
    assert len(win.files) == 5
    # breakpoints
    win.points_load_ui("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/bp_670/67.txt")  # 6 points, range 7
    assert win.ui.dsb_p_3.value() == 1590
    assert win.ui.dsb_p_6.value() == 3170
    assert win.ui.check_p1.isChecked() == False
    assert win.ui.check_p6_p7.isChecked() == True
    # correction
    win.correct()
    assert win.p_array == [670, 990, 1590, 2050, 2830, 3170]
    assert win.ref_intervals == [False, False, False, False, False, False, True]
    assert win.reflectance_error == False
    assert win.file_type == "3-col. data"
    assert win.ui.dsb_p1.value() == 0.9906
    assert win.ui.dsb_p5.value() == 0.9543
    assert win.ui.dsb_p7.value() == 1.0000
    win.export("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    win.log("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few")
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/1_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/2_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/3_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/4_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_corr.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/5_corr.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/1_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/1_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/2_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/2_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/3_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/3_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/4_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/4_cal-grating.txt")
    assert result == True
    result = filecmp.cmp("C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/few/5_cal-grating.txt", "C:/Users/flex_virt/Dev/Spectro_decalage_gonio_dev/test/files/GUI/few/simple_noerr/67/5_cal-grating.txt")
    assert result == True
