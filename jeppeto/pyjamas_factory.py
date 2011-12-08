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

#import zipfile
from pyjamas.ui.RootPanel   import RootPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui import KeyboardListener as KL
from __pyjamas__ import JS
from pyjamas.raphael.raphael import Raphael,DOCK_CONNECTION
from pyjamas.JSONParser import JSONParser
from pyjamas.Window import alert
from pyjamas import DOM

IMAGEREPO = ''
CANVASW, CANVASH = 800, 600
IMAGEREPO = '/static/imagens/'
IMAGEREPO = 'imagens/'
COLOR={'forest green':'#228B22' , 'navajo white':'#FFDFB0', 'white':'#FFFFFF'
        ,'darksalmon':'#E9967A', 'peachpuff':'#FFDAB9', 'maroon':'#800000'
        ,'lightsalmon':'#FFA07A', 'saddlebrown':'#8B4513'
        ,'darkbrown':'#462813','linen':'#FAF0E6'}

class FakeJSON:
    def encode(self,astring):
        st = str(astring)
        return st.replace("'",'"')
    def decode(self,astring):
        jparser = JSONParser()
        return jparser.decode(astring)
        #anobj = None
        #JS("""
        #    anobj = JSON.parse(astring);
        # """)
        #return anobj
    def wdecode(self,astring):
        anobj = None
        JS("""
            anobj = unescape(astring);
         """)
        nastring = '''
[ { "body" : "escreva",
    "line" : 1
  },
  { "body" : "aqui",
    "line" : 2
  }
]'''
        #JS("""
        #    anobj = JSON.parse(astring);
        # """)
        #return anobj
        astring = anobj.replace("'",'"')
        jparser = JSONParser()
        return jparser.decode(astring) #anobj
        
j_p = FakeJSON()
        
def dpx(d):
    return '%spx'%d
def fkj(j):
    st = str(j)
    return st.replace("'",'"')
    return st
class EventWrapper:
    def __init__(self,action,offset):
        self._action= action
        self.ox, self.oy = offset
        #alert('init %s %s'%offset)
    def action(self,element,event):
        x = DOM.eventGetClientX(event) - self.ox
        y = DOM.eventGetClientY(event) - self.oy
        DOM.eventCancelBubble(event,True)
        DOM.eventPreventDefault(event)
        #alert('clic %s %s'%(x,y))
        self._action(x,y)

class DragWrapper:
    def __init__(self,dropper,object,offset):
        self._object = object
        self._action= object.action
        self._start= object.start
        self._stop= object.stop
        self._dropper= dropper
    def action(self,obj,*args):
        self._action(*args)
    def start(self,obj,*args):
        self._start(*args)
    def stop(self,obj):#,*args):
        self._dropper(self._object)
        self._stop()
class Text_Area(TextArea):
    def __init__(self, panel,  text ='', left=0, top=0, width=0 , height=0, 
                 color = None, background = None, click = None, focus = None):
        TextArea.__init__(self)#, text=text)
        self.panel = panel
        
        attrs = dict (position = 'absolute', left=dpx(left), top=dpx(top) ,
                      width=dpx(width) , height=dpx(height),
                      color = color, background = background)
        for key in attrs:
            if not attrs[key]: del(attrs[key])
        #self.setName(source)
        self.setText(text)
        self.setStyleAttribute(attrs)
        #self.setStyleAttribute({'position':'absolute',
        #    'top':'175px','left':'158px'
        #    ,'color':COLOR['maroon']
        #    ,'background':COLOR['peachpuff']
        #    ,'background-color':COLOR['peachpuff']})
        #self.setSize(width,height)
        #self.setReadonly('readonly')
        if click :
            self.addClickListener(click)
        if focus :
            self.addFocusListener(focus)
        self.panel.add(self)
        #t =TextArea()
        #t.addFocusListener()
        #t.
        

class Empacotador:
    IMAGES = {}
    CAMADA = {}
    Z=10
    def __init__(self, canvas, source=None, x=0, y=0 ,w=0 , h=0, l = None, f= None, buff= None):
        self.canvas = canvas
        self._create(source, x, y ,w , h, l , f, buff)
    def _create(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.name = image = source
        graphic = self.canvas.image(IMAGEREPO+source,x,y,w,h)
        #if image not in Empacotador.IMAGES:
        #    graphic = self.canvas.image(source,x,y,w,h)
        #    Empacotador.IMAGES[image] = graphic
        #else:
        #    graphic = Empacotador.IMAGES[image]
        self.image = self.avatar = graphic
        self.image.avatar = graphic
        self.rect = self.image.getBBox()
        self.camada = z = l or y
        if z > 0:
            self.add(self.camada)
            self.reorder()
    def drag(self, action,start,stop):
        self.image.drag(action,start,stop)
    def addListener(self, typpe,wrapper):
        self.image.addListener(typpe,wrapper)

    def add(self, camada):
        if camada not in Empacotador.CAMADA:
            Empacotador.CAMADA[camada] = [self]
        else:
            Empacotador.CAMADA[camada].append(self)
        
        
    def reorder(self):
        cmd = Empacotador.CAMADA
        NOUSE = [img.image.toFront() for it in sorted(cmd.keys())
                 for img in cmd[it]]
    def remove(self):
        
        if self.camada in Empacotador.CAMADA and \
            self in Empacotador.CAMADA[self.camada]:
            Empacotador.CAMADA[self.camada].remove(self)
        #self.image.remove()
        self.image.toBack()
    def position(self):
        return self.image.getBBox()['x'], self.image.getBBox()['y']
    def posX(self):
        return self.image.getBBox()['x']
    def posY(self):
        return self.image.getBBox()['y']
    def deltaX(self):
        return self.image.getBBox()['width']
    def deltaY(self):
        return self.image.getBBox()['height']
    def collidepoint(self,x,y):
        i, j = self.posX(),self.posY()
        w, h = self.deltaX(),self.deltaY()
        #alert('collidepoint %s < %s < %s  &  %s < %s < %s'%(i,x,i+w,j,y,j+w))
        return (i < x < (i + w)) and (j < y < (j + w))
    def move(self,x,y):
        ox, oy = self.position()
        self.image.translate(x-ox,y-oy)
    def pos(self):
        return self.image.getBBox()['x'], self.image.getBBox()['y']
    def translate(self,x,y):
        self.image.translate(x,y)
    def translatez(self,x,y):
        self.image.translate(x,y)
        ox, oy = self.pos()
        Empacotador.CAMADA[self.camada].remove(self)
        self.camada = oy
        self.add(oy)
        self.reorder()
    def __eq__(self,other):
        self.canvas.text(50,Empacotador.Z,'%s = %s'%(self.name,other.name))
        Empacotador.Z+=10
        return self.name == other.name


class Slate(Empacotador):
    def _create(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.name = image = source
        self.image = self.rect(0,0,w,h)
        z = l or y
        self._add_buff(z)
    def rect(self,x,y,dx,dy,color):
        r = self.canvas.rect(x,y,dx-x,dy-y)
        r.setAttrs({'fill':COLOR[color],'stroke':COLOR[color]})
        return r

class Menu(Empacotador):
    BUFFER = []
    MBUFF = None
    def _create(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.names = [x for x in NAMES.split('\n') if ('16' in x) and ('.jpg' in x)]
        #alert(str(self.names))
        self.avatar = self
        for ind, name in enumerate(self.names):
            x, y = 10+(ind // 20) * 20, 10+(ind % 20) * 20
            img = self.canvas.image(name,x,y,16,16)
            img.addListener('click',self.activate)
            self._add_buff(img)
            #Icon(self.canvas,name, x, y,16, 16)
    def activate(self, obj, ev):
        self._action(obj,ev)
    def addListener(self,typpe,action):
        self._action = action
    def _add_buff(self,z=None):
        Menu.BUFFER.append(z)
    def remove(self, x=10, y=10):
        #Menu.clear()
        while Menu.BUFFER : Menu.BUFFER.pop().remove()
        index = ((x-10)//20) *20 + (y-10)//20
        name = self.names[index]
        name = name.replace('16x16','128x128')
        names = [name,name]
        return name
    def translatez(self,x,y):
        self.translate(x,y)
    def collidepoint(self,x,y):
        return True
    @classmethod
    def clear(self,buffer):
        while Menu.BUFFER : Menu.BUFFER.pop().remove()
    @classmethod
    def init(self):
        pass

class Flyer(Menu):
    def _create(self, source, x, y ,w=16 , h=16, l = None, f= None, buff= None):
        print 'flyer names', source
        self.name = source
        #f = ICONS.open(source).read()
        #buff = BytesIO(f)
        #x, y = 10+(ind // 20) * 20, 10+(ind % 20) * 20
        Empacotador._create(self,source, x, y ,w, h, l , f, buff)
    def remove(self, x=10, y=10):
        Menu.clear()
        name = name.replace('128x128','16x16')
        f = ICONS.open(name).read()
        print name
        return (name,BytesIO(f))

class Icon(Menu):
    pass
    def _create(self, source, x, y ,w , h, l = None, f= None, buff= None):
        Empacotador._create(self,source, x, y ,w , h, l , f, buff)
    
class NullIcon(Menu):
    def __init__(self, source, x, y ,w , h, l = None, f= None, buff= None):
        self.create(source, x, y ,w , h, l , f, buff)
    def collidepoint(self,x,y):
        return False

class GUI_Event:
#    LY = Camada()
    def __init__(self):
        '''
        self.click_listeners = []
        self.drag_listeners = []
        self.roll_listeners = []
        self.act_listeners = []
        '''
        self.drop_listeners = []
        self.do_up = self._do_up
        self.do_move = self._do_nothing
        self.do_down = self._do_down #self._do_nothing
    

    def _do_nothing(self, ev, noev= None):
        pass
    def _do_move(self, ev):
        print 'moving ',ev.pos
        self.mover.action(*ev.pos)
    def _do_end_drag(self, ev):
        print 'end moving ',ev.pos
        self.do_up = self.do_move = self._do_nothing
        self.do_down = self._do_down
        if ev.button == 1:
            for item in self.drop_listeners:
                print item.action
                if item.collide(*ev.pos):
                    par = ( ev.pos[0], ev.pos[1], self.mover )
                    print 'drop collision ', ev.pos
                    if item.action(*par ): break
    def do_roll(self, ev):
       if True: #ev.button == 1:
            for item in self.roll_listeners:
                item.action(*ev.pos)
    def do_act(self, ev):
       if True: #ev.button == 1:
            for item in self.act_listeners:
                item.action(ev)
    def _do_down(self, ev):
        self.do_down = self._do_nothing
        if ev.button == 1:
            for item in self.drag_listeners:
                print item.action
                if item.collide(*ev.pos):
                    print 'drag collision ', ev.pos
                    self.mover = item
                    self.do_move = self._do_move
                    self.do_up = self._do_end_drag
                    break
            else:
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
                    #item.action(*ev.pos)
                    if item.action(*ev.pos): break
                    break
        

    def click(self, object):
        av= object.avatar()
        av.addListener('click',EventWrapper(object.action,self.offset).action)
    def dragg(self, object):
        wrapper = DragWrapper(self._drop,object)
        #action = DragWrapper(object.action).action
        #start = DragWrapper(object.start).action
        #stop = DragWrapper(object.stop).action
        object.avatar().drag(wrapper.action,wrapper.start,wrapper.stop)
        #object.avatar().drag(object.action,object.start,object.stop)
    def _drop(self, source):
        av= source.avatar()
        x, y = av.posX(),av.posY()
        for target in self.drop_listeners:
            if target.collide(x, y ):
                target.action(x, y, source)
    def drop(self, object):
        #av= object.avatar()
        #wrapper = EventWrapper(object.action,self.offset).action
        #av.addListener('mouseup',wrapper)
        self.drop_listeners.append(object)
    def roll(self, object):
        object.avatar().mousemove(object.action)
    def act(self, object):
        self.act_listeners.append(object)
    def undrop(self, object):
        self.drop_listeners.remove(object)
    def unclick(self, object):
        pass #object.avatar().unclick(object.action)
    def undrag(self, object):
        object.avatar().undrag(object.action)
         

class GUI(VerticalPanel,GUI_Event):
    def __init__(self):
        """ Standard initialiser.
        """
        VerticalPanel.__init__(self)
        GUI_Event.__init__(self)
        self.canvas = Raphael(900,700)
        #self.canvas.addListener('mousedown',self.test)
        #self.canvas.addListener('contextmenu',self.test)
        #self.tb = TextArea()
        #self.tb.setName("textBoxFormElement")
        #self.tb.setStyleAttribute({'position':'absolute',
        #    'top':'175px','left':'158px'
        #    ,'color':COLOR['maroon']
        #    ,'background':COLOR['peachpuff']
        #    ,'background-color':COLOR['peachpuff']})
        #self.tb.setSize(450,100)
        #self.tb.setReadonly('readonly')
        self.add(self.canvas)
        #self.add(self.tb)
        x = DOM.getAbsoluteLeft(self.canvas.getElement())
        y = DOM.getAbsoluteTop(self.canvas.getElement())
        self.offset = (x,y)
        '''
    
        Empacotador.init()
        Menu.init()
        
        self.click_listeners = []
        self.drag_listeners = []
        self.drop_listeners = []
        self.roll_listeners = []
        self.act_listeners = []
        self.do_up = self._do_up
        self.do_move = self._do_nothing
        self.do_down = self._do_down #self._do_nothing
        self._create()
        '''
        
    def _inicia(self,game):
        self.game = game
    def _decorate(self,element):
        element.avatar = element
        return element
    def talk(self,msg='foi'):
        alert (msg)
    def test(self,elm,event,msg='foi'):
        location = None
        JS('''
           location = window.location.hostname;

           ''')
        if 'localhost' == location: location +=':8004'
        return location
        x = DOM.eventGetClientX(event)
        y = DOM.eventGetClientY(event)
        alert ('%s %s %s'%(msg,x,y))
    def create_game(self,game,title):
        self.game = game
        RootPanel().add(self)
        return self.inicia()
    def remove(self, element):
        if element in self.drop_listeners:
            self.drop_listeners.remove(element)
        element.remove()
        
    def text(self,x,y,texto,color='navajo white', size =16):
        t = self.canvas.text(x,y,texto)
        t.setAttrs({'fill':COLOR[color],'stroke':COLOR[color],'font-size':'%d'%size})
        return t
    def path(self,path, width = 1, color='navajo white', background ='white'):
        #color:#000000;fill:#462813;fill-opacity:1;stroke:#d08554;stroke-width:1;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate
        pathParams = {'stroke'         : COLOR[color],
                      'color'           : color,
                      'fill'            : COLOR[background],
                      #'stroke-width'   : width, #"%dpx"%width,
                      'stroke-linecap' : "round"}

        t  = self.canvas.path(data=path,attrs=pathParams)
        return t
    def textarea(self,x,y,w,h,texto,color='navajo white', background ='white'):
        t = Text_Area(self,texto,x,y,w,h,color, background)
        return t
        #return self._decorate(t)
    def rect(self,x,y,dx,dy,color='navajo white', line =None):
        r = self.canvas.rect(x,y,dx-x,dy-y)
        r.setAttrs({'fill':COLOR[color],'stroke':line and COLOR[line] or COLOR[color]})
        #r.addListener('click',self.test)
        #r.addListener('mousedown',self.test)
        #r.addListener('contextmenu',self.test)
        #return r
        return self._decorate(r)
    def image(self,glyph,x,y,dx,dy, l=None, f='png', buff=''):
        return Empacotador(self.canvas,glyph,x,y,dx,dy, l)
    def score(self,score,houses):
        score =  j_p.encode(score)
        houses =  j_p.encode(houses)
        DOM.setAttribute(self.scored,"value",score)
        DOM.setAttribute(self.housed,"value",houses)
        #self.talk(str((score,houses)))
        frm = self.__form
        JS("""
            frm.submit()
        """)
        #self.__form.submit()
        return score
    def send(self,uid,**kwargs):
        score =  j_p.encode(uid)
        message = dict(line= uid, _xsrf= self.x)
        message.update(kwargs)
        message =  j_p.encode(message)
        self._socket.sending(message)
    def inicia(self):
        global IMAGEREPO
        self.__form = f = DOM.getElementById('mainform')
        self.x = DOM.getChild(f,0).value #DOM.getElementByName('_xsrf').value
        g = DOM.getChild(f,1).value
        self.scored = DOM.getChild(f,2)
        self.housed = DOM.getChild(f,3)
        if g == '12de6b622cbfe4d8f5c8d3347e56ae8c': IMAGEREPO = 'imagens/'
        #self.talk(self.scored.value+self.housed.value+IMAGEREPO)
        self._socket = NullSocket() #WebSocket("ws://%s/chatsocket"%self.test())
        self._socket.register_receiver(self.game.receive)
        obj = j_p.wdecode(self.housed.value)
        #self.text(400,85, str(obj) ,'darkbrown',10)
        #obj = [dict(body='nonono')]
        return obj
    def receive(self,message = 'nono'):
        self.talk(message.line+ ':'+ message.body)
    def slate(self,source,x,y,w,h, element = None, l=None, f=None, buff= None):
        return Slate(self.canvas,source,x,y,w,h, l, f, buff)
    def icon(self):#,source,x,y,w,h, l=None, f=None, buff= None):
        return Menu(self.canvas)#source,x,y,w,h, l, f, buff)
    def flyer(self,source,x,y,w=16,h=16):#, l=None, f=None, buff= None):
        return Flyer(self.canvas,source,x,y,w,h)#source,x,y,w,h, l, f, buff)
        
class WebSocket:
    def __init__(self,host):
        self._socket = None
        JS("""
            if ("WebSocket" in window) {
            this._socket = new WebSocket(host);
            } else {
                this._socket = new MozWebSocket(host);
            }
        """)
    def sending(self,message):
        #message = fkj(message)
        JS("""
            this._socket.send(message);
         """)
    def register_receiver(self,receiving_method):
        decoding = j_p.decode
        #JS("""
        #    this._socket.onmessage = function(event) {
        #        receiving_method(JSON.parse(event.data));
        #    }
        # """)
        JS("""
            this._socket.onmessage = function(event) {
                receiving_method(decoding(event.data));
            }
         """)
class NullSocket:
    def __init__(self,host):
       pass
    def sending(self,message):
        pass
    def register_receiver(self,receiving_method):
        pass
       

'''
if __name__ == "__main__":
    mundo = MainTrain()
    RootPanel().add(mundo)
    mundo.inicia()
'''

