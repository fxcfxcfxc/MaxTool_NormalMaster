import os
import sys
sys.path.append(r'E:\CodeProject\MaxTool_NormalMaster')
sys.path.append(r'C:\DamMaxTools')
from PySide2.QtWidgets import QVBoxLayout,QDialog
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QDockWidget,QProgressDialog
from PySide2.QtWidgets import QPushButton,QRadioButton,QSlider,QLabel, QProgressBar, QVBoxLayout
from PySide2.QtCore import QFile,QThread, Signal
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import qtmax
from pymxs import runtime as rt
import time


'''
3dmax2022  
继承QDockWidget 版本，窗口属于3dmax工具面板
python版本3.7

'''


class Worker(QThread):
    """
    Worker thread
    """
    progress = Signal()
    aborted = False
    def __init__(self,normal_array_1, normalmodif, normal_dir_1):
        """
        Construct the worker
        """
        QThread.__init__(self)

        self.normal_array_1 = normal_array_1
        self.normal = normalmodif
        self.normal_dir_1 = normal_dir_1

        self.progress.emit()

        x = 0
        # 遍历之前的索引数组
        for a in self.normal_array_1:

            # a是从1 开始，x是从0开始 ，代表方向值的索引
            # 索引a的法线 对应的向量值 a+1 的索引
            self.normal.SetNormal(a, self.normal_dir_1[x])
            if (x <= len(self.normal_array_1)):
                x += 1
            rt.redrawViews()
            time.sleep(0.1)
        rt.redrawViews()


    def run(self):
        print("ss")
        # self.progress.emit()
        # print("aaaaaa")
        # x = 0
        # # 遍历之前的索引数组
        # for a in self.normal_array_1:
        #
        #     # a是从1 开始，x是从0开始 ，代表方向值的索引
        #     # 索引a的法线 对应的向量值 a+1 的索引
        #     self.normal.SetNormal(a, self.normal_dir_1[x])
        #     if (x <= len(self.normal_array_1)):
        #         x += 1
        #     rt.redrawViews()
        #     time.sleep(0.1)
        # rt.redrawViews()


        # """
        # Increment a counter an notify progress.
        # Abort if aborted is True
        # # """
        # for i in range(0, 100):
        #     self.progress.emit(i)
        #
        #     #延迟0.5秒执行
        #     time.sleep(0.5)
        #     if self.aborted:
        #         return
        #
        # self.progress.emit(100)

    def abort(self):
        """
        Make the worker terminate before it's done.
        """
        self.aborted = True

class PyMaxDialog(QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    """
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Progress')

        main_layout = QVBoxLayout()
        label = QLabel("Progress so far")
        main_layout.addWidget(label)

        # progress bar
        self.progb = QProgressBar()
        self.progb.minimum = 0
        self.progb.maximum = 0
        main_layout.addWidget(self.progb)

        # abort button
        btn = QPushButton("abort")
        main_layout.addWidget(btn)

        self.setLayout(main_layout)
        self.resize(350, 100)

        # # # start the worker
        # self.worker = Worker()
        # self.worker.progress.connect(progb.setValue)
        # self.worker.start()
        #
        # # connect abort button
        # btn.clicked.connect(self.worker.abort)

#继承Qdialog类 这是一个窗口面板类型
class TestDialog(QDockWidget):
    #构造函数，实例化时自动执行，用于初始化
    def __init__(self, parent=None):
        # 继承父类的构造方法
        # 经典类的写法： 父类名称.__init__(self, 参数1，参数2，...)
        # 新式类的写法：super(子类，self).__init__(参数1，参数2，....)

        # 当testDialog被实例化之后，调用顺序  自己的__init__ ——> 父类__init__
        # 经典写法，继承父类的构造函数
        super(TestDialog, self).__init__(parent)


        # QuiLoder类 主要负责加载UI外部文件
        loader = QUiLoader()

        #得到ui文件路径
        ui_file_path = os.path.join(  os.path.dirname(os.path.realpath(__file__)), 'ui/normal.ui')

        #读取ui
        ui_file = QFile(ui_file_path)#打开文件
        ui_file.open(QFile.ReadOnly)#文件只读


        # 导入ui内部的信息
        self.ui = loader.load(ui_file, self)
        ui_file.close()


        #设置窗口属性
        self.setWindowFlags(QtCore.Qt.Tool)#设置窗口属性，枚举
        self.setWindowTitle("技术中心_法线工具套件")

        #创建组件
        self.creat_widget()


        #链接方法
        self.creat_connections()

        #设置窗口大小
        self.resize(500, 550)
        self.setValue()

    #创建ui组件
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

        self.but_normal_pick = self.ui.findChild(QPushButton, 'pushButtonPick')
        self.but_normal_stroe = self.ui.findChild(QPushButton, 'pushButtonStore')
        self.but_TransformNorml = self.ui.findChild(QPushButton, 'TransformNorml')

        self.but_label_5 = self.ui.findChild(QLabel, 'label_5')
        self.but_label_6 = self.ui.findChild(QLabel, 'label_6')

    #创建connect
    def creat_connections(self):


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



        self.but_normal_pick.clicked.connect(self.getNormalTransformTarget)
        self.but_normal_stroe.clicked.connect(self.getMyNormalObject)
        self.but_TransformNorml.clicked.connect(self.setTransformNormal)

        self.horizontalSlider.valueChanged.connect(self.normal_length)

        self.resize(500, 550)

    def setValue(self):
        self.offsetvalue = 0.1
        if (self.rad_five.isChecked()):
            # value  = 0.05
            self.offset_value_x_add = rt.Point3(self.offsetvalue, 0, 0)
            self.offset_value_x_sub = rt.Point3(-self.offsetvalue, 0, 0)

            self.offset_value_y_add = rt.Point3(0, self.offsetvalue, 0)
            self.offset_value_y_sub = rt.Point3(0, -self.offsetvalue, 0)

            self.offset_value_z_add = rt.Point3(0, 0, self.offsetvalue)
            self.offset_value_z_sub = rt.Point3(0, 0, -self.offsetvalue)

    #-----------------------------------传递法线功能
    def getNormalTransformTarget(self):

        #判断是否只选择了一个物体
        if(1 == len(rt.selection)):
            # 获取a物体
            self.a_target = rt.selection[0]

            #获取a物体的顶点数量
            self.a_Count = rt.getPolygonCount(self.a_target)[1]

            #将a物体名称设置到label上
            self.but_label_5.setText("目标对象:"+self.a_target.name)

            #转换为edit_mesh
            rt.convertToMesh(self.a_target)

        else:
            #如果没有选择物体就窗口警告
            rt.messageBox("没有选择物体或选择了个多个物体")

    def getMyNormalObject(self):

        if (1 == len(rt.selection) ):
            #获取b物体
            self.b_target = rt.selection[0]

            # 获取b物体的顶点数量
            self.b_Count = rt.getPolygonCount(self.b_target)[1]

            # 将b物体名称设置到label上
            self.but_label_6.setText("最终对象:"+self.b_target.name)

            rt.convertToMesh(self.b_target)
        else:
            rt.messageBox("没有选择物体或选择了个多个物体")

    def setTransformNormal(self):

        #设置使用世界坐标
        rt.setRefCoordSys(rt.Name('world'))
        por = self.setPrograss()
        #得到a物体的第一个点位置
        a_num1 = rt.getVert(self.a_target, 1)

        # 遍历b物体的每一个顶点
        for b_index in range(self.b_Count):
                #根据顶点序号得到b物体 当前点位置（顶点序号从1开始时）
                b_pos = rt.getVert(self.b_target,b_index+1)

                #算出当前点 到 a物体 序号为1的顶点 距离
                min_distance = rt.distance(b_pos,a_num1)

                #用来存储对应 最近的点 的序号
                finalindex=1;
                #遍历a物体的每一个顶点，从第二个顶点开始,和B当前循环点算距离，和第一个顶点距离作比较，小于就更新最小值
                for a_index in range(self.a_Count):
                    QtCore.QCoreApplication.processEvents()
                    if a_index+2 <= self.a_Count :
                        a_pos = rt.getVert(self.a_target,a_index+2)
                        comp_distance = rt.distance(b_pos,a_pos)
                        if(comp_distance < min_distance):
                            min_distance = comp_distance
                            finalpos = a_pos
                            finalindex = a_index+2

                #从算出来的顶点索引获取到 对应点的法线方向
                normalDir = rt.getNormal(self.a_target,finalindex)

                #将算出来的对应的 A物体的顶点的法线 传入B物体的顶点法线
                rt.setNormal(self.b_target, b_index+1 ,normalDir)

        rt.convertToPoly(self.a_target)
        rt.convertToPoly(self.b_target)
        # rt.messageBox("传递结束")

        por.close()
        #更新视图
        #rt.redrawViews()

    #----------------------------固定值偏移

    def normal_length(self):
        #将滑块UI值 传入法线修改器值
        self.normal.displayLength = self.horizontalSlider.value()

    def add_normal(self):
        #生成一个法线修改器对象
        self.normal = rt.Edit_Normals()

        #获取当前选择的物体 返回数组
        a = rt.selection

        #将物体a加上之前的修改器
        for x in a :
            rt.addModifier(x,self.normal)


        #更新UI组件的显示值为修改器默认值
        self.horizontalSlider.setValue(self.normal.displayLength)


        rt.redrawViews()

    def close_normal(self):

        #转化为convertTopoly
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
        self.normal.Move(self.offset_value_y_sub)

    def offert_z_add(self):
        self.normal.Move(self.offset_value_z_add)

    def offert_z_sub(self):
        self.normal.Move(self.offset_value_z_sub)

    def offset_value_rad(self):
        if(self.rad_one.isChecked()):
            # value  = 0.05
            self.offsetvalue = 0.05
            self.offset_value_x_add = rt.Point3(self.offsetvalue,0,0)
            self.offset_value_x_sub = rt.Point3(-self.offsetvalue,0,0)

            self.offset_value_y_add = rt.Point3(0,self.offsetvalue,0)
            self.offset_value_y_sub = rt.Point3(0,-self.offsetvalue,0)

            self.offset_value_z_add = rt.Point3(0,0,self.offsetvalue)
            self.offset_value_z_sub = rt.Point3(0,0,-self.offsetvalue)

        if(self.rad_five.isChecked()):
            # value  = 0.1
            self.offsetvalue = 0.1
            self.offset_value_x_add = rt.Point3(self.offsetvalue,0,0)
            self.offset_value_x_sub = rt.Point3(-self.offsetvalue,0,0)

            self.offset_value_y_add = rt.Point3(0,self.offsetvalue,0)
            self.offset_value_y_sub = rt.Point3(0,-self.offsetvalue,0)

            self.offset_value_z_add = rt.Point3(0,0,self.offsetvalue)
            self.offset_value_z_sub = rt.Point3(0,0,-self.offsetvalue)


        if(self.rad_ten.isChecked()):
            # value  = 1
            self.offsetvalue = 1
            self.offset_value_x_add = rt.Point3(self.offsetvalue,0,0)
            self.offset_value_x_sub = rt.Point3(-self.offsetvalue,0,0)

            self.offset_value_y_add = rt.Point3(0,self.offsetvalue,0)
            self.offset_value_y_sub = rt.Point3(0,-self.offsetvalue,0)

            self.offset_value_z_add = rt.Point3(0,0,self.offsetvalue)
            self.offset_value_z_sub = rt.Point3(0,0,-self.offsetvalue)


    # 自定义函数 b2a ，将bitarray类型 转换为 python array类型
    def bitArray_To_Array(self, bitArray):
        rt.execute("fn b2a b = (return b as Array)")

        # 类型转换bitarray -》 array
        array_select_normal = rt.b2a(bitArray)
        return array_select_normal


    def store_normal(self,array):
        # 存储法 线方向
        array_normal_dir = []
        for x in array:
            normalTest = self.normal.GetNormal(x)  # 传入index，得到index法线对应的方向向量
            array_normal_dir.append(normalTest)  #

        return array_normal_dir



    #---------------------暂存法线功能
    #法线数据暂存
    def store_1(self):

        #获取当前选择的法线索引
        self.bitArray_sel_1 = self.normal.GetSelection()

        #数据类型转换 bitarray -》array
        self.normal_array_1 = self.bitArray_To_Array(self.bitArray_sel_1)

        #根据索引得到方向值，存入数组，从0开始
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

    #选择法线
    def select_1(self):

        #选择之前存入的法线
        self.normal_selection_1 = self.normal.SetSelection(self.bitArray_sel_1)

    '''
    def runtest(self):
        dialog = PyMaxDialog()
        dialog.show()

        self.worker = Worker( self.normal_array_1, self.normal , self.normal_dir_1)
        # self.worker.progress.connect(dialog.progb.setValue)
        self.worker.start()
        
    '''

    #创建一个进度条
    def setPrograss(self):
        num =5
        pro = QProgressDialog("waiting to proces", "Cancel", 0, num, self)
        pro.setWindowTitle("ProGress")
        pro.setRange(0, 0)
        pro.setWindowModality(QtCore.Qt.WindowModal)
        pro.resize(650, 220)
        pro.show()

        return pro

    #法线数据回到初始
    def recover_1(self):
        pro = self.setPrograss()
        x = 0
        #遍历之前的索引数组
        for a in self.normal_array_1:
            #a是从1 开始，x是从0开始 ，代表方向值的索引
            #索引a的法线 对应的向量值 a+1 的索引
            self.normal.SetNormal(a, self.normal_dir_1[x])
            if (x <= len(self.normal_array_1)):
                x += 1
            rt.redrawViews()
            pro.setRange(0, 0)
            #刷新ui
            QtCore.QCoreApplication.processEvents()

        rt.redrawViews()
        pro.close()

    def store_2(self):

        self.bitArray_sel_2 = self.normal.GetSelection()  # 当前选择的法线索引存入 bitarray
        self.normal_array_2 = self.bitArray_To_Array(self.bitArray_sel_2)
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
        self.bitArray_sel_3 = self.normal.GetSelection()
        self.normal_array_3 = self.bitArray_To_Array(self.bitArray_sel_3)
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



    #异常处理，防止实例化多个窗口
    try:
        tool_window.close()
        tool_window.deleteLater()

    except:
        pass

    #获取maxmainwindow 类型
    main_window2 = qtmax.GetQMaxMainWindow()

    #实例化窗口，传入类型
    tool_window = TestDialog(parent=main_window2)

    #设置窗口浮动
    tool_window.setFloating(True)
    tool_window.show()

