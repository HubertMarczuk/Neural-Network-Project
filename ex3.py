from numpy import exp,arange
import matplotlib.pyplot as plt

def F(t):
    return 1/(1+exp(-1*t))

def Fprime(x):
    return x*(1-x)

def E(d,y):
    return (d-y)*(d-y)

def Eprime(d,y):
    return -2*(d-y)

def TotalEnergy(w, x1, d, eps, alfa, mode, iterations):
    energy_hist = []
    counter = 0
    while(True):
        energy_sum = 0
        grad_sum = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for k in range(4):
            x2 = [1]
            for i in range(2):
                sum = 0
                for j in range(3):
                    sum+=w[i][j]*x1[k][j]
                x2.append(F(sum))
            x3 = 0
            sum = 0 
            for i in range(3):
                sum += w[2][i]*x2[i]
            x3 = F(sum)
            energy = E(d[k],x3)
            energy_sum += energy
            grad = Propagation(w, x1[k], x2, x3, d[k])
            for i in range(3):
                for j in range(3):
                    grad_sum[i][j] += grad[i][j]
        energy_hist.append(energy_sum)
        for i in range(3):
            for j in range(3):
                w[i][j] = w[i][j] - alfa * grad_sum[i][j]
        counter += 1
        if mode == True:
            if energy_sum <= eps:
                break
        else:
            if counter >= iterations:
                break
    return energy_hist

def PartialEnergy(w, x1, d, eps, alfa, mode, iterations):
    energy_hist = []
    counter = 0
    while(True):
        energy_sum = 0
        for k in range(4):
            x2 = [1]
            for i in range(2):
                sum = 0
                for j in range(3):
                    sum+=w[i][j]*x1[k][j]
                x2.append(F(sum))
            x3 = 0
            sum = 0
            for i in range(3):
                sum += w[2][i]*x2[i]
            x3 = F(sum)
            energy = E(d[k],x3)
            energy_sum += energy
            grad = Propagation(w, x1[k], x2, x3, d[k])
            for i in range(3):
                for j in range(3):
                    w[i][j] = w[i][j] - alfa * grad[i][j]
        counter +=1
        energy_hist.append(energy_sum)
        if mode == True:
            if energy_sum <= eps:
                break
        else:
            if counter >= iterations:
                break
    return energy_hist

def Propagation(w, x1, x2, x3, d):
    dx3 = Eprime(d,x3)
    dw3 = []
    for i in range(3):
        dw3.append(dx3*Fprime(x3)*x2[i])
    dw21 = []
    for i in range(3):
        dw21.append(dx3*Fprime(x3)*w[2][1]*Fprime(x2[1])*x1[i])
    dw22 = []
    for i in range(3):
        dw22.append(dx3*Fprime(x3)*w[2][2]*Fprime(x2[2])*x1[i])
    return [dw21, dw22, dw3]

def Plot(energy):
    x2 = energy
    x1 = arange(0, len(energy), 1)
    plt.plot(x1,x2)
    plt.show()

x1 = [[1,0,0],
      [1,0,1],
      [1,1,0],
      [1,1,1]]

d = [0,
     1,
     1,
     0]

w = [[0.86, -0.16, 0.28],
     [0.82, -0.51, -0.89],
     [0.04, -0.43, 0.48]]

alfa = 0.5

eps = 0.001

eps_mode = True

iterations = 6000

mode = True                    #False(total energy), True(partial energy)

if mode == True:
    energy_part = PartialEnergy(w, x1, d, eps, alfa, eps_mode, iterations)
    Plot(energy_part)
else:
    energy_total = TotalEnergy(w, x1, d, eps, alfa, eps_mode, iterations)
    Plot(energy_total)
