#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/12/12  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/12/12 $Date$"

from gui_decorator import Item

class App(Item):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        app = self.gui.text(350, 10, 'Jeppeto')
        app = self.gui.rect(50, 50, 700, 500)
        return app
    def _click(self,x,y):
        
            self.xy = (x,y)
            print 'self.xy x, y = ',self.xy
            self.menu = Menu(self.gui,self,action=self.create_child)
    def _click_template(self,x,y):
        self.activate = self._no_click
        self._click(x, y)
    
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()

