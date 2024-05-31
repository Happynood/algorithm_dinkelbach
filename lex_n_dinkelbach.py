#все импорты
import pandas as pd
import copy
import numpy as np
from fractions import Fraction
#import time
#Функия для обратной записи массива
def rev(lst):
    return [ -i for i in lst ] 
#Есть ли в столбце элемент меньше нуля
def check_stb_more_zero(a,x):
    count = 0
    for i in range(0,len(a)-1):
      if a[i][x]<=0: count+=1
    if count==len(a)-1:
       print(a,x) 
       return False
    return True

#Красивый вывод симплекс-таблицы
def beauty_print_simplex_table(a):
   df = pd.DataFrame(data = a)
   print(df)

#Поиск номеров вектров, входящих в базис
def search_main_basis(a):
   if len(a)==2:
      n = []
      for i in range(1,len(a[0])):
         if a[0][i]==1: n.append(i)
         return n
   num_of_vectors_which_are_basis = []
   for i in range(1,len(a[0])):
       count_of_zeros = 0
       for j in range(0,len(a)-1):
          if a[j][i]==0:count_of_zeros+=1
             
       if count_of_zeros==len(a)-2 and len(num_of_vectors_which_are_basis)<len(a)-1: num_of_vectors_which_are_basis.append(i)
   correct_nums=[0]*len(num_of_vectors_which_are_basis)
   for i in range(len(num_of_vectors_which_are_basis)):
      for j in range(0,len(a)-1):
         if a[j][num_of_vectors_which_are_basis[i]]==1:correct_nums[i] = j
   vse = [0]*len(num_of_vectors_which_are_basis)
   for x in range(len(correct_nums)):
      vse[correct_nums[x]] = num_of_vectors_which_are_basis[x]
   return vse

#Итерация симлекс-методом
def iter(a):
  max_x = 1
  max_y = 0
  while a[len(a)-1][max_x]>=0:
    max_x+=1
    if max_x>len(a[0])-1:
      return a,True
  for x in range(max_x,len(a[0])):
    if check_stb_more_zero(a,x)==False:
         return [],False 
    if abs(a[len(a)-1][x])>abs(a[len(a)-1][max_x]) and a[len(a)-1][x]<0 and check_stb_more_zero(a,x) :
      
      max_x = x
  while a[max_y][max_x]<=0:
    max_y+=1
    if max_y==len(a)-2: break
  for y in range(len(a)-1):
    if a[y][max_x] <=0: continue
    if a[y][max_x]>0 and abs(a[y][0]/a[y][max_x])<abs(a[max_y][0]/a[max_y][max_x]): max_y = y
  b = copy.deepcopy(a)
  for i in range(len(a)-1):
    for j in range(len(a[0])):
      if i==max_y:
        b[i][j]= a[i][j]/a[max_y][max_x]
      if i!=max_y: b[i][j]=a[i][j]- a[i][max_x]*a[max_y][j]/a[max_y][max_x]
  return b,False

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
    if check_stb_more_zero(a,x)==False:
         return [],False
    if x!=0 and abs(a[len(a)-1][x])>abs(a[len(a)-1][max_x]) and a[len(a)-1][x]<0  and  check_stb_more_zero(a,x) : 
       
      max_x = x
  while a[max_y][max_x]<=0:
    max_y+=1
    if max_y==len(a)-2: break
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

#находится ли точка в симплексе
def dot_in_place(A,b,x):
    for i in range(len(A)):
        sum_line = [0]*len(b)
        for j in range(len(A)):
           sum_line[i]+=A[i][j]*x[j]
    for s in range(len(sum_line)):
       if sum_line[s]>b[s]: return False
    return True

#поиск начального дбра
def search_dbr(P,A,b,symb):
    lin_prog = create_simplex_table(A,b,P,symb)
    solved = solution_of_lin_prog(A,lin_prog)      
    return solved[0]

#Создание симплекс таблицы из матрицы А и вектора б
def create_simplex_table(A,b,new_C,symb):
    lin_prog = A.tolist()
    lin_prog.insert(len(A),rev(new_C[:-1]))
    lin_prog[len(A)].insert(0,Fraction(new_C[len(new_C)-1]))
    for x in range(len(A)):
        lin_prog[x].insert(0,b[x])
    if symb =="<" or symb =="=":
        count_stb = len(lin_prog[0])
        for l in range(len(lin_prog)):
            for k in range(len(lin_prog)-1):
                lin_prog[l].insert(count_stb+k,Fraction(0))
        strr = 0
        for l in range(count_stb,len(lin_prog[0])):    
            lin_prog[strr][l]=Fraction(1)
            strr+=1
    return lin_prog

#Вывод в txt начальной симплекс таблицы
def print_to_txt(save_txt,save,count_lambda_iter,lambda_alg,lin_prog,path,new_C):
    if save_txt and save==True:
        log = open(path + '/log.txt', 'a', encoding='utf-8')
        print('--------------ITERATION ',count_lambda_iter,'------------------',file = log)
        print(count_lambda_iter,' lambda',lambda_alg,file=log)
        print('Mission: ',new_C,file=log)
        print('Task of lin prog',file=log)
        df = pd.DataFrame(data = lin_prog)
        print(df,file=log)
    if save_txt and save==False:
        log = open('./log.txt', 'a')
        print('--------------ITERATION ',count_lambda_iter,'------------------',file = log)
        print(count_lambda_iter,' lambda',lambda_alg,file=log)
        print('Mission: ',new_C,file=log)
        print('Task of lin prog',file=log)
        df = pd.DataFrame(data = lin_prog)
        print(df,file=log)

#Решение симплекс метода принимает на вход матрицу прямых ограничений без b и задачи линейного программирования
def solution_of_lin_prog(A,lin_prog):
    dbr = [0]*(len(A[0]))
    solved_lin_prog_task = False
    crit_count_lin_prog = 1000
    count_lin_prog = 0
    zacikliv = False
    pre_last_lin_prog = []
    while solved_lin_prog_task==False and count_lin_prog <crit_count_lin_prog:
        for i in range(len(lin_prog)):
            for j in range(len(lin_prog[0])):
                if count_lin_prog != 0 and lin_prog[i][j]==pre_last_lin_prog[i][j]:
                    zacikliv = True
                    break
        if zacikliv==False: 
            lin_prog,solved_lin_prog_task = iter(lin_prog)
        else :
            lin_prog,solved_lin_prog_task = iter_lex(lin_prog)

           
        pre_last_lin_prog = copy.deepcopy(lin_prog)
        count_lin_prog+=1
        
    nums_of_basis = search_main_basis(lin_prog)
    for copy_dbr in range(len(dbr)):
           
        if (copy_dbr+1) in nums_of_basis:
            dbr[copy_dbr]=lin_prog[nums_of_basis.index(copy_dbr+1)][0]
        else:
            dbr[copy_dbr]=0
    return dbr,lin_prog

#Номера векторов в базисе
def num_of_basis_func(lin_prog,dbr):
    nums_of_basis = search_main_basis(lin_prog)
    for copy_dbr in range(len(dbr)):
           
        if (copy_dbr+1) in nums_of_basis:
            dbr[copy_dbr]=lin_prog[nums_of_basis.index(copy_dbr+1)][0]
        else:
            dbr[copy_dbr]=0
    return nums_of_basis

#Вывод конечной симплекс таблицы
def print_end_of_alg(lin_prog,nums_of_basis,dbr,neg,mission,save_txt,insert_x_in_P,insert_x_in_D,save,path,F):
    print('End iteration:')
    beauty_print_simplex_table(lin_prog)
    print('Num of vec in basis',nums_of_basis)
    print ('Basis solution', dbr)
    print('F = ',F, '\n\n')
    print('Optimum result = ',neg*(-1)**mission*insert_x_in_P(dbr)/insert_x_in_D(dbr), '\n\n')
    if save_txt:
        if save_txt and save==True:
            log = open(path + '/log.txt', 'a', encoding='utf-8')
            print('End iteration:',file=log)
            df = pd.DataFrame(data = lin_prog)
            print(df,file=log)
            print('Num of vec in basis',nums_of_basis,file=log)
            print ('Basis solution', dbr,file=log)
            print('F = ',F, '\n\n',file=log)
            print('Optimum result = ',neg*(-1)**mission*insert_x_in_P(dbr)/insert_x_in_D(dbr), '\n\n',file=log)
        if save_txt and save==False:
            log = open('./log.txt', 'a')
            print('End iteration:',file=log)
            df = pd.DataFrame(data = lin_prog)
            print(df,file=log)
            print('Num of vec in basis',nums_of_basis,file=log)
            print ('Basis solution', dbr,file=log)
            print('F = ',F, '\n\n',file=log)
            print('Optimum result = ',neg*(-1)**mission*insert_x_in_P(dbr)/insert_x_in_D(dbr), '\n\n',file=log)


#полный алгоритм динкельбаха
def alg_dinkelbach(P,D,A,b,symb,save_txt,mission,path,save,neg):
    #проверка знака
    if neg==-1:
       D=D*(-1)
       mission=1-mission
    if mission:
       P=P*(-1)
    print(P,D)

    #вспомогательные функции вставки точки в P или D
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
    
    #Ищем первый ДБР
    dbr = [0]*len(A[0])
    dbr = search_dbr(P,A,b,symb)

    #Переменные алгоритма динкельбаха
    lambda_alg = Fraction()
    count_lambda_iter = 0
    crit_count_lambda_iter = 1000
    F = 1

    while (lambda_alg!=0 and F!=0 and count_lambda_iter<crit_count_lambda_iter) or count_lambda_iter==0:
        #Подсчет лямбды
        print('--------------ITERATION ',count_lambda_iter,'------------------')
        pre_lambda_alg = lambda_alg
        lambda_alg = Fraction(insert_x_in_P(dbr),insert_x_in_D(dbr))

        #Если зациклилось останавливаемся
        if count_lambda_iter!=0 and lambda_alg==pre_lambda_alg:
           break

        print(count_lambda_iter,' lambda',lambda_alg)

        #Подсчет новой целевой функции
        new_C = P-lambda_alg*D
        print('Mission: ',new_C)

        #Создание симлекс таблицы
        lin_prog= create_simplex_table(A,b,new_C,symb)
        print('Task of lin prog')
        
        #Вывод в txt задачи линейного программирования
        print_to_txt(save_txt,save,count_lambda_iter,lambda_alg,lin_prog,path,new_C)

        #Вывод в консоль задачи линейного программирования
        beauty_print_simplex_table(lin_prog)

        #Решение задачи линейного программирования 
        solution_task = solution_of_lin_prog(A,lin_prog)
        dbr = solution_task[0]
        lin_prog = solution_task[1]

        #Поиск номеров входящих в базис
        nums_of_basis = num_of_basis_func(lin_prog,dbr)

        count_lambda_iter+=1
        F = lin_prog[len(lin_prog)-1][0]

        #Вывод в консоль и txt конечной итерации
        print_end_of_alg(lin_prog,nums_of_basis,dbr,neg,mission,save_txt,insert_x_in_P,insert_x_in_D,save,path,F)
        
  
    return dbr, neg*(-1)**mission*insert_x_in_P(dbr)/insert_x_in_D(dbr)


def alg_dinkelbach_with_no_output(P, D, A, b, symb, save_txt, mission, path, save):
    if mission:
        P = P * (-1)

        #вспомогательные функции вставки точки в P или D
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
    
    #Ищем первый ДБР
    dbr = [0]*len(A[0])
    dbr = search_dbr(P,A,b,symb)

    #Переменные алгоритма динкельбаха
    lambda_alg = Fraction()
    count_lambda_iter = 0
    crit_count_lambda_iter = 1000
    F = 1

    while (lambda_alg!=0 and F!=0 and count_lambda_iter<crit_count_lambda_iter) or count_lambda_iter==0:
        #Подсчет лямбды
        print('--------------ITERATION ',count_lambda_iter,'------------------')
        pre_lambda_alg = lambda_alg
        lambda_alg = Fraction(insert_x_in_P(dbr),insert_x_in_D(dbr))

        #Если зациклилось останавливаемся
        if count_lambda_iter!=0 and lambda_alg==pre_lambda_alg:
           break

        print(count_lambda_iter,' lambda',lambda_alg)

        #Подсчет новой целевой функции
        new_C = P-lambda_alg*D
        print('Mission: ',new_C)

        #Создание симлекс таблицы
        lin_prog= create_simplex_table(A,b,new_C,symb)
        print('Task of lin prog')
        
        #Вывод в txt задачи линейного программирования
        print_to_txt(save_txt,save,count_lambda_iter,lambda_alg,lin_prog,path,new_C)

        #Вывод в консоль задачи линейного программирования
        beauty_print_simplex_table(lin_prog)

        #Решение задачи линейного программирования 
        solution_task = solution_of_lin_prog(A,lin_prog)
        dbr = solution_task[0]
        lin_prog = solution_task[1]

        #Поиск номеров входящих в базис
        nums_of_basis = num_of_basis_func(lin_prog,dbr)

        count_lambda_iter+=1
        F = lin_prog[len(lin_prog)-1][0]

        #Вывод в консоль и txt конечной итерации
        print_end_of_alg(lin_prog,nums_of_basis,dbr,1,mission,save_txt,insert_x_in_P,insert_x_in_D,save,path,F)
        
    return dbr,  (-1) ** mission * insert_x_in_P(dbr) / insert_x_in_D(dbr)