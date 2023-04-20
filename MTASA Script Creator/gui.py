from PyQt5 import uic, QtWidgets
import util



class MyMainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)

        #Buttons functions
        self.pushButton.clicked.connect(self.button_select_txd)
        self.pushButton_2.clicked.connect(self.button_select_dff)
        self.pushButton_3.clicked.connect(self.button_create)
        self.pushButton_4.clicked.connect(self.select_save_loc)
        self.radioButton.toggled.connect(self.change_veh)
        self.radioButton_2.toggled.connect(self.change_ped)
        self.radioButton_3.toggled.connect(self.change_object)
        self.radioButton_4.toggled.connect(self.change_weapon)
        self.checkBox.toggled.connect(self.set_acl_group_mode)
        self.checkBox_2.toggled.connect(self.set_data_mode)  

    #Buttons functions
    def select_save_loc(self):
        util.select_save_location()
    def button_select_txd(self):
        file_name = util.select_file(True)
        self.editWidget = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.editWidget.setText(file_name)

    def button_select_dff(self):
        file_name = util.select_file(False)
        self.editWidget = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
        self.editWidget.setText(file_name)
    #created function
    def button_create(self):
        #txd file
        self.editWidget = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        txd_file = self.editWidget.text()


        #txd file
        self.editWidget2 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
        dff_file = self.editWidget2.text()

            
        #ACL Group
        self.editWidget4 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
        acl_group = self.editWidget4.text()
        if util.acl_group_mode and acl_group == "":
            return
        
        #Data Name
        self.editWidget5 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_5')
        data_name = self.editWidget5.text()
        if util.data_mode and data_name == "":
            return

        #Model ID
        self.editWidget3 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_4')
        id = self.editWidget3.text()
        if id =="": 
            return


        # create type if not selected blocked creating
        if util.create_type:
            util.create(util.create_type,id,txd_file,dff_file,acl_group,util.acl_group_mode,data_name,util.data_mode)


    #change create type
    def change_veh(self):
        util.create_type = 1
    def change_ped(self):
        util.create_type = 2
    def change_object(self):
        util.create_type = 3
    def change_weapon(self):
        util.create_type = 4

    #Acl Group Mode
    def set_acl_group_mode(self):
        util.acl_group_mode = not util.acl_group_mode

    #Data Mode
    def set_data_mode(self):
        util.data_mode = not util.data_mode
 





if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()