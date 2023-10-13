import pygame, random, math
from pygame import mixer


# Inicializar Pygame
pygame.init()

# Crear la Pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

# agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables del Jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8


for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables de la bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_funete_final = fuente_final.render("Juego Terminado", True, (255, 255, 255))
    pantalla.blit(mi_funete_final, (60, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Putaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))
    
# Funcion disparar bala
def dispara_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# Funcion detectar coliciones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta = True
while se_ejecuta:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar Eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar tecla 
        if evento.type == pygame.KEYDOWN: 
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
        
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = jugador_x
                    dispara_bala(bala_x, bala_y)
        
        # Evento soltar tecla 
        if evento.type == pygame.KEYUP: 
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # Mantener dentro del borde al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    
    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break


        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro del borde al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e] 

        # Colicion
        for bala in balas:

            colicion_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colicion_bala_enemigo:
                sonido_colision = mixer.Sound('golpe.mp3')
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                break
                
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)


    

    jugador(jugador_x, jugador_y)

    # Mostrar puntaje
    mostrar_puntaje(texto_x, texto_y)
    

    # Actualizar
    pygame.display.update()

