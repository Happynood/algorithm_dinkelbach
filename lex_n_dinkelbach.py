#все импорты
import pandas as pd
from scipy import spatial
import copy
import numpy as np
from fractions import Fraction
#import time
#Функия для обратной записи массива
def rev(lst):
    return [ -i for i in lst ] 
#Есть ли в столбце элемент меньше нуля
def check_stb_more_zero(a,x):
    for i in range(1,len(a)-1):
      if a[i][x]<0: return False
    return True

#Красивый вывод симплекс-таблицы
def beauty_print_simplex_table(a):
   df = pd.DataFrame(data = a)
   print(df)

#Поиск номеров вектров, входящих в базис
def search_main_basis(a):
   num_of_vectors_which_are_basis = []
   for i in range(1,len(a[0])-1):
       count_of_zeros = 0
       for j in range(0,len(a)-1):
          if a[j][i]==0:count_of_zeros+=1
       if count_of_zeros==len(a)-2 and len(num_of_vectors_which_are_basis)<len(a)-1: num_of_vectors_which_are_basis.append(i-1)
   return num_of_vectors_which_are_basis

#Итерация лексикографическим симлекс-методом
def iter_lex(a):
  #Начинаем поиск элемента, который мы пустим в базис
  max_x = 1
  max_y = 0
  while a[len(a)-1][max_x]>=0:
    max_x+=1
    if max_x>len(a[0])-1: #Если не найдем, какой выводить - мы нашли оптимальное решение
      #print('Оптимальное решение найдено')
      return a,True
  for x in range(max_x,len(a[0])):
    if x!=0 and abs(a[len(a)-1][x])>abs(a[len(a)-1][max_x]) and a[len(a)-1][x]<0  and  check_stb_more_zero(a,x) : 
      max_x = x
  while a[max_y][max_x]<=0:
    max_y+=1
  for y in range(len(a)):
    if a[y][max_x] <=0: continue
    if a[y][max_x]>0 and abs(a[y][0]/a[y][max_x])<abs(a[max_y][0]/a[max_y][max_x]): max_y = y
    if a[y][max_x]>0 and abs(a[y][0]/a[y][max_x])==abs(a[max_y][0]/a[max_y][max_x]):
      for i in range(1,len(a)):
          if a[y][max_x]>0 and abs(a[y][i]/a[y][max_x])==abs(a[max_y][i]/a[max_y][max_x]): pass
          if a[y][max_x]>0 and abs(a[y][i]/a[y][max_x])<abs(a[max_y][i]/a[max_y][max_x]): 
            max_y = y
            break
  b = copy.deepcopy(a)
  for i in range(len(a)):
    for j in range(len(a[0])):
      if i==max_y:
        b[i][j]= a[i][j]/a[max_y][max_x]
      if i!=max_y: b[i][j]=a[i][j]- a[i][max_x]*a[max_y][j]/a[max_y][max_x]
  return b,False

def dot_in_place(A,b,x):
    for i in range(len(A)):
        sum_line = [0]*len(b)
        for j in range(len(A)):
           sum_line[i]+=A[i][j]*x[j]
    for s in range(len(sum_line)):
       if sum_line[s]>b[s]: return False
    return True

def alg_dinkelbach(P,D,A,b,symb,save_txt,mission):
    if mission:
       P=P*(-1)
    def insert_x_in_P(x):
        sum = 0
        for i in range(len(P)-1):
            sum+=P[i]*x[i]
        return sum+P[len(P)-1]
    def insert_x_in_D(x):
        sum = 0
        for i in range(len(D)-1):
            sum+=D[i]*x[i]
        return sum+D[len(D)-1]
    find_dbr = False
    count_find_dbr = 0
    crit_count_iter = 200000
    dbr = [0]*len(A[0])
    add_to_dbr_index=0
    while not find_dbr and count_find_dbr<crit_count_iter:
        if(dot_in_place(A,b,dbr)):
            break
        else:
            dbr[add_to_dbr_index]+=1
            if add_to_dbr_index==len(dbr):
                add_to_dbr_index=-1
            add_to_dbr_index+=1

        count_find_dbr+=1

    
    lambda_alg = Fraction()
    count_lambda_iter = 0
    crit_count_lambda_iter = 1000
    F = 1
    while (lambda_alg!=0 and F!=0 and count_lambda_iter<crit_count_lambda_iter) or count_lambda_iter==0:
        print('--------------ITERATION ',count_lambda_iter,'------------------')
       
        lambda_alg = Fraction(insert_x_in_P(dbr),insert_x_in_D(dbr))
        print(count_lambda_iter,' lambda',lambda_alg)
        new_C = P-lambda_alg*D
        print('Mission: ',new_C)
        lin_prog = A.tolist()

        lin_prog.insert(len(A),rev(new_C[:-1]))
        lin_prog[len(A)].insert(0,Fraction(new_C[len(new_C)-1]))
        for x in range(len(A)):
            lin_prog[x].insert(0,b[x])
        if symb =="<":
            count_stb = len(lin_prog[0])
            for l in range(len(lin_prog)):
                for k in range(len(lin_prog)-1):
                    lin_prog[l].insert(count_stb+k,Fraction(0))
            strr = 0
            for l in range(count_stb,len(lin_prog[0])):    
                lin_prog[strr][l]=Fraction(1)
                strr+=1
        print('Task of lin prog')
        beauty_print_simplex_table(lin_prog)
        solved_lin_prog_task = False
        crit_count_lin_prog = 1000
        count_lin_prog = 0
        while solved_lin_prog_task==False and count_lin_prog <crit_count_lin_prog:
           lin_prog,solved_lin_prog_task = iter_lex(lin_prog)
           count_lin_prog+=1
        nums_of_basis = search_main_basis(lin_prog)
        for copy_dbr in range(len(dbr)):
           if copy_dbr in nums_of_basis:
              dbr[copy_dbr]=lin_prog[copy_dbr][0]
           else:
              dbr[copy_dbr]=0
        count_lambda_iter+=1
        F = lin_prog[len(lin_prog)-1][0]
        print('End iteration:')
        beauty_print_simplex_table(lin_prog)
        print('Num of vec in basis',nums_of_basis)
        print ('Basis solution', dbr)
        print('F = ',F, '\n\n')
        if save_txt:
            log = open("log.txt", "a")
            print('--------------ITERATION ',count_lambda_iter,'------------------',file = log)
            print(count_lambda_iter,' lambda',lambda_alg,file=log)
            print('Mission: ',new_C,file=log)
            print('Task of lin prog',file=log)
            print('End iteration:',file=log)
            df = pd.DataFrame(data = lin_prog)
            print(df,file=log)
            print('Num of vec in basis',nums_of_basis,file=log)
            print ('Basis solution', dbr,file=log)
            print('F = ',F, '\n\n',file=log)
        #time.sleep(5)
    return dbr


#alg_dinkelvach(np.array([Fraction(5),Fraction(2),Fraction(3)]),np.array([Fraction(3),Fraction(1),Fraction(2)]),np.array([[Fraction(6),Fraction(4)],[Fraction(3),Fraction(5)]]),np.array([Fraction(25),Fraction(20)]),"<=")