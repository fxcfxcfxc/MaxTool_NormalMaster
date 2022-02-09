import os
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QPushButton,QRadioButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from pymxs import runtime as rt



class TestDialog(QDialog):
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        QDialog.__init__(self, parent)
        loader = QUiLoader()
        ui_file_path = os.path.join(  os.path.dirname(os.path.realpath(__file__)), 'ui/normal.ui')
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)
        self.setWindowTitle("技术中心_法线工具1.0")

        # -------------------creat weight----------------
        but_display_normal = self.ui.findChild(QPushButton, 'but_display_normal')
        but_close_normal = self.ui.findChild(QPushButton, 'but_close_normal')
        but_x_add = self.ui.findChild(QPushButton, 'but_x_add')
        but_x_sub = self.ui.findChild(QPushButton, 'but_x_sub')
        but_y_add = self.ui.findChild(QPushButton, 'but_y_add')
        but_y_sub = self.ui.findChild(QPushButton, 'but_y_sub')
        but_z_add = self.ui.findChild(QPushButton, 'but_z_add')
        but_z_sub = self.ui.findChild(QPushButton, 'but_z_sub')


        self.rad_one = self.ui.findChild(QRadioButton,'rad_one')
        self.rad_five = self.ui.findChild(QRadioButton,'rad_five')
        self.rad_ten = self.ui.findChild(QRadioButton,'rad_ten')

        but_normal_strore = self.ui.findChild(QPushButton, 'but_normal_strore')
        but_normal_select = self.ui.findChild(QPushButton, 'but_normal_select')
        but_normal_strore_2 = self.ui.findChild(QPushButton, 'but_normal_strore_2')
        but_normal_select_2 = self.ui.findChild(QPushButton, 'but_normal_select_2')
        but_normal_strore_3 = self.ui.findChild(QPushButton, 'but_normal_strore_3')
        but_normal_select_3 = self.ui.findChild(QPushButton, 'but_normal_select_3')


        #---------------------------connect funcution------------------------
        but_display_normal.clicked.connect(self.display_normal)

        if (self.rad_one.isChecked()):
            self.offset_value_x_add = rt.quat(0.0871557 / 10, 0, 0, 0.999848)
            self.offset_value_x_sub = rt.quat(-0.0871557 / 10, 0, 0, 0.999848)

            self.offset_value_y_add = rt.quat(0, 0, 0.0871557 / 10, 0.999848)
            self.offset_value_y_sub = rt.quat(0, 0, -0.0871557 / 10, 0.999848)

            self.offset_value_z_add = rt.quat(0, 0.0871557 / 10, 0, 0.999848)
            self.offset_value_z_sub = rt.quat(0, -0.0871557 / 10, 0, 0.999848)

        self.rad_one.toggled.connect(self.offset_value_rad)
        self.rad_five.toggled.connect(self.offset_value_rad)
        self.rad_ten.toggled.connect(self.offset_value_rad)

        but_close_normal.clicked.connect(self.close_normal)
        but_x_add.clicked.connect(self.offert_x_add)
        but_x_sub.clicked.connect(self.offert_x_sub)
        but_y_add.clicked.connect(self.offert_y_add)
        but_y_sub.clicked.connect(self.offert_y_sub)
        but_z_add.clicked.connect(self.offert_z_add)
        but_z_sub.clicked.connect(self.offert_z_sub)

        but_normal_strore.clicked.connect(self.store_1)
        but_normal_select.clicked.connect(self.select_1)

        but_normal_strore_2.clicked.connect(self.store_2)
        but_normal_select_2.clicked.connect(self.select_2)

        but_normal_strore_3.clicked.connect(self.store_3)
        but_normal_select_3.clicked.connect(self.select_3)

        self.resize(400, 350)


    def display_normal(self):
        self.normal = rt.Edit_Normals()
        a = rt.selection

        for x in a :
            rt.addModifier(x,self.normal)
        rt.redrawViews()


    def close_normal(self):
        rt.convertToPoly(rt.selection)
        return
        rt.redrawViews()

    def offert_x_add(self):
        self.normal.Rotate(self.offset_value_x_add)

    def offert_x_sub(self):
        self.normal.Rotate(self.offset_value_x_sub)

    def offert_y_add(self):
        self.normal.Rotate(self.offset_value_y_add)

    def offert_y_sub(self):
        self.normal.Rotate(self.offset_value_z_sub)

    def offert_z_add(self):
        self.normal.Rotate(self.offset_value_z_add)

    def offert_z_sub(self):
        self.normal.Rotate(self.offset_value_z_sub)

    def offset_value_rad(self):
        if(self.rad_one.isChecked()):
            self.offset_value_x_add = rt.quat(0.0871557 / 10, 0, 0, 0.999848)
            self.offset_value_x_sub = rt.quat(-0.0871557 / 10, 0, 0, 0.999848)

            self.offset_value_y_add = rt.quat(0, 0, 0.0871557 / 10, 0.999848)
            self.offset_value_y_sub = rt.quat(0, 0, -0.0871557 / 10, 0.999848)

            self.offset_value_z_add = rt.quat(0, 0.0871557 / 10, 0, 0.999848)
            self.offset_value_z_sub = rt.quat(0, -0.0871557 / 10, 0, 0.999848)

        if(self.rad_five.isChecked()):
            self.offset_value_x_add = rt.quat(0.0871557/2, 0, 0, 0.999048)
            self.offset_value_x_sub = rt.quat(-0.0871557/2, 0, 0, 0.999048)

            self.offset_value_y_add = rt.quat(0, 0, 0.0871557/2, 0.999048)
            self.offset_value_y_sub = rt.quat(0, 0, -0.0871557/2, 0.999048)

            self.offset_value_z_add = rt.quat(0, 0.0871557/2, 0, 0.999048)
            self.offset_value_z_sub = rt.quat(0, -0.0871557/2, 0, 0.999048)


        if(self.rad_ten.isChecked()):

            self.offset_value_x_add = rt.quat(0.0871557, 0, 0, 0.996195)
            self.offset_value_x_sub = rt.quat(-0.0871557, 0, 0, 0.996195)

            self.offset_value_y_add = rt.quat(0, 0, 0.0871557, 0.996195)
            self.offset_value_y_sub = rt.quat(0, 0, -0.0871557, 0.996195)

            self.offset_value_z_add = rt.quat(0, 0.0871557, 0, 0.996195)
            self.offset_value_z_sub = rt.quat(0, -0.0871557, 0, 0.996195)

    def store_1(self):
        self.bitArray_sel = self.normal.GetSelection()

    def  select_1(self):

        self.normal_selection_1 = self.normal.SetSelection(self.bitArray_sel)

    def store_2(self):

        self.bitArray_sel_2 = self.normal.GetSelection()

    def  select_2(self):

        self.normal_selection_2 = self.normal.SetSelection(self.bitArray_sel_2)

    def store_3(self):
        self.bitArray_sel_3 = self.normal.GetSelection()

    def  select_3(self):

        self.normal_selection_3 = self.normal.SetSelection(self.bitArray_sel_3)






if __name__ == '__main__':

    try:
        dlg.close()
        dlg.deleteLater()

    except:
        pass
    dlg = TestDialog()
    dlg.show()
