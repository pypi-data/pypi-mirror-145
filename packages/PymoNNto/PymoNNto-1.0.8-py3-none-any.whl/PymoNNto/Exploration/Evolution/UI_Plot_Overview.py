from PymoNNto.Exploration.Evolution.common_UI import *
from PymoNNto.Exploration.Evolution.PlotQTObjects import *

class UI_Plot_Overview(UI_Base):

    def update_order(self):
        for i in range(self.listwidget.count()):
            item = self.listwidget.item(i)
            #print(i, item.text())
            smg=self.interactive_scatter.get_smg(item.text())
            if smg is not None:
                smg.add_virtual_multi_parameter('index', i)


    def __init__(self):
        super().__init__(None, label='Plot Overview', create_sidebar=True)

        self.listwidget = QListWidget()

        self.folder = 'Plot_Project_Clones'

        self.Next_Tab('main')

        self.interactive_scatter = self.Add_element(InteractiveScatter())

        dirs = []
        for dir in os.listdir(get_epc_folder(self.folder)):
            if os.path.isdir(get_epc_folder(self.folder) + '/' + dir):
                dirs.append(dir)
                #self.add_tab(dir)

        self.listwidget.addItems(dirs)

        self.listwidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove);

        def drop_event(ev):
            print(ev)
            super(QListWidget, self.listwidget).dropEvent(ev)
            self.update_order()
            self.interactive_scatter.refresh_data()

        self.update_order()

        self.listwidget.dropEvent=drop_event


        for i in range(self.listwidget.count()):
            item = self.listwidget.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

        self.Add_element(self.listwidget, sidebar=True)

        def on_item_clicked(item):
            for i in range(self.listwidget.count()):
                item=self.listwidget.item(i)
                smg = StorageManagerGroup(item.text(), data_folder=get_data_folder() + '/' + self.folder + '/' + item.text() + '/Data')

                if item.checkState() == QtCore.Qt.Checked:
                    if self.interactive_scatter.get_smg(item.text()) is None:
                        self.interactive_scatter.add_StorageManagerGroup(smg)
                else:
                    self.interactive_scatter.remove_StorageManagerGroup(smg)

            self.update_order()
            self.interactive_scatter.refresh_data()

        self.listwidget.itemClicked.connect(on_item_clicked)

        def on_item_doubleclicked(item):
            item = self.listwidget.itemFromIndex(item)
            smg = self.interactive_scatter.get_smg(item.text())

            if smg is not None:
                color = QColorDialog.getColor()
                print(color.red(), color.green(), color.blue())

                smg.color=(color.red(), color.green(), color.blue())
                self.interactive_scatter.add_StorageManagerGroup(smg)
                self.interactive_scatter.refresh_data()

        self.listwidget.doubleClicked.connect(on_item_doubleclicked)



if __name__ == '__main__':
    UI_Plot_Overview().show()
