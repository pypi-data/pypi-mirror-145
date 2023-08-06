from PymoNNto.Exploration.Network_UI.TabBase import *
from PymoNNto.Exploration.StorageManager.StorageManager import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np


#UI_base.Add_element(InteractiveScatter(...), sidebar, stretch)
class InteractiveScatter(pg.GraphicsLayoutWidget):#canvas object

    def __init__(self, *args, **kwargs):#default_x default_y
        super().__init__(*args, **kwargs)

        self.default_x = 'score'
        self.default_y = 'score'

        self.storage_manager_groups = []

        self.initialize_plot()


    def scatter_clicked(self, plot, points):
        print('clicked')
        if len(points) > 0:
            self.clicked_generation = points[-1]._data[0]
            self.clicked_score = points[-1]._data[1]

            self.clicked_id = points[-1]._data[3]
            self.clicked_smg = points[-1]._data[4]
            print(self.clicked_id)

            self.scatter2.setData(x=[self.clicked_generation], y=[self.clicked_score])  # set second scatter to new selection
            self.scatter2.data[0][3] = self.clicked_id

    def scatter_double_clicked(self, plot, points):#scatter2

        print('double clicked', self.clicked_id)

        #evo_id = tab.data[-3, tab.clicked_id][0]
        # print(evo_id)

        sm = self.clicked_smg['id==' + str(int(self.clicked_id))][0]

        txt = open(sm.absolute_path + sm.config_file_name, 'r').read()

        layout = QVBoxLayout()
        pte = QPlainTextEdit()
        pte.setPlainText(txt)
        pte.setReadOnly(True)
        layout.addWidget(pte)

        dlg = QDialog()
        #dlg.setWindowTitle(sm.absolute_path + sm.config_file_name)
        dlg.setLayout(layout)
        dlg.resize(1200, 800)
        dlg.exec()

    def change_axis_param(self, axis_name, param):
        dx = self.default_x
        dy = self.default_y
        try:
            if axis_name == 'bottom':
                self.default_x = param

            if axis_name == 'left':
                self.default_y = param

            self.refresh_data()
            self.plot.getAxis(axis_name).setLabel(text=param)
        except:
            self.default_x = dx
            self.default_y = dy



    def get_all_params(self):
        result_dict = {}
        for smg in self.storage_manager_groups:
            for param in smg.get_all_params():
                result_dict[param] = True
        return result_dict.keys()


    def axis_dialog(self, axis_name):
        dlg = QDialog()
        dlg.setWindowTitle('Select ' + axis_name + ' axis parameter')
        layout = QVBoxLayout()

        listwidget = QListWidget()

        listwidget.addItems(self.get_all_params())

        layout.addWidget(listwidget)

        def btn_clicked():
            self.change_axis_param(axis_name, listwidget.currentItem().text())
            dlg.close()

        btn = QPushButton('set new axis parameter')
        btn.clicked.connect(btn_clicked)

        layout.addWidget(btn)
        dlg.setLayout(layout)
        dlg.resize(300, 300)
        dlg.exec()


    def initialize_plot(self):
        self.setBackground((255, 255, 255))

        #if tooltip_message is not None:
        #    self.ci.setToolTip(tooltip_message)

        self.clicked_generation = -1
        self.clicked_score = -1
        self.clicked_id = -1
        self.clicked_smg = ''

        self.plot = self.addPlot(row=0, col=0)#, axisItems=axisItems
        self.plot.addLegend()

        #tab.item = pg.FillBetweenItem(curve1=tab.curves[1], curve2=tab.curves[2], brush=(255, 0, 0, 100))
        #tab.plot.addItem(tab.item)


        self.scatter2 = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(0, 0, 255, 255))
        self.plot.addItem(self.scatter2)
        self.scatter2.sigClicked.connect(self.scatter_double_clicked)


        self.plot.getAxis('bottom').setLabel(text=self.default_x)
        self.plot.getAxis('left').setLabel(text=self.default_y)

        def bottom_axis_clicked(ev):
            self.axis_dialog('bottom')

        self.plot.getAxis('bottom').mouseClickEvent = bottom_axis_clicked

        def left_axis_clicked(ev):
            self.axis_dialog('left')

        self.plot.getAxis('left').mouseClickEvent = left_axis_clicked

    def find_same_path_smg(self, smg):
        found = None
        for attached_smg in self.storage_manager_groups:
            if smg.absolute_path == attached_smg.absolute_path:
                found = attached_smg

        return found

    def remove_StorageManagerGroup(self, smg):
        found = self.find_same_path_smg(smg)
        if found is not None:
            self.storage_manager_groups.remove(found)
            self.plot.removeItem(found.scatter)
            self.update_indices()
            self.scatter2.clear()

    def get_smg(self, tag):
        for smg in self.storage_manager_groups:
            if smg.Tag == tag:
                return smg

    def add_StorageManagerGroup(self, smg):

        found = self.find_same_path_smg(smg)

        if found is None:
            smg.scatter = pg.ScatterPlotItem(size=10, name=smg.Tag)#, brush=pg.mkBrush(np.random.randint(0,255), np.random.randint(0,255), 255, 120)
            smg.scatter.sigClicked.connect(self.scatter_clicked)
            self.plot.legend.addItem(smg.scatter, smg.Tag)
            self.plot.addItem(smg.scatter)
        else:
            smg.scatter = found.scatter
            smg.color = found.color
            self.storage_manager_groups.remove(found)

        if not hasattr(smg, 'color'):
            smg.color = (np.random.randint(0, 255), np.random.randint(0, 255), 255)

            #print('ck', smg.color[0], smg.color[1], smg.color[2], 120)
            #color = pg.mkBrush(smg.color[0], smg.color[1], smg.color[2], 120)
            #color = pg.mkBrush(np.random.randint(0, 255), np.random.randint(0, 255), 255, 120)
            #smg.scatter.setData(brush=color)

        self.storage_manager_groups.append(smg)

        self.update_indices()

        self.plot.removeItem(self.scatter2)#bring to front
        self.plot.addItem(self.scatter2)
        self.scatter2.clear()


    def update_indices(self):
        return
        #for i, smg in enumerate(self.storage_manager_groups):
        #    smg.add_virtual_multi_parameter('index', i)

    def refresh_data(self):
        for smg in self.storage_manager_groups:

            data = smg.get_multi_param_list(['id', self.default_x, self.default_y], remove_None=True)

            smg.scatter.setData(x=data[1], y=data[2], brush=pg.mkBrush(smg.color[0], smg.color[1], smg.color[2], 120))  #

            for i, d in enumerate(smg.scatter.data):  # set ids to each point (d[3] very ugly coding...) (each point is a set, not an object)
                d[3] = data[0][i]
                d[4] = smg

        self.scatter2.clear()



