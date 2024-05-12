import sys
import time
import copy
from PyQt5 import QtWidgets, QtGui
from main_page import Ui_Dialog
from lex_n_dinkelbach import rev,alg_dinkelbach
from lex_n_dinkelbach import alg_dinkelbach1
from fractions import Fraction
import numpy as np

pashalko = ''
counter = 5
class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super(mywindow, self).__init__()
        self.path = None
        self.save = False
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btnClicked)
        self.path = self.ui.pushButton2.clicked.connect(lambda: self.open())

    
    def open(self):
        self.path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите путь", "C:\\Users\\{os.getlogin()}")
        self.save = True
    
    def btnClicked(self):
        global pashalko
        global counter
        self.ui.textBrowser.clear()
        # Если не использовать, то часть текста исчезнет.
        task = self.ui.textEdit.toPlainText()
        if task == pashalko:
            counter -= 1
        else:
            pashalko = task
            counter = 5
        if -10<= counter <= 0:
            self.ui.textBrowser.append("Уважаемый пользователь!\nХватит вводить одинаковые\nданные! Ответ не изменится!")
            return
        elif -25<= counter < -10:
            self.ui.textBrowser.append("Пожалуйста, прекратите!\nЭто совсем не смешно!")
            return
        elif -45<= counter < -25:
            self.ui.textBrowser.append("Последнее предупреждение...")
            return
        elif counter == -46:
            self.ui.textBrowser.append("СТОЙТЕ!!! НЕ НАЖИМАЙТЕ\nКНОПКУ!!!!")
            return
        elif counter<-46:
            while True:
                time.sleep(10000)
            return
        for i in range(len(task)):
            if task[i].isdigit()==False and task[i]!=' 'and task[i]!='\n'and task[i]!='-':
                self.ui.textBrowser.append("Некорректные данные!\nСимвольная ошибка")
                return
            if i<len(task)-1 and task[i].isdigit()  and task[i+1]=='-':
                self.ui.textBrowser.append("Некорректные данные!\nСимвольная ошибка")
                return
            if (i<len(task)-1 and not task[i+1].isdigit()  and task[i]=='-' or
                    i==len(task)-1 and task[i]=='-'):
                self.ui.textBrowser.append("Некорректные данные!\nСимвольная ошибка")
                return
        task_arr = [int(x) for x in task.split()]
        if len(task_arr) != (self.ui.spinBox_2.value() + 1) * (self.ui.spinBox.value() + 2):
            self.ui.textBrowser.append("Некорректные данные!\nОшибка количества\nвводных данных!")
            return
        P,D,A,b,symb = [],[],[],[],self.ui.comboBox.currentText()
        A_ras = []
        A_c = []
        b_c = []
        for x in range(self.ui.spinBox_2.value()+1):
            P.append(Fraction(task_arr[x]))
        for x in range(self.ui.spinBox_2.value()+1,self.ui.spinBox_2.value()*2+2):
            D.append(Fraction(task_arr[x]))
        count = 1
        arr_ogr = []
        arr_ogr_c=np.array([])

        for i in range(self.ui.spinBox_2.value()*2+2,len(task_arr)):
            if(count%(self.ui.spinBox_2.value()+1)!=0):
                arr_ogr.append(Fraction(task_arr[i]))
                arr_ogr_c = np.append(arr_ogr_c,task_arr[i])
            if count%(self.ui.spinBox_2.value()+1)==0:
                A.append(arr_ogr)
                A_c.append(arr_ogr_c)
                arr_ogr = []
                arr_ogr_c = []
                b.append(Fraction(task_arr[i]))
                b_c.append(task_arr[i])
            count+=1
        if len(A) ==0:
            self.ui.textBrowser.append("Некорректные данные!\nОтсутствие ограничений!")
            return
        if len(P) ==1:
            self.ui.textBrowser.append("Некорректные данные!\nОтсутствие переменных!")
            return
        
        A_ras = copy.deepcopy(A_c)
        for i in range(len(A_ras)):
            A_ras[i] = np.append(A_ras[i],b_c[i])
        #Для совместности СЛАУ необходимо и достаточно, чтобы ранг её матрицы A был равен рангу её расширенной матрицы A.
        if np.linalg.matrix_rank(np.array(A_c))!=np.linalg.matrix_rank(np.array(A_ras)) and symb=='=':
            self.ui.textBrowser.append("Некорректные данные!\nСистема ограничений\nнесовместна!")
            return
        if np.linalg.matrix_rank(np.array(A_c))!=np.linalg.matrix_rank(np.array(A_ras)) and symb=='<':
            self.ui.textBrowser.append("Некорректные данные!\nВозможно зацикливание\n")
            return
        one_massive = [0]*len(D)
        one_massive[-1]=1
        try:
            test1 = alg_dinkelbach1(np.array(D),np.array(one_massive),np.array(A),np.array(b),
                               self.ui.comboBox.currentText(),False,False)
        except:
            self.ui.textBrowser.append("Ошибка\nВеликая ошибка...")
            return

        
        test2 = alg_dinkelbach1(np.array(D), np.array(one_massive), np.array(A), np.array(b),
                               self.ui.comboBox.currentText(), False, True)
        print(test1, test2)

        def im_sorry(x):
            sum = 0
            for i in range(len(D) - 1):
                sum += D[i] * x[i]
            return sum + D[len(D) - 1]
        if im_sorry(test1)>=0>=im_sorry(test2):
            self.ui.textBrowser.append("Некорректные данные!\nЗнаменатель может\nпринять ноль!")
            return
        if im_sorry(test1) < 0:
            rev(D)
            mission = not mission
        solution = alg_dinkelbach(np.array(P),np.array(D),np.array(A),np.array(b),symb,self.ui.checkBox.isChecked(),self.ui.checkBox_2.isChecked(),self.path,self.save)

        for i in range(len(solution)):
            a = 'X'+str(i)+' = '+str(solution[i])+' '
            self.ui.textBrowser.append(a)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
    
sys.exit(app.exec())