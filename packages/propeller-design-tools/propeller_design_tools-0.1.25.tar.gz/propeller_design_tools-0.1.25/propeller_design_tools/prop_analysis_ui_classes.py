from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
try:
    from PyQt5 import QtWidgets, QtCore
    from propeller_design_tools.helper_ui_subclasses import PDT_Label, PDT_GroupBox, PDT_ComboBox, PDT_PushButton
    from propeller_design_tools.helper_ui_classes import SingleAxCanvas, AxesComboBoxWidget, PropellerCreationPanelCanvas
except:
    pass


class PropellerSweepWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        super(PropellerSweepWidget, self).__init__()
        main_lay = QtWidgets.QHBoxLayout()
        self.setLayout(main_lay)

        left_lay = QtWidgets.QVBoxLayout()
        center_lay = QtWidgets.QVBoxLayout()
        # right_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(left_lay)
        main_lay.addLayout(center_lay)
        # main_lay.addLayout(right_lay)

        # left layout
        left_lay.addStretch()
        exist_data_grp = PDT_GroupBox('Existing Data (plot controls)')
        exist_data_grp.setMinimumSize(400, 250)
        exist_data_grp.setLayout(QtWidgets.QVBoxLayout())
        left_lay.addWidget(exist_data_grp)
        left_lay.addStretch()
        add_data_grp = PDT_GroupBox('Add Data Points By Range')
        add_data_grp.setMinimumSize(400, 250)
        add_data_grp.setLayout(QtWidgets.QVBoxLayout())
        left_lay.addWidget(add_data_grp)
        left_lay.addStretch()

        # center layout
        select_prop_cb = PDT_ComboBox(width=200)
        select_prop_cb.setEnabled(False)
        select_prop_cb.currentTextChanged.connect(self.select_prop_cb_changed)
        center_lay.addStretch()
        center_top_lay = QtWidgets.QHBoxLayout()
        center_top_lay.addStretch()
        center_top_lay.addWidget(PDT_Label('Select Propeller:', font_size=14, bold=True))
        center_top_lay.addWidget(select_prop_cb)
        center_top_lay.addStretch()
        center_lay.addLayout(center_top_lay)
        self.wvel_3d_canvas = wvel_3d_canvas = SingleAxCanvas(projection='3d', height=6, width=6)
        center_lay.addWidget(wvel_3d_canvas)

        # right layout

        self.metric_plot_widget = PropellerCreationMetricPlotWidget(main_win=main_win)
        main_lay.addWidget(self.metric_plot_widget)

        # metric_lay = QtWidgets.QHBoxLayout()
        # x_param_cb = PDT_ComboBox(width=150)
        # y_param_cb = PDT_ComboBox(width=150)
        # metric_lay.addStretch()
        # metric_lay.addWidget(PDT_Label('Plot Metric:', font_size=14, bold=True))
        # metric_lay.addStretch()
        # metric_lay.addWidget(y_param_cb)
        # metric_lay.addWidget(PDT_Label('vs'))
        # metric_lay.addWidget(x_param_cb)
        # metric_lay.addStretch()
        # right_lay.addLayout(metric_lay)
        # self.metric_canvas = metric_canvas = SingleAxCanvas()
        # right_lay.addWidget(metric_canvas)

    def select_prop_cb_changed(self):
        pass


class PropellerCreationMetricPlotWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        self.main_win = main_win
        super(PropellerCreationMetricPlotWidget, self).__init__()
        main_lay = QtWidgets.QVBoxLayout()
        self.setLayout(main_lay)
        self.creation_panel_canvas = None

        axes_cb_lay = QtWidgets.QHBoxLayout()
        main_lay.addLayout(axes_cb_lay)
        self.plot_opts = ['r/R', 'c/R', 'beta(deg)', 'CL', 'CD', 'RE', 'Mach', 'effi', 'effp', 'GAM', 'Ttot', 'Ptot', 'VA/V',
                          'VT/V']
        x_txts = ['x-axis'] + self.plot_opts
        y_txts = ['y-axis'] + self.plot_opts
        self.axes_cb_widg = AxesComboBoxWidget(x_txts=x_txts, y_txts=y_txts, init_xtxt='r/R',
                                               init_ytxt='GAM')
        self.xax_cb = self.axes_cb_widg.xax_cb
        self.yax_cb = self.axes_cb_widg.yax_cb
        self.xax_cb.currentTextChanged.connect(self.update_data)
        self.yax_cb.currentTextChanged.connect(self.update_data)

        axes_cb_lay.addStretch()
        axes_cb_lay.addWidget(PDT_Label('Plot Metric:', font_size=14, bold=True))
        axes_cb_lay.addWidget(self.axes_cb_widg)
        axes_cb_lay.addStretch()

        self.plot_canvas = SingleAxCanvas(self, width=4.5, height=5)
        self.axes = self.plot_canvas.axes
        main_lay.addWidget(self.plot_canvas)
        toolbar = NavigationToolbar(self.plot_canvas, self)
        main_lay.addWidget(toolbar)
        main_lay.setAlignment(toolbar, QtCore.Qt.AlignHCenter)
        main_lay.addStretch()

    def update_data(self):
        self.plot_canvas.clear_axes()

        yax_txt = self.yax_cb.currentText()
        xax_txt = self.xax_cb.currentText()
        if yax_txt == 'y-axis' or xax_txt == 'x-axis':
            return
        prop = self.main_win.prop_widg.prop
        if prop is None:
            return

        self.axes.set_xlabel(xax_txt)
        self.axes.set_ylabel(yax_txt)
        self.axes.grid(True)
        xdata = prop.xrotor_op_dict[xax_txt]
        if yax_txt in prop.blade_data:
            self.axes.plot(xdata, prop.blade_data[yax_txt], marker='*', markersize=4)
        else:
            if yax_txt in prop.xrotor_op_dict:
                self.axes.plot(xdata, prop.xrotor_op_dict[yax_txt], marker='o', markersize=3)

        self.plot_canvas.draw()
