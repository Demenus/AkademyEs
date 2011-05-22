# -*- coding: utf-8 -*-

""" Copyright (C) 2011  Aarón Negrín Santamaría

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

#Importamos las nuevas librerias
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

#Definimos el ancho y largo de nuestra ventana
WIDTH = 600
HEIGHT = 600

faceIndex = (GLushort * 4)(0, 1, 2, 3)

def init():
    #inicializamos pygame
    pygame.init()

    #creamos una pantalla de WIDTHxHEIGHT pixeles que use doblebuffer,
    #que se pueda redimensionar y que acepte opengl
    flags = DOUBLEBUF|OPENGL|RESIZABLE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)


def init_gl():
    #Cada vez que se dibuja la escena esta se borra enteramente
    #glClearColor y ClearDepth definen el color y la profundidad
    #del borrado
    glClearColor(0.0,0.0,0.0,1.0); 
    glClearDepth(1.0);

def resize_glscene(w,h):
    #Especifica el tamaño de la ventana para OPENGL
    #Aunque la ventana física tenga ciertas dimensiones
    #podemos hacer que las de OpenGL no coincidan con
    #estas.
    glViewport(0,0,w,h);

    #Se establece la matriz de proyeccion como la identidad
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(45.0, float(w)/float(h), 0.1, 100.0);

    #Se establece la matriz de modelado como la identidad
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
 
#vértices del cuadrado a dibujar
#expresados como un array de C   
vertices = (GLfloat * (4*4))(
    1.0, 1.0, 0.0, 1.0,
    1.0,-1.0, 0.0, 1.0,

    -1.0,-1.0, 0.0, 1.0,
    -1.0, 1.0, 0.0, 1.0)


def draw_scene():
    #Limpiamos la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    #Colocamos la matriz identidad
    glLoadIdentity();
    #Movemos en el eje Z (profundidad) 6 puntos hacia atras
    glTranslatef(0.0, 0.0, -6.0);

    #Pasa a OpenGL los datos almacenados en vertices y le asignamos
    #el identificador 0
    glVertexAttribPointer(0, 4, GL_FLOAT, 1, 0, vertices);
    #Activamos este atributo con identificador 0
    glEnableVertexAttribArray(0);

    #Dibujamos, usando cuadrados, los vertices en el orden 0,1,2,3
    glDrawElements(GL_QUADS, len(faceIndex), GL_UNSIGNED_SHORT, faceIndex);

    #Desactivamos este atributo
    glDisableVertexAttribArray(0);


def load_Shaders(vsFileName, fsFileName):
    #creamos un identificador del programa
    program = glCreateProgram();

    #leemos el contenido de los ficheros
    vsSource = open(vsFileName, 'r').read()
    fsSource = open(fsFileName, 'r').read()

    #creamos unos identificadores de los shaders y les
    #asociamos su codigo
    vsShader = glCreateShader(GL_VERTEX_SHADER);   #Vertex Shader
    glShaderSource(vsShader, vsSource);

    fsShader = glCreateShader(GL_FRAGMENT_SHADER); #Fragment Shader
    glShaderSource(fsShader, fsSource);

    #Compilamos los shaders
    glCompileShader(vsShader);
    glCompileShader(fsShader);

    #Adjuntamos los shaders al programa
    glAttachShader(program, vsShader);
    glAttachShader(program, fsShader);
    
    #Enlazamos el programa
    glLinkProgram(program);

    return program



#Metodo main
def main():
    running = True
    init()
    init_gl()
    resize_glscene(WIDTH, HEIGHT)

    program = load_Shaders("Shader.vsh", "Shader.fsh")
    glUseProgram(program);


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        draw_scene()

        pygame.display.flip()

    pygame.quit()


#Llamamos al metodo main
main()
	
