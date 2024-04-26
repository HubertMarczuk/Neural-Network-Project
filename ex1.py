import numpy as np
import matplotlib.pyplot as plt


def Dane():
    # dane
    x = [[1,0,0],[1,0,1],[1,1,0],[1,1,1]] # tablica wektorów wejściowych
    ro = 1 # stała uczenia
    d = [] # wartości oczekiwane

    # wybór AND, XOR czy własne wartości
    t1 = 0
    t11 = 0
    while (t1!=1 and t1!=2 and t1!=3):
        try:
            t1 = int(input("Wybierz czy wartości oczekiwane mają być realizowane przez: 1 - AND, 2 - XOR, 3 - własne wartości (wprowadź liczbę): "))
        except ValueError:
            print("Podaj liczbę!")   
    if t1 == 1:
        for i in range(len(x)):
            d.append(int(x[i][1] and x[i][2]))
    if t1 == 2:
        print("Dla funkcji XOR proponowane jest podniesienie wymiaru wektorów wejściowych RBF")
        for i in range(len(x)):
            d.append(int(x[i][1] ^ x[i][2]))
        t11 = int(input("Czy chcesz podnieść wymiar? 1 - Tak, 2 - Nie (wprowadź liczbę): "))
        if t11 == 1:
            RBF(x)
        
    if t1 == 3:
        d = [int(input("Podaj "+str(i+1)+". wartość oczekiwaną (podaj liczbę i naciśnij enter): ")) for i in range(len(x))]


    # wybór wag
    t2 = 0
    while t2==0:
        try:
            w = [float(input("Podaj "+str(i+1)+". wagę (podaj liczbę i naciśnij enter): ")) for i in range(len(x[0]))] # wektor wag
            t2=1
        except ValueError:
            print("Zły format danych")
    
    # wybór trybu perceptronu (PA, BUPA)
    t3 = 0
    while (t3!=1 and t3!=2):
        try:
            t3 = int(input("Wybierz tryb perceptronu: 1 - PA, 2 - BUPA (wprowadź liczbę): "))
        except ValueError:
            print("Podaj liczbę!")   
    if t3 == 1:
        PerceptronPA(x,ro,d,w,t11)
    if t3 == 2:
        PerceptronBUPA(x,ro,d,w,t11)


def PerceptronPA(x,ro,d,w,t11):
    #algorytm
    condition = 0
    nr = 0
    tab = []
    while(condition == 0):
        for i in range(len(x)):
            nr+=1
            fi = np.dot(x[i],w)
            y = g(fi)
            InfoPA(nr, x[i], w, fi, y, d[i])  
                     
            #wykres
            if len(x[1]) == 3 and w[2] != 0:
                Plot(x,w,nr)
            elif len(x[1]) == 4 and w[3] != 0:
                Plot3D(x,w,nr)
            else:
                print(f"Nie można ustalić granicy decyzyjnej iteracji {nr}.")
                print("------------------------------------------")
            
            #zmiana wag
            if y!=d[i]:
                tab.append(0)
                for j in range(len(w)):
                    w[j]=w[j]+ro*(d[i]-y)*x[i][j]
            else:
                tab.append(1)

            #warunek stopu
            if len(tab)>=len(x) and all(element == 1 for element in tab[-len(x):]):
                condition = 1
                plt.show()
                break

            #warunek stopu dla XOR
            if t11 == 2 and nr == 40:
                condition = 1
                print("Zbiór liniowo nieseparowalny")
                plt.show()
                break
           
    
def PerceptronBUPA(x,ro,d,w,t11):
    #algorytm
    condition = 0
    nr = 0
    while(condition == 0):
        z = [0 for x in range(len(x[0]))] 
        for i in range(len(x)):
            nr+=1 
            fi = np.dot(x[i],w)
            y = g(fi)
            difference = d[i] - y # błąd rezydualny
            InfoBUPA(nr, x[i], w, fi, y, d[i], difference)
            if difference < 0:
                z=np.subtract(z,x[i])
            if difference > 0:
                z=np.add(z,x[i])         
        #wykres
        if len(x[1]) == 3 and w[2] != 0:
            Plot(x,w,int(nr/4))
        elif len(x[1]) == 4 and w[3] != 0:
            Plot3D(x,w,int(nr/4))
        else:
            print(f"Nie można ustalić granicy decyzyjnej iteracji {nr}.")
            print("------------------------------------------")
        
        #zmiana wag
        w = np.add(w,ro*z)
        
        #warunek stopu
        if all(element==0 for element in z):
            plt.show()
            condition = 1
        
        #warunek stopu dla XOR
        if t11 == 2 and nr == 40:
            print("Zbiór liniowo nieseparowalny")
            condition = 1

# funkcje pomocnicze   
def g(x):
    if x>0:
        return 1
    else:
        return 0
    
def Plot(x,w,nr):
    plt.figure()
    # wektory na wykresie
    x1_values = [vector[1] for vector in x]
    x2_values = [vector[2] for vector in x]
    plt.scatter(x1_values, x2_values)

    # granica decyzyjna
    x1 = np.array([0,1])
    x2 = -1*w[0]/w[2] - x1*w[1]/w[2]
    plt.plot(x1,x2)
    plt.xlabel("oś x1")
    plt.ylabel("oś x2")
    plt.title(f"Wykres {nr} granicy decyzyjnej o wzorze x2 = {-1*w[1]/w[2]}*x1+{-1*w[0]/w[2]}")

def Plot3D(x,w,nr):
    ax = plt.figure().add_subplot(projection='3d')

    # wektory na wykresie
    x1_values = [vector[1] for vector in x]
    x2_values = [vector[2] for vector in x]
    x3_values = [vector[3] for vector in x]
    ax.scatter(x1_values, x2_values, x3_values)

    # granica decyzyjna
    x1 = np.array([0,1])
    x2 = np.array([0,1])
    X1, X2 = np.meshgrid(x1, x2)
    X3 = -1*w[0]/w[3] - X1*w[1]/w[3] - X2*w[2]/w[3]
    ax.plot_surface(X1,X2,X3)
    ax.set_xlabel("oś x1")
    ax.set_ylabel("oś x2")
    ax.set_zlabel("oś x3")
    plt.title(f"Wykres {nr} granicy decyzyjnej o wzorze x3 = {-1*w[0]/w[3]}-x1*{w[1]/w[3]}-x2*{w[2]/w[3]}")

def RBF(x):
    for i in range(len(x)):
        x[i].append(np.exp(-1/2*(x[i][1] - x[i][2])**2))
    print(x)

def InfoPA(nr, x, w, fi, y, d):
    headers = ["Iteracja", "Wektor trenujący", "weights", "Fi", "Wynik", "Wartość oczekiwana"]
    data = [nr, x, w, fi, y, d]
    for i in range(len(headers)):
        print(headers[i], ": ", data[i])       
    print("------------------------------------------")

def InfoBUPA(nr, x, w, fi, y, d, difference):
    headers = ["Iteracja", "Wektor trenujący", "weights", "Fi", "Wynik", "Wartość oczekiwana", "Różnica (d-y)"]
    data = [nr, x, w, fi, y, d, difference]
    for i in range(len(headers)):
        print(headers[i], ": ", data[i])       
    print("------------------------------------------")

Dane()