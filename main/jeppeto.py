#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Jeppeto : An Educational Game Builder
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/09/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/09/09 $Date$"
import zipfile
from io import BytesIO
ICONS = zipfile.ZipFile('/home/carlo/shine-icon-set.zip', 'r')
ICO = file('/home/carlo/png/16x16/accept.png')

class JPObject(list):
    def __init__(self, container = None):
        self.container = container
    def create(self):
        pass
    def create_child(self,icon):
        pass

class JPClass(JPObject):
    def create(self):
        return self.icon 
    def create_child(self,master):
        child = JPMethod(self)
        self.append(child)
        return (child, child.create_child)

class JPMethod(JPObject):
    def create(self):
        return self.icon 
     
class Jeppeto(JPObject):
    """ Engenho de Criação de Jogos educacionais
    """
    def create_child(self,master):
        child = JPClass(self)
        self.append(child)
        return (child, child.create_child)
    
def main():
    from pygame_factory import GUI
    from gui_wrapper import App
    jeppeto = Jeppeto()
    main = App(GUI(),jeppeto,action = jeppeto.create_child)
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()
