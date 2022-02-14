import os
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QDockWidget
from PySide2.QtWidgets import QPushButton,QRadioButton,QSlider
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import qtmax
from pymxs import runtime as rt
'''
3dmax2022
继承QDockWidget 版本，窗口属于3dmax工具面板


'''

#继承Qdialog类，代表对话框类
class TestDialog(QDockWidget):
    #TestDialog类的构造函数，传入参数，参数为类类型
    def __init__(self, parent=None):
        # 继承父类的构造方法
        # 经典类的写法： 父类名称.__init__(self, 参数1，参数2，...)
        # 新式类的写法：super(子类，self).__init__(参数1，参数2，....)
        # 当testDialog被实例化之后，调用顺序  自己的__init__ ——> 父类__init__
        super(TestDialog, self).__init__(parent)#经典写法，继承父类的构造函数,也就是拥有父类的属性和方法
        loader = QUiLoader()#QuiLoder类 主要负责加载UI外部文件
        ui_file_path = os.path.join(  os.path.dirname(os.path.realpath(__file__)), 'ui/normal.ui')
        ui_file = QFile(ui_file_path)#打开文件
        ui_file.open(QFile.ReadOnly)#文件只读
        self.ui = loader.load(ui_file, self)#导入ui内部的信息
        ui_file.close()
        self.setWindowFlags(QtCore.Qt.Tool)#设置窗口属性，枚举
        self.setWindowTitle("技术中心_法线工具v1.0")

        self.creat_widget()
        self.creat_layout()
        self.resize(500, 550)

    def creat_widget(self):

        self.horizontalSlider = self.ui.findChild(QSlider, 'horizontalSlider')

        self.but_display_normal = self.ui.findChild(QPushButton, 'but_display_normal')
        self.but_close_normal = self.ui.findChild(QPushButton, 'but_close_normal')
        self.but_x_add = self.ui.findChild(QPushButton, 'but_x_add')
        self.but_x_sub = self.ui.findChild(QPushButton, 'but_x_sub')
        self.but_y_add = self.ui.findChild(QPushButton, 'but_y_add')
        self.but_y_sub = self.ui.findChild(QPushButton, 'but_y_sub')
        self.but_z_add = self.ui.findChild(QPushButton, 'but_z_add')
        self.but_z_sub = self.ui.findChild(QPushButton, 'but_z_sub')

        self.rad_one = self.ui.findChild(QRadioButton, 'rad_one')
        self.rad_five = self.ui.findChild(QRadioButton, 'rad_five')
        self.rad_ten = self.ui.findChild(QRadioButton, 'rad_ten')

        self.but_normal_strore = self.ui.findChild(QPushButton, 'but_normal_strore')
        self.but_normal_select = self.ui.findChild(QPushButton, 'but_normal_select')
        self.but_normal_strore_2 = self.ui.findChild(QPushButton, 'but_normal_strore_2')
        self.but_normal_select_2 = self.ui.findChild(QPushButton, 'but_normal_select_2')
        self.but_normal_strore_3 = self.ui.findChild(QPushButton, 'but_normal_strore_3')
        self.but_normal_select_3 = self.ui.findChild(QPushButton, 'but_normal_select_3')

        self.start_value()

    def creat_layout(self):

        self.but_display_normal.clicked.connect(self.display_normal)
        self.rad_one.toggled.connect(self.offset_value_rad)
        self.rad_five.toggled.connect(self.offset_value_rad)
        self.rad_ten.toggled.connect(self.offset_value_rad)

        self.but_close_normal.clicked.connect(self.close_normal)
        self.but_x_add.clicked.connect(self.offert_x_add)
        self.but_x_sub.clicked.connect(self.offert_x_sub)
        self.but_y_add.clicked.connect(self.offert_y_add)
        self.but_y_sub.clicked.connect(self.offert_y_sub)
        self.but_z_add.clicked.connect(self.offert_z_add)
        self.but_z_sub.clicked.connect(self.offert_z_sub)

        self.but_normal_strore.clicked.connect(self.store_1)
        self.but_normal_select.clicked.connect(self.select_1)

        self.but_normal_strore_2.clicked.connect(self.store_2)
        self.but_normal_select_2.clicked.connect(self.select_2)

        self.but_normal_strore_3.clicked.connect(self.store_3)
        self.but_normal_select_3.clicked.connect(self.select_3)

        self.horizontalSlider.valueChanged.connect(self.normal_length)

        self.resize(500, 550)

    def start_value(self):
        if (self.rad_one.isChecked()):
            self.offset_value_x_add = rt.quat(0.0871557 / 10, 0, 0, 0.999848)
            self.offset_value_x_sub = rt.quat(-0.0871557 / 10, 0, 0, 0.999848)

            self.offset_value_y_add = rt.quat(0, 0, 0.0871557 / 10, 0.999848)
            self.offset_value_y_sub = rt.quat(0, 0, -0.0871557 / 10, 0.999848)

            self.offset_value_z_add = rt.quat(0, 0.0871557 / 10, 0, 0.999848)
            self.offset_value_z_sub = rt.quat(0, -0.0871557 / 10, 0, 0.999848)

    def normal_length(self):
        self.normal.displayLength = self.horizontalSlider.value()

    def display_normal(self):
        self.normal = rt.Edit_Normals()
        a = rt.selection

        for x in a :
            rt.addModifier(x,self.normal)

        self.horizontalSlider.setValue(self.normal.displayLength)
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
        tool_window.close()
        tool_window.deleteLater()

    except:
        pass
    main_window2 = qtmax.GetQMaxMainWindow()
    tool_window = TestDialog(parent=main_window2)
    tool_window.setFloating(True)
    tool_window.show()

