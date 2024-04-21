def GenerateVectors(v_values, length):
    v = [[0 for i in range(length)] for j in range(pow(len(v_values),length))]
    print(len(v), length)
    for i in range(length):
        for j in range(len(v)):
            v[j][length-(i+1)] = v_values[int((j/int(pow(len(v_values),i)))%len(v_values))]
    return v



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
    if activation_type == False:
        if x > threshold:
            return high_value
        else:
            return low_value
    else:
        if x < threshold:
            return low_value
        else:
            return high_value
        

weight = [[0, -1, 1],
          [-1, 0, 0.5],
          [1, 0.5, 0]]
v_values = [0,1]
v = GenerateVectors(v_values,len(weight[0]))
threshold = 0
activation_type = True                  #True(< and >=), False(<= >)
low_value = 0
high_value = 1
#CheckStabilization(weight)
