import numpy as np
import matplotlib.pyplot as plt

# Função que gera uma curva de Bézier cúbica
def curva_bezier(t, P0, P1, P2, P3):
    return (1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3

# Função que gera uma curva de Hermite
def curva_hermite(t, P0, T0, P1, T1):
    return (2*t**3 - 3*t**2 + 1)*P0 + (t**3 - 2*t**2 + t)*T0 + (-2*t**3 + 3*t**2)*P1 + (t**3 - t**2)*T1

# Gerando pontos aleatórios 3D
def ponto_aleatorio3D(escala=1):
    return np.array([np.random.uniform(-escala, escala),
                     np.random.uniform(-escala, escala),
                     np.random.uniform(-escala, escala)])

# Gerando um circuito
def gerar_circuito():
    # Começa e termina no ponto (0, 0, 0)
    P0 = np.array([0, 0, 0])
    
    # Primeira curva de Bézier
    P1 = ponto_aleatorio3D()
    P2 = ponto_aleatorio3D()
    P3 = ponto_aleatorio3D()
    
    bezier1 = [curva_bezier(t, P0, P1, P2, P3) for t in np.linspace(0, 1, 50)]
    
    # Primeira curva de Hermite
    T0 = ponto_aleatorio3D(escala=0.5)
    P4 = ponto_aleatorio3D()
    T1 = ponto_aleatorio3D(escala=0.5)
    
    hermite1 = [curva_hermite(t, P3, T0, P4, T1) for t in np.linspace(0, 1, 50)]
    
    # Segunda curva de Bézier
    P5 = ponto_aleatorio3D()
    P6 = ponto_aleatorio3D()
    P7 = ponto_aleatorio3D()
    
    bezier2 = [curva_bezier(t, P4, P5, P6, P7) for t in np.linspace(0, 1, 50)]
    
    # Segunda curva de Hermite
    T2 = ponto_aleatorio3D(escala=0.5)
    P8 = np.array([0, 0, 0])  # Retornando ao início
    T3 = ponto_aleatorio3D(escala=0.5)
    
    hermite2 = [curva_hermite(t, P7, T2, P8, T3) for t in np.linspace(0, 1, 50)]
    
    return np.vstack([bezier1, hermite1, bezier2, hermite2])

# Plotando em 3D
def plotar_circuito(pontos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(pontos[:, 0], pontos[:, 1], pontos[:, 2], '-o', markersize=3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()
    
circuito = gerar_circuito()
plotar_circuito(circuito)
