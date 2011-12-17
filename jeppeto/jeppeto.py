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

class JPTerm:
    def __init__(self, container = None, name = None):
        self.container = container
        self.name = name
    def create(self):
        pass
    def append(self,name):
        pass
NULLTERM = type('_Nenhures',(),dict(__call__ = lambda self: self
                                    , create = lambda self: self))

class JPClass(JPTerm,dict):
    def create(self):
        return self.icon 
    def create_class(self,name):
        self.append(name)
        return name
    def create_method(self,name):
        child = JPMethod(self)
        self[name]= child
        return (name, child)
    def build(self):
        return type(self.name,tuple(s for s in self)
                , dict((m, c.build()) for m, c in self.items()))

class JPMethod(JPTerm,dict):
    def create(self):
        return self.icon 
    def create_argument(self,name,value=NULLTERM()):
        self[name]= value
        return (name, value)
    def create_statement(self,name):
        child = JPStatement(self,name)
        self.append(child)
        return child
    def create_assignment(self,name):
        child = JPAssignment(self,name)
        self.append(child)
        return (name, child)
    def build(self):
        a = [argument for argument, value in self.items() if value is NULLTERM]
        k = dict((argument,value) for argument, value in self.items()
            if not (value is NULLTERM()))
        lines = ','.join(line.build() for line in self[:-1])
        last = self[-1].build()
        body ='body = lambda self, %s : (%s) and None or %s'%(param, lines, last)
        eval(body)
        return body
        return lambda zelf, lines=lines, **kwargs: tuple(
                line(zelf, **kwargs) for line in lines[:-1]
            ) and None or lines[-1](zelf, **kwargs)
     
class JPAssignment(JPTerm):
    def create(self):
        return self.icon 
    def create_value(self, value=NULLTERM()):
        self.value = value
        return self.value
    def create_statement(self,name):
        self.value = JPStatement(self,name)
        return self.value
    def create_assignment(self,name):
        self.value = JPAssignment(self,name)
        return self.value
    def build(self):
        return 'setattr(self,%s,%s)'%(self.name,self.value)
     
class JPStatement(JPTerm):
    def create(self):
        return self.icon 
    def create_argument(self,name,value=NULLTERM()):
        self[name]= value
        return (name, value)
    def create_name(self,name, value=NULLTERM()):
        self.value = value
        return self.value
    def create_statement(self):
        self.value = JPStatement(self)
        return self.value
    def create_assignment(self,name):
        self.value = JPAssignment(self,name)
        return self.value
    def build(self):
        return lambda zelf, name = self.name, value = self.value, **kwargs: setattr(
            zelf,name,value(zelf,**kwargs))
     
class Jeppeto(JPTerm):
    """ Engenho de Criação de Jogos educacionais
    """
    def create_child(self,master):
        child = JPClass(self)
        self.append(child)
        return (child, child.create_child)
    
def main():
    from pygame_factory import GUI
    from gui_decorator import App
    jeppeto = Jeppeto()
    main = App(GUI(),jeppeto,action = jeppeto.create_child)
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()
