def DataInput():
    print("1) Podaj liczbę neuronów (>1):")
    n = int(input())
    weightmatrix = []
    for i in range (n):
        weightmatrix.append([])
    print("2) Podaj wartości macierzy wag:")
    for i in range(n):
        for j in range(n):
            print("   w{i}{j} = ")
            weightmatrix[i].append(float(input()))
    v = []
    print("3) Podaj wartości elementów wektora wejściowego:")
    for i in range(n):
        print("   v{i} = ")
        v.append(input())
    print("4) Podaj cechy funkcji aktywacji:")
    print("   4a) Podaj próg funkcji aktywacji:")
    threshold = float(input())
    print("   4b) Czy funkcja aktywacji ma zmieniać wartość po osiągnięciu czy po przekroczeniu progu (podaj literkę: \"o\" - po osiągnięciu, \"p\" - po osiągnięciu)?")
    activation_type = input()
    print("   4c) Podaj wartość funkcji aktywacji, gdy jej argument jest mniejszy od progu: ")
    low_value = float(input())
    print("   4d) Podaj wartość funkcji aktywacji, gdy jej argument jest większy od progu: ")
    high_value = float(input())
    return weightmatrix, v, threshold, activation_type, low_value, high_value

def CheckStabilization(weightmatrix):
    for i in range(len(weightmatrix[0])):
        if weightmatrix[i][i]==0:
            print("Warunek 1) niespełniony. Macierz wag nie ma wartości 0 na wszystkich elementach diagonali!!!")
            break
    for i in range(len(weightmatrix[0])):
        for j in range(i):
            if weightmatrix[i][j]!=weightmatrix[j][i]:
                print("Warunek 2) niespełniony. Macierz wag nie jest macierzą symetryczną!!!")
                break


def Synchronous(weightmatrix, v, threshold, activation_type, low_value, high_value):
    v_history = []
    v_history.append(v)
    while True:
        u = MatrixMultipliesvector(weightmatrix,v)
        for i in range(len(u)):
            v[i] = ActivationFunction(u[i], threshold, activation_type, low_value, high_value)
        v_history.append(v)
        stop = False
        for i in range(len(v_history)-1):
            if v == v_history[i]:
                stop = True
                break
        if stop == True:
            break
    return v_history
        
            


def Asynchronous():
    k=0

def MatrixMultipliesvector(M,v):
    u = []
    for i in range(len(v)):
        sum = 0
        for j in range(len(v)):
            sum+=M[i][j]*u[j]
        u.append(sum)
    return u

def ActivationFunction(x, threshold, activation_type, low_value, high_value):
    if activation_type == "p":
        if x > threshold:
            return high_value
        else:
            return low_value
    else:
        if x < threshold:
            return low_value
        else:
            return high_value
        

weightmatrix, v, threshold, activation_type, low_value, high_value = DataInput()
CheckStabilization(weightmatrix)


