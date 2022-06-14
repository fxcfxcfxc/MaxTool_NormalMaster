import os
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QPushButton,QRadioButton,QSlider,QLabel
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from pymxs import runtime as rt

'''
3dmax2022
继承QDialog 版本，窗口属于3dmax同级面板


'''

#继承Qdialog类，代表对话框类
class TestDialog(QDialog):
    #TestDialog类的构造函数，传入参数，参数为类类型
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        # 继承父类的构造方法
        # 经典类的写法： 父类名称.__init__(self, 参数1，参数2，...)
        # 新式类的写法：super(子类，self).__init__(参数1，参数2，....)
        # 当testDialog被实例化之后，调用顺序  自己的__init__ ——> 父类__init__

        # 经典写法，继承父类的构造函数,也就是拥有父类的属性和方法
        QDialog.__init__(self, parent)

        # 创建一个quiloader对象， 主要负责加载UI外部文件
        loader = QUiLoader()

        #加载UI文件
        ui_file_path = os.path.join(  os.path.dirname(os.path.realpath(__file__)), 'ui/normal.ui')
        ui_file = QFile(ui_file_path)

        #设置文件只读
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)
        self.setWindowTitle("技术中心_法线工具")

        self.create_weight()
        self.create_layout()

        self.resize(400, 450)


    def create_weight(self):
        self.horizontalSlider = self.ui.findChild(QSlider, 'horizontalSlider')

        self.but_display_normal = self.ui.findChild(QPushButton, 'but_display_normal')
        self.but_close_normal = self.ui.findChild(QPushButton, 'but_close_normal')
        self.but_x_add = self.ui.findChild(QPushButton, 'but_x_add')
        self.but_x_sub = self.ui.findChild(QPushButton, 'but_x_sub')
        self.but_y_add = self.ui.findChild(QPushButton, 'but_y_add')
        self.but_y_sub = self.ui.findChild(QPushButton, 'but_y_sub')
        self.but_z_add = self.ui.findChild(QPushButton, 'but_z_add')
        self.but_z_sub = self.ui.findChild(QPushButton, 'but_z_sub')


        self.rad_one = self.ui.findChild(QRadioButton,'rad_one')
        self.rad_five = self.ui.findChild(QRadioButton,'rad_five')
        self.rad_ten = self.ui.findChild(QRadioButton,'rad_ten')

        self.but_normal_strore = self.ui.findChild(QPushButton, 'but_normal_strore')
        self.but_normal_select = self.ui.findChild(QPushButton, 'but_normal_select')
        self.but_normal_strore_2 = self.ui.findChild(QPushButton, 'but_normal_strore_2')
        self.but_normal_select_2 = self.ui.findChild(QPushButton, 'but_normal_select_2')
        self.but_normal_strore_3 = self.ui.findChild(QPushButton, 'but_normal_strore_3')
        self.but_normal_select_3 = self.ui.findChild(QPushButton, 'but_normal_select_3')

        self.but_normal_pick = self.ui.findChild(QPushButton, 'pushButtonPick')
        self.but_normal_stroe = self.ui.findChild(QPushButton, 'pushButtonStore')
        self.but_TransformNorml = self.ui.findChild(QPushButton, 'TransformNorml')

        self.but_label_5 = self.ui.findChild(QLabel, 'label_5')
        self.but_label_6 = self.ui.findChild(QLabel, 'label_6')


    def create_layout(self):
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


        self.but_normal_pick.clicked.connect(self.getNormalTransformTarget)
        self.but_normal_stroe.clicked.connect(self.getMyNormalObject)
        self.but_TransformNorml.clicked.connect(self.setTransformNormal)

        self.horizontalSlider.valueChanged.connect(self.normal_length)



if __name__ == '__main__':

    try:
        tool_window.close()
        tool_window.deleteLater()

    except:
        pass
    tool_window = TestDialog()
    tool_window.show()

