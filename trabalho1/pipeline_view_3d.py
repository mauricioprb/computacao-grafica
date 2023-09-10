# Bernardo e Mauricio
import numpy as np
import math
import matplotlib.pyplot as plt

# Limites da window
xminw = -1
yminw = -1
xmaxw = 1
ymaxw = 1

# Limites da viewport
xminv = 0
yminv = 0
xmaxv = 500
ymaxv = 500

def mostraPontos(*pontos):
    for ponto in pontos:
        print(ponto)

def desenhaLinha(p1, p2):
    x_values = [p1[0], p2[0]]
    y_values = [p1[1], p2[1]]
    plt.plot(x_values, y_values, 'bo-', linestyle="--")

# Modelo - Tetraedro
p1 = np.array([0,0,0, 1.0])
p2 = np.array([0,1,0, 1.0])
p3 = np.around(np.array([math.sqrt(3)/2, 0.5, 0, 1.0]), 1)
p4 = np.around(np.array([0.5, 0.5, math.sqrt(2/3), 1.0]), 1)

print("\nCoordenadas do modelo")
mostraPontos(p1, p2, p3, p4)

matrizModelo = np.identity(4)

matrizVisualizacao = np.identity(4)

matrizProjecao = np.identity(4)

def atualizaMundo():
    global p1, p2, p3, p4, matrizModelo
    p1u = matrizModelo.dot(p1)
    p2u = matrizModelo.dot(p2)
    p3u = matrizModelo.dot(p3)
    p4u = matrizModelo.dot(p4)
    return p1u, p2u, p3u, p4u

def atualizaVisualizacao(p1u, p2u, p3u, p4u):
    global matrizVisualizacao
    p1v = matrizVisualizacao.dot(p1u)
    p2v = matrizVisualizacao.dot(p2u)
    p3v = matrizVisualizacao.dot(p3u)
    p4v = matrizVisualizacao.dot(p4u)
    return p1v, p2v, p3v, p4v

def atualizaProjecao(p1v, p2v, p3v, p4v):
    global matrizProjecao
    p1p = matrizProjecao.dot(p1v)
    p2p = matrizProjecao.dot(p2v)
    p3p = matrizProjecao.dot(p3v)
    p4p = matrizProjecao.dot(p4v)

    # Homogeneização
    p1p = p1p / p1p[3]
    p2p = p2p / p2p[3]
    p3p = p3p / p3p[3]
    p4p = p4p / p4p[3]

    return p1p, p2p, p3p, p4p

def mapeamento(p1p, p2p, p3p, p4p):
    global xminw, yminw, xmaxw, ymaxw, xminv, yminv, xmaxv, ymaxv
    def map_point(p):
        x = (((p[0] - xminw) * (xmaxv - xminv)) / (xmaxw - xminw)) + xminv
        y = (((p[1] - yminw) * (ymaxv - yminv)) / (ymaxw - yminw)) + yminv
        return [x, y]

    p1m = map_point(p1p)
    p2m = map_point(p2p)
    p3m = map_point(p3p)
    p4m = map_point(p4p)

    return p1m, p2m, p3m, p4m

def translation(dx, dy, dz):
    global matrizModelo
    T = np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])
    matrizModelo = T.dot(matrizModelo)

def scale(sx, sy, sz):
    global matrizModelo
    S = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])
    matrizModelo = S.dot(matrizModelo)

def rotação_x(angulo):
    global matrizModelo
    rad = np.radians(angulo)
    R = np.array([
        [1, 0, 0, 0],
        [0, np.cos(rad), -np.sin(rad), 0],
        [0, np.sin(rad), np.cos(rad), 0],
        [0, 0, 0, 1]
    ])
    matrizModelo = R.dot(matrizModelo)

def rotação_y(angulo):
    global matrizModelo
    rad = np.radians(angulo)
    R = np.array([
        [np.cos(rad), 0, np.sin(rad), 0],
        [0, 1, 0, 0],
        [-np.sin(rad), 0, np.cos(rad), 0],
        [0, 0, 0, 1]
    ])
    matrizModelo = R.dot(matrizModelo)

def rotação_z(angulo):
    global matrizModelo
    rad = np.radians(angulo)
    R = np.array([
        [np.cos(rad), -np.sin(rad), 0, 0],
        [np.sin(rad), np.cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    matrizModelo = R.dot(matrizModelo)

def main():
    global p1, p2, p3, p4

    while True:
        opcao = int(input("\nSelecione uma transformação:\n1. Translação\n2. Escala\n3. Rotação\n4. Sair\nOpção: "))

        if opcao == 1:
            dx = float(input("Informe o deslocamento em x: "))
            dy = float(input("Informe o deslocamento em y: "))
            dz = float(input("Informe o deslocamento em z: "))
            translation(dx, dy, dz)

        elif opcao == 2:
            sx = float(input("Informe a escala em x: "))
            sy = float(input("Informe a escala em y: "))
            sz = float(input("Informe a escala em z: "))
            scale(sx, sy, sz)

        elif opcao == 3:
            sub_opcao = int(input("Escolha o eixo para rotação:\n1. X\n2. Y\n3. Z\nOpção: "))
            angulo = float(input("Informe o ângulo (graus): "))
            if sub_opcao == 1:
                rotação_x(angulo)
            elif sub_opcao == 2:
                rotação_y(angulo)
            elif sub_opcao == 3:
                rotação_z(angulo)

        elif opcao == 4:
            break

        # Atualiza Mundo, Visualização e Projeção
        p1u, p2u, p3u, p4u = atualizaMundo()
        p1v, p2v, p3v, p4v = atualizaVisualizacao(p1u, p2u, p3u, p4u)
        p1p, p2p, p3p, p4p = atualizaProjecao(p1v, p2v, p3v, p4v)

        # Mapeamento
        p1m, p2m, p3m, p4m = mapeamento(p1p, p2p, p3p, p4p)

        # Plot
        plt.figure(figsize=(6,6))
        desenhaLinha(p1m, p2m)
        desenhaLinha(p1m, p3m)
        desenhaLinha(p2m, p3m)
        desenhaLinha(p1m, p4m)
        desenhaLinha(p2m, p4m)
        desenhaLinha(p3m, p4m)
        plt.xlim(0, 500)
        plt.ylim(0, 500)
        plt.show()
        
        plt.close()  # Fecha a janela de plotagem atual após mostrar a figura

main()