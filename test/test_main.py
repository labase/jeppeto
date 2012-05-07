#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Jeppeto : An Educational Game Builder - Test Main
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2012/02/18  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2012, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2012/02/18 $Date$"


from mock import Mock

import unittest
from jeppeto.main import App, BLOCK_SIZE
from StringIO import StringIO as Sio

CLICK, RECT, IMG, DRAG, DROP = 'click rect image dragg drop'.split()

class FixApp(App):
    def __init__(self, gui, inf = None, ouf =None, rw = False):
        self.inf = inf and Sio(buf = inf) or Sio()
        self.ouf = ouf and Sio(buf = ouf) or Sio()
        if inf or ouf or rw:
            self._setup = self.setup
            self.setup = self._string_io_setup
        else:
            self.setup = self._null_setup
        App.__init__(self, gui)
    def _null_setup(self, *args): pass
    def _string_io_setup(self, *args): 
        self._setup(self.inf, self.ouf)

class _TestEditWithJeppeto(unittest.TestCase):
    """can build Jeppeto Game Editor"""
    def _find(self, call, reset = False, anything= False):
        self._callings = [called for called in self.GUI.method_calls
                 if anything or call == called[0]]
        reset and self.GUI.reset_mock()
        return self._callings
    def _count(self, call, reset = False, anything= False):
        self._counting = len(self._find(call,reset = reset, anything = anything))
        return self._counting
        
    def setUp(self):
        self.GUI = Mock()
        self.app = FixApp(self.GUI)
   
    def tearDown(self):
        self.GUI.reset_mock()
        self.app = None

    def test_app_has_props_and_create_tools(self):
        "tm cor nula e mock gui, cria quatro ferramentas"
        assert self.app.color == None, "instead color was %s"%self.app.color
        assert self.app.items == [], "instead color was %s"%self.app.items
        assert self.app.gui == self.GUI, "instead gui was %s"%self.GUI
        call = CLICK
        assert self._count(call, reset = True) == 5\
        , "instead calls %d %s"%(self._count(call),self._find(call))
        #self.app.create()
        assert self._count(call) == 0\
            , "instead calls %d %s"%(self._count(call),self._find(call))
    def test_locus_creation(self):
        "cria um locus na pos (1,1)"
        clicks = self._count(CLICK, reset = True)
        assert clicks == 5,'%d'%clicks
        self.app._create(1,1)
        assert self.app.items[0].size[0] == BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert len(self.app.items) == 1, "instead items was %s"%self.app.items
        call = CLICK
        assert self._count(call, reset = True, anything= True) == 5\
            , "instead calls %d %s"%(self._counting, self._callings)
    def test_another_locus_creation(self):
        "cria um locus na pos (50, 50)"
        self.test_locus_creation()
        self.app._create(50,50)
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        assert self._count(None, reset = True, anything= True) == 5\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_inner_locus_creation_and_inflate_external(self):
        "cria um locus interno  na pos (10, 10) e infla o externo"
        self.test_locus_creation()
        self.app.items[0]._create(10,10)
        assert len(self.app.items) == 1, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert self.app.items[0].items[0].container == self.app.items[0] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[0].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 5\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_reference_creation_and_inflate_external(self):
        "cria uma referência interna  na pos (10, 10) e infla o externo"
        self.test_another_locus_creation()
        self.app.items[0].paste(10,10,self.app.items[1])
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert self.app.items[0].items[0].container == self.app.items[0] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[0].items[0].referee == self.app.items[1] \
            , "instead items was %s"%self.app.items[0].items[0].referee
        assert self.app.items[0].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 7\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_copy_reference_creation_and_inflate_external(self):
        "copia uma referencia a locus na pos (110, 110) e infla o externo"
        self.test_reference_creation_and_inflate_external()
        self.app._create(100,100)
        self.app.items[2].paste(110, 110,self.app.items[0].items[0])
        assert len(self.app.items) == 3, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert len(self.app.items[2].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert self.app.items[0].items[0].container == self.app.items[0] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[2].items[0].container == self.app.items[2] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[2].items[0].referee == self.app.items[1] \
            , "instead items was %s"%self.app.items[0].items[0].referee
        assert self.app.items[2].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 13\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_copy_self_reference_creation_dangerously(self):
        "copia uma perigosa referencia de locus a si mesmo na pos (60, 60) "
        self.test_reference_creation_and_inflate_external()
        master = self.app.items[0].items[0]
        extracopy = master.clone(60, 60, owner=master)
        master.revert()
        assert extracopy.xy[0] == 60 , "instead items was %s"%extracopy.xy[0]
        assert master.xy[0] == 10 , "instead items was %s"%master.xy[0]
        #self.app._create(100,100)
        self.app.items[1].paste(60, 60,master)
        refcopy = self.app.items[1].items[0]
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert len(self.app.items[1].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert master.container == self.app.items[0] \
            , "instead items was %s"%master.container
        assert refcopy.container == self.app.items[1] \
            , "instead items was %s"%refcopy.container
        assert refcopy.referee == self.app.items[1] \
            , "instead items was %s"%refcopy.referee
        assert self.app.items[1].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 16\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_actor_creation_and_inflate_external(self):
        "cria um ator interno  na pos (10, 10) e infla o externo"
        self.test_locus_creation()
        locus = self.app.items[0]
        locus.paste(10,10,self.app.actor_tool)
        actor = locus.items[0]
        assert actor.__class__.__name__ == "Actor" \
            , 'but the type was %s'%actor.__class__.__name__
        assert len(self.app.items) == 1, "instead items was %s"%self.app.items
        assert len(locus.items) == 1 \
            , "instead items was %s"%locus.items
        assert actor.container == locus \
            , "instead items was %s"%actor.container
        assert locus.size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(locus.size)
        assert self._count(None, reset = True, anything= True) == 6\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_portal_creation_and_inflate_external(self):
        "cria um portal interno  na pos (10, 10) e infla o externo"
        self.test_another_locus_creation()
        self.app.items[0].paste(10,10,self.app.port_tool)
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert self.app.items[0].items[0].container == self.app.items[0] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[0].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 5\
            , "instead calls %d %s"%(self._counting, self._callings)

    def test_portal_reference_and_inflate_external(self):
        "cria uma referencia a portal na pos (60, 60) e infla o externo"
        self.test_portal_creation_and_inflate_external()
        self.app.items[1].paste(10,10,self.app.items[0].items[0])
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert self.app.items[0].items[0].container == self.app.items[0] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[0].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 7\
            , "instead calls %d %s"%(self._counting, self._callings)

class TestSaveLoadJeppeto(_TestEditWithJeppeto):
    """can persist Jeppeto Game Editor"""
    def _rw_setup(self, inf = None, ouf =None):
        self.GUI = Mock()
        self.app = FixApp(self.GUI, inf, ouf, rw=True)
        self.inf, self.ouf = self.app.inf, self.app.ouf
    def setUp(self):
        self._rw_setup()
    def test_rw_with_stringio(self):
        self.test_app_has_props_and_create_tools()
        self.app.cleanup()
        file = self.ouf.len
        assert not file, 'instead file was %d'%file 
    def test_rw_add_two_locus(self):
        self.test_another_locus_creation()
        file = self.ouf.len
        assert  file > 40, 'instead file was %d %s'%(file, self.ouf.buflist)
        outfile = '\n'.join(self.ouf.buflist)
        assert len(outfile) == 177, "n, outfile : %d %s"%(len(outfile), outfile)
        self._rw_setup(outfile)
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        call = CLICK
        assert self._count(call, reset = True, anything= True) == 39\
            , "instead calls %d %s"%(self._counting, self._callings)
    def test_read_two_locus_add_locus_reference(self):
        self.test_rw_add_two_locus()
        self.app.items[0].paste(10,10,self.app.items[1])
        assert len(self.app.items) == 2, "instead items was %s"%self.app.items
        assert len(self.app.items[0].items) == 1 \
            , "instead items was %s"%self.app.items[0].items
        assert self.app.items[0].items[0].container == self.app.items[0] \
            , "instead items was %s"%self.app.items[0].items[0].container
        assert self.app.items[0].items[0].referee == self.app.items[1] \
            , "instead items was %s"%self.app.items[0].items[0].referee
        assert self.app.items[0].size[0] > BLOCK_SIZE \
            , "instead items was %s"%str(self.app.items[0].size)
        assert self._count(None, reset = True, anything= True) == 7\
            , "instead calls %d %s"%(self._counting, self._callings)
