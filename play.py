import pygame
import random
import math
from pygame import mixer

#Inicialiazar Pygame
pygame.init()
#Crear Pantalla
pantalla = pygame.display.set_mode((800, 600))

#Entorno Grafico de Juego
pygame.display.set_caption('Invasion Espacial')
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("galaxy.jpg")
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)
blanco = (250,250,250)
#Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#Game Over
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

#Jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0

#Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigo = 8

for i in range(cantidad_enemigo):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(0,200))
    if puntaje % 10 == 0:
        multiplicar = 1
        vel = 0.5
        multiplicar /= vel
        enemigo_x_cambio.append(multiplicar)
    enemigo_y_cambio.append(50)

#Bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_y_cambio = 3
bala_visible = False

#Funcion Game Over
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO FINALIZADO", True, blanco)
    pantalla.blit(mi_fuente_final, (60, 200))

#Funcion Puntaje
def Mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, blanco)
    pantalla.blit(texto, (x, y))

#Funcion Jugador
def Jugador(x, y):
    pantalla.blit(img_jugador,(x, y))

#Funcion Enemigo
def Enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene],(x, y))

#Funcion Bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y+16))

#Funcion de Colision
def hay_colision (x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 35:
        return True
    else:
        return False


#Loop del juego
ejecuta = True
while ejecuta:
    #Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    #Eventos Teclado
    for event in pygame.event.get():
        #Evento cerrar
        if event.type == pygame.QUIT:
            ejecuta = False

        #EventoPresiono una tecla
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)

        #Evento Solto Tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Modificar ubicacion
    jugador_x += jugador_x_cambio
    #Mantener dentro del borde al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    # Modificar ubicacion
    for e in range(cantidad_enemigo):
        if enemigo_y[e] > 500:
            for k in range (cantidad_enemigo):
                enemigo_y[k] = 1000
            texto_final()
        enemigo_x[e] += enemigo_x_cambio[e]
    #Mantener dentro de los bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        #Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        Enemigo(enemigo_x[e], enemigo_y[e], e)
    #Movimiento Bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    #Definir la funcion de Jugador
    Jugador(jugador_x, jugador_y)
    Mostrar_puntaje(texto_x, texto_y)
    #Actulizar pantalla
    pygame.display.update()