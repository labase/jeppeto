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

class TextBox(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.initFont()
        self.initImage()
        self.initGroup()
        self.setText(['a','b'])

    def initFont(self):
        pygame.font.init()
        self.font = pygame.font.Font(None,3)

    def initImage(self):
        self.image = pygame.Surface((200,80))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.top = 0 ; self.rect.left = 0
    def display_box(screen, message):
        "Print a message in a box in the middle of the screen"
        font = pygame.font.Font(None, 18)
        rect = pygame.Rect([0, 0, 220, 22])
        offset = (3, 3)
    
        center = screen.get_rect().center
        rect.center = center
    
        pygame.draw.rect(screen, (0, 0, 0), rect, 0)
        pygame.draw.rect(screen, (255,255,255), rect, 1)
    
        rect.left += offset[0]
        rect.top  += offset[1]
    
        if len(message) != 0:
            screen.blit(font.render(message, 1, (255,255,255)), rect.topleft)
        
        pygame.display.flip()
    
    def ask(screen, question):
        "ask(screen, question) -> answer"
        pygame.font.init()  
        text = ""
        display_box(screen, question + ": " + text)
    
        while True:
            pygame.time.wait(50)
            event = pygame.event.poll()
            
            if event.type == QUIT:
                sys.exit()	 
            if event.type != KEYDOWN:
              continue
              
            if event.key == K_BACKSPACE:
                text = text[0:-1]
            elif event.key == K_RETURN:
                break
            else:
                text += event.unicode.encode("ascii")
                
            display_box(screen, question + ": " + text)
            
        return text


    def setText(self,text):
        tmp = pygame.display.get_surface()
        x_pos = self.rect.left+5
        y_pos = self.rect.top+5

        for t in text:
            x = self.font.render(t,False,(0,0,0))
            tmp.blit(x,(x_pos,y_pos))
            x_pos += 10

            if (x_pos > self.image.get_width()-5):
                x_pos = self.rect.left+5
                y_pos += 10

    def initGroup(self):
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)
    
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
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
    def click(self, handler):
        self.click_listener.add((handler,self.collidepoint))
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
    def collidepoint(self,x,y):
        return True
    @classmethod
    def clear(self,buffer):
        print 'cl ',
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
    
class NullIcon(Menu):
    def __init__(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.create(source, x, y ,w , h, l , f, buff)
    def collidepoint(self,x,y):
        return False
    
class GUI:
    LY = Camada()
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.click_listeners = []
        self.do_up = self._do_up
        self.do_down = self._do_down #self._do_nothing
    
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
    def create_game(self,game,title):
        self.game = game
        pygame.display.set_caption(title)
        if android:
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

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
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                self.do_down(ev)
            elif ev.type == pygame.MOUSEBUTTONUP:
                self.do_up(ev)
    def _do_nothing(self, ev):
        pass
    def _do_down(self, ev):
        self.do_down = self._do_nothing
        self.last = self.tela.copy()
        self.do_up = self._do_up
    def _do_up(self, ev):
        self.do_up = self._do_nothing
        self.do_down = self._do_down
        #print ev.button, self.listeners
        if ev.button == 1:
            for item in self.click_listeners:
                print item.action
                if item.collide(*ev.pos):
                    print ev.pos
                    item.action(*ev.pos)
        
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
        Menu.MBUFF = self.buffer.copy()#self.last #self.tela.copy()
        return Menu()#source,x,y,w,h, l, f, buff)
    def click(self, object):
        self.click_listeners.append(object)
    def unclick(self, object):
        print 'removing'
        self.click_listeners.remove(object)
        self._redraw()
        self.tela.blit(self.buffer,(0,0))
        pygame.display.flip()
        
    
    def terminate(self):
        pygame.quit()
        #sys.exit()

