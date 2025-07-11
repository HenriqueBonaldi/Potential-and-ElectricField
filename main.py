#!pip install dataframe_image
#!apt-get install -y xvfb

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

from mpl_toolkits import mplot3d
from matplotlib import cm

import dataframe_image as dfi


def potencial(value):
  i=1
  j=1
  maxVar = value

  while (i<pontos-1):
    while (j<pontos-1):
      #"pular" calculo na posição do condutor 1
      if i==12 and j==10:
        j=j+1
      elif i==13 and j==10:
        j=j+1
      elif i==14 and j==10:
        j=j+1
      elif i==15 and j==10:
        j=j+1
      elif i==16 and j==10:
        j=j+1
      elif i==17 and j==10:
        j=j+1
      elif i==18 and j==10:
        j=j+1
      elif i==19 and j==10:
        j=j+1

      #"pular" calculo na posição do condutor 2
      elif i==15 and j==17:
        j=j+1
      elif i==15 and j==18:
        j=j+1
      elif i==15 and j==19:
        j=j+1
      elif i==15 and j==20:
        j=j+1
      elif i==15 and j==21:
        j=j+1
      elif i==15 and j==22:
        j=j+1
      elif i==15 and j==23:
        j=j+1
      else:
        V=0.25*(net[i][j-1]+net[i][j+1]+net[i-1][j]+net[i+1][j])
        variation = (V-net[i][j])/net[i][j]
        variation = abs(variation)
        if variation > maxVar:
          maxVar = variation
        net[i][j]=V
        j=j+1

    i=i+1
    j=1

  return maxVar




def campo():
  i=1
  j=1
  while (i<pontos-1):
    while (j<pontos-1):
      Ex=round(-(net[i+1][j]-net[i-1][j])/(2*deltaL),4)
      Ey=round(-(net[i][j+1]-net[i][j-1])/(2*deltaL),4)

      E=round(math.sqrt(Ex**2+Ey**2),4)

      campoPonto = [Ex,Ey,E]

      campoE[i][j]=campoPonto

      #atribuição de valor zero para o campo no centro do condutor 2 - "sumidouro" de campo, qualquer outra posição há campo
      #o condutor 2 é simétrico nas condições de GRID que foram desenvolvidas- ou seja, seu centro é coincidente com um ponto do grid, dessa forma, nesse ponto o campo é zero
      if i == 15 and j == 20:
        lX.append(0)
        lY.append(0)
      else:
        lX.append(0.5*Ex/E)
        lY.append(0.5*Ey/E)

      posX.append(x[i])
      posY.append(y[j])

      j=j+1

    i=i+1
    j=1

#condições iniciais das barras
m1=7
m10=6

u=0.5 #precisa ter valor tal qual "l" seja inteiro para que a posicao dos condutores tenha correspondencia com os pontos da malha
l=30*u

b1=m1*u
b1c=[10*u,15*u]
b1v=10

b2=m10*u
b2c=[20*u,15*u]
b2v=-10

deltaL=0.5
pontos=int(l/deltaL+1)

net = [[5 for i in range(pontos)] for j in range(pontos)]

#condiçaõ de contorno da caixa
for i in range(pontos):
  net[0][i]=0
  net[pontos-1][i]=0
  net[i][0]=0
  net[i][pontos-1]=0

col1=int(b1c[0]/deltaL)
lin1=int(b1c[1]/deltaL)
z=int(-b1/(2*deltaL))

while (z<=1+int(b1/(2*deltaL))):
  i=int(lin1+z)
  net[i][col1]=10
  z+=1

col2=int(b2c[0]/deltaL)
lin2=int(b2c[1]/deltaL)
z=int(-b2/(2*deltaL))

while (z<=int(b2/(2*deltaL))):
  i=int(col2+z)
  net[lin2][i]=-10
  z+=1

#calculo do potencial
delt=0
delt = potencial(delt)

while (delt > 0.001):
  delt=0
  delt = potencial(delt)

df = pd.DataFrame(net)
pd.set_option('display.precision', 1)

plt.title('Figura 3: Caixa com condutores - Representação do gradiente de potencial')
plt.xlabel('x')
plt.ylabel('y')
plt.imshow(df, cmap='plasma')

styled_df = (df.style.set_properties(**{'background-color': 'lightgrey',
                           'color': 'black',
                           'border-color': 'darkgrey',
                           'border-width': '1px',
                           'border-style': 'solid'}).background_gradient(cmap='plasma'))
styled_df.to_html("tabela_completa.html")

#calculo do campo eletrico
#configuração de vetores para armazenamento
campoE = [[[0 for i in range(3)] for j in range(pontos)] for k in range(pontos)]
lX = []
posX=[]
lY = []
posY=[]

#configuração da grid
x = np.zeros(pontos)
y = np.zeros(pontos)
#iterando a grid
for i in range(pontos):
  x[i]=i*deltaL
  y[i]=i*deltaL
#arredondando o ultimo valor da grid a fim de evitar erro de aproximação pelo programa
x[pontos-1]=15
y[pontos-1]=15

X,Y = np.meshgrid(x, y)

campo()

pd.set_option('display.precision', 1)
df_E = pd.DataFrame(campoE)
styled_df2 = (df_E.style.set_properties(**{'background-color': 'lightgrey',
                           'color': 'black',
                           'border-color': 'darkgrey',
                           'border-width': '1px',
                           'border-style': 'solid'}))
styled_df2.to_html("tabela_.html")

# Configuracao do plotting
plt.figure(1, figsize=[6.4,6.4])
plt.contour(x, y, net, 40,cmap="plasma")
plt.title('Figura 4: Representação de curvas Equipotenciais')
plt.xlabel('x')
plt.ylabel('y')

plt.figure(2, figsize=[6.4,6.4])
plt.quiver(posY, posX, lY, lX, scale=30)
plt.title('Figura 5: Representação vetorial do Campo Elétrico ponto-a-ponto')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()


plt.figure(3, figsize=[6.4,6.4])
plt.contour(x, y, net, 40, cmap="plasma")
plt.quiver(posY, posX, lY, lX, scale=30)
plt.title('Figura 6: Curvas Equipotenciais e Vetores Campo Elétrico')
plt.xlabel('x')
plt.ylabel('y')

plt.show()

# curvas de nível tridimensional:
plt.figure(figsize=[9,9])
ax = plt.axes(projection='3d')
ax.contour3D(x, y, net, 100, cmap='plasma')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('V')
plt.title("Figura 7: Curvas 3D Equipotenciais")
ax.view_init(20, 120)

plt.show()