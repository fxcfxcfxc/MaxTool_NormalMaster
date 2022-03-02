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
法线工具
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
        #-----
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
        self.btn_recover_normal = self.ui.findChild(QPushButton, 'btn_recover_normal')

        self.but_normal_strore_2 = self.ui.findChild(QPushButton, 'but_normal_strore_2')
        self.but_normal_select_2 = self.ui.findChild(QPushButton, 'but_normal_select_2')
        self.btn_recover_normal2 = self.ui.findChild(QPushButton, 'btn_recover_normal2')

        self.but_normal_strore_3 = self.ui.findChild(QPushButton, 'but_normal_strore_3')
        self.but_normal_select_3 = self.ui.findChild(QPushButton, 'but_normal_select_3')
        self.btn_recover_normal3 = self.ui.findChild(QPushButton, 'btn_recover_normal3')

        self.start_value()

    def creat_layout(self):

        self.but_display_normal.clicked.connect(self.add_normal)
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
        self.btn_recover_normal.clicked.connect(self.recover_1)

        self.but_normal_strore_2.clicked.connect(self.store_2)
        self.but_normal_select_2.clicked.connect(self.select_2)
        self.btn_recover_normal2.clicked.connect(self.recover_2)

        self.but_normal_strore_3.clicked.connect(self.store_3)
        self.but_normal_select_3.clicked.connect(self.select_3)
        self.btn_recover_normal3.clicked.connect(self.recover_3)

        self.horizontalSlider.valueChanged.connect(self.normal_length)

        self.resize(500, 550)

    def start_value(self):
        #设置初始化偏移值，防止报错
        if (self.rad_one.isChecked()):
            # value  = 0.1
            self.offset_value_x_add = rt.Point3(0.05, 0, 0)
            self.offset_value_x_sub = rt.Point3(-0.05, 0, 0)

            self.offset_value_y_add = rt.Point3(0, 0.05, 0)
            self.offset_value_y_sub = rt.Point3(0, -0.05, 0)

            self.offset_value_z_add = rt.Point3(0, 0, 0.05)
            self.offset_value_z_sub = rt.Point3(0, 0, -0.05)

    def normal_length(self):
        #设置修改器法线长度值等于滑块值
        self.normal.displayLength = self.horizontalSlider.value()

    def add_normal(self):
        self.normal = rt.Edit_Normals()
        a = rt.selection

        for x in a :
            rt.addModifier(x,self.normal)

        #将滑块ui的值设置成法线修改器的默认值
        self.horizontalSlider.setValue(self.normal.displayLength)
        rt.redrawViews()

    def close_normal(self):
        rt.convertToPoly(rt.selection)
        return
        rt.redrawViews()

    def offert_x_add(self):
        self.normal.Move(self.offset_value_x_add)

    def offert_x_sub(self):
        self.normal.Move(self.offset_value_x_sub)

    def offert_y_add(self):
        self.normal.Move(self.offset_value_y_add)

    def offert_y_sub(self):
        self.normal.Move(self.offset_value_z_sub)

    def offert_z_add(self):
        self.normal.Move(self.offset_value_z_add)

    def offert_z_sub(self):
        self.normal.Move(self.offset_value_z_sub)

    def offset_value_rad(self):
        if(self.rad_one.isChecked()):
            # value  = 0.1
            self.offset_value_x_add = rt.Point3(0.05,0,0)
            self.offset_value_x_sub = rt.Point3(-0.05,0,0)

            self.offset_value_y_add = rt.Point3(0,0.05,0)
            self.offset_value_y_sub = rt.Point3(0,-0.05,0)

            self.offset_value_z_add = rt.Point3(0,0,0.05)
            self.offset_value_z_sub = rt.Point3(0,0,-0.05)

        if(self.rad_five.isChecked()):
            # value  = 0.05
            self.offset_value_x_add = rt.Point3(0.1,0,0)
            self.offset_value_x_sub = rt.Point3(-0.1,0,0)

            self.offset_value_y_add = rt.Point3(0,0.1,0)
            self.offset_value_y_sub = rt.Point3(0,-0.1,0)

            self.offset_value_z_add = rt.Point3(0,0,0.1)
            self.offset_value_z_sub = rt.Point3(0,0,-0.1)


        if(self.rad_ten.isChecked()):
            # value  = 1
            self.offset_value_x_add = rt.Point3(1,0,0)
            self.offset_value_x_sub = rt.Point3(-1,0,0)

            self.offset_value_y_add = rt.Point3(0,1,0)
            self.offset_value_y_sub = rt.Point3(0,-1,0)

            self.offset_value_z_add = rt.Point3(0,0,1)
            self.offset_value_z_sub = rt.Point3(0,0,-1)

    def get_normal_array(self,bitArray):

        # 暴露函数 bitarray to array
        rt.execute("fn b2a b = (return b as Array)")
        # 类型转换bitarray -》 array
        array_select_normal = rt.b2a(bitArray)
        return array_select_normal;

    def store_normal(self,array):
        # 法线向量数组存储
        array_normal_dir = [];
        for x in array:
            normalTest = self.normal.GetNormal(x)  # 传入index，得到index法线对应的方向向量
            array_normal_dir.append(normalTest)  #

        return array_normal_dir;

    def store_1(self):
        self.bitArray_sel_1 = self.normal.GetSelection()#当前选择的法线索引存入 bitarray
        self.normal_array_1 = self.get_normal_array(self.bitArray_sel_1)
        self.normal_dir_1 = self.store_normal(self.normal_array_1)

        '''
        
       
        #暴露函数 bitarray to array
        rt.execute("fn b2a b = (return b as Array)")
        #类型转换bitarray -》 array
        self.array_select_normal = rt.b2a(self.bitArray_sel_1)

        #法线向量数组存储
        self.array_normal_dir = []
        for x in self.array_select_normal:
            self.normalTest = self.normal.GetNormal(x)  # 传入index，得到index法线对应的方向向量
            self.array_normal_dir.append(self.normalTest) #
        '''

    def select_1(self):

        self.normal_selection_1 = self.normal.SetSelection(self.bitArray_sel_1)

    def recover_1(self):
        x = 0
        for a in self.normal_array_1:
            self.normal.SetNormal(a, self.normal_dir_1[x])
            if (x <= len(self.normal_array_1)):
                x = x + 1
            rt.redrawViews()

    def store_2(self):

        self.bitArray_sel_2 = self.normal.GetSelection()  # 当前选择的法线索引存入 bitarray
        self.normal_array_2 = self.get_normal_array(self.bitArray_sel_2)
        self.normal_dir_2 = self.store_normal(self.normal_array_2)

    def select_2(self):

        self.normal_selection_2 = self.normal.SetSelection(self.bitArray_sel_2)

    def recover_2(self):
        x = 0
        for a in self.normal_array_2:
            self.normal.SetNormal(a, self.normal_dir_2[x])
            if (x <= len(self.normal_array_2)):
                x = x + 1
            rt.redrawViews()

    def store_3(self):
        self.bitArray_sel_3 = self.normal.GetSelection()  # 当前选择的法线索引存入 bitarray
        self.normal_array_3 = self.get_normal_array(self.bitArray_sel_3)
        self.normal_dir_3 = self.store_normal(self.normal_array_3)

    def select_3(self):

        self.normal_selection_3 = self.normal.SetSelection(self.bitArray_sel_3)

    def recover_3(self):
        x = 0
        for a in self.normal_array_3:
            self.normal.SetNormal(a, self.normal_dir_3[x])
            if (x <= len(self.normal_array_3)):
                x = x + 1
            rt.redrawViews()



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

