import sys
import copy
from PyQt5 import QtWidgets
from main_page import Ui_Dialog
from lex_n_dinkelbach import rev,alg_dinkelbach,alg_dinkelbach_with_no_output
from lex_n_dinkelbach import iter_lex,solution_of_lin_prog,create_simplex_table

from fractions import Fraction
import numpy as np

def double_phaz_sm(A,b):
    task_of_test = [Fraction(0)]*(len(A[0])+1)
    lin_prog =copy.deepcopy(A)
    lin_prog.insert(len(A),rev(task_of_test[:-1]))
    for x in range(len(A)):
        lin_prog[x].insert(0,b[x])
    
    lin_prog[len(A)].insert(0,Fraction(0))  

    count_stb = len(lin_prog[0])
    for l in range(len(lin_prog)):
        for k in range(len(lin_prog)-1):
            lin_prog[l].insert(count_stb+k,Fraction(0))
    strr = 0
    for l in range(count_stb,len(lin_prog[0])):    
        lin_prog[strr][l]=Fraction(1)
        strr+=1
    count_stb = len(lin_prog[0])
    for l in range(len(lin_prog)):
        for k in range(len(lin_prog)-1):
            lin_prog[l].insert(count_stb+k,Fraction(0))
    strr = 0
    for l in range(count_stb,len(lin_prog[0])):    
        lin_prog[strr][l]=Fraction(1)
        strr+=1 
     
    solved_lin_prog_task =False
    while lin_prog != [] and solved_lin_prog_task ==False:
        lin_prog,solved_lin_prog_task = iter_lex(lin_prog)
    #Критерий отсутствия решения
    if lin_prog[len(lin_prog)-1][0]<0 or lin_prog == [] : return False
    return True

def output_error_log(message,is_check,path,save):
        if is_check and save:
            log = open(path + '/log.txt', 'a', encoding='utf-8')
            print(message,file=log)
        if is_check and save==False:
            log = open('./log.txt', 'a', encoding='utf-8')
            print(message,file=log)

def inf_simplex(A,b):
    task_of_test = [Fraction(1)]*(len(A[0])+1)
    lin_prog =copy.deepcopy(A)
    lin_prog.insert(len(A),rev(task_of_test[:-1]))
    for x in range(len(A)):
        lin_prog[x].insert(0,b[x])
    
    lin_prog[len(A)].insert(0,Fraction(0))  

    count_stb = len(lin_prog[0])
    for l in range(len(lin_prog)):
        for k in range(len(lin_prog)-1):
            lin_prog[l].insert(count_stb+k,Fraction(0))
    strr = 0
    for l in range(count_stb,len(lin_prog[0])):    
        lin_prog[strr][l]=Fraction(1)
        strr+=1 
    solved_lin_prog_task =False
    while lin_prog != [] and solved_lin_prog_task ==False:
        lin_prog,solved_lin_prog_task = iter_lex(lin_prog)
    #Критерий отсутствия решения
    if lin_prog == [] and solved_lin_prog_task ==False: return False
    return True
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
      
        self.ui.textBrowser.clear()
        # Если не использовать, то часть текста исчезнет.
        task = self.ui.textEdit.toPlainText()
        for i in range(len(task)):
            if task[i].isdigit()==False and task[i]!=' 'and task[i]!='\n'and task[i]!='-':
                self.ui.textBrowser.append("Некорректные данные!\nСимвольная ошибка")
                output_error_log("Некорректные данные!\nСимвольная ошибка",self.ui.checkBox.isChecked(),self.path,self.save)
                return
            if i<len(task)-1 and task[i].isdigit()  and task[i+1]=='-':
                self.ui.textBrowser.append("Некорректные данные!\nСимвольная ошибка")
                output_error_log("Некорректные данные!\nСимвольная ошибка",self.ui.checkBox.isChecked(),self.path,self.save)
                return
            if (i<len(task)-1 and not task[i+1].isdigit()  and task[i]=='-' or
                    i==len(task)-1 and task[i]=='-'):
                self.ui.textBrowser.append("Некорректные данные!\nСимвольная ошибка")
                output_error_log("Некорректные данные!\nСимвольная ошибка",self.ui.checkBox.isChecked(),self.path,self.save)
                return
        task_arr = [int(x) for x in task.split()]
        if len(task_arr) != (self.ui.spinBox_2.value() + 1) * (self.ui.spinBox.value() + 2):
            self.ui.textBrowser.append("Некорректные данные!\nОшибка количества\nвводных данных!")
            output_error_log("Некорректные данные!\nОшибка количества\nвводных данных!",self.ui.checkBox.isChecked(),self.path,self.save)
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
            output_error_log("Некорректные данные!\nОтсутствие ограничений!",self.ui.checkBox.isChecked(),self.path,self.save)
            return
        if len(P) ==1:
            self.ui.textBrowser.append("Некорректные данные!\nОтсутствие переменных!")
            output_error_log("Некорректные данные!\nОтсутствие переменных!",self.ui.checkBox.isChecked(),self.path,self.save)
            return
        if symb=='<' and inf_simplex(A,b)==False:
            self.ui.textBrowser.append("Некорректные данные!\nСимплекс не ограничен!")
            output_error_log("Некорректные данные!\nСимплекс не ограничен!",self.ui.checkBox.isChecked(),self.path,self.save)
            return
        if symb=='<' and double_phaz_sm(A,b)==False:
            self.ui.textBrowser.append("Некорректные данные!\nСистема не совместна!")
            output_error_log("Некорректные данные!\nСистема не совместна!",self.ui.checkBox.isChecked(),self.path,self.save)
            return

        A_ras = copy.deepcopy(A_c)
        for i in range(len(A_ras)):
            A_ras[i] = np.append(A_ras[i],b_c[i])
        #Для совместности СЛАУ необходимо и достаточно, чтобы ранг её матрицы A был равен рангу её расширенной матрицы A.
        if np.linalg.matrix_rank(np.array(A_c))!=np.linalg.matrix_rank(np.array(A_ras)) and symb=='=':
            self.ui.textBrowser.append("Некорректные данные!\nСистема ограничений\nнесовместна!")
            output_error_log("Некорректные данные!\nСистема ограничений\nнесовместна!",self.ui.checkBox.isChecked(),self.path,self.save)
            return
        #if np.linalg.matrix_rank(np.array(A_c))!=np.linalg.matrix_rank(np.array(A_ras)) and symb=='<':
            #self.ui.textBrowser.append("Некорректные данные!\nВозможно зацикливание\n")
            #return
        one_massive = [0]*len(D)
        one_massive[-1]=1
        try:
            test1 = alg_dinkelbach_with_no_output(np.array(D),np.array(one_massive),np.array(A),np.array(b),
                               symb,False,False,self.path,self.save)
            test2 = alg_dinkelbach_with_no_output(np.array(D), np.array(one_massive), np.array(A), np.array(b),
                                   symb, False, True, self.path, self.save)

        except:
            self.ui.textBrowser.append("Некорректные данные!\nНекорректная задача")
            return
        if test1[1]*test2[1]<=0:
            self.ui.textBrowser.append("Некорректные данные!\nЗнаменатель может\nпринять ноль!")
            output_error_log("Некорректные данные!\nЗнаменатель может\nпринять ноль!", self.ui.checkBox.isChecked(),
                             self.path, self.save)
            return
        if test1[1]>0:
            neg=1
        else:
            neg=-1
        if self.path =='':self.path = '.'

        solution = alg_dinkelbach(np.array(P),np.array(D),np.array(A),np.array(b),symb,self.ui.checkBox.isChecked(),self.ui.checkBox_2.isChecked(),self.path,self.save, neg)

        for i in range(len(solution[0])):
            a = 'X'+str(i+1)+' = '+str(solution[0][i])+' '
            self.ui.textBrowser.append(a)
        bb = 'Q(x*) = '+str(solution[1])
        self.ui.textBrowser.append(bb)
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
    
sys.exit(app.exec())