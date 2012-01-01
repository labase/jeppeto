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
import logging

logger = logging.getLogger('myapp')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.CRITICAL)


try:
    import android
    android.init()
except ImportError:
    android = None
from time import time
'''
import zipfile
from io import BytesIO
ICONS = zipfile.ZipFile('/home/carlo/shine-icon-set.zip', 'r')
IMAGEREPO = 'image/'
'''
# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 8
CANVASW, CANVASH = 800, 480
COLOR={'forest green':'#228B22' , 'navajo white':'#FFDFB0', 'white':'#FFFFFF'
        ,'darksalmon':'#E9967A', 'peachpuff':'#FFDAB9', 'maroon':'#800000'
        ,'lightsalmon':'#FFA07A', 'saddlebrown':'#8B4513'
        ,'darkbrown':'#462813','linen':'#FAF0E6'}

COLOR = dict((name,CL(color))for name, color in COLOR.items())

class HandleEvent(dict):
    def __init__(self,gui):
        self.gui = gui
        self.update(
            {pygame.QUIT	     : self.QUIT,
            pygame.ACTIVEEVENT	     : self.ACTIVEEVENT,
            pygame.KEYDOWN	     : self.KEYDOWN,
            pygame.KEYUP	     : self.KEYUP,
            pygame.MOUSEMOTION	     : self.MOUSEMOTION,
            pygame.MOUSEBUTTONUP    : self.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN  : self.MOUSEBUTTONDOWN,
            pygame.JOYAXISMOTION    : self.JOYAXISMOTION,
            pygame.JOYBALLMOTION    : self.JOYBALLMOTION,
            pygame.JOYHATMOTION     : self.JOYHATMOTION,
            pygame.JOYBUTTONUP      : self.JOYBUTTONUP,
            pygame.JOYBUTTONDOWN    : self.JOYBUTTONDOWN,
            pygame.VIDEORESIZE      : self.VIDEORESIZE,
            pygame.VIDEOEXPOSE      : self.VIDEOEXPOSE,
            pygame.USEREVENT        : self.USEREVENT
            }
        )
    def QUIT(self, event): 
        self.gui.terminate()
        return True
    def ACTIVEEVENT(self, event): pass
    def KEYDOWN(self, event):
        if event.key in (pygame.K_ESCAPE,'q',4):
            self.gui.terminate()
            return True
    def KEYUP(self, event): pass
    def MOUSEMOTION(self, event):
        self.gui.do_drag(event)
    def MOUSEBUTTONUP(self, event):
        self.gui.do_up(event)
    def MOUSEBUTTONDOWN(self, event):
        self.gui.do_down(event)
    def JOYAXISMOTION(self, event): pass
    def JOYBALLMOTION(self, event): pass
    def JOYHATMOTION(self, event): pass
    def JOYBUTTONUP(self, event): pass
    def JOYBUTTONDOWN(self, event): pass
    def VIDEORESIZE(self, event): pass
    def VIDEOEXPOSE(self, event): pass
    def USEREVENT(self, event):
        self.gui._redraw()
    def loop(self):
        while True:
            event = pygame.event.wait()
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            if self[event.type](event): break

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
    def __init__(self, source, x, y ,w , h, l = None, f= None, buff= None, cl='#FFFFFF'):
        self.create(source, x, y ,w , h, l , f, buff, cl)
    def create(self, source, x, y ,w , h, l = None, f= None, buff= None, cl= None):
        Sprite.__init__(self)
        self.name = image = source
        if image:
            if image not in Empacotador.IMAGES:
                if f:
                    graphic = pygame.image.load(buff).convert()
                else:
                    graphic = pygame.image.load("image/%s"%image).convert()
                Empacotador.IMAGES[image] = graphic
            else:
                graphic = Empacotador.IMAGES[image]
            graphic = pygame.transform.scale(graphic, (w, h))
        else:
            graphic = pygame.Surface([w, h])
            graphic.fill(CL(cl))
        self.image, self.color = graphic, cl
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.z = l or y
        self._add_buff(self.z)
    def _add_buff(self,z=None):
        Empacotador.MESTRE.add(self,layer = z)
    def remove(self):
        self.translate(-1000,-1000)
        #Empacotador.MESTRE.remove_internal(self)
        #Empacotador.MESTRE.remove(self)
        #Empacotador.MESTRE.remove_sprites_of_layer(self.z)
    def position(self):
        return self.rect.topleft
    def move(self,x,y):
        self.rect.topleft = (x,y)
    def pos(self):
        return self.rect.topleft
    def scale(self,w,h):
        tl = self.rect.topleft
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = tl
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
        buff.fill(COLOR['navajo white']) #(COLOR['forest green'])
        Empacotador.EBUFF = buff.convert()

    def __eq__(self,other): return self.name == other.name

class GUI:
    LY = Camada()
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.click_listeners = []
        self.drag_listeners = []
        self.drop_listeners = []
        self.do_up = self._do_up
        self.do_down = self._do_down #self._do_nothing
        self.do_drag = self._do_nothing
    
        # Set the screen size.
        self.tela = pygame.display.set_mode((CANVASW, CANVASH))
        #self.tela.fill(COLOR['forest green'])
        Empacotador.init()
        #Menu.init()
        # Use a timer to control FPS.
        pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

        self.buffer = pygame.Surface([CANVASW, CANVASH])
        self.buffer.fill(COLOR['navajo white']) #(COLOR['forest green'])
        self.buffer = self.buffer.convert()
    def create_game(self,game,title):
        self.game = game
        pygame.display.set_caption(title)
        if android:
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        HandleEvent(self).loop()
    def _do_nothing(self, ev):
        pass
    def _do_drag(self, ev):
        #self.do_down = self._do_nothing
        self.last = self.tela.copy()
        self.mover.action(*ev.pos)
        self.do_up = self._do_drop
        #self._redraw()
    def _do_move(self, ev):
        self.mover.action(*ev.pos)
    def action(self, ev):
        pass
    def _do_drop(self, ev):
        logger.info("end moving: %d , %d", *ev.pos)
        self.do_up = self.do_drag = self.do_drop = self._do_nothing
        if ev.button == 1:
            for item in self.drop_listeners:
                print item.action
                if item.collide(*ev.pos):
                    par = ( ev.pos[0], ev.pos[1], self.mover.object )
                    print 'drop collision ', ev.pos
                    if item.action(*par ): break
        self.mover.stop( ev.pos[0], ev.pos[1], self.mover.object)
        self.mover = self
        self.do_down = self._do_down
    def _do_down(self, ev):
        self.do_down = self._do_nothing
        self.last = self.tela.copy()
        self.do_up = self._do_up
        self.item = lambda: None
        if ev.button == 1:
            for item in self.click_listeners:
                #logger.info( item.action)
                if item.collide(*ev.pos):
                    #logger.info( ev.pos)
                    if item.start(*ev.pos):
                        self.item = lambda: item.action(*ev.pos)
                        for drag_item in self.drag_listeners:
                            if drag_item.object is item.object:
                                self.do_drag = self._do_drag
                                drag_item.start(*ev.pos)
                                logger.info("to drag: %d , %d", *ev.pos)
                                self.mover = drag_item
                                self.do_move = self._do_move
                                break
                        break
    def _do_up(self, ev):
        self.do_up = self.do_drag = self.do_drop = self._do_nothing
        self.do_down = self._do_down
        self.mover = self
        #print ev.button, self.listeners
        self.item()
        
    def _redraw(self):
        rectlist = Empacotador.clear(self.buffer)
        #rectlist += Menu.clear(self.buffer)
        pygame.display.update(rectlist)
        self.tela.blit(self.buffer,(0,0))
        pygame.display.flip()

    def text(self,x,y,texto,color='navajo white', hexcolor=None):
        label = self.font.render(texto, 1,  hexcolor and CL(hexcolor) or COLOR[color])
        self.buffer.blit(label, (x,y))
        return label
    def rect(self,x,y,w,h,color='navajo white', hexcolor=None, buff=None):
        obj = pygame.draw.rect(buff or self.buffer, hexcolor and CL(hexcolor) or COLOR[color], (x,y,w,h))
        return obj

    def image(self,source,x,y,w,h, l=None, f=None, buff= None, cl= None):
        return Empacotador(source,x,y,w,h, l, f, buff, cl)
    def icon(self):#,source,x,y,w,h, l=None, f=None, buff= None):
        #menu = Menu(source,x,y,w,h, l, f, buff)
        Menu.MBUFF = self.buffer.copy()#self.last #self.tela.copy()
        return Menu()#source,x,y,w,h, l, f, buff)
    def dragg(self, object):
        self.drag_listeners.insert(0,object)
        logger.info("to drag listeners: %s", str(object))
    def drop(self, object):
        self.drop_listeners.insert(0,object)
        logger.info("to drop listeners: %s", str(object))
    def click(self, object):
        self.click_listeners.insert(0,object)
    def unclick(self, object):
        print 'removing clicker'
        [self.click_listeners.remove(obj)
         for obj in self.click_listeners if object is obj.object]
        self._redraw()
        self.tela.blit(self.buffer,(0,0))
        pygame.display.flip()
        
    def undrop(self, object):
        print 'removing dropper'
        [self.drop_listeners.remove(obj)
         for obj in self.drop_listeners if object is obj.object]
        self._redraw()
        self.tela.blit(self.buffer,(0,0))
        pygame.display.flip()
    def undrag(self, object):
        print 'removing dragger'
        [self.drag_listeners.remove(obj)
         for obj in self.drag_listeners if object is obj.object]
        self._redraw()
        self.tela.blit(self.buffer,(0,0))
        pygame.display.flip()
        
    
    def terminate(self):
        pygame.quit()
        #sys.exit()


