import numpy as np
import os
from propeller_design_tools.airfoil import Airfoil
from propeller_design_tools.settings import _get_cursor_fpath, _get_gunshot_fpaths
from propeller_design_tools.funcs import get_all_airfoil_files, get_all_propeller_dirs
try:
    from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
    from propeller_design_tools.helper_ui_classes import Capturing, DatabaseSelectionWidget, SingleAxCanvas, \
        AxesComboBoxWidget, PdtGuiPrinter
    from propeller_design_tools.foil_ui_classes import ExistingFoilDataWidget, FoilAnalysisWidget, AddFoilDataPointWidget
    from propeller_design_tools.prop_creation_ui_classes import PropellerCreationWidget
    from propeller_design_tools.prop_analysis_ui_classes import PropellerSweepWidget
    from propeller_design_tools.opt_ui_classes import OptimizationWidget
    from propeller_design_tools.helper_ui_subclasses import PDT_TextEdit, PDT_GroupBox, PDT_Label, PDT_PushButton, \
        PDT_ComboBox, PDT_TabWidget
except:
    pass


class InterfaceMainWindow(QtWidgets.QMainWindow):
    def __init__(self, foil: Airfoil = None):
        super(InterfaceMainWindow, self).__init__()
        self.setWindowTitle('PDT Control Dashboard')
        self.setMinimumSize(1600, 900)
        self.foil = foil

        cursor_fpath = _get_cursor_fpath()
        cursor = QtGui.QCursor(QtGui.QPixmap(cursor_fpath))
        self.setCursor(cursor)

        # central widget
        center_widg = QtWidgets.QWidget()
        center_lay = QtWidgets.QVBoxLayout()
        center_widg.setLayout(center_lay)
        self.setCentralWidget(center_widg)

        # the main groups
        top_lay = QtWidgets.QHBoxLayout()
        sett_grp = PDT_GroupBox('Settings'.upper(), italic=True, font_size=16)
        sett_grp.setFixedHeight(250)
        # sett_grp.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        top_lay.addWidget(sett_grp)
        console_grp = PDT_GroupBox('Console Output'.upper(), italic=True, font_size=16)
        console_grp.setFixedHeight(250)
        # console_grp.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        top_lay.addWidget(console_grp)
        center_lay.addLayout(top_lay)

        # tab widget
        tab_widg = PDT_TabWidget(font_size=16, italic=True)
        center_lay.addWidget(tab_widg)
        self.af_widg = FoilAnalysisWidget(main_win=self)
        tab_widg.addTab(self.af_widg, 'Airfoil Analysis'.upper())
        self.prop_widg = PropellerCreationWidget(main_win=self)
        tab_widg.addTab(self.prop_widg, 'Propeller Creation'.upper())
        self.prop_sweep_widg = PropellerSweepWidget(main_win=self)
        tab_widg.addTab(self.prop_sweep_widg, 'Propeller Analysis'.upper())
        self.opt_widg = OptimizationWidget()
        tab_widg.addTab(self.opt_widg, 'Optimization'.upper())


        # settings group
        sett_lay = QtWidgets.QFormLayout()
        sett_grp.setLayout(sett_lay)
        self.af_db_select_widg = DatabaseSelectionWidget(main_win=self, db_type='airfoil')
        sett_lay.addRow(PDT_Label('Airfoil Database:', font_size=14), self.af_db_select_widg)
        self.prop_db_select_widg = DatabaseSelectionWidget(main_win=self, db_type='propeller')
        sett_lay.addRow(PDT_Label('Propeller Database:', font_size=14), self.prop_db_select_widg)

        # console group
        console_lay = QtWidgets.QVBoxLayout()
        console_grp.setLayout(console_lay)
        self.console_te = PDT_TextEdit(height=150)
        console_lay.addWidget(self.console_te)
        btn_bar_lay = QtWidgets.QHBoxLayout()
        clear_console_btn = PDT_PushButton('Clear', font_size=11, width=100)
        clear_console_btn.clicked.connect(self.clear_console_btn_clicked)
        btn_bar_lay.addWidget(clear_console_btn)

        self.prog_bar = QtWidgets.QProgressBar()
        self.prog_bar.setMinimumSize(500, 30)
        self.prog_bar.setValue(0)
        btn_bar_lay.addStretch()
        btn_bar_lay.addWidget(self.prog_bar)
        btn_bar_lay.addStretch()
        console_lay.addLayout(btn_bar_lay)

        # call these last because they rely on self.console_te existing
        self.af_db_select_widg.set_current_db()
        self.prop_db_select_widg.set_current_db()
        self.printer = PdtGuiPrinter(console_te=self.console_te)

        # connecting signals
        self.af_db_select_widg.currentDatabaseChanged.connect(self.repop_select_foil_cb)
        self.af_widg.add_foil_data_widg.add_btn.clicked.connect(self.add_foil_data_btn_clicked)
        self.af_widg.add_foil_data_widg.reset_btn.clicked.connect(self.reset_foil_ranges_btn_clicked)
        self.af_widg.select_foil_cb.currentTextChanged.connect(self.select_foil_cb_changed)
        self.af_widg.af_yax_cb.currentTextChanged.connect(self.af_metric_cb_changed)
        self.af_widg.af_xax_cb.currentTextChanged.connect(self.af_metric_cb_changed)

        self.prop_db_select_widg.currentDatabaseChanged.connect(self.repop_select_prop_cb)


    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        fpaths = _get_gunshot_fpaths()
        num = int(np.random.rand() * 3.4)

        url = QtCore.QUrl.fromLocalFile(fpaths[num])
        content = QtMultimedia.QMediaContent(url)
        player = QtMultimedia.QMediaPlayer(self)
        player.setMedia(content)
        player.setVolume(20)
        player.play()

    def repop_select_prop_cb(self):
        self.print('Changing Propeller Database...')
        self.prop_widg.plot3d_widg.populate_select_prop_cb()

    def repop_select_foil_cb(self):
        self.print('Changing Airfoil Database...')
        self.af_widg.select_foil_cb.clear()
        self.af_widg.select_foil_cb.addItems(['None'] + get_all_airfoil_files())

    def af_metric_cb_changed(self):
        self.af_widg.foil_metric_canvas.axes.clear()
        self.af_widg.foil_metric_canvas.draw()
        y_txt, x_txt = self.af_widg.af_yax_cb.currentText(), self.af_widg.af_xax_cb.currentText()
        if y_txt == 'y-axis' or x_txt == 'x-axis':
            return

        if self.foil is not None:
            if len(self.foil.polar_data) == 0:
                self.print('No data for current foil')
                return

            with Capturing() as output:
                self.foil.plot_polar_data(x_param=x_txt, y_param=y_txt, fig=self.af_widg.foil_metric_canvas.figure)
            self.console_te.append('\n'.join(output) if len(output) > 0 else '')

            self.af_widg.foil_metric_canvas.draw()

    def clear_console_btn_clicked(self):
        self.prog_bar.setValue(0)
        self.console_te.clear()

    def select_foil_cb_changed(self, foil_txt):
        self.print('Changing Current Foil...')
        self.af_widg.foil_xy_canvas.axes.clear()
        if not foil_txt == 'None':
            try:

                with Capturing() as output:
                    self.foil = Airfoil(name=foil_txt, exact_namematch=True)
                self.console_te.append('\n'.join(output))

            except Exception as e:
                with Capturing() as output:
                    self.print(e)
                self.console_te.append('\n'.join(output))
                self.foil = None
        else:
            self.foil = None

        if self.foil is not None:
            self.foil.plot_geometry(fig=self.af_widg.foil_xy_canvas.figure)
            self.af_metric_cb_changed()  # updates the metric plot
        else:
            self.af_widg.foil_xy_canvas.axes.clear()
            self.af_widg.foil_metric_canvas.axes.clear()
        self.af_widg.foil_xy_canvas.draw()
        self.af_widg.foil_metric_canvas.draw()
        self.af_widg.exist_data_widg.update_airfoil(af=self.foil)

    def add_foil_data_btn_clicked(self):

        if self.foil is None:
            self.print('Must select a foil first!')
            return

        self.prog_bar.setValue(0)

        re_min, re_max, re_step = self.af_widg.add_foil_data_widg.get_re_range()
        mach_min, mach_max, mach_step = self.af_widg.add_foil_data_widg.get_mach_range()
        ncrit_min, ncrit_max, ncrit_step = self.af_widg.add_foil_data_widg.get_ncrit_range()

        res = np.arange(re_min, re_max, re_step)
        machs = np.arange(mach_min, mach_max, mach_step)
        ncrits = np.arange(ncrit_min, ncrit_max, ncrit_step)

        self.thread = QtCore.QThread()
        self.foil_worker = AddFoilDataWorker(foil=self.foil, res=res, machs=machs, ncrits=ncrits)
        self.foil_worker.moveToThread(self.thread)
        self.thread.started.connect(self.foil_worker.run)
        self.foil_worker.finished.connect(self.thread.quit)
        self.foil_worker.finished.connect(self.foil_worker.deleteLater)
        self.foil_worker.finished.connect(self.on_foil_worker_finish)
        self.thread.finished.connect(self.thread.deleteLater)
        self.foil_worker.progress.connect(self.update_foil_worker_progress)

        self.af_widg.add_foil_data_widg.setEnabled(False)
        self.af_widg.exist_data_widg.setEnabled(False)
        self.af_widg.select_foil_cb.setEnabled(False)
        self.thread.start()

    def on_foil_worker_finish(self):
        self.af_widg.add_foil_data_widg.setEnabled(True)
        self.af_widg.exist_data_widg.setEnabled(True)
        self.af_widg.select_foil_cb.setEnabled(True)
        self.prog_bar.setValue(0)

    def update_foil_worker_progress(self, prog: int, output: list):
        self.print(output)
        self.prog_bar.setValue(prog)
        with Capturing() as output:
            self.foil.load_polar_data()
        self.print(output)
        self.select_foil_cb_changed(foil_txt=self.af_widg.select_foil_cb.currentText())  # updates everything

    def reset_foil_ranges_btn_clicked(self):
        self.af_widg.add_foil_data_widg.reset_ranges()

    def print(self, s: str, fontfamily: str = None):
        self.printer.print(s, fontfamily=fontfamily)


class AddFoilDataWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int, list)

    def __init__(self, foil: 'Airfoil', res: list, machs: list, ncrits: list):
        super(AddFoilDataWorker, self).__init__()
        self.foil = foil
        self.res = res
        self.machs = machs
        self.ncrits = ncrits

    def run(self):
        total_polars = len(self.res) * len(self.machs) * len(self.ncrits)

        counter = 0
        for re in self.res:
            for mach in self.machs:
                for ncrit in self.ncrits:
                    counter += 1
                    with Capturing() as output:
                        self.foil.calculate_xfoil_polars(re=[re], mach=[mach], ncrit=[ncrit])
                    self.progress.emit(int(counter / total_polars * 100), output)

        self.finished.emit()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = InterfaceMainWindow()
    w.show()
    app.exec_()
