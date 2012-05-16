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
#from pyjamas.json import JSONParser
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
        
class Window(VerticalPanel):
    def __init__(self):
        """ Standard initialiser.
        """
        VerticalPanel.__init__(self)
        self.canvas = Raphael(900,700)
        self.add(self.canvas)
        x = DOM.getAbsoluteLeft(self.canvas.getElement())
        y = DOM.getAbsoluteTop(self.canvas.getElement())
        self.offset = (x,y)
    def build_event(self,action,offset):
        return EventWrapper(action,offset)
    def build_drag(self,action,offset):
        return DragWrapper(action,offset)
        
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
        return #self.inicia()
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

