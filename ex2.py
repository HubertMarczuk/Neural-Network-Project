def GenerateVectors(v_values, length):
    v = [[0 for i in range(length)] for j in range(pow(len(v_values),length))]
    for i in range(length):
        for j in range(len(v)):
            v[j][length-(i+1)] = v_values[int((j/int(pow(len(v_values),i)))%len(v_values))]
    return v


def CheckStabilizationSync(weight):
    req1 = True
    req2 = True
    req3 = True
    for i in range(len(weight[0])):
        if weight[i][i]<0:
            print("Warunek 1) niespełniony. Macierz wag nie ma nieujemnych wartości na wszystkich elementach diagonali!")
            print("Energia może być rosnąca.")
            req2 = False
            break
    for i in range(len(weight[0])):
        stop = False
        for j in range(i):
            if weight[i][j]!=weight[j][i]:
                print("Warunek 2) niespełniony. Macierz wag nie jest macierzą symetryczną!")
                print("Sieć może wpaść w wielookresowy cykl.")
                req2 = False
                stop = True
                break
        if stop == True:
            break
    if len(weight)==2:
        if weight[0][0]<=0 or weight[0][0]*weight[1][1]-weight[1][0]*weight[0][1]<=0:
            req3 = False
    if len(weight)==3:
        deter = weight[0][0]*weight[1][1]*weight[2][2]
        deter+= weight[1][0]*weight[2][1]*weight[0][2]
        deter+= weight[2][0]*weight[0][1]*weight[1][2]
        deter-= weight[2][0]*weight[1][1]*weight[0][2]
        deter-= weight[0][0]*weight[2][1]*weight[1][2]
        deter-= weight[1][0]*weight[0][1]*weight[2][2]
        if weight[0][0]<=0 or weight[0][0]*weight[1][1]-weight[1][0]*weight[0][1]<=0 or deter<=0:
            req3 = False
    
    if req1 == True:
        print("Warunek 1) spełniony. Wszystkie wartości na diagonali są nieujemne!")
    if req2 == True:
        print("Warunek 2) spełniony. Macierz wag jest macierzą symetryczną!")
        print("Sieć ustabilizuje się na jednym stanie lub wpadnie w dwuokresowy cykl.")
    if req3 == False:
        print("Warunek 3) niespełniony. Macierz wag nie jest dodatnio określona!")
        print("Sieć może wpaść w wielookresowy cykl.")
    else:
        print("Warunek 3) spełniony. Macierz wag dodatnio określona!")
        print("Sieć może się ustabilizować na jednym stanie.")
    if req1 == True and req2 == True and req3 == False:
        print("Warunki 1) oraz 2) spełniony, a 3) nie!")
        print("Sieć ustabilizuje się na jednym stanie lub wpadnie w dwuokresowy cykl.")
    if req1 == True and req2 == True and req3 == True:
        print("Wszystkie warunki spełnione!")
        print("Sieć powinna się ustabilizować na jednym stanie. Energia niemalejąca.")



def CheckStabilizationAsync(weight):
    req1 = True
    req2 = True
    for i in range(len(weight[0])):
        if weight[i][i]<0:
            print("Warunek 1) niespełniony. Macierz wag nie ma nieujemnych wartości na wszystkich elementach diagonali!")
            print("Energia może być rosnąca.")
            req2 = False
            break
    for i in range(len(weight[0])):
        stop = False
        for j in range(i):
            if weight[i][j]!=weight[j][i]:
                print("Warunek 2) niespełniony. Macierz wag nie jest macierzą symetryczną!")
                print("Sieć może wpaść w wielookresowy cykl.")
                req2 = False
                stop = True
                break
        if stop == True:
            break
    if req1 == True:
        print("Warunek 1) spełniony. Wszystkie wartości na diagonali są nieujemne!")
        print("Energia będzie niemalejąca.")
    if req2 == True:
        print("Warunek 2) spełniony. Macierz wag jest macierzą symetryczną!")
        print("Sieć ustabilizuje się na jednym stanie lub wpadnie w dwuokresowy cykl.")
    if req1 == True and req2 == True:
        print("Oba warunki spełnione!")
        print("Sieć powinna się ustabilizować na jednym stanie.")

def Synchronous(weight, v, threshold, activation_type, low_value, high_value):
    v_histories = []
    for i in range(len(v)):
        v_histories.append(Synchronous_a(weight, v[i][:], threshold, activation_type, low_value, high_value))
    return v_histories

def Synchronous_a(weight, v, threshold, activation_type, low_value, high_value):
    v_history = []
    v_history.append(v[:])
    while True:
        u = MatrixMultipliesvector(weight,v)
        for i in range(len(u)):
            v[i] = ActivationFunction(u[i], threshold, activation_type, low_value, high_value)
        v_history.append(v[:])
        stop = False
        for i in range(len(v_history)-1):
            repeat = True
            for j in range(len(v)):
                if v[j] != v_history[i][j]:
                    repeat = False
                    break
            if len(v_history) == 1:
                repeat = False
            if repeat == True:
                stop = True
                break
        if stop == True:
            break
    return v_history
        
def Asynchronous(weight, v, threshold, activation_type, low_value, high_value):
    v_histories = []
    for i in range(len(v)):
        v_histories.append(Asynchronous_a(weight, v[i][:], threshold, activation_type, low_value, high_value))
    return v_histories

def Asynchronous_a(weight, v, threshold, activation_type, low_value, high_value):
    v_history = []
    v_history.append(v[:])
    while True:
        for i in range(len(v)):
            u = DotProduct(weight[i],v)
            v[i] = ActivationFunction(u, threshold, activation_type, low_value, high_value)
            v_history.append(v[:])
        stop = False
        for i in range(len(v_history)-1):
            if i%len(v)==0:
                repeat = True
                for j in range(len(v)):
                    if v[j] != v_history[i][j]:
                        repeat = False
                        break
                if len(v_history) == 1:
                    repeat = False
                if repeat == True:
                    stop = True
                    break
        if stop == True:
            break
    return v_history

def MatrixMultipliesvector(M,v):
    u = []
    for i in range(len(v)):
        sum = 0
        for j in range(len(v)):
            sum+=M[i][j]*v[j]
        u.append(sum)
    return u

def DotProduct(v1,v2):
    sum = 0
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum

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
        
def PrintHistoriesSync(v_histories):
    for i in range(len(v_histories)):
        for j in range(len(v_histories[i])):
            print(v_histories[i][j])
        states = 0
        for j in range(len(v_histories[i])):
            same = True
            for k in range(len(v_histories[i][j])):
                if v_histories[i][j][k] != v_histories[i][len(v_histories[i])-1][k]:
                    same = False
                    break
            states += 1
            if same == True:
                break
        states = len(v_histories[i])-states
        if states == 1:
            print("Wektor stabilizuje się na jednym stanie.")
        else:
            print("Wektor posiada", states, "okresową konfigurację.")
        print()


def PrintHistoriesAsync(v_histories):
    for i in range(len(v_histories)):
        for j in range(len(v_histories[i])):
            print(v_histories[i][j])
            if j%len(v_histories[i][j])==0:
                print("-------")
        states = 0
        for j in range(len(v_histories[i])):
            same = True
            if j%len(v_histories[i][j])==0:
                for k in range(len(v_histories[i][j])):
                    if v_histories[i][j][k] != v_histories[i][len(v_histories[i])-1][k]:
                        same = False
                        break
                states += 1
                if same == True:
                    break
        states = int((len(v_histories[i])-1)/len(v_histories[i][0])+1)-states
        if states == 1:
            print("Wektor stabilizuje się na jednym stanie.")
        else:
            print("Wektor posiada", states, "okresową konfigurację.")
        print()
        

#weight = [[0, -2/3, 2/3],
#          [-2/3, 0, -2/3],
#          [2/3, -2/3, 0]]

#weight = [[-1, 3/4],
#          [3/4, 0]]

weight = [[0, 1],
          [-1, 0]]

v_values = [-1, 1]

v = GenerateVectors(v_values,len(weight[0]))

threshold = 0

activation_type = False      #True(< and >=), False(<= and >)

low_value = -1

high_value = 1

CheckStabilizationSync(weight)
sync = Synchronous(weight, v, threshold, activation_type, low_value, high_value)
PrintHistoriesSync(sync)

#CheckStabilizationAsync(weight)
#a_sync = Asynchronous(weight, v, threshold, activation_type, low_value, high_value)
#PrintHistoriesAsync(a_sync)
