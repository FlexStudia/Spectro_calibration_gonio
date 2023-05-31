# coding: utf-8

"""
    This soft makes correction of grating/detector shifts (Gonios).
    Here is app code. It handles GUI version based on the core code.

    Forge: https://gricad-gitlab.univ-grenoble-alpes.fr/gonios-ipag/logiciels-gonios/-/issues/47
"""

# IMPORTS
# PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction, QLabel, QApplication
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QMovie
import pyqtgraph as pg
# other
import sys
import os
import copy
# numpy
import numpy as np
# ui templates
from templates.mw import Ui_MainWindow as Ui_MainWindow
from templates.calc_w import Ui_QDialog as Ui_CalcWindow
from templates.help import Ui_QDialog as Ui_HelpWindow
# code
import core

# GLOBALS
__version__ = 0.941
__copyright__ = "<a href='https://www.gnu.org/licenses/gpl-3.0.html'>The GNU General Public License v3.0</a>"
__author_mail__ = "<a href='mailto: flex.studia.dev@gmail.com'>flex.studia.dev@gmail.com</a>"
__bug_support_mail__ = "<a href='mailto: flex.studia.help@gmail.com'>flex.studia.help@gmail.com</a>"
__github__ = "https://github.com/FlexStudia/Spectro_decalage_gonio"
# register
__app_name__ = "Gonios grating shift"
__org_name__ = "Flex Studia Dev"
settings = QSettings(__org_name__, __app_name__)
# style
button_style_small = 'QPushButton{padding: 5px}'
button_style_big = 'QPushButton{padding: 15px}'
line_edit_read_only = 'QLineEdit{background-color: #cccccc}'
graph_title = {'color': "#000000", 'size': "11pt"}
# others
unit_set = ('free format', 'BRDF data', 'full data', '3-col. data')


"""
TODO:
    next UPD:
        * работа с NaN
            Сейчас строки с NaN просто выбрасываются. Нужно, чтобы сетка wavelengths сохранялась.
            Кроме того, файлы одного типа и с одинаковыми breakpoints, но разными местами с NaN выдают ошибку (т.к. у них разня длина и не одинаковый набор wavelengths). 
            Сохранив сетку wavelength до расчётов, эту проблему можно решить.
        * сделать spin_box изменяемыми по наведению мыши на соответствующий знак после запятой
        * создать часть, где для исходных данных можно загрузить log с f-коеффициентами и попавить их вручную на графике
        * пофиксить график (точнее то, что нужно вручную расширить окно, чтобы он в него влез)
        * сделать tools (сюда или отдельно), позвояляющий визуализировать несколько графиков (из большего набора данных) и поднимать/опускать кривые

    one day UPD:
        * добавить temperature present (когда Б скажет, как он выглядит)

    maybe UPD:
        * detection automatique des breakpoints, via les discontinuites en flux ou resolution (faisable qu'avec les format BRDF et full) => BS: a evaluer
            Есть мнение, что в некоторых случаях (BRDF и full) можно определить точки автоматически. Поскольку есть скачки разрешения, где и происходят break.
            Но не ясно, насколько сильно это нужно. Ведь эти точки часто одни и теже, если речь идёт о серии экспериментов, а в проге их можно сохранить.
        * 
"""


class MainWindow(QtWidgets.QMainWindow):
    """
        This is main "mother" window.
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # GUI beauties
        # Title
        self.setWindowTitle(f'Correction of grating/detector shifts (Gonios) v{__version__}')
        # Menu
        extractAction = QAction("&About", self)
        extractAction.setStatusTip('About The App')
        extractAction.triggered.connect(self.show_about)
        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Help')
        fileMenu.addAction(extractAction)
        # btns
        self.ui.calc_btn.setText("Correct data for the first time")
        self.ui.change_btn.setText("Adjust existing correction\n(coming soon)")
        self.ui.change_btn.setDisabled(True)
        # Signals & slots
        self.ui.calc_btn.clicked.connect(self.DecalCorr_f)

    def show_about(self):
        """
            It is menu "About" message with all legal information.
        :return:
        """
        self.dialog_ok(f"<b>Correction of decalage for the Gonio</b> v{__version__}"
                       f"<p>Copyright: {__copyright__}</p>"
                       f"<p><a href='{__github__}'>GitHub repository</a> (program code and more information)</p>"
                       f"<p>Created by Gorbacheva Maria ({__author_mail__})</p>"
                       "<p>Scientific base by Bernard Schmitt, IPAG (<a href='mailto: bernard.schmitt@univ-grenoble-alpes.fr'>bernard.schmitt@univ-grenoble-alpes.fr</a>)</p>"
                       f"<p>For any questions and bug reports, please, mail at {__bug_support_mail__}</p>"
                       "<p>In case of a bug, please report it and specify your operating system, "
                       "provide a detailed description of the problem with screenshots "
                       "and the files used and produced, if possible. Your contribution matters to make it better!</p>")

    def dialog_ok(self, s):
        """
            It is a custom Ok window.
        :param s: text to show
        :return: None
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Ok!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def DecalCorr_f(self):
        """
            It is the first correction window class
        :return: None
        """
        DecalCorr()


class DecalCorr(QtWidgets.QDialog):
    """
        This is the first correction window and its functions.
        It:
        1. provides the GUI and data correction (referring to core.py for the last)
        2. shows the result as an interactive graph (from pyqtgraph) and allows to adjust the correction manually
        3. exports the results of manual correction and the log with manual correction coefficients
    """
    def __init__(self):
        super(DecalCorr, self).__init__()
        self.ui = Ui_CalcWindow()
        self.ui.setupUi(self)
        # GLOBALS
        self.files = ""
        self.open_dir = ""
        self.calc_result = ""
        self.calc_result_flag = False
        self.first_run = True
        self.p_array = ""
        self.points_qty = 3
        self.manuel_adjust = []
        self.ref_intervals = []
        self.p_intrvals = []
        self.sb_change_last = []
        self.dsb_user = False
        self.reflectance_column = ""
        self.reflectance_error = True
        self.current_file = 0
        self.file_type = ""
        self.current_column = 0
        # GUI beauties
        # Title
        self.setWindowTitle(f'Correction')
        self.ui.window_title.setText("Correction of grating/detector shifts")
        # ToolBox
        self.ui.toolBox.setStyleSheet("QToolBox::tab {background: #D1D1D1; color: black;} QToolBox::tab:selected {background: #C9EAF3; color: black;} QToolBox::tab:hover{background: #B5D3DB;}")
        self.ui.toolBox.setCurrentIndex(0)
        # file tab
        self.ui.btn_f.setStyleSheet(f'{button_style_big}')
        for index in range(0, len(unit_set)):
            self.ui.cb_f_type.insertItem(index, unit_set[index])
        self.ui.cb_f_type.setCurrentIndex(0)
        self.ui.lb_type_help = QLabelClickable(self)
        self.ui.lb_type_help.setObjectName("lb_type_help")
        self.ui.gridLayout.addWidget(self.ui.lb_type_help, 0, 2, 1, 1)
        self.ui.lb_type_help.setPixmap(QPixmap('img/questions.png').scaled(20, 20))
        self.ui.lb_type_help.setCursor(Qt.PointingHandCursor)
        self.ui.sb_refl_c.setValue(2)
        self.ui.le_refl_c.setText("")
        self.ui.le_refl_c.setVisible(False)
        self.ui.chb_erro_c.setChecked(True)
        # points tab
        self.ui.lb_point_help = QLabelClickable(self)
        self.ui.lb_point_help.setObjectName("lb_point_help")
        self.ui.gridLayout_2.addWidget(self.ui.lb_point_help, 1, 0, 1, 1)
        self.ui.lb_point_help.setPixmap(QPixmap('img/questions.png').scaled(20, 20))
        self.ui.lb_point_help.setCursor(Qt.PointingHandCursor)
        self.ui.lbl_p4.setVisible(False)
        self.ui.dsb_p_4.setVisible(False)
        self.ui.check_p4_p5.setVisible(False)
        self.ui.lbl_p5.setVisible(False)
        self.ui.dsb_p_5.setVisible(False)
        self.ui.check_p5_p6.setVisible(False)
        self.ui.lbl_p6.setVisible(False)
        self.ui.dsb_p_6.setVisible(False)
        self.ui.check_p6_p7.setVisible(False)
        self.ui.lbl_p7.setVisible(False)
        self.ui.dsb_p_7.setVisible(False)
        self.ui.check_p7.setVisible(False)
        self.ui.check_p3_p4.setText("after p3")
        self.ui.check_p3_p4.setChecked(True)
        self.ui.btn_add_point.setStyleSheet(f'{button_style_small}')
        self.ui.btn_remove_point.setStyleSheet(f'{button_style_small}')
        self.ui.btn_save.setStyleSheet(f'{button_style_small}')
        self.ui.btn_load.setStyleSheet(f'{button_style_small}')
        self.ui.btn_calc.setStyleSheet(f'{button_style_big}')
        # plot tab
        self.ui.cb_file.insertItem(0, 'no file selected')
        self.ui.cb_file.setCurrentIndex(0)
        self.ui.cb_cn.insertItem(0, '---')
        self.ui.cb_cn.setCurrentIndex(0)
        self.ui.btn_reset.setStyleSheet(f'{button_style_small}')
        self.ui.btn_reset_all.setStyleSheet(f'{button_style_small}')
        self.ui.lb_graph_help = QLabelClickable(self)
        self.ui.lb_graph_help.setObjectName("lb_graph_help")
        self.ui.gridLayout_3.addWidget(self.ui.lb_graph_help, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.ui.lb_graph_help.setPixmap(QPixmap('img/questions.png').scaled(20, 20))
        self.ui.lb_graph_help.setCursor(Qt.PointingHandCursor)
        self.ui.dsb_p1.setDisabled(True)
        self.ui.dsb_p2.setDisabled(True)
        self.ui.dsb_p3.setDisabled(True)
        self.ui.dsb_p4.setDisabled(True)
        self.ui.dsb_p5.setDisabled(True)
        self.ui.dsb_p5.setVisible(False)
        self.ui.dsb_p6.setDisabled(True)
        self.ui.dsb_p6.setVisible(False)
        self.ui.dsb_p7.setDisabled(True)
        self.ui.dsb_p7.setVisible(False)
        self.ui.dsb_p8.setDisabled(True)
        self.ui.dsb_p8.setVisible(False)
        self.ui.lb_p1_v.setText('f before p1')
        self.ui.lb_p2_v.setText('f between p1 and p2')
        self.ui.lb_p3_v.setText('f between p2 and p3')
        self.ui.lb_p4_v.setText('f after p3')
        self.ui.lb_p5_v.setVisible(False)
        self.ui.lb_p6_v.setVisible(False)
        self.ui.lb_p7_v.setVisible(False)
        self.ui.lb_p8_v.setVisible(False)
        # plot tab: graph
        self.ui.graphWidget.addLegend((100, 1))
        self.ui.graphWidget.addItem(pg.GridItem())
        self.ui.graphWidget.setBackground('#ffffff')
        self.ui.graphWidget.setMenuEnabled(False)
        styles = {'color': '#000000', 'font-size': '13px'}
        self.ui.graphWidget.setLabel('left', 'Reflectance', **styles)
        self.ui.graphWidget.setLabel('bottom', 'Wavelength (nm)', **styles)
        self.ui.graphWidget.setTitle(f"{self.ui.cb_file.currentText()}, column: ---", **graph_title)
        self.p1_inf = pg.InfiniteLine(0)
        self.p2_inf = pg.InfiniteLine(0)
        self.p3_inf = pg.InfiniteLine(0)
        self.p4_inf = pg.InfiniteLine(0)
        self.p5_inf = pg.InfiniteLine(0)
        self.p6_inf = pg.InfiniteLine(0)
        self.p7_inf = pg.InfiniteLine(0)
        line_width = 3
        # plot tab: initial data plot
        pen_st = pg.mkPen(color=(54, 135, 211), width=line_width)
        self.line_initial = pg.PlotCurveItem(clear=True, pen=pen_st, name="initial")
        self.ui.graphWidget.addItem(self.line_initial)
        # plot tab: corrected data plot
        pen_st = pg.mkPen(color=(178, 0, 122), width=line_width)
        self.line_calculated = pg.PlotCurveItem(clear=True, pen=pen_st, name="corrected")
        self.ui.graphWidget.addItem(self.line_calculated)
        # plot tab: adjusted data plot
        pen_st = pg.mkPen(color=(0, 169, 113), width=line_width)
        self.line_corrected = pg.PlotCurveItem(clear=True, pen=pen_st, name="adjusted")
        self.ui.graphWidget.addItem(self.line_corrected)
        # export tab
        self.ui.le_prefix.setText("_corr")
        self.ui.le_log.setText("_cal-grating")
        self.ui.btn_exp.setStyleSheet(f'{button_style_big}')
        self.ui.btn_log.setStyleSheet(f'{button_style_small}')
        # SIGNALS & SLOTS
        # file select
        self.ui.btn_f.clicked.connect(self.file_ui)
        self.ui.btn_f_x.clicked.connect(self.file_dell)
        self.ui.cb_f_type.currentIndexChanged.connect(self.type_preset)
        self.ui.lb_type_help.clicked.connect(self.type_help)
        # points
        self.ui.lb_point_help.clicked.connect(self.point_help)
        self.ui.check_p1.clicked.connect(lambda: self.checker_toggle(1))
        self.ui.check_p1_p2.clicked.connect(lambda: self.checker_toggle(2))
        self.ui.check_p2_p3.clicked.connect(lambda: self.checker_toggle(3))
        self.ui.check_p3_p4.clicked.connect(lambda: self.checker_toggle(4))
        self.ui.check_p4_p5.clicked.connect(lambda: self.checker_toggle(5))
        self.ui.check_p5_p6.clicked.connect(lambda: self.checker_toggle(6))
        self.ui.check_p6_p7.clicked.connect(lambda: self.checker_toggle(7))
        self.ui.check_p7.clicked.connect(lambda: self.checker_toggle(8))
        self.ui.btn_add_point.clicked.connect(self.add_point)
        self.ui.btn_remove_point.clicked.connect(self.remove_point)
        self.ui.btn_save.clicked.connect(self.points_save)
        self.ui.btn_load.clicked.connect(self.points_load)
        # calc
        self.ui.btn_calc.clicked.connect(self.correct)
        # plot
        self.ui.cb_cn.currentIndexChanged.connect(lambda: self.column_changed("user"))
        self.ui.cb_file.currentIndexChanged.connect(lambda: self.file_changed("user"))
        self.ui.lb_graph_help.clicked.connect(self.graph_help)
        self.ui.dsb_p1.valueChanged.connect(lambda: self.dsb_change(1))
        self.ui.dsb_p2.valueChanged.connect(lambda: self.dsb_change(2))
        self.ui.dsb_p3.valueChanged.connect(lambda: self.dsb_change(3))
        self.ui.dsb_p4.valueChanged.connect(lambda: self.dsb_change(4))
        self.ui.dsb_p5.valueChanged.connect(lambda: self.dsb_change(5))
        self.ui.dsb_p6.valueChanged.connect(lambda: self.dsb_change(6))
        self.ui.dsb_p7.valueChanged.connect(lambda: self.dsb_change(7))
        self.ui.dsb_p8.valueChanged.connect(lambda: self.dsb_change(8))
        self.ui.btn_reset.clicked.connect(self.reset_current)
        self.ui.btn_reset_all.clicked.connect(self.reset_all)
        # export
        self.ui.btn_exp.clicked.connect(self.export_ui)
        self.ui.btn_log.clicked.connect(self.log_ui)
        # QDialog show
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.exec_()

    def type_help(self):
        """
            It runs file type help window.
        :return: None
        """
        TypeHelp()

    def point_help(self):
        """
            It runs help window for breakpoints.
        :return: None
        """
        PointHelp()

    def graph_help(self):
        """
            It runs help window for the graph.
        :return: None
        """
        GraphHelp()

    def dialog_ok(self, s):
        """
            It is a custom Ok window.
        :param s: text to show
        :return: None
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Ok!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def dialog_critical(self, s):
        """
            It is a custom error/warning window.
        :param s: text to show
        :return: None
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Error!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def last_dir(self, str_path):
        """
            This function searches for the nearest existing path.
        :param str_path: str with a path to process
        :return: str with the nearest existing path or "" if there is no such a path
        """
        if str_path:
            if len(str_path) <= 2 and not os.path.exists(str_path):
                return ""
            while not os.path.exists(str_path) and not len(str_path) <= 2:
                str_path = str_path[:str_path.rfind("/")]
            return str_path
        else:
            return ""

    def file_ui(self):
        """
            This function is an input allowing the user to select files containing data to correct.
            It handles the QFileDialog.getOpenFileNames and sends the result to self.file_select() for further processing.
        :return: None
        """
        try:
            if settings.value("data_dir"):
                if not os.path.exists(settings.value("data_dir")):
                    settings.setValue("data_dir", self.last_dir(settings.value("data_dir")))
                paths, _ = QFileDialog.getOpenFileNames(self, f"Choose file(s) with data to correct", settings.value("data_dir"), "Text documents (*.txt);;All files (*.*)")
            else:
                paths, _ = QFileDialog.getOpenFileNames(self, f"Choose file(s) with data to correct", "", "Text documents (*.txt);;All files (*.*)")
            if paths:
                self.file_select(paths)
        except Exception as e:
            self.dialog_critical(f'Critical error in file_select:\n{str(e)}.')

    def file_select(self, paths):
        """
            This function:
            1. puts the selected folder in "data_dir" QSetting (to save the path to the data, so that the next time one runs the program it will look for data in this place)
            2. puts paths in self.files global class variable (to make it available for all later functions)
            3. changes self.ui.lbl_f to display the name of the selected file or the number of selected files in their folder (so the user can see that the data is indeed selected)
            4. puts the selected folder in self.open_dir global class variable (to keep it for later export functions; this is only used for the very first run and then replaced by the corresponding QSettings)
        :param paths: list of str with paths
        :return: None
        """
        try:
            if paths:
                settings.setValue("data_dir", paths[0][:paths[0].rfind("/")])
                self.files = paths
                # lbl_f
                if len(paths) == 1:
                    file_name = paths[0][paths[0].rfind("/") + 1:]
                    self.ui.lbl_f.setText(file_name)
                else:
                    folder_name = paths[0][paths[0][:paths[0].rfind("/")].rfind("/") + 1:paths[0].rfind("/")]
                    self.ui.lbl_f.setText(f"{len(paths)} files in {folder_name}")
                self.open_dir = paths[0][:paths[0].rfind("/")]
        except Exception as e:
            self.dialog_critical(f'Critical error in file_select:\n{str(e)}.')

    def file_dell(self):
        """
            This function cancels the selection of files.
            It:
            1. empties self.files global class variable (which stores paths to the data).
            2. sets "no file selected" to self.ui.lbl_f to show it in GUI
        :return: None
        """
        self.files = ""
        self.ui.lbl_f.setText("no file selected")

    def type_preset(self):
        """
            This function changes the GUI depending on the file type (selected by the user in self.ui.cb_f_type QComboBox).
        :return: None
        """
        try:
            if self.ui.cb_f_type.currentText() == unit_set[0]: # free format
                # reflectance column QSpinBox
                self.ui.sb_refl_c.setValue(2)
                self.ui.sb_refl_c.setDisabled(False)
                self.ui.sb_refl_c.setVisible(True)
                # BRDF special 'reflectance' column
                self.ui.le_refl_c.setText("")
                self.ui.le_refl_c.setVisible(False)
                # error column existence QCheckBox
                self.ui.chb_erro_c.setChecked(True)
            elif self.ui.cb_f_type.currentText() == unit_set[1]: # BRDF data
                self.ui.sb_refl_c.setValue(0)
                self.ui.sb_refl_c.setDisabled(True)
                self.ui.sb_refl_c.setVisible(False)
                self.ui.le_refl_c.setText("brdf format")
                self.ui.le_refl_c.setVisible(True)
                self.ui.le_refl_c.setDisabled(True)
                self.ui.chb_erro_c.setChecked(True)
            elif self.ui.cb_f_type.currentText() == unit_set[2]: # full data
                self.ui.sb_refl_c.setValue(4)
                self.ui.sb_refl_c.setDisabled(True)
                self.ui.sb_refl_c.setVisible(True)
                self.ui.le_refl_c.setText("")
                self.ui.le_refl_c.setVisible(False)
                self.ui.chb_erro_c.setChecked(True)
            elif self.ui.cb_f_type.currentText() == unit_set[3]: #3-col. data
                self.ui.sb_refl_c.setValue(2)
                self.ui.sb_refl_c.setDisabled(True)
                self.ui.sb_refl_c.setVisible(True)
                self.ui.le_refl_c.setText("")
                self.ui.le_refl_c.setVisible(False)
                self.ui.chb_erro_c.setChecked(True)
            # temperature present will be here
        except Exception as e:
            self.dialog_critical(f'Critical error in type_preset:\n{str(e)}.')

    def checker_toggle(self, param):
        """
            This function toggles QCheckBox for the reference ranges so only one of them can be selected.
        :param param: number of QCheckBox starting from 1 (up to 8)
        :return: None
        """
        if param == 1:
            self.ui.check_p1.setChecked(True)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(False)
        elif param == 2:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(True)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(False)
        elif param == 3:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(True)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(False)
        elif param == 4:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(True)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(False)
        elif param == 5:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(True)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(False)
        elif param == 6:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(True)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(False)
        elif param == 7:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(True)
            self.ui.check_p7.setChecked(False)
        else:
            self.ui.check_p1.setChecked(False)
            self.ui.check_p1_p2.setChecked(False)
            self.ui.check_p2_p3.setChecked(False)
            self.ui.check_p3_p4.setChecked(False)
            self.ui.check_p4_p5.setChecked(False)
            self.ui.check_p5_p6.setChecked(False)
            self.ui.check_p6_p7.setChecked(False)
            self.ui.check_p7.setChecked(True)

    def add_point(self):
        """
            This GUI function changes the interface to add one more breakpoint (at the end of them).
        :return: None
        """
        if self.points_qty == 1:
            self.ui.lbl_p2.setVisible(True)
            self.ui.dsb_p_2.setValue(0)
            self.ui.dsb_p_2.setVisible(True)
            self.ui.check_p2_p3.setVisible(True)
            self.ui.check_p2_p3.setText("after p2")
            self.ui.check_p1_p2.setText("between p1 and p2")
            self.points_qty = self.points_qty + 1
            self.ui.btn_remove_point.setDisabled(False)
        elif self.points_qty == 2:
            self.ui.lbl_p3.setVisible(True)
            self.ui.dsb_p_3.setValue(0)
            self.ui.dsb_p_3.setVisible(True)
            self.ui.check_p3_p4.setVisible(True)
            self.ui.check_p3_p4.setText("after p3")
            self.ui.check_p2_p3.setText("between p2 and p3")
            self.points_qty = self.points_qty + 1
        elif self.points_qty == 3:
            self.ui.lbl_p4.setVisible(True)
            self.ui.dsb_p_4.setValue(0)
            self.ui.dsb_p_4.setVisible(True)
            self.ui.check_p4_p5.setVisible(True)
            self.ui.check_p4_p5.setText("after p4")
            self.ui.check_p3_p4.setText("between p3 and p4")
            self.points_qty = self.points_qty + 1
        elif self.points_qty == 4:
            self.ui.lbl_p5.setVisible(True)
            self.ui.dsb_p_5.setValue(0)
            self.ui.dsb_p_5.setVisible(True)
            self.ui.check_p5_p6.setVisible(True)
            self.ui.check_p5_p6.setText("after p5")
            self.ui.check_p4_p5.setText("between p4 and p5")
            self.points_qty = self.points_qty + 1
        elif self.points_qty == 5:
            self.ui.lbl_p6.setVisible(True)
            self.ui.dsb_p_6.setValue(0)
            self.ui.dsb_p_6.setVisible(True)
            self.ui.check_p6_p7.setVisible(True)
            self.ui.check_p6_p7.setText("after p6")
            self.ui.check_p5_p6.setText("between p5 and p6")
            self.points_qty = self.points_qty + 1
        elif self.points_qty == 6:
            self.ui.lbl_p7.setVisible(True)
            self.ui.dsb_p_7.setValue(0)
            self.ui.dsb_p_7.setVisible(True)
            self.ui.check_p7.setVisible(True)
            self.ui.check_p7.setText("after p7")
            self.ui.check_p6_p7.setText("between p6 and p7")
            self.points_qty = self.points_qty + 1
            self.ui.btn_add_point.setDisabled(True)
            self.ui.btn_remove_point.setFocus()

    def remove_point(self):
        """
            This GUI function changes the interface to remove the last breakpoint.
        :return: None
        """
        if self.points_qty == 2:
            self.ui.lbl_p2.setVisible(False)
            self.ui.dsb_p_2.setValue(0)
            self.ui.dsb_p_2.setVisible(False)
            self.ui.check_p2_p3.setVisible(False)
            self.ui.check_p1_p2.setText("after p1")
            if self.ui.check_p2_p3.isChecked():
                self.ui.check_p1_p2.setChecked(True)
                self.ui.check_p2_p3.setChecked(False)
            self.points_qty = self.points_qty - 1
            self.ui.btn_remove_point.setDisabled(True)
        elif self.points_qty == 3:
            self.ui.lbl_p3.setVisible(False)
            self.ui.dsb_p_3.setValue(0)
            self.ui.dsb_p_3.setVisible(False)
            self.ui.check_p3_p4.setVisible(False)
            self.ui.check_p2_p3.setText("after p2")
            if self.ui.check_p3_p4.isChecked():
                self.ui.check_p2_p3.setChecked(True)
                self.ui.check_p3_p4.setChecked(False)
            self.points_qty = self.points_qty - 1
        elif self.points_qty == 4:
            self.ui.lbl_p4.setVisible(False)
            self.ui.dsb_p_4.setValue(0)
            self.ui.dsb_p_4.setVisible(False)
            self.ui.check_p4_p5.setVisible(False)
            self.ui.check_p3_p4.setText("after p3")
            if self.ui.check_p4_p5.isChecked():
                self.ui.check_p3_p4.setChecked(True)
                self.ui.check_p4_p5.setChecked(False)
            self.points_qty = self.points_qty - 1
        elif self.points_qty == 5:
            self.ui.lbl_p5.setVisible(False)
            self.ui.dsb_p_5.setValue(0)
            self.ui.dsb_p_5.setVisible(False)
            self.ui.check_p5_p6.setVisible(False)
            self.ui.check_p4_p5.setText("after p4")
            if self.ui.check_p5_p6.isChecked():
                self.ui.check_p4_p5.setChecked(True)
                self.ui.check_p5_p6.setChecked(False)
            self.points_qty = self.points_qty - 1
        elif self.points_qty == 6:
            self.ui.lbl_p6.setVisible(False)
            self.ui.dsb_p_6.setValue(0)
            self.ui.dsb_p_6.setVisible(False)
            self.ui.check_p6_p7.setVisible(False)
            self.ui.check_p5_p6.setText("after p5")
            if self.ui.check_p6_p7.isChecked():
                self.ui.check_p5_p6.setChecked(True)
                self.ui.check_p6_p7.setChecked(False)
            self.points_qty = self.points_qty - 1
        elif self.points_qty == 7:
            self.ui.lbl_p7.setVisible(False)
            self.ui.dsb_p_7.setValue(0)
            self.ui.dsb_p_7.setVisible(False)
            self.ui.check_p7.setVisible(False)
            self.ui.check_p6_p7.setText("after p6")
            if self.ui.check_p7.isChecked():
                self.ui.check_p6_p7.setChecked(True)
                self.ui.check_p7.setChecked(False)
            self.points_qty = self.points_qty - 1
            self.ui.btn_add_point.setDisabled(False)
            self.ui.btn_remove_point.setFocus()

    def points_save(self):
        """
            This function saves breakpoints and reference ranges in a txt file.
            It also sets "point_dir" QSetting.
        :return: None
        """
        try:
            # making str to save
            str_to_save = ""
            if self.ui.check_p1.isChecked():
                str_to_save = str_to_save + "X\n"
            else:
                str_to_save = str_to_save + "O\n"
            str_to_save = str_to_save + str(self.ui.dsb_p_1.value()) + "\n"
            if self.ui.check_p1_p2.isChecked():
                str_to_save = str_to_save + "X\n"
            else:
                str_to_save = str_to_save + "O\n"
            if self.ui.dsb_p_2.isVisible():
                str_to_save = str_to_save + str(self.ui.dsb_p_2.value()) + "\n"
                if self.ui.check_p2_p3.isChecked():
                    str_to_save = str_to_save + "X\n"
                else:
                    str_to_save = str_to_save + "O\n"
            if self.ui.dsb_p_3.isVisible():
                str_to_save = str_to_save + str(self.ui.dsb_p_3.value()) + "\n"
                if self.ui.check_p3_p4.isChecked():
                    str_to_save = str_to_save + "X\n"
                else:
                    str_to_save = str_to_save + "O\n"
            if self.ui.dsb_p_4.isVisible():
                str_to_save = str_to_save + str(self.ui.dsb_p_4.value()) + "\n"
                if self.ui.check_p4_p5.isChecked():
                    str_to_save = str_to_save + "X\n"
                else:
                    str_to_save = str_to_save + "O\n"
            if self.ui.dsb_p_5.isVisible():
                str_to_save = str_to_save + str(self.ui.dsb_p_5.value()) + "\n"
                if self.ui.check_p5_p6.isChecked():
                    str_to_save = str_to_save + "X\n"
                else:
                    str_to_save = str_to_save + "O\n"
            if self.ui.dsb_p_6.isVisible():
                str_to_save = str_to_save + str(self.ui.dsb_p_6.value()) + "\n"
                if self.ui.check_p6_p7.isChecked():
                    str_to_save = str_to_save + "X\n"
                else:
                    str_to_save = str_to_save + "O\n"
            if self.ui.dsb_p_7.isVisible():
                str_to_save = str_to_save + str(self.ui.dsb_p_7.value()) + "\n"
                if self.ui.check_p7.isChecked():
                    str_to_save = str_to_save + "X\n"
                else:
                    str_to_save = str_to_save + "O\n"
            save_file_name = "_points.txt"
            # file name
            if self.files:
                if len(self.files) == 1:
                    save_file_name = self.files[0][self.files[0].rfind("/") + 1:self.files[0].rfind(".")] + "_points.txt"
                else:
                    save_file_name = self.files[0][self.files[0][:self.files[0].rfind("/")].rfind("/") + 1:self.files[0].rfind("/")] + "_points.txt"
            file_name = ""
            if settings.value("point_dir"):
                if not os.path.exists(settings.value("point_dir")):
                    settings.setValue("point_dir", self.last_dir(settings.value("point_dir")))
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", settings.value("point_dir") + '/' + save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
            else:
                if self.open_dir:
                    file_name, _ = QFileDialog.getSaveFileName(self, "Save File", self.open_dir + '/' + save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
                else:
                    file_name, _ = QFileDialog.getSaveFileName(self, "Save File", save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
            # save
            if file_name:
                settings.setValue("point_dir", file_name[:file_name.rfind("/")])
                with open(file_name, 'w+') as file_output:
                    file_output.write(str_to_save)
                self.dialog_ok("The file is successfully saved!")
        except Exception as e:
            self.dialog_critical(f'Critical error in points_save:\n{str(e)}.')

    def points_load(self):
        """
            This function handels the user input for a txt-file with breakpoints.
            It also sets "point_dir" QSetting.
        :return: None
        """
        try:
            if settings.value("point_dir"):
                if not os.path.exists(settings.value("point_dir")):
                    settings.setValue("point_dir", self.last_dir(settings.value("point_dir")))
                path, _ = QFileDialog.getOpenFileName(self, f"Choose a file with data", settings.value("point_dir"), "Text documents (*.txt);;All files (*.*)")
            else:
                path, _ = QFileDialog.getOpenFileName(self, f"Choose a file with data", self.open_dir, "Text documents (*.txt);;All files (*.*)")
            if path:
                self.points_load_ui(path)
        except Exception as e:
            self.dialog_critical(f'Critical error in points_load:\n{str(e)}.')

    def points_load_ui(self, path):
        """
            This function loads breakpoints from its txt file.
            It also sets "point_dir" QSetting.
        :param path: str with path to a breakpoints file
        :return: None
        """
        try:
            if path:
                settings.setValue("point_dir", path[:path.rfind("/")])
                file_content = []
                with open(path, "r", encoding="utf8") as file:
                    # load the data from file
                    for line in file:
                        file_content.append(line.strip())
                # verification
                verif_Ok = True
                x_qty = 0
                message = ""
                for i, v in enumerate(file_content):
                    if i % 2 == 0:
                        if v.lower() != "x" and v.lower() != "o":
                            verif_Ok = False
                            message = "Xs and Os order is interrupted"
                            break
                        elif v.lower() == "x":
                            x_qty = x_qty + 1
                    else:
                        if type(self.set_point(v)) != float:
                            message = "only numeric values are allowed for point positions\nor there are too much of Xs and/or Os"
                            verif_Ok = False
                            break
                if x_qty != 1 and verif_Ok:
                    verif_Ok = False
                    message = "too much of Xs"
                if verif_Ok:
                    # max point determination
                    self.points_qty = int((len(file_content) - 1) / 2)
                    # show the data
                    # show the data: check_p1
                    if file_content[0].lower() == "x":
                        self.ui.check_p1.setChecked(True)
                    else:
                        self.ui.check_p1.setChecked(False)
                    # show the data: dsb_p_1
                    self.ui.dsb_p_1.setValue(self.set_point(file_content[1]))
                    # show the data: check_p1_p2
                    if file_content[2].lower() == "x":
                        self.ui.check_p1_p2.setChecked(True)
                    else:
                        self.ui.check_p1_p2.setChecked(False)
                    if self.points_qty == 1:
                        self.ui.check_p1_p2.setText("after p1")
                    else:
                        self.ui.check_p1_p2.setText("between p1 and p2")
                    # show the data: dsb_p_2
                    if self.points_qty > 1:
                        self.ui.dsb_p_2.setVisible(True)
                        self.ui.dsb_p_2.setValue(self.set_point(file_content[3]))
                        self.ui.lbl_p2.setVisible(True)
                    else:
                        self.ui.dsb_p_2.setVisible(False)
                        self.ui.dsb_p_2.setValue(0)
                        self.ui.lbl_p2.setVisible(False)
                    # show the data: check_p2_p3
                    if self.points_qty > 1:
                        self.ui.check_p2_p3.setVisible(True)
                        if file_content[4].lower() == "x":
                            self.ui.check_p2_p3.setChecked(True)
                        else:
                            self.ui.check_p2_p3.setChecked(False)
                        if self.points_qty == 2:
                            self.ui.check_p2_p3.setText("after p2")
                        else:
                            self.ui.check_p2_p3.setText("between p2 and p3")
                    else:
                        self.ui.check_p2_p3.setVisible(False)
                        self.ui.check_p2_p3.setChecked(False)
                    # show the data: dsb_p_3
                    if self.points_qty > 2:
                        self.ui.dsb_p_3.setVisible(True)
                        self.ui.dsb_p_3.setValue(self.set_point(file_content[5]))
                        self.ui.lbl_p3.setVisible(True)
                    else:
                        self.ui.dsb_p_3.setVisible(False)
                        self.ui.dsb_p_3.setValue(0)
                        self.ui.lbl_p3.setVisible(False)
                    # show the data: check_p3_p4
                    if self.points_qty > 2:
                        self.ui.check_p3_p4.setVisible(True)
                        if file_content[6].lower() == "x":
                            self.ui.check_p3_p4.setChecked(True)
                        else:
                            self.ui.check_p3_p4.setChecked(False)
                        if self.points_qty == 3:
                            self.ui.check_p3_p4.setText("after p3")
                        else:
                            self.ui.check_p3_p4.setText("between p3 and p4")
                    else:
                        self.ui.check_p3_p4.setVisible(False)
                        self.ui.check_p3_p4.setChecked(False)
                    # show the data: dsb_p_4
                    if self.points_qty > 3:
                        self.ui.dsb_p_4.setVisible(True)
                        self.ui.dsb_p_4.setValue(self.set_point(file_content[7]))
                        self.ui.lbl_p4.setVisible(True)
                    else:
                        self.ui.dsb_p_4.setVisible(False)
                        self.ui.dsb_p_4.setValue(0)
                        self.ui.lbl_p4.setVisible(False)
                    # show the data: check_p4_p5
                    if self.points_qty > 3:
                        self.ui.check_p4_p5.setVisible(True)
                        if file_content[8].lower() == "x":
                            self.ui.check_p4_p5.setChecked(True)
                        else:
                            self.ui.check_p4_p5.setChecked(False)
                        if self.points_qty == 4:
                            self.ui.check_p4_p5.setText("after p4")
                        else:
                            self.ui.check_p4_p5.setText("between p4 and p5")
                    else:
                        self.ui.check_p4_p5.setVisible(False)
                        self.ui.check_p4_p5.setChecked(False)
                    # show the data: dsb_p_5
                    if self.points_qty > 4:
                        self.ui.dsb_p_5.setVisible(True)
                        self.ui.dsb_p_5.setValue(self.set_point(file_content[9]))
                        self.ui.lbl_p5.setVisible(True)
                    else:
                        self.ui.dsb_p_5.setVisible(False)
                        self.ui.dsb_p_5.setValue(0)
                        self.ui.lbl_p5.setVisible(False)
                    # show the data: check_p5_p6
                    if self.points_qty > 4:
                        self.ui.check_p5_p6.setVisible(True)
                        if file_content[10].lower() == "x":
                            self.ui.check_p5_p6.setChecked(True)
                        else:
                            self.ui.check_p5_p6.setChecked(False)
                        if self.points_qty == 5:
                            self.ui.check_p5_p6.setText("after p5")
                        else:
                            self.ui.check_p5_p6.setText("between p5 and p6")
                    else:
                        self.ui.check_p5_p6.setVisible(False)
                        self.ui.check_p5_p6.setChecked(False)
                    # show the data: dsb_p_6
                    if self.points_qty > 5:
                        self.ui.dsb_p_6.setVisible(True)
                        self.ui.dsb_p_6.setValue(self.set_point(file_content[11]))
                        self.ui.lbl_p6.setVisible(True)
                    else:
                        self.ui.dsb_p_6.setVisible(False)
                        self.ui.dsb_p_6.setValue(0)
                        self.ui.lbl_p6.setVisible(False)
                    # show the data: check_p6_p7
                    if self.points_qty > 5:
                        self.ui.check_p6_p7.setVisible(True)
                        if file_content[12].lower() == "x":
                            self.ui.check_p6_p7.setChecked(True)
                        else:
                            self.ui.check_p6_p7.setChecked(False)
                        if self.points_qty == 6:
                            self.ui.check_p6_p7.setText("after p6")
                        else:
                            self.ui.check_p6_p7.setText("between p6 and p7")
                    else:
                        self.ui.check_p6_p7.setVisible(False)
                        self.ui.check_p6_p7.setChecked(False)
                    # show the data: dsb_p_7
                    if self.points_qty == 7:
                        self.ui.dsb_p_7.setVisible(True)
                        self.ui.dsb_p_7.setValue(self.set_point(file_content[13]))
                        self.ui.lbl_p7.setVisible(True)
                    else:
                        self.ui.dsb_p_7.setVisible(False)
                        self.ui.dsb_p_7.setValue(0)
                        self.ui.lbl_p7.setVisible(False)
                    # show the data: check_p7
                    if self.points_qty == 7:
                        self.ui.check_p7.setVisible(True)
                        if file_content[14].lower() == "x":
                            self.ui.check_p7.setChecked(True)
                        else:
                            self.ui.check_p7.setChecked(False)
                        self.ui.check_p7.setText("after p7")
                    else:
                        self.ui.check_p7.setVisible(False)
                        self.ui.check_p7.setChecked(False)
                else:
                    self.dialog_critical(f'Critical error while reading points:\n{message}.')
        except Exception as e:
            self.dialog_critical(f'Critical error in points_load_ui:\n{str(e)}.')

    def set_point(self, str_value):
        """
            This function converts str to float. Or it returns an error if impossible.
        :param str_value: str with a float in a text form
        :return: float from str or a message "error of conversion"
        """
        try:
            return float(str_value)
        except:
            return "error of conversion"

    def correct(self):
        """
            This is the main calculation function.
            It:
            1. checks the user's input and asks for improvements if there are problems
            2. reads the data, applies correction to it, and places the result in the global variable self.calc_result
            3. also creates a global variable self.manuel_adjust, which will contain the result of the manual adjustment, but so far it has the same data as self.calc_result
            4. configures the graph interface and manual adjustment, and plots the corrected data
        :return: None
        """
        # data verification
        # file(s) to read
        if self.files == "":
            self.ui.toolBox.setCurrentIndex(0)
            self.ui.btn_f.setFocus()
            self.dialog_critical(f'Please, choose a txt spectrum file to correct.')
        else:
            # all p values are non-zeros
            p_verif_non_zero = True
            if self.ui.dsb_p_1.value() == 0:
                p_verif_non_zero = False
            if self.ui.dsb_p_2.isVisible() and self.ui.dsb_p_2.value() == 0:
                p_verif_non_zero = False
            if self.ui.dsb_p_3.isVisible() and self.ui.dsb_p_3.value() == 0:
                p_verif_non_zero = False
            if self.ui.dsb_p_4.isVisible() and self.ui.dsb_p_4.value() == 0:
                p_verif_non_zero = False
            if self.ui.dsb_p_5.isVisible() and self.ui.dsb_p_5.value() == 0:
                p_verif_non_zero = False
            if self.ui.dsb_p_6.isVisible() and self.ui.dsb_p_6.value() == 0:
                p_verif_non_zero = False
            if self.ui.dsb_p_7.isVisible() and self.ui.dsb_p_7.value() == 0:
                p_verif_non_zero = False
            if not p_verif_non_zero:
                self.dialog_critical(f"All breakpoints must be non-zeros.\nPlease, fill or remove all empty point fields.")
                self.ui.toolBox.setCurrentIndex(1)
                self.ui.dsb_p_1.setFocus()
            else:
                # all p values must increase
                p_verif_increase = True
                if self.ui.dsb_p_2.value() != 0 and self.ui.dsb_p_1.value() >= self.ui.dsb_p_2.value():
                    p_verif_increase = False
                if self.ui.dsb_p_3.value() != 0 and self.ui.dsb_p_2.value() >= self.ui.dsb_p_3.value():
                    p_verif_increase = False
                if self.ui.dsb_p_4.value() != 0 and self.ui.dsb_p_3.value() >= self.ui.dsb_p_4.value():
                    p_verif_increase = False
                if self.ui.dsb_p_5.value() != 0 and self.ui.dsb_p_4.value() >= self.ui.dsb_p_5.value():
                    p_verif_increase = False
                if self.ui.dsb_p_6.value() != 0 and self.ui.dsb_p_5.value() >= self.ui.dsb_p_6.value():
                    p_verif_increase = False
                if self.ui.dsb_p_7.value() != 0 and self.ui.dsb_p_6.value() >= self.ui.dsb_p_7.value():
                    p_verif_increase = False
                if not p_verif_increase:
                    self.dialog_critical(f"Breakpoint values should increase.")
                    self.ui.toolBox.setCurrentIndex(1)
                    self.ui.dsb_p_1.setFocus()
                else:
                    self.p_array = []
                    self.p_array.append(self.ui.dsb_p_1.value())
                    if self.ui.dsb_p_2.value() != 0:
                        self.p_array.append(self.ui.dsb_p_2.value())
                    if self.ui.dsb_p_3.value() != 0:
                        self.p_array.append(self.ui.dsb_p_3.value())
                    if self.ui.dsb_p_4.value() != 0:
                        self.p_array.append(self.ui.dsb_p_4.value())
                    if self.ui.dsb_p_5.value() != 0:
                        self.p_array.append(self.ui.dsb_p_5.value())
                    if self.ui.dsb_p_6.value() != 0:
                        self.p_array.append(self.ui.dsb_p_6.value())
                    if self.ui.dsb_p_7.value() != 0:
                        self.p_array.append(self.ui.dsb_p_7.value())
                    # ref_intervals (True & False)
                    self.ref_intervals = []
                    for i in range(len(self.p_array) + 1):
                        if i == 0:
                            self.ref_intervals.append(self.ui.check_p1.isChecked())
                        elif i == 1:
                            self.ref_intervals.append(self.ui.check_p1_p2.isChecked())
                        elif i == 2:
                            self.ref_intervals.append(self.ui.check_p2_p3.isChecked())
                        elif i == 3:
                            self.ref_intervals.append(self.ui.check_p3_p4.isChecked())
                        elif i == 4:
                            self.ref_intervals.append(self.ui.check_p4_p5.isChecked())
                        elif i == 5:
                            self.ref_intervals.append(self.ui.check_p5_p6.isChecked())
                        elif i == 6:
                            self.ref_intervals.append(self.ui.check_p6_p7.isChecked())
                        elif i == 7:
                            self.ref_intervals.append(self.ui.check_p7.isChecked())
                    # fields reading
                    if self.ui.cb_f_type.currentIndex() != 1:
                        self.reflectance_column = self.ui.sb_refl_c.value()
                    else:
                        self.reflectance_column = "brdf"
                    self.reflectance_error = self.ui.chb_erro_c.isChecked()
                    self.file_type = self.ui.cb_f_type.currentText()
                    # data reading
                    if self.files:
                        self.calc_result = np.zeros((len(self.files), 7), dtype='object')
                        self.manuel_adjust = np.zeros((len(self.files), 2), dtype='object') # the manuel adjustment is made with this list
                        err_col_verif = False
                        p_verif = False
                        for file_number, file in enumerate(self.files):
                            try:
                                reading_error = False
                                data_reading_result = core.data_reading(file)
                                if type(data_reading_result) == str:
                                    reading_error = True
                                if not reading_error:
                                    # verification error column
                                    err_col_verif = True
                                    if self.reflectance_error:
                                        if self.file_type == unit_set[1]: # BRDF
                                            if len(data_reading_result[1][0]) % 2 != 1:
                                                err_col_verif = False
                                        elif self.file_type == unit_set[2]: # full data
                                            if len(data_reading_result[1][0]) != 13:
                                                err_col_verif = False
                                        elif self.file_type == unit_set[3]: # 3-col. data
                                            if len(data_reading_result[1][0]) != 3:
                                                err_col_verif = False
                                        else: # free format
                                            if len(data_reading_result[1][0]) != 3:
                                                if len(data_reading_result[1][0]) <= 2:
                                                    err_col_verif = False
                                                elif self.reflectance_column == len(data_reading_result[1][0]) - 1:
                                                    err_col_verif = False
                                    else:
                                        if self.file_type == unit_set[1]: # BRDF
                                            if len(data_reading_result[1][0]) < 2:
                                                err_col_verif = False
                                        elif self.file_type == unit_set[2]: # full data
                                            if len(data_reading_result[1][0]) != 12:
                                                err_col_verif = False
                                        elif self.file_type == unit_set[3]: # 3-col. data
                                            if len(data_reading_result[1][0]) != 2:
                                                err_col_verif = False
                                        else: # free format
                                            if len(data_reading_result[1][0]) != 3:
                                                if len(data_reading_result[1][0]) < 2:
                                                    err_col_verif = False
                                    if err_col_verif:
                                        # verification all p's are among wavelengths
                                        p_verif = True
                                        k = 0
                                        for item in data_reading_result[1]:
                                            if item[0] == self.p_array[k]:
                                                k = k + 1
                                                if k == len(self.p_array):
                                                    break
                                        if k != len(self.p_array):
                                            p_verif = False
                                        if p_verif:
                                            self.calc_result[file_number][0] = file[file.rfind("/") + 1:] # file name
                                            self.calc_result[file_number][1] = data_reading_result[0] # file header
                                            self.calc_result[file_number][2] = data_reading_result[1] # initial data
                                            self.calc_result[file_number][3] = data_reading_result[2] # file separator
                                            self.calc_result[file_number][4] = data_reading_result[3] # accuracy array
                                            try:
                                                self.p_intrvals = core.points_to_p_intervals(data_reading_result[1], self.p_array)
                                                adjusted_data = core.adjust_data(data_reading_result[1], self.reflectance_column, self.p_intrvals, self.ref_intervals, self.reflectance_error)
                                                self.calc_result[file_number][5] = adjusted_data[0] # calc result
                                                self.calc_result[file_number][6] = adjusted_data[1] # list of all f-factors
                                                self.manuel_adjust[file_number][0] = copy.deepcopy(adjusted_data[0])  # calc result
                                                self.manuel_adjust[file_number][1] = copy.deepcopy(adjusted_data[1])  # list of all f-factors
                                            except Exception as e:
                                                self.dialog_critical(f'Critical error while calculating the correction:\n{str(e)}.')
                                                break
                                        else:
                                            self.dialog_critical(f'There is a problem with breakpoints in {file[file.rfind("/") + 1:]}.'
                                                                 f'\nAt least {self.p_array[k]} nm was not found among the wavelengths of the data to be corrected.'
                                                                 f'\nAll breakpoints must be among the wavelengths of the data to be corrected.')
                                            self.ui.toolBox.setCurrentIndex(1)
                                            break
                                    else:
                                        self.dialog_critical(f'There is a problem with the error column in {file[file.rfind("/") + 1:]}.'
                                                             f'\nPossible cause of the error: wrong file format.'
                                                             f'\nOr there is no column with errors in this file, while it is indicated that there is.')
                                        self.ui.toolBox.setCurrentIndex(0)
                                        break
                                else:
                                    self.dialog_critical(f'Critical error while reading the data from {file[file.rfind("/") + 1:]}: {data_reading_result}.')
                                    break
                            except Exception as e:
                                self.dialog_critical(f'Critical error while reading the data from {file[file.rfind("/") + 1:]}.')
                                break
                        try:
                            if err_col_verif and p_verif:
                                # cb_file
                                self.ui.cb_file.clear()
                                for number, file in enumerate(self.files):
                                    file_name = file[file.rfind("/") + 1:]
                                    self.ui.cb_file.insertItem(number, file_name)
                                self.ui.cb_file.setCurrentIndex(0)
                                # graph title
                                self.ui.graphWidget.setTitle(f"{self.ui.cb_file.currentText()}, column: ---", **graph_title)
                                # gpraph ui
                                self.graphe_ui_f()
                                # columns ui (default view of the manuel adjustment interface)
                                self.ui.cb_cn.clear()
                                if self.file_type != unit_set[1]: # free, complete or simple
                                    self.ui.cb_cn.insertItem(0, 'reflectance')
                                else: # BRDF
                                    k = 0
                                    for i, v in enumerate(self.calc_result[0][1][5].split(self.calc_result[0][3])):
                                        if "Refl" in v:
                                            self.ui.cb_cn.insertItem(k, f"{v[v.rfind('_') + 1:]}")
                                            k = k + 1
                                self.ui.cb_cn.setCurrentIndex(0)
                                # graph plot
                                self.current_column = self.ui.cb_cn.currentIndex()
                                self.plot_refresh()
                                # graph: adjusted data plot
                                self.manuel_adjust_compute()
                                self.calc_result_flag = True
                                self.first_run = False
                                self.dialog_ok("The correction is calculated successfully!\nNow you can plot or export the result.")
                        except Exception as e:
                            self.dialog_critical(f'Critical error during the first plot:\n{str(e)}.')
                    else:
                        self.dialog_critical(f'Please chose a txt file to correct\nbefore the correction.')
                        self.ui.toolBox.setCurrentIndex(0)
                        self.ui.btn_f.setFocus()

    def graphe_ui_f(self):
        """
            This function sets the graph and GUI for the manually adjust depending on the breakpoints.
            It is executed only once: at the end of self.correction().
            It:
            1. shows or hides fields for correction factors (depending on whether they are used or not)
            2. changes the labels with ranges for these fields
            3. sets the infinity lines to display breakpoints on the graph
        :return: None
        """
        try:
            # default disable state
            self.ui.graphWidget.removeItem(self.p1_inf)
            self.ui.graphWidget.removeItem(self.p2_inf)
            self.ui.graphWidget.removeItem(self.p3_inf)
            self.ui.graphWidget.removeItem(self.p4_inf)
            self.ui.graphWidget.removeItem(self.p5_inf)
            self.ui.graphWidget.removeItem(self.p6_inf)
            self.ui.graphWidget.removeItem(self.p7_inf)
            # 7 points
            if self.ui.dsb_p_7.value() and self.ui.dsb_p_6.value() and self.ui.dsb_p_5.value() and self.ui.dsb_p_4.value() and self.ui.dsb_p_3.value() and self.ui.dsb_p_2.value() and self.ui.dsb_p_1.value():
                # shows all dsb-fields
                self.set_visible_all()
                # enables the used dsb-fields and hides the unused ones
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p4.setDisabled(False)
                self.ui.dsb_p5.setDisabled(False)
                self.ui.dsb_p6.setDisabled(False)
                self.ui.dsb_p7.setDisabled(False)
                self.ui.dsb_p8.setDisabled(False)
                # changes labels (and hides them if they are unused)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.mid_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value(), self.ui.dsb_p_2.value())
                # lb_p3_v
                self.mid_point_ui_set(self.ui.lb_p3_v, self.ui.dsb_p_2.value(), self.ui.dsb_p_3.value())
                # lb_p4_v
                self.mid_point_ui_set(self.ui.lb_p4_v, self.ui.dsb_p_3.value(), self.ui.dsb_p_4.value())
                # lb_p5_v
                self.mid_point_ui_set(self.ui.lb_p5_v, self.ui.dsb_p_4.value(), self.ui.dsb_p_5.value())
                # lb_p6_v
                self.mid_point_ui_set(self.ui.lb_p6_v, self.ui.dsb_p_5.value(), self.ui.dsb_p_6.value())
                # lb_p7_v
                self.mid_point_ui_set(self.ui.lb_p7_v, self.ui.dsb_p_6.value(), self.ui.dsb_p_7.value())
                # lb_p8_v
                self.last_point_ui_set(self.ui.lb_p8_v, self.ui.dsb_p_7.value())
                # adds infinity lines for the breakpoints
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
                self.ui.graphWidget.removeItem(self.p2_inf)
                self.p2_inf = pg.InfiniteLine(self.ui.dsb_p_2.value())
                self.ui.graphWidget.addItem(self.p2_inf)
                self.ui.graphWidget.removeItem(self.p3_inf)
                self.p3_inf = pg.InfiniteLine(self.ui.dsb_p_3.value())
                self.ui.graphWidget.addItem(self.p3_inf)
                self.ui.graphWidget.removeItem(self.p4_inf)
                self.p4_inf = pg.InfiniteLine(self.ui.dsb_p_4.value())
                self.ui.graphWidget.addItem(self.p4_inf)
                self.ui.graphWidget.removeItem(self.p5_inf)
                self.p5_inf = pg.InfiniteLine(self.ui.dsb_p_5.value())
                self.ui.graphWidget.addItem(self.p5_inf)
                self.ui.graphWidget.removeItem(self.p6_inf)
                self.p6_inf = pg.InfiniteLine(self.ui.dsb_p_6.value())
                self.ui.graphWidget.addItem(self.p6_inf)
                self.ui.graphWidget.removeItem(self.p7_inf)
                self.p7_inf = pg.InfiniteLine(self.ui.dsb_p_7.value())
                self.ui.graphWidget.addItem(self.p7_inf)
            # 6 points
            elif self.ui.dsb_p_6.value() and self.ui.dsb_p_5.value() and self.ui.dsb_p_4.value() and self.ui.dsb_p_3.value() and self.ui.dsb_p_2.value() and self.ui.dsb_p_1.value():
                self.set_visible_all()
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p4.setDisabled(False)
                self.ui.dsb_p5.setDisabled(False)
                self.ui.dsb_p6.setDisabled(False)
                self.ui.dsb_p7.setDisabled(False)
                self.ui.dsb_p8.setVisible(False)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.mid_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value(), self.ui.dsb_p_2.value())
                # lb_p3_v
                self.mid_point_ui_set(self.ui.lb_p3_v, self.ui.dsb_p_2.value(), self.ui.dsb_p_3.value())
                # lb_p4_v
                self.mid_point_ui_set(self.ui.lb_p4_v, self.ui.dsb_p_3.value(), self.ui.dsb_p_4.value())
                # lb_p5_v
                self.mid_point_ui_set(self.ui.lb_p5_v, self.ui.dsb_p_4.value(), self.ui.dsb_p_5.value())
                # lb_p6_v
                self.mid_point_ui_set(self.ui.lb_p6_v, self.ui.dsb_p_5.value(), self.ui.dsb_p_6.value())
                # lb_p7_v
                self.last_point_ui_set(self.ui.lb_p7_v, self.ui.dsb_p_6.value())
                self.ui.lb_p8_v.setVisible(False)
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
                self.ui.graphWidget.removeItem(self.p2_inf)
                self.p2_inf = pg.InfiniteLine(self.ui.dsb_p_2.value())
                self.ui.graphWidget.addItem(self.p2_inf)
                self.ui.graphWidget.removeItem(self.p3_inf)
                self.p3_inf = pg.InfiniteLine(self.ui.dsb_p_3.value())
                self.ui.graphWidget.addItem(self.p3_inf)
                self.ui.graphWidget.removeItem(self.p4_inf)
                self.p4_inf = pg.InfiniteLine(self.ui.dsb_p_4.value())
                self.ui.graphWidget.addItem(self.p4_inf)
                self.ui.graphWidget.removeItem(self.p5_inf)
                self.p5_inf = pg.InfiniteLine(self.ui.dsb_p_5.value())
                self.ui.graphWidget.addItem(self.p5_inf)
                self.ui.graphWidget.removeItem(self.p6_inf)
                self.p6_inf = pg.InfiniteLine(self.ui.dsb_p_6.value())
                self.ui.graphWidget.addItem(self.p6_inf)
            # 5 points
            elif self.ui.dsb_p_5.value() and self.ui.dsb_p_4.value() and self.ui.dsb_p_3.value() and self.ui.dsb_p_2.value() and self.ui.dsb_p_1.value():
                self.set_visible_all()
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p4.setDisabled(False)
                self.ui.dsb_p5.setDisabled(False)
                self.ui.dsb_p6.setDisabled(False)
                self.ui.dsb_p7.setVisible(False)
                self.ui.dsb_p8.setVisible(False)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.mid_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value(), self.ui.dsb_p_2.value())
                # lb_p3_v
                self.mid_point_ui_set(self.ui.lb_p3_v, self.ui.dsb_p_2.value(), self.ui.dsb_p_3.value())
                # lb_p4_v
                self.mid_point_ui_set(self.ui.lb_p4_v, self.ui.dsb_p_3.value(), self.ui.dsb_p_4.value())
                # lb_p5_v
                self.mid_point_ui_set(self.ui.lb_p5_v, self.ui.dsb_p_4.value(), self.ui.dsb_p_5.value())
                # lb_p6_v
                self.last_point_ui_set(self.ui.lb_p6_v, self.ui.dsb_p_5.value())
                self.ui.lb_p7_v.setVisible(False)
                self.ui.lb_p8_v.setVisible(False)
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
                self.ui.graphWidget.removeItem(self.p2_inf)
                self.p2_inf = pg.InfiniteLine(self.ui.dsb_p_2.value())
                self.ui.graphWidget.addItem(self.p2_inf)
                self.ui.graphWidget.removeItem(self.p3_inf)
                self.p3_inf = pg.InfiniteLine(self.ui.dsb_p_3.value())
                self.ui.graphWidget.addItem(self.p3_inf)
                self.ui.graphWidget.removeItem(self.p4_inf)
                self.p4_inf = pg.InfiniteLine(self.ui.dsb_p_4.value())
                self.ui.graphWidget.addItem(self.p4_inf)
                self.ui.graphWidget.removeItem(self.p5_inf)
                self.p5_inf = pg.InfiniteLine(self.ui.dsb_p_5.value())
                self.ui.graphWidget.addItem(self.p5_inf)
            # 4 points
            elif self.ui.dsb_p_4.value() and self.ui.dsb_p_3.value() and self.ui.dsb_p_2.value() and self.ui.dsb_p_1.value():
                self.set_visible_all()
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p4.setDisabled(False)
                self.ui.dsb_p5.setDisabled(False)
                self.ui.dsb_p6.setVisible(False)
                self.ui.dsb_p7.setVisible(False)
                self.ui.dsb_p8.setVisible(False)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.mid_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value(), self.ui.dsb_p_2.value())
                # lb_p3_v
                self.mid_point_ui_set(self.ui.lb_p3_v, self.ui.dsb_p_2.value(), self.ui.dsb_p_3.value())
                # lb_p4_v
                self.mid_point_ui_set(self.ui.lb_p4_v, self.ui.dsb_p_3.value(), self.ui.dsb_p_4.value())
                # lb_p5_v
                self.last_point_ui_set(self.ui.lb_p5_v, self.ui.dsb_p_4.value())
                self.ui.lb_p6_v.setVisible(False)
                self.ui.lb_p7_v.setVisible(False)
                self.ui.lb_p8_v.setVisible(False)
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
                self.ui.graphWidget.removeItem(self.p2_inf)
                self.p2_inf = pg.InfiniteLine(self.ui.dsb_p_2.value())
                self.ui.graphWidget.addItem(self.p2_inf)
                self.ui.graphWidget.removeItem(self.p3_inf)
                self.p3_inf = pg.InfiniteLine(self.ui.dsb_p_3.value())
                self.ui.graphWidget.addItem(self.p3_inf)
                self.ui.graphWidget.removeItem(self.p4_inf)
                self.p4_inf = pg.InfiniteLine(self.ui.dsb_p_4.value())
                self.ui.graphWidget.addItem(self.p4_inf)
            # 3 points
            elif self.ui.dsb_p_3.value() and self.ui.dsb_p_2.value() and self.ui.dsb_p_1.value():
                self.set_visible_all()
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p4.setDisabled(False)
                self.ui.dsb_p5.setVisible(False)
                self.ui.dsb_p6.setVisible(False)
                self.ui.dsb_p7.setVisible(False)
                self.ui.dsb_p8.setVisible(False)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.mid_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value(), self.ui.dsb_p_2.value())
                # lb_p3_v
                self.mid_point_ui_set(self.ui.lb_p3_v, self.ui.dsb_p_2.value(), self.ui.dsb_p_3.value())
                # lb_p4_v
                self.last_point_ui_set(self.ui.lb_p4_v, self.ui.dsb_p_3.value())
                self.ui.lb_p5_v.setVisible(False)
                self.ui.lb_p6_v.setVisible(False)
                self.ui.lb_p7_v.setVisible(False)
                self.ui.lb_p8_v.setVisible(False)
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
                self.ui.graphWidget.removeItem(self.p2_inf)
                self.p2_inf = pg.InfiniteLine(self.ui.dsb_p_2.value())
                self.ui.graphWidget.addItem(self.p2_inf)
                self.ui.graphWidget.removeItem(self.p3_inf)
                self.p3_inf = pg.InfiniteLine(self.ui.dsb_p_3.value())
                self.ui.graphWidget.addItem(self.p3_inf)
            # 2 points
            elif self.ui.dsb_p_2.value() and self.ui.dsb_p_1.value():
                self.set_visible_all()
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p4.setVisible(False)
                self.ui.dsb_p5.setVisible(False)
                self.ui.dsb_p6.setVisible(False)
                self.ui.dsb_p7.setVisible(False)
                self.ui.dsb_p8.setVisible(False)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.mid_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value(), self.ui.dsb_p_2.value())
                # lb_p3_v
                self.last_point_ui_set(self.ui.lb_p3_v, self.ui.dsb_p_2.value())
                self.ui.lb_p4_v.setVisible(False)
                self.ui.lb_p5_v.setVisible(False)
                self.ui.lb_p6_v.setVisible(False)
                self.ui.lb_p7_v.setVisible(False)
                self.ui.lb_p8_v.setVisible(False)
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
                self.ui.graphWidget.removeItem(self.p2_inf)
                self.p2_inf = pg.InfiniteLine(self.ui.dsb_p_2.value())
                self.ui.graphWidget.addItem(self.p2_inf)
            # 1 points
            elif self.ui.dsb_p_1.value():
                self.set_visible_all()
                self.ui.dsb_p1.setDisabled(False)
                self.ui.dsb_p2.setDisabled(False)
                self.ui.dsb_p3.setVisible(False)
                self.ui.dsb_p4.setVisible(False)
                self.ui.dsb_p5.setVisible(False)
                self.ui.dsb_p6.setVisible(False)
                self.ui.dsb_p7.setVisible(False)
                self.ui.dsb_p8.setVisible(False)
                # lb_p1_v
                self.first_point_ui_set(self.ui.lb_p1_v, self.ui.dsb_p_1.value())
                # lb_p2_v
                self.last_point_ui_set(self.ui.lb_p2_v, self.ui.dsb_p_1.value())
                self.ui.lb_p3_v.setVisible(False)
                self.ui.lb_p4_v.setVisible(False)
                self.ui.lb_p5_v.setVisible(False)
                self.ui.lb_p6_v.setVisible(False)
                self.ui.lb_p7_v.setVisible(False)
                self.ui.lb_p8_v.setVisible(False)
                self.ui.graphWidget.removeItem(self.p1_inf)
                self.p1_inf = pg.InfiniteLine(self.ui.dsb_p_1.value())
                self.ui.graphWidget.addItem(self.p1_inf)
            # no points
            else:
                self.ui.dsb_p1.setVisible(False)
                self.ui.dsb_p2.setVisible(False)
                self.ui.dsb_p3.setVisible(False)
                self.ui.dsb_p4.setVisible(False)
                self.ui.dsb_p5.setVisible(False)
                self.ui.dsb_p6.setVisible(False)
                self.ui.dsb_p7.setVisible(False)
                self.ui.dsb_p8.setVisible(False)
                self.ui.lb_p1_v.setText('f before p1')
                self.ui.lb_p2_v.setText('f between p1 and p2')
                self.ui.lb_p3_v.setText('f between p2 and p3')
                self.ui.lb_p4_v.setText('f between p3 and p4')
                self.ui.lb_p5_v.setText('f between p4 and p5')
                self.ui.lb_p6_v.setText('f between p5 and p6')
                self.ui.lb_p7_v.setText('f between p6 and p7')
                self.ui.lb_p8_v.setText('f after p7')
                self.ui.lb_p1_v.setVisible(False)
                self.ui.lb_p2_v.setVisible(False)
                self.ui.lb_p3_v.setVisible(False)
                self.ui.lb_p4_v.setVisible(False)
                self.ui.lb_p5_v.setVisible(False)
                self.ui.lb_p6_v.setVisible(False)
                self.ui.lb_p7_v.setVisible(False)
                self.ui.lb_p8_v.setVisible(False)
        except Exception as e:
            self.dialog_critical(f'Critical error in point_added_ui:\n{str(e)}.')

    def set_visible_all(self):
        """
            This function shows all dsb-fields.
        :return: None
        """
        self.ui.dsb_p1.setVisible(True)
        self.ui.dsb_p2.setVisible(True)
        self.ui.dsb_p3.setVisible(True)
        self.ui.dsb_p4.setVisible(True)
        self.ui.dsb_p5.setVisible(True)
        self.ui.dsb_p6.setVisible(True)
        self.ui.dsb_p7.setVisible(True)
        self.ui.dsb_p8.setVisible(True)
        self.ui.lb_p1_v.setVisible(True)
        self.ui.lb_p2_v.setVisible(True)
        self.ui.lb_p3_v.setVisible(True)
        self.ui.lb_p4_v.setVisible(True)
        self.ui.lb_p5_v.setVisible(True)
        self.ui.lb_p6_v.setVisible(True)
        self.ui.lb_p7_v.setVisible(True)
        self.ui.lb_p8_v.setVisible(True)

    def first_point_ui_set(self, p_lbl, p_value):
        """
            This function sets p_lbl for the first breakpoint.
        :param p_lbl: label for a dsb-field
        :param p_value: breakpoint value
        :return: None
        """
        p_lbl.setText(f'f for wl<={p_value}')

    def mid_point_ui_set(self, p_lbl, p_l_value, p_u_value):
        """
            This function sets p_lbl for any breakpoint if it is not first or last.
        :param p_lbl: label for a dsb-field
        :param p_l_value: lower value of breakpoint for the range
        :param p_u_value: upper value of breakpoint for the range
        :return:
        """
        p_lbl.setText(f'f for {p_l_value}<wl<={p_u_value}')

    def last_point_ui_set(self, p_lbl, p_value):
        """
            This function sets p_lbl for the last breakpoint.
        :param p_lbl: label for a dsb-field
        :param p_value: breakpoint value
        :return: None
        """
        p_lbl.setText(f'f wl>{p_value}')

    def plot_refresh(self):
        """
            This function is used each time the graph must be modified (the first display but also when the user chooses another BRDF column or/and another spectrum).
        It:
            1. Initializes all f-factors in the dsb-fields
            2. Plots the initial data
            3. Plots the calculated correction data
        :return: None
        """
        try:
            self.dsb_user = False # dsb-fields are not changed by user, so dsb_change will not take it
            self.sb_change_last = []
            # reset all dsb-fields
            self.ui.dsb_p1.setValue(0)
            self.ui.dsb_p2.setValue(0)
            self.ui.dsb_p3.setValue(0)
            self.ui.dsb_p4.setValue(0)
            self.ui.dsb_p5.setValue(0)
            self.ui.dsb_p6.setValue(0)
            self.ui.dsb_p7.setValue(0)
            # set current f-factors in the dsb-fields
            self.ui.dsb_p1.setDisabled(False)
            self.ui.dsb_p1.setValue(self.manuel_adjust[self.current_file][1][self.current_column][0]) # self.manuel_adjust list has indexes [file][1][column][f]
            self.sb_change_last.append(self.ui.dsb_p1.value())
            self.ui.dsb_p2.setDisabled(False)
            self.ui.dsb_p2.setValue(self.manuel_adjust[self.current_file][1][self.current_column][1])
            self.sb_change_last.append(self.ui.dsb_p2.value())
            if len(self.p_array) >= 2:
                self.ui.dsb_p3.setDisabled(False)
                self.ui.dsb_p3.setValue(self.manuel_adjust[self.current_file][1][self.current_column][2])
                self.sb_change_last.append(self.ui.dsb_p3.value())
            if len(self.p_array) >= 3:
                self.ui.dsb_p4.setDisabled(False)
                self.ui.dsb_p4.setValue(self.manuel_adjust[self.current_file][1][self.current_column][3])
                self.sb_change_last.append(self.ui.dsb_p4.value())
            if len(self.p_array) >= 4:
                self.ui.dsb_p5.setDisabled(False)
                self.ui.dsb_p5.setValue(self.manuel_adjust[self.current_file][1][self.current_column][4])
                self.sb_change_last.append(self.ui.dsb_p5.value())
            if len(self.p_array) >= 5:
                self.ui.dsb_p6.setDisabled(False)
                self.ui.dsb_p6.setValue(self.manuel_adjust[self.current_file][1][self.current_column][5])
                self.sb_change_last.append(self.ui.dsb_p6.value())
            if len(self.p_array) >= 6:
                self.ui.dsb_p7.setDisabled(False)
                self.ui.dsb_p7.setValue(self.manuel_adjust[self.current_file][1][self.current_column][6])
                self.sb_change_last.append(self.ui.dsb_p7.value())
            if len(self.p_array) >= 7:
                self.ui.dsb_p8.setDisabled(False)
                self.ui.dsb_p8.setValue(self.manuel_adjust[self.current_file][1][self.current_column][7])
                self.sb_change_last.append(self.ui.dsb_p8.value())
            # fixed field color change
            self.ui.dsb_p1.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p2.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p3.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p4.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p5.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p6.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p7.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            self.ui.dsb_p8.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", "white"))
            bg_color = "#C4E2FF"
            for i, v in enumerate(self.ref_intervals):
                if v:
                    if i == 0:
                        self.ui.dsb_p1.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 1:
                        self.ui.dsb_p2.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 2:
                        self.ui.dsb_p3.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 3:
                        self.ui.dsb_p4.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 4:
                        self.ui.dsb_p5.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 5:
                        self.ui.dsb_p6.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 6:
                        self.ui.dsb_p7.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
                    elif i == 7:
                        self.ui.dsb_p8.setStyleSheet("QDoubleSpinBox { background-color: blue; }".replace("blue", bg_color))
            self.dsb_user = True # set user control again
            # initial data plot
            wlth_array = []
            temp_array = []
            for line in self.calc_result[self.current_file][2]:
                wlth_array.append(line[0])
                if self.file_type != unit_set[1]: # free, simple, full
                    temp_array.append(line[self.reflectance_column - 1])
                else: # BRDF
                    if self.reflectance_error:
                        temp_array.append(line[2 * self.current_column + 1])
                    else:
                        temp_array.append(line[self.current_column + 1])
            self.line_initial.setData(wlth_array, temp_array)
            # graph: corrected data plot
            temp_array = []
            for line in self.calc_result[self.current_file][5]:
                if self.file_type != unit_set[1]:  # free, simple, full
                    temp_array.append(line[self.reflectance_column - 1])
                else:  # BRDF
                    if self.reflectance_error:
                        temp_array.append(line[2 * self.current_column + 1])
                    else:
                        temp_array.append(line[self.current_column + 1])
            self.line_calculated.setData(wlth_array, temp_array)
        except Exception as e:
            self.dialog_critical(f'Critical error in plot_refresh: {str(e)}.')

    def manuel_adjust_compute(self):
        """
            This function calculates and plots the adjustments made by the user.
        It:
            1. Computes self.manuel_adjust (the list where the result of the manual adjustment is) by multiplying the initial data (in self.calc_result) by the dsb-fields values
            2. Plots the manually corrected data
        :return: None
        """
        try:
            if self.dsb_user:
                # calc
                for index, interval in enumerate(self.ref_intervals):
                    for i in range(self.p_intrvals[index][0], self.p_intrvals[index][1] + 1):
                        if index == 0:
                            if self.file_type != unit_set[1]: # free, simple, full
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p1.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p1.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p1.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p1.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p1.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p1.value()
                        if index == 1:
                            if self.file_type != unit_set[1]: # free, simple, full
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p2.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p2.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p2.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p2.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p2.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p2.value()
                        if index == 2:
                            if self.file_type != unit_set[1]: # free, simple
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p3.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p3.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p3.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p3.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p3.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p3.value()
                        if index == 3:
                            if self.file_type != unit_set[1]: # free, simple, full
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p4.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p4.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p4.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p4.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p4.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p4.value()
                        if index == 4:
                            if self.file_type != unit_set[1]: # free, simple, full
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p5.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p5.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p5.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p5.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p5.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p5.value()
                        if index == 5:
                            if self.file_type != unit_set[1]: # free, simple, full
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p6.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p6.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p6.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p6.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p6.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p6.value()
                        if index == 6:
                            if self.file_type != unit_set[1]: # free, simple, full
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p7.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p7.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p7.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p7.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p7.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p7.value()
                        if index == 7:
                            if self.file_type != unit_set[1]: # free, simple
                                self.manuel_adjust[self.current_file][0][i][self.reflectance_column - 1] = self.calc_result[self.current_file][2][i][self.reflectance_column - 1] * self.ui.dsb_p8.value()
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][self.reflectance_column] = self.calc_result[self.current_file][2][i][self.reflectance_column] * self.ui.dsb_p8.value()
                            else:  # BRDF
                                if self.reflectance_error:
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 1] = self.calc_result[self.current_file][2][i][2 * self.current_column + 1] * self.ui.dsb_p8.value()
                                    self.manuel_adjust[self.current_file][0][i][2 * self.current_column + 2] = self.calc_result[self.current_file][2][i][2 * self.current_column + 2] * self.ui.dsb_p8.value()
                                else:
                                    self.manuel_adjust[self.current_file][0][i][self.current_column + 1] = self.calc_result[self.current_file][2][i][self.current_column + 1] * self.ui.dsb_p8.value()
                            self.manuel_adjust[self.current_file][1][self.current_column][index] = self.ui.dsb_p8.value()
                # plot
                temp_array = []
                wlth_array = []
                for line in self.manuel_adjust[self.current_file][0]:
                    wlth_array.append(line[0])
                    if self.file_type != unit_set[1]:  # free, simple, full
                        temp_array.append(line[self.reflectance_column - 1])
                    else:  # BRDF
                        if self.reflectance_error:
                            temp_array.append(line[2 * self.current_column + 1])
                        else:
                            temp_array.append(line[self.current_column + 1])
                self.line_corrected.setData(wlth_array, temp_array)
        except Exception as e:
            self.dialog_critical(f'Critical error in manuel_adjust_compute: {str(e)}.')

    def dsb_change(self, index=0):
        """
            This function starts when a dsb field is modified.
        It:
            1. Runs self.dsb_value_change() which determines the change in the dsb-field affected by the manual change and calculates the appropriate changes for the other fields
            2. Runs self.dsb_show() which changes all dsb-fields accordingly
            3. Runs self.manuel_adjust_compute() which calculates the changes made manually and plots them in the graph
        :param index: int from 1 to 8 which is the concerned dsb-field number
        :return: None
        """
        if index != 0:
            self.dsb_value_change(index)
            self.dsb_show()
            self.manuel_adjust_compute()

    def dsb_value_change(self, index):
        """
            This function determines the change in the dsb-field affected by the manual change and calculates the appropriate changes for the other fields.
        :param index: int from 1 to 8 which is the concerned dsb-field number
        :return: None
        """
        try:
            if self.dsb_user:
                # determines the delta = last_value - new_value
                delta = 0
                if index == 1:
                    delta =  self.ui.dsb_p1.value() - self.sb_change_last[index - 1]
                elif index == 2:
                    delta = self.ui.dsb_p2.value() - self.sb_change_last[index - 1]
                elif index == 3:
                    delta = self.ui.dsb_p3.value() - self.sb_change_last[index - 1]
                elif index == 4:
                    delta = self.ui.dsb_p4.value() - self.sb_change_last[index - 1]
                elif index == 5:
                    delta = self.ui.dsb_p5.value() - self.sb_change_last[index - 1]
                elif index == 6:
                    delta = self.ui.dsb_p6.value() - self.sb_change_last[index - 1]
                elif index == 7:
                    delta = self.ui.dsb_p7.value() - self.sb_change_last[index - 1]
                elif index == 8:
                    delta = self.ui.dsb_p8.value() - self.sb_change_last[index - 1]
                # determines the break interval
                i_break = 0
                for i in range(0, len(self.ref_intervals)):
                    if self.ref_intervals[i]:
                        i_break = i + 1
                        break
                # propagates the changes
                if index < i_break:
                    for i in range(index - 1, -1, -1):
                        self.sb_change_last[i] = self.sb_change_last[i] + delta
                elif index > i_break:
                    for i in range(index - 1, len(self.sb_change_last)):
                        self.sb_change_last[i] = self.sb_change_last[i] + delta
                else:
                    for i in range(0, len(self.sb_change_last)):
                        self.sb_change_last[i] = self.sb_change_last[i] + delta
        except Exception as e:
            self.dialog_critical(f'Critical error in dsb_value_change: {str(e)}.')

    def dsb_show(self):
        """
            This function changes all dsb-fields accordingly to the result found by self.dsb_value_change()
        :return: None
        """
        try:
            if self.dsb_user:
                self.dsb_user = False
                self.ui.dsb_p1.setValue(self.sb_change_last[0])
                self.ui.dsb_p2.setValue(self.sb_change_last[1])
                if len(self.sb_change_last) >= 3:
                    self.ui.dsb_p3.setValue(self.sb_change_last[2])
                if len(self.sb_change_last) >= 4:
                    self.ui.dsb_p4.setValue(self.sb_change_last[3])
                if len(self.sb_change_last) >= 5:
                    self.ui.dsb_p5.setValue(self.sb_change_last[4])
                if len(self.sb_change_last) >= 6:
                    self.ui.dsb_p6.setValue(self.sb_change_last[5])
                if len(self.sb_change_last) >= 7:
                    self.ui.dsb_p7.setValue(self.sb_change_last[6])
                if len(self.sb_change_last) >= 8:
                    self.ui.dsb_p8.setValue(self.sb_change_last[7])
                self.dsb_user = True
        except Exception as e:
            self.dialog_critical(f'Critical error in dsb_show: {str(e)}.')

    def column_changed(self, input_type=0):
        """
            This function starts when another BRDF-column is selected in the graphics window.
        It:
            1. It collects the new column number in self.current_column
            2. Executes self.column_file_changed() which changes the title of the graph and executes self.plot_refresh() and self.manuel_adjust_compute() (to calculate and plot new colon/file)
        :return: None
        """
        try:
            if input_type != 0:
                if self.ui.cb_cn.currentIndex() != -1:
                    self.current_column = self.ui.cb_cn.currentIndex()
                    self.column_file_changed()
        except Exception as e:
            self.dialog_critical(f'Critical error in column_changed: {str(e)}.')

    def file_changed(self, input_type=0):
        """
            This function starts when another file is selected in the graph window.
        It:
            1. It collects the new file number in self.current_file
            2. Executes self.column_file_changed() which changes the title of the graph and executes self.plot_refresh() and self.manuel_adjust_compute() (to calculate and plot new colon/file)
        :return: None
        """
        try:
            if input_type != 0:
                if self.ui.cb_file.currentIndex() != -1:
                    self.current_file = self.ui.cb_file.currentIndex()
                    self.column_file_changed()
        except Exception as e:
            self.dialog_critical(f'Critical error in file_changed: {str(e)}.')

    def column_file_changed(self):
        """
            This function applies column/file changes.
        It:
            1. Changes the title of the graph
            2. Executes self.plot_refresh() to plot the calculated and initial data for that column/file
            3. Executes self.manuel_adjust_compute() to plot manually adjusted data
        :return: None
        """
        try:
            # graph title
            column_text = ""
            if self.file_type == unit_set[0]:
                column_text = f"column: {self.ui.cb_cn.currentText()}"
            else:
                column_text = f"{self.ui.cb_cn.currentText()}"
            self.ui.graphWidget.setTitle(f"{self.ui.cb_file.currentText()}, {column_text}", **graph_title)
            # graph plot
            if self.calc_result_flag:
                self.plot_refresh()
                self.manuel_adjust_compute()
        except Exception as e:
            self.dialog_critical(f'Critical error in column_file_changed: {str(e)}.')

    def reset_current(self):
        """
            This function resets the current graph.
        It:
            1. Resets all f-coefficients in self.manuel_adjust
            2. Executes self.plot refresh() to put these f-coefficients in the GUI
            3. Executes self.manuel_adjust_compute() to recalculate the data in self.manuel_adjust and to retrace the graph
        :return: None
        """
        try:
            if self.calc_result_flag:
                ret = QMessageBox.question(self, 'Reset the current correction? ', "Are you sure to reset\nthe current spectrum correction?", QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.Yes:
                    # reset f
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 1: # self.manuel_adjust list has indexes [file][0 for data/1 for f][column][data-line/f]
                        self.manuel_adjust[self.current_file][1][self.current_column][0] = self.calc_result[self.current_file][6][self.current_column][0]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 2:
                        self.manuel_adjust[self.current_file][1][self.current_column][1] = self.calc_result[self.current_file][6][self.current_column][1]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 3:
                        self.manuel_adjust[self.current_file][1][self.current_column][2] = self.calc_result[self.current_file][6][self.current_column][2]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 4:
                        self.manuel_adjust[self.current_file][1][self.current_column][3] = self.calc_result[self.current_file][6][self.current_column][3]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 5:
                        self.manuel_adjust[self.current_file][1][self.current_column][4] = self.calc_result[self.current_file][6][self.current_column][4]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 6:
                        self.manuel_adjust[self.current_file][1][self.current_column][5] = self.calc_result[self.current_file][6][self.current_column][5]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 7:
                        self.manuel_adjust[self.current_file][1][self.current_column][6] = self.calc_result[self.current_file][6][self.current_column][6]
                    if len(self.manuel_adjust[self.current_file][1][self.current_column]) >= 8:
                        self.manuel_adjust[self.current_file][1][self.current_column][7] = self.calc_result[self.current_file][6][self.current_column][7]
                    # graph plot & dsb-fields
                    self.plot_refresh()
                    # graph: adjusted data plot & self.manuel_adjust compute
                    self.manuel_adjust_compute()
        except Exception as e:
            self.dialog_critical(f'Critical error in reset_current: {str(e)}.')

    def reset_all(self):
        """
            This function resets all graphs.
        It:
            1. Deep-copies all the data and f-coefficients from self.calc_result to self.manuel_adjust
            2. Executes self.plot refresh() to put these f-coefficients in the GUI
            3. Executes self.manuel_adjust_compute() to recalculate the data in self.manuel_adjust and to retrace the graph
        :return: None
        """
        try:
            if self.calc_result_flag:
                ret = QMessageBox.question(self, 'Reset all corrections? ', "Are you sure to reset\nall spectrum corrections?", QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.Yes:
                    # deep copy f-coefficients
                    for file_number in range(0, len(self.calc_result)):
                        self.manuel_adjust[file_number][0] = copy.deepcopy(self.calc_result[file_number][5])
                        self.manuel_adjust[file_number][1] = copy.deepcopy(self.calc_result[file_number][6])
                    # graph plot & dsb-fields
                    self.plot_refresh()
                    # graph: adjusted data plot & self.manuel_adjust compute
                    self.manuel_adjust_compute()
        except Exception as e:
            self.dialog_critical(f'Critical error in reset_all: {str(e)}.')

    def export_ui(self):
        """
            This function asks the user for the export path.
        :return: None
        """
        """
        For the reference purposes self.calc_result & self.manuel_adjust structures are here:
            self.calc_result[file_number][0] : file name
            self.calc_result[file_number][1] : file header
            self.calc_result[file_number][2] : initial data
            self.calc_result[file_number][3] : file separator
            self.calc_result[file_number][4] : accuracy array
            self.calc_result[file_number][5] : calc result
            self.calc_result[file_number][6] : list of all f-factors
            self.manuel_adjust[file_number][0] : calc result
            self.manuel_adjust[file_number][1] : list of all f-factors in form [column][f]
        """
        if not self.first_run:
            try:
                if len(self.files) == 1:
                    save_file_name = self.calc_result[0][0][:self.calc_result[0][0].rfind(".")] + f"{self.ui.le_prefix.text()}.txt"
                    file_name = ""
                    if settings.value("export_dir"):
                        if not os.path.exists(settings.value("export_dir")):
                            settings.setValue("export_dir", self.last_dir(settings.value("export_dir")))
                        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", settings.value("export_dir") + '/' + save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
                    else:
                        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", self.open_dir + '/' + save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
                    if file_name:
                        self.export(file_name)
                else:
                    folder_name = ""
                    if settings.value("export_dir"):
                        if not os.path.exists(settings.value("export_dir")):
                            settings.setValue("export_dir", self.last_dir(settings.value("export_dir")))
                        folder_name = QFileDialog.getExistingDirectory(self, "Select Directory", settings.value("export_dir"))
                    else:
                        folder_name = QFileDialog.getExistingDirectory(self, "Select Directory", self.open_dir)
                    if folder_name:
                        self.export(folder_name)
            except Exception as e:
                self.dialog_critical(f'Critical error in export_ui: {str(e)}.')
        else:
            self.dialog_critical(f'Nothing to export!\n'
                                 f'Please, calculate something before')
            self.ui.toolBox.setCurrentIndex(1)
            self.ui.btn_calc.setFocus()

    def export(self, path):
        """
            This function exports the corrected data (self.manuel_adjust).
        :return: None
        """
        """
        For the reference purposes self.calc_result & self.manuel_adjust structures are here:
            self.calc_result[file_number][0] : file name
            self.calc_result[file_number][1] : file header
            self.calc_result[file_number][2] : initial data
            self.calc_result[file_number][3] : file separator
            self.calc_result[file_number][4] : accuracy array
            self.calc_result[file_number][5] : calc result
            self.calc_result[file_number][6] : list of all f-factors
            self.manuel_adjust[file_number][0] : calc result
            self.manuel_adjust[file_number][1] : list of all f-factors in form [column][f]
        """
        try:
            if len(self.files) == 1:
                if path:
                    settings.setValue("export_dir", path[:path.rfind("/")])
                    separator = self.calc_result[0][3]
                    data_header = ""
                    for item in self.calc_result[0][1]:
                        data_header = data_header + item
                    for line in self.manuel_adjust[0][0]:
                        for i, item in enumerate(line):
                            data_header = data_header + f'{item:.{self.calc_result[0][4][i]}f}' + separator
                        data_header = data_header + "\n"
                    # save
                    with open(path, 'w+') as file_output:
                        file_output.write(data_header)
                    self.dialog_ok("The data was successfully exported!")
            else:
                if path:
                    settings.setValue("export_dir", path)
                    for file_number in range(0, len(self.files)):
                        file_name = self.calc_result[file_number][0][:self.calc_result[file_number][0].rfind(".")] + f"{self.ui.le_prefix.text()}.txt"
                        separator = self.calc_result[file_number][3]
                        data_header = ""
                        for item in self.calc_result[file_number][1]:
                            data_header = data_header + item
                        for line in self.manuel_adjust[file_number][0]:
                            for i, item in enumerate(line):
                                data_header = data_header + f'{item:.{self.calc_result[file_number][4][i]}f}' + separator
                            data_header = data_header + "\n"
                        # save
                        with open(path + '/' + file_name, 'w+') as file_output:
                            file_output.write(data_header)
                    self.dialog_ok("The data was successfully exported!")
        except Exception as e:
            self.dialog_critical(f'Critical error while exporting: {str(e)}.')

    def log_ui(self):
        """
            This function asks the user for the log path.
        :return: None
        """
        if not self.first_run:
            try:
                if len(self.files) == 1:
                    save_file_name = self.calc_result[0][0][:self.calc_result[0][0].rfind(".")] + f"{self.ui.le_log.text()}.txt"
                    file_name = ""
                    if settings.value("log_dir"):
                        if not os.path.exists(settings.value("log_dir")):
                            settings.setValue("log_dir", self.last_dir(settings.value("log_dir")))
                        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", settings.value("log_dir") + '/' + save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
                    else:
                        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", self.open_dir + '/' + save_file_name, "Text Files (*.txt)", options=QFileDialog.Options())
                    if file_name:
                        self.log(file_name)
                else:
                    folder_name = ""
                    if settings.value("log_dir"):
                        if not os.path.exists(settings.value("log_dir")):
                            settings.setValue("log_dir", self.last_dir(settings.value("log_dir")))
                        folder_name = QFileDialog.getExistingDirectory(self, "Select Directory", settings.value("log_dir"))
                    else:
                        folder_name = QFileDialog.getExistingDirectory(self, "Select Directory", self.open_dir)
                    if folder_name:
                        self.log(folder_name)
            except Exception as e:
                self.dialog_critical(f'Critical error in log_ui: {str(e)}.')
        else:
            self.dialog_critical(f'No log to export!\n'
                                 f'Please, calculate something before')
            self.ui.toolBox.setCurrentIndex(1)
            self.ui.btn_calc.setFocus()

    def log(self, paths):
        """
            This function exports the f-coefficients (aka calc log from self.manuel_adjust).
        :return: None
        """
        try:
            separator = '\t'
            accuracy = 4
            if len(self.files) == 1:
                if paths:
                    settings.setValue("log_dir", paths[:paths.rfind("/")])
                    data_header = f'Adjustment factors of the gratings in {self.files[0][self.files[0].rfind("/") + 1:]}\n'
                    data_header = data_header + 'Gratings' + separator + 'Wavelengths_nm' + separator + 'Ref_range' + separator
                    if len(self.manuel_adjust[0][1]) == 1: # not BRDF
                        data_header = data_header + "Factors\n"
                    else:
                        for i, v in enumerate(self.calc_result[0][1][5].split(self.calc_result[0][3])):
                            if "Refl" in v:
                                data_header = data_header + f"f_{v[v.rfind('_') + 1:]}" + separator
                        data_header = data_header[0:-1]
                        data_header = data_header + "\n"
                    for i in range(len(self.manuel_adjust[0][1][0])):
                        data_header = data_header + f'grating_{i + 1}' + separator + f'{self.calc_result[0][2][self.p_intrvals[i][0]][0]}-{self.calc_result[0][2][self.p_intrvals[i][1]][0]}' + separator
                        data_header = data_header + ("fixed" if self.ref_intervals[i] else "not") + separator
                        for j in range(0, len(self.manuel_adjust[0][1])):
                            data_header = data_header + f'{self.manuel_adjust[0][1][j][i]:.{accuracy}f}' + ("" if j == len(self.manuel_adjust[0][1]) - 1 else separator)
                        data_header = data_header + "\n"
                    # save
                    with open(paths, 'w+') as file_output:
                        file_output.write(data_header)
                    self.dialog_ok("The log file was successfully saved!")
            else:
                if paths:
                    settings.setValue("log_dir", paths)
                    for file_number in range(0, len(self.files)):
                        file_name = self.calc_result[file_number][0][:self.calc_result[file_number][0].rfind(".")] + f"{self.ui.le_log.text()}.txt"
                        data_header = f"Adjustment factors of the gratings in {self.files[file_number][self.files[file_number].rfind('/') + 1:]}\n"
                        data_header = data_header + 'Gratings' + separator + 'Wavelengths_nm' + separator
                        if len(self.manuel_adjust[file_number][1]) == 1:  # not BRDF
                            data_header = data_header + "Factors\n"
                        else:
                            for i, v in enumerate(self.calc_result[file_number][1][5].split(self.calc_result[file_number][3])):
                                if "Refl" in v:
                                    data_header = data_header + f"f_{v[v.rfind('_') + 1:]}" + separator
                            data_header = data_header[0:-1]
                            data_header = data_header + "\n"
                        for i in range(len(self.manuel_adjust[file_number][1][0])):
                            data_header = data_header + f'grating_{i + 1}' + separator + f'{self.calc_result[file_number][2][self.p_intrvals[i][0]][0]}-{self.calc_result[file_number][2][self.p_intrvals[i][1]][0]}' + separator
                            data_header = data_header + ("fixed" if self.ref_intervals[i] else "not") + separator
                            for j in range(0, len(self.manuel_adjust[file_number][1])):
                                data_header = data_header + f'{self.manuel_adjust[file_number][1][j][i]:.{accuracy}f}' + ("" if j == len(self.manuel_adjust[file_number][1]) - 1 else separator)
                            data_header = data_header + "\n"
                        # save
                        with open(paths + '/' + file_name, 'w+') as file_output:
                            file_output.write(data_header)
                    self.dialog_ok("The log files were successfully saved!")
        except Exception as e:
            self.dialog_critical(f'Critical error while saving log: {str(e)}.')


class TypeHelp(QtWidgets.QDialog):
    """
        This is help window for file types.
    """
    def __init__(self):
        super(TypeHelp, self).__init__()
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)
        # CLASS GLOBALS
        title_font = "QLabel{font-size: 13pt; font-weight: bold;}"
        # GUI
        # title
        self.setWindowTitle(f'File type help')
        self.resize(940, 550)
        # text: intro
        self.ui.lbl1 = QLabel(self)
        self.ui.lbl1.setObjectName("lbl1")
        self.ui.vl_info_box.addWidget(self.ui.lbl1, 0, Qt.AlignLeft)
        self.ui.lbl1.setText("There are four types of accepted files: 'BRDF', 'full', '3 columns' and 'free format'.")
        # text: title BRDF
        self.ui.lbl2 = QLabel(self)
        self.ui.lbl2.setObjectName("lbl2")
        self.ui.vl_info_box.addWidget(self.ui.lbl2, 1, Qt.AlignLeft)
        self.ui.lbl2.setStyleSheet(f"{title_font}")
        self.ui.lbl2.setText("BRDF")
        # text: text BRDF
        self.ui.lbl3 = QLabel(self)
        self.ui.lbl3.setObjectName("lbl3")
        self.ui.vl_info_box.addWidget(self.ui.lbl3, 2, Qt.AlignLeft)
        self.ui.lbl3.setText("BRDF files are the '_geo' files. They contain several columns of the reflectance at a series of geometries."
                             "\nHere is an example of the BRDF file for NH4-Jarosite:")
        # text: example BRDF
        self.ui.lbl4 = QLabel(self)
        self.ui.lbl4.setObjectName("lbl4")
        self.ui.vl_info_box.addWidget(self.ui.lbl4, 3, Qt.AlignCenter)
        self.ui.lbl4.setPixmap(QPixmap('img/type/BRDF.jpg'))
        # text: title full
        self.ui.lbl5 = QLabel(self)
        self.ui.lbl5.setObjectName("lbl5")
        self.ui.vl_info_box.addWidget(self.ui.lbl5, 4, Qt.AlignLeft)
        self.ui.lbl5.setStyleSheet(f"{title_font}")
        self.ui.lbl5.setText("full")
        # text: text full
        self.ui.lbl6 = QLabel(self)
        self.ui.lbl6.setObjectName("lbl6")
        self.ui.vl_info_box.addWidget(self.ui.lbl6, 5, Qt.AlignLeft)
        self.ui.lbl6.setText("Full files contain all information about a reflectance spectrum (13 columns)."
                             "\nHere is an example of the full file for Phillipsite powder:")
        # text: example full
        self.ui.lbl7 = QLabel(self)
        self.ui.lbl7.setObjectName("lbl7")
        self.ui.vl_info_box.addWidget(self.ui.lbl7, 6, Qt.AlignCenter)
        self.ui.lbl7.setPixmap(QPixmap('img/type/full.jpg'))
        # text: title simple
        self.ui.lbl8 = QLabel(self)
        self.ui.lbl8.setObjectName("lbl8")
        self.ui.vl_info_box.addWidget(self.ui.lbl8, 7, Qt.AlignLeft)
        self.ui.lbl8.setStyleSheet(f"{title_font}")
        self.ui.lbl8.setText("3 columns")
        # text: text simple
        self.ui.lbl9 = QLabel(self)
        self.ui.lbl9.setObjectName("lbl9")
        self.ui.vl_info_box.addWidget(self.ui.lbl9, 8, Qt.AlignLeft)
        self.ui.lbl9.setText("3-column files have three (sometimes two) columns for wavelength, reflectance, and its error (if known)."
                             "\nHere is an example of the 3 column file for mascagnite:")
        # text: example simple
        self.ui.lbl10 = QLabel(self)
        self.ui.lbl10.setObjectName("lbl10")
        self.ui.vl_info_box.addWidget(self.ui.lbl10, 9, Qt.AlignCenter)
        self.ui.lbl10.setPixmap(QPixmap('img/type/simple.jpg'))
        # text: title free
        self.ui.lbl11 = QLabel(self)
        self.ui.lbl11.setObjectName("lbl11")
        self.ui.vl_info_box.addWidget(self.ui.lbl11, 10, Qt.AlignLeft)
        self.ui.lbl11.setStyleSheet(f"{title_font}")
        self.ui.lbl11.setText("free format")
        # text: text free
        self.ui.lbl12 = QLabel(self)
        self.ui.lbl12.setObjectName("lbl12")
        self.ui.vl_info_box.addWidget(self.ui.lbl12, 11, Qt.AlignLeft)
        self.ui.lbl12.setText("Free format files are any other files with a reflectance spectrum.")
        # QDialog show
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.exec_()


class PointHelp(QtWidgets.QDialog):
    """
        This is help window for breakpoints.
    """
    def __init__(self):
        super(PointHelp, self).__init__()
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)
        # CLASS GLOBALS
        title_font = "QLabel{font-size: 13pt; font-weight: bold;}"
        # GUI
        # title
        self.setWindowTitle(f'Points help')
        self.resize(900, 550)
        # text: intro
        self.ui.lbl1 = QLabel(self)
        self.ui.lbl1.setObjectName("lbl1")
        self.ui.vl_info_box.addWidget(self.ui.lbl1, 0, Qt.AlignLeft)
        self.ui.lbl1.setText("The breakpoints are due to changes of gratings, detectors, and sometimes also filters.")
        # text: title break
        self.ui.lbl2 = QLabel(self)
        self.ui.lbl2.setObjectName("lbl2")
        self.ui.vl_info_box.addWidget(self.ui.lbl2, 1, Qt.AlignLeft)
        self.ui.lbl2.setStyleSheet(f"{title_font}")
        self.ui.lbl2.setText("The breakpoint")
        # text: text break
        self.ui.lbl3 = QLabel(self)
        self.ui.lbl3.setObjectName("lbl3")
        self.ui.vl_info_box.addWidget(self.ui.lbl3, 2, Qt.AlignLeft)
        self.ui.lbl3.setText("The breakpoint 'p' is the last wavelength just before the break."
                             "\nFor example, below point p is at 1590 nm:")
        # text: img break
        self.ui.lbl4 = QLabel(self)
        self.ui.lbl4.setObjectName("lbl4")
        self.ui.vl_info_box.addWidget(self.ui.lbl4, 3, Qt.AlignCenter)
        self.ui.lbl4.setPixmap(QPixmap('img/points/break.png'))
        # text: title all points
        self.ui.lbl5 = QLabel(self)
        self.ui.lbl5.setObjectName("lbl5")
        self.ui.vl_info_box.addWidget(self.ui.lbl5, 4, Qt.AlignLeft)
        self.ui.lbl5.setStyleSheet(f"{title_font}")
        self.ui.lbl5.setText("All breakpoints")
        # text: text all points
        self.ui.lbl6 = QLabel(self)
        self.ui.lbl6.setObjectName("lbl6")
        self.ui.vl_info_box.addWidget(self.ui.lbl6, 5, Qt.AlignLeft)
        self.ui.lbl6.setText("You must specify all the points where the breaks occur."
                             "\nUp to seven breakpoints are supported."
                             "\nIn the example below there are two breakpoints:")
        # text: img all points
        self.ui.lbl7 = QLabel(self)
        self.ui.lbl7.setObjectName("lbl7")
        self.ui.vl_info_box.addWidget(self.ui.lbl7, 6, Qt.AlignCenter)
        self.ui.lbl7.setPixmap(QPixmap('img/points/all_points.png'))
        # text: title reference
        self.ui.lbl8 = QLabel(self)
        self.ui.lbl8.setObjectName("lbl8")
        self.ui.vl_info_box.addWidget(self.ui.lbl8, 7, Qt.AlignLeft)
        self.ui.lbl8.setStyleSheet(f"{title_font}")
        self.ui.lbl8.setText("The reference range")
        # text: text reference
        self.ui.lbl9 = QLabel(self)
        self.ui.lbl9.setObjectName("lbl9")
        self.ui.vl_info_box.addWidget(self.ui.lbl9, 8, Qt.AlignLeft)
        self.ui.lbl9.setText("The breakpoints divide the spectrum into ranges."
                             "\nOne of these ranges is considered as a reference, i.e., with a correct photometry."
                             "\nAll other parts will be multiplied by correction factors 'f' in order to connect all them to the reference range with a continuous slope across all"
                             "\nthe breaks."
                             "\nApplied to the above example we get this corrected spectrum (in red):")
        # text: img reference
        self.ui.lbl10 = QLabel(self)
        self.ui.lbl10.setObjectName("lbl10")
        self.ui.vl_info_box.addWidget(self.ui.lbl10, 9, Qt.AlignCenter)
        self.ui.lbl10.setPixmap(QPixmap('img/points/reference.png'))
        # QDialog show
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.exec_()


class GraphHelp(QtWidgets.QDialog):
    """
        This is help window for the graph.
    """
    def __init__(self):
        super(GraphHelp, self).__init__()
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)
        # CLASS GLOBALS
        title_font = "QLabel{font-size: 13pt; font-weight: bold;}"
        # GUI
        # title
        self.setWindowTitle(f'Graph help')
        self.resize(900, 550)
        # text: intro
        self.ui.lbl1 = QLabel(self)
        self.ui.lbl1.setObjectName("lbl1")
        self.ui.vl_info_box.addWidget(self.ui.lbl1, 0, Qt.AlignLeft)
        self.ui.lbl1.setText("Some tips on how to use the graph:")
        # text: title legend
        self.ui.lbl2 = QLabel(self)
        self.ui.lbl2.setObjectName("lbl2")
        self.ui.vl_info_box.addWidget(self.ui.lbl2, 1, Qt.AlignLeft)
        self.ui.lbl2.setStyleSheet(f"{title_font}")
        self.ui.lbl2.setText("Legend")
        # text: text legend
        self.ui.lbl3 = QLabel(self)
        self.ui.lbl3.setObjectName("lbl3")
        self.ui.vl_info_box.addWidget(self.ui.lbl3, 2, Qt.AlignLeft)
        self.ui.lbl3.setText("To move the legend, drag and drop it.")
        # text: img legend
        self.ui.lbl4 = QLabel(self)
        self.ui.lbl4.setObjectName("lbl4")
        self.ui.vl_info_box.addWidget(self.ui.lbl4, 3, Qt.AlignCenter)
        legend_movie = QMovie('img/graph/legend.gif')
        self.ui.lbl4.setMovie(legend_movie)
        legend_movie.start()
        # text: title zoom
        self.ui.lbl5 = QLabel(self)
        self.ui.lbl5.setObjectName("lbl5")
        self.ui.vl_info_box.addWidget(self.ui.lbl5, 4, Qt.AlignLeft)
        self.ui.lbl5.setStyleSheet(f"{title_font}")
        self.ui.lbl5.setText("Zoom")
        # text: text zoom
        self.ui.lbl6 = QLabel(self)
        self.ui.lbl6.setObjectName("lbl6")
        self.ui.vl_info_box.addWidget(self.ui.lbl6, 5, Qt.AlignLeft)
        self.ui.lbl6.setText("To zoom in or out, move your mouse where you want to zoom and scroll on the graph.")
        # text: img zoom
        self.ui.lbl7 = QLabel(self)
        self.ui.lbl7.setObjectName("lbl7")
        self.ui.vl_info_box.addWidget(self.ui.lbl7, 6, Qt.AlignCenter)
        zoom_movie = QMovie('img/graph/zoom.gif')
        self.ui.lbl7.setMovie(zoom_movie)
        zoom_movie.start()
        # text: title zoom_v_h
        self.ui.lbl8 = QLabel(self)
        self.ui.lbl8.setObjectName("lbl8")
        self.ui.vl_info_box.addWidget(self.ui.lbl8, 7, Qt.AlignLeft)
        self.ui.lbl8.setStyleSheet(f"{title_font}")
        self.ui.lbl8.setText("Horizontal and vertical zooms")
        # text: text zoom_v_h
        self.ui.lbl9 = QLabel(self)
        self.ui.lbl9.setObjectName("lbl9")
        self.ui.vl_info_box.addWidget(self.ui.lbl9, 8, Qt.AlignLeft)
        self.ui.lbl9.setText("To scale only horizontally or vertically, scroll on the axes.")
        # text: img zoom_v_h
        self.ui.lbl10 = QLabel(self)
        self.ui.lbl10.setObjectName("lbl10")
        self.ui.vl_info_box.addWidget(self.ui.lbl10, 9, Qt.AlignCenter)
        zoom_v_h_movie = QMovie('img/graph/zoom_v_h.gif')
        self.ui.lbl10.setMovie(zoom_v_h_movie)
        zoom_v_h_movie.start()
        # text: title zoom_reset
        self.ui.lbl11 = QLabel(self)
        self.ui.lbl11.setObjectName("lbl11")
        self.ui.vl_info_box.addWidget(self.ui.lbl11, 10, Qt.AlignLeft)
        self.ui.lbl11.setStyleSheet(f"{title_font}")
        self.ui.lbl11.setText("Zoom reset")
        # text: text zoom_reset
        self.ui.lbl12 = QLabel(self)
        self.ui.lbl12.setObjectName("lbl12")
        self.ui.vl_info_box.addWidget(self.ui.lbl12, 11, Qt.AlignLeft)
        self.ui.lbl12.setText("To reset a zoom, click on 'A' in the lower left corner.")
        # text: img zoom_reset
        self.ui.lbl13 = QLabel(self)
        self.ui.lbl13.setObjectName("lbl13")
        self.ui.vl_info_box.addWidget(self.ui.lbl13, 12, Qt.AlignCenter)
        zoom_reset_movie = QMovie('img/graph/zoom_reset.gif')
        self.ui.lbl13.setMovie(zoom_reset_movie)
        zoom_reset_movie.start()
        # QDialog show
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.exec_()


"""
        This is clickable label class.
"""
class QLabelClickable(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = "Clic"

    def mouseReleaseEvent(self, event):
        QTimer.singleShot(QApplication.instance().doubleClickInterval() / 6, self.performSingleClickAction)

    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    win.show()
    sys.exit(app.exec())
