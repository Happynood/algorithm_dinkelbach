import sys
from PyQt5 import QtWidgets, QtGui
from main_page import Ui_Dialog
from lex_n_dinkelbach import alg_dinkelbach
from fractions import Fraction
import numpy as np

class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btnClicked)
 
    def btnClicked(self):
        # Если не использовать, то часть текста исчезнет.
        task = self.ui.textEdit.toPlainText()
        task_arr = [int(x) for x in task.split()]
        P,D,A,b,symb = [],[],[],[],'<='
        for x in range(self.ui.spinBox_2.value()+1):
            P.append(Fraction(task_arr[x]))
        for x in range(self.ui.spinBox_2.value()+1,self.ui.spinBox.value()*2+2):
            D.append(Fraction(task_arr[x]))
        count = 1
        arr_ogr = []
        for i in range(self.ui.spinBox_2.value()*2+2,len(task_arr)):
            if(count%(self.ui.spinBox_2.value()+1)!=0):
                arr_ogr.append(Fraction(task_arr[i]))
            if count%(self.ui.spinBox_2.value()+1)==0:
                A.append(arr_ogr)
                arr_ogr = []
                b.append(Fraction(task_arr[i]))
            count+=1
        solution = alg_dinkelbach(np.array(P),np.array(D),np.array(A),np.array(b),self.ui.comboBox.currentText(),self.ui.checkBox.isChecked(),self.ui.checkBox_2.isChecked())
        for i in range(len(solution)):
            a = 'X'+str(i)+' = '+str(solution[i])+' '
            self.ui.textBrowser.append(a)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
    
sys.exit(app.exec())