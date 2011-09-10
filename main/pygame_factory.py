#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/07/31  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/07/31 $Date$"

import pygame
import pygame as KL
from pygame.color import Color as CL
from pygame.sprite import Sprite
from pygame.sprite import LayeredUpdates as Renderer
from pygame.sprite import RenderUpdates as Camada

try:
    import android
except ImportError:
    android = None
from time import time

import zipfile
from io import BytesIO
ICONS = zipfile.ZipFile('/home/carlo/shine-icon-set.zip', 'r')
IMAGEREPO = 'image/'
# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 8
CANVASW, CANVASH = 800, 600
COLOR={'forest green':CL('#228B22') , 'navajo white':CL('#FFDFB0')}

class TECLA: 
    ACIMA=111
    ABAIXO=116
    DIREITA=114
    ESQUERDA=113

    BRANCO=65
    ENTER=36
    SOBE=112
    DESCE=117
    EMPURRA=97
    PUXA=103
    
class Empacotador(Sprite):
    EBUFF = None
    MESTRE = Renderer()
    IMAGES = {}
    def __init__(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.create(source, x, y ,w , h, l , f, buff)
    def create(self, source, x, y ,w , h, l = None, f= None, buff= None):
        Sprite.__init__(self)
        self.name = image = source
        if image not in Empacotador.IMAGES:
            if f:
                graphic = pygame.image.load(buff).convert()
            else:
                graphic = pygame.image.load("image/%s"%image).convert()
            Empacotador.IMAGES[image] = graphic
        else:
            graphic = Empacotador.IMAGES[image]
        graphic = pygame.transform.scale(graphic, (w, h))
        self.image = graphic
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        z = l or y
        self._add_buff(z)
    def _add_buff(self,z=None):
        Empacotador.MESTRE.add(self,layer = z)
    def remove(self):
        Empacotador.MESTRE.remove(self)
    def position(self):
        return self.rect.topleft
    def move(self,x,y):
        self.rect.topleft = (x,y)
    def pos(self):
        return self.rect.topleft
    def translate(self,x,y):
        ox, oy = self.rect.topleft
        self.rect.topleft = (ox+x,oy+y)
    def translatez(self,x,y):
        ox, oy = self.rect.topleft
        self.rect.topleft = (ox+x,oy+y)
        Empacotador.MESTRE.change_layer(self,oy+y)
    @classmethod
    def clear(self,buffer):
        Empacotador.MESTRE.clear(buffer, Empacotador.EBUFF)
        return Empacotador.MESTRE.draw(buffer)
    @classmethod
    def init(self):
        buff = pygame.Surface([CANVASW, CANVASH])
        buff.fill(COLOR['forest green']) #(COLOR['navajo white'])
        Empacotador.EBUFF = buff.convert()

    def __eq__(self,other): return self.name == other.name

class Menu(Empacotador):
    BUFFER = Camada()
    MBUFF = None
    def __init__(self):
        self.create_menu()
    def create_menu(self):
        self.names = [x for x in ICONS.namelist() if ('16' in x) and ('.png' in x)]
        for ind, name in enumerate(self.names):
            f = ICONS.open(name).read()
            contents = BytesIO(f)
            x, y = 10+(ind // 20) * 20, 10+(ind % 20) * 20
            Icon(name, x, y,16, 16, f='png', buff=contents)
    def _add_buff(self,z=None):
        Menu.BUFFER.add(self)
    def remove(self, x=10, y=10):
        for icon in Menu.BUFFER :
            Menu.BUFFER.remove(icon)
        index = ((x-10)//20) *20 + (y-10)//20
        name = self.names[index]
        name = name.replace('16x16','128x128')
        f = ICONS.open(name).read()
        print name
        return (name,BytesIO(f))
    def translatez(self,x,y):
        self.translate(x,y)
    @classmethod
    def clear(self,buffer):
        Menu.BUFFER.clear(buffer, Menu.MBUFF)
        return Menu.BUFFER.draw(buffer)
    @classmethod
    def init(self):
        buff = pygame.Surface([CANVASW, CANVASH])
        buff.fill(COLOR['forest green']) #(COLOR['navajo white'])
        Menu.MBUFF = buff.convert()

class Icon(Menu):
    def __init__(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.create(source, x, y ,w , h, l , f, buff)
    
class GUI:
    LY = Camada()
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.listeners = []
        self.layers = Empacotador
    
        # Set the screen size.
        self.tela = pygame.display.set_mode((CANVASW, CANVASH))
        self.tela.fill(COLOR['forest green'])
        Empacotador.init()
        Menu.init()
        # Use a timer to control FPS.
        pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

        self.buffer = pygame.Surface([CANVASW, CANVASH])
        self.buffer.fill(COLOR['forest green']) #(COLOR['navajo white'])
        self.buffer = self.buffer.convert()
        self.LIDADOR = {KL.K_DOWN: self.Down,KL.K_END: self.End,
                   KL.K_RETURN: self.Return, KL.K_HOME: self.Home,
                   KL.K_LEFT: self.Left,KL.K_PAGEDOWN: self.Next,
                   KL.K_PAGEUP: self.Prior,KL.K_RIGHT: self.Right,
                   KL.K_UP: self.Up, ' ':self.space}

    def create_game(self,game,title):
        self.game = game
        pygame.display.set_caption(title)
        if android:
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
            android.map_key(66, KL.K_PAGEUP)
            android.map_key(67, KL.K_PAGEDOWN)
            android.map_key(23, KL.K_HOME)
            self.text(150,50,'android: %d  escape: %d'%(
                android.KEYCODE_BACK, pygame.K_ESCAPE))
 

        while True:
            ev = pygame.event.wait()
            #self._redraw()
            if android:
                if android.check_pause():
                    android.wait_for_resume()

            if ev.type == TIMEREVENT:
                self._redraw()
                self.tela.blit(self.buffer,(0,0))
                pygame.display.flip()
            elif ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_ESCAPE,'q',4):
                    self.terminate()
                    break
                else:
                    self.lidador_de_tecla(ev.key)
                    pygame.display.flip()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                print ev.button, self.listeners
                if ev.button == 1:
                    for object in self.listeners:
                        object.click(*ev.pos)
    def _redraw(self):
        rectlist = Empacotador.clear(self.buffer)
        rectlist += Menu.clear(self.buffer)
        pygame.display.update(rectlist)

    def text(self,x,y,texto,color='navajo white'):
        label = self.font.render(texto, 1, COLOR[color])
        self.buffer.blit(label, (x,y))
        return label
    def rect(self,x,y,w,h,color='navajo white'):
        obj = pygame.draw.rect(self.buffer, COLOR[color], (x,y,w,h))
        return obj

    def image(self,source,x,y,w,h, l=None, f=None, buff= None):
        return Empacotador(source,x,y,w,h, l, f, buff)
    def icon(self):#,source,x,y,w,h, l=None, f=None, buff= None):
        #menu = Menu(source,x,y,w,h, l, f, buff)
        Menu.MBUFF = self.tela.copy()
        return Menu()#source,x,y,w,h, l, f, buff)
    def add_listener(self, evento):
        self.listeners.append(evento)
    def remove_listener(self, evento):
        self.listeners.remove(evento)
    def lidador_de_tecla(self, evento):
        if evento in self.LIDADOR:
            self.LIDADOR[evento](evento)
            return False
        return True
    def Return(self, ev): self.game.quandoApertaUmaTecla(TECLA.ENTER);return False
    def space(self, ev): self.game.quandoApertaUmaTecla(TECLA.BRANCO);return False
    def Right(self, ev): self.game.track.forward();return False
    def Left(self, ev): self.game.track.backward();return False
    def Up(self, ev): self.game.track.popback();return False
    def Down(self, ev): self.game.track.popfront();return False
    def Next(self, ev): self.game.quandoApertaUmaTecla(TECLA.DESCE);return False
    def Prior(self, ev): self.game.quandoApertaUmaTecla(TECLA.SOBE);return False
    def Home(self, ev): self.game.quandoApertaUmaTecla(TECLA.EMPURRA);return False
    def End(self, ev): self.game.quandoApertaUmaTecla(TECLA.PUXA);return False
    
    def terminate(self):
        pygame.quit()
        #sys.exit()


def main():
    from train import Trains
    trains = Trains()
    trains.init(GUI())
    
if __name__ == "__main__":
    main()

