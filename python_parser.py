#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Jeppeto : Parses a python file and convert to Jeppeto
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/12/02  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/12/02 $Date$"
import ast

class Py2Jeppeto(ast.NodeVisitor):
    TYPES = {}
    COUNT = 0
    def generic_visit(self, node):
        tipo = type(node).__name__
        if not tipo in Py2Jeppeto.TYPES:
            out = Py2Jeppeto.TYPES[tipo] = Py2Jeppeto.COUNT
            Py2Jeppeto.COUNT +=1
        else:
            out = Py2Jeppeto.TYPES[tipo]
        print '%02d'%out,'##'+tipo,
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Module(self, node):
        print '\nM:',# node.id
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self,node):#, bases, body,decorator_list):
        print '\nC:', node.name
        ast.NodeVisitor.generic_visit(self, node)
        print '\n/C', node.name

    def visit_FunctionDef(self, node):
        print '\nF:', node.name
        ast.NodeVisitor.generic_visit(self, node)
        print '\n/F', node.name


    def visit_Call(self, node):
        print 'c(',
        ast.NodeVisitor.generic_visit(self, node)
        print ')c',

    def visit_Compare(self, node):
        print '<(',
        ast.NodeVisitor.generic_visit(self, node)
        print ')>',

    def visit_Assert(self, node):
        print '!(',
        ast.NodeVisitor.generic_visit(self, node)
        print ')!',

    def visit_Delete(self, node):
        print '-(',
        ast.NodeVisitor.generic_visit(self, node)
        print ')-',
    def visit_Del(self, node):
        print 'XX',
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Return(self, node):
        print '<<',
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Raise(self, node):
        print '!!!',
        ast.NodeVisitor.generic_visit(self, node)
        
    def visit_Num(self, node):
        print 'D:', node.__dict__['n'],
        #ast.NodeVisitor.generic_visit(self, node)
    def visit_BoolOp(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    def visit_BinOp(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    def visit_In(self, node):
        print '?>',
    def visit_Or(self, node):
        print '++',
        ast.NodeVisitor.generic_visit(self, node)
    def visit_And(self, node):
        print '**',
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Sub(self, node):
        print '--',
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Add(self, node):
        print '++',
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Mod(self, node):
        print '%%',
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        print "N:", node.id,
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Param(self, node):
        #print "pr:",
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print "S:", node.s,
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Tuple(self, node):
        print "T(",# str(node.elts),
        ast.NodeVisitor.generic_visit(self, node)
        print ")T",# str(node.elts),
        
    def visit_Print(self, node):
        print "P:",
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Store(self, node):
        #print "rr:",
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node):
        #print "dd:",
        ast.NodeVisitor.generic_visit(self, node)
 
    def visit_Pass(self, node):
        print "SS:",
        ast.NodeVisitor.generic_visit(self, node)
 
    def visit_Assign(self, node):
        print "=(",
        ast.NodeVisitor.generic_visit(self, node)
        print ")=",
 
    def visit_AugAssign(self, node):
        print "#(",
        ast.NodeVisitor.generic_visit(self, node)
        print ")#",

    def visit_comprehension(self, node):
        print "c[",
        ast.NodeVisitor.generic_visit(self, node)
        print "]c",
    def visit_List(self, node):
        print "L[",
        ast.NodeVisitor.generic_visit(self, node)
        print "]L",
    def visit_ListComp(self, node):
        print "C[",
        ast.NodeVisitor.generic_visit(self, node)
        print "]C",
    def visit_If(self, node):
        print "?I",
        ast.NodeVisitor.generic_visit(self, node)
        print "I?",
    def visit_While(self, node):
        print "?W",
        ast.NodeVisitor.generic_visit(self, node)
        print "W?",
    def visit_For(self, node):
        print "?F",
        ast.NodeVisitor.generic_visit(self, node)
        print "F?",
        
    def visit_Subscript(self, node):
        print "s_",
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Index(self, node):
        print "i@",
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Attribute(self, node):
        print "At:", node.attr,
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Expr(self, node):
        print "E:",
        ast.NodeVisitor.generic_visit(self, node)
    def visit_arguments(self, node):
        print "\ta(",
        ast.NodeVisitor.generic_visit(self, node)
        print ")a\n",
'''
'''
if __name__ == '__main__':
    node = ast.parse('''
class Elemento:
    """ Um elemento básico do Jogo.
    """
    TEMPO = 0
    def __init__(self, x=0, y=0, imagem = None):
        """ inicia a posição e a imagem
        """
        self.x, self.y = x, y
        self.imagem = imagem or self
        self._inicia()
    def _inicia(self):
        pass
       
class Local(Elemento):
    """ Um local onde se pode colocar Elementos
    """
    def _inicia(self):
        pass

class Atividade(Elemento):
    """ Um comportamento que pode ser atribuido a um elemento ou local
    """
    def _inicia(self):
        pass
class Passagem(Local):
    def recebe(self,elemento):
        self.mestre.do_move(self,self.x,self.y)
    def registra(self,elemento,via):
        self.item = elemento
        self.via = via
        self.mestre = elemento
        self.mestre.move(self,self.x,self.y)
    def envia(self,elemento):
        self.via.envia(elemento)
    def devolve(self,elemento):
        self.item = None
        pass
    def move(self,local,x,y):
        pass
    def adentra(self,elemento):
        self.item = elemento
        pass
class _PassagemNenhuma(Passagem):
    def __call__(self):
        return self
NENHURES = _PassagemNenhuma()
del _PassagemNenhuma

class Porto(Passagem):
    def _inicia(self):
        self.items = []
    def recebe(self,elemento):
        [item.recebe(elemento) for item in self.items]
    def envia(self,elemento):
        mestre = self.mestre
        elemento.move(mestre,mestre.x,mestre.y)
    def devolve(self,elemento):
        self.items.remove(elemento)
        self.via.apura()
    def adentra(self,elemento):
        self.items.append(elemento)
      
class Passageiro(Local):
    def _inicia(self):
        self.local = NENHURES
        self.items =[]
        self.do_move = self.__no_move
    def entra(self,destino):
        destino.recebe(self)
        self.local.devolve(self)
    def age(self):
        self.do_move = self.move
        self.local.envia(self)
        self.do_move = self.__no_move
    def __no_move(self,local,x,y):
        pass
    def move(self,local,x,y):
        self.local.devolve(self)
        self.local = local
        self.local.adentra(self)
        dx, dy = x - self.x, y - self.y
        self.x, self.y = x,y
        [item.ajusta(dx,dy) for item in self.items]
    def ajusta(self,x,y):
        self.x += x
        self.y += y
    #def sai(self,item):
    #    pass
    def devolve(self,elemento):
        pass
    def adentra(self,elemento):
        pass
class Lobo(Passageiro):pass
class Ovelha(Passageiro):pass
class Couve(Passageiro):pass
class Barco(Passageiro):#,Passagem):
    def recebe(self,elemento):
        elemento.move(self,self.x,self.y)
        self.items.append(elemento)
        self.__recebe, self.recebe= self.recebe, self._nem_recebe
    def _nem_recebe(self,elemento):
        pass
    def devolve(self,elemento):
        assert isinstance(elemento, Passageiro), 'Instead retrieved %s'%str(elemento)
        self.items.remove(elemento)
        self.recebe= self.__recebe
    def envia(self,elemento):
        self.local.via.recebe(elemento)
    pass
      
class Margem(Local):
    def _inicia(self):
        self.lobo = Passagem(self.x,100)
        self.ovelha = Passagem(self.x,200)
        self.couve = Passagem(self.x,300)
        self.lugares = (self.lobo,self.ovelha,self.couve)
    def apura(self):
        passageiros_nesta_margem = set([lugar.item for lugar in self.lugares])
        if (passageiros_nesta_margem in Rio.AZAR):
            raise Exception, 'Desastre: %s'%str(passageiros_nesta_margem)
    def recebe(self,elemento):
        [lugar.recebe(elemento) for lugar in self.lugares]
    def envia(self,elemento):
        self.via.recebe(elemento)
    def registra(self,elemento,via):
        self.via = via
        lugares = (self.lobo,self.ovelha,self.couve)
        [lugar.registra(item,self) for lugar,item in zip(lugares,elemento)]
LOBO,OVELHA,COUVE = range(3)        
class Rio(Margem):
    AZAR=[]
    def _inicia(self):
        self.x = 100
        #p = self.passageiros = [Passageiro(),Passageiro(),Passageiro()]
        p = self.passageiros = [Lobo(),Ovelha(),Couve()]
        Rio.AZAR = [set([p[LOBO],p[OVELHA],None]),set([p[COUVE],p[OVELHA],None])]
        self.ante_margem = Margem()
        self.margem = Margem(300)
        self.via = Barco(100)
        self.ante_pier, self.pier = self.lugares = [Porto(100),Porto(200)]
        self.ante_pier.registra(self.pier,self.ante_margem)
        self.pier.registra(self.ante_pier,self.margem)
        self.pier.envia(self.via)
        self.margem.registra(self.passageiros,self.pier)
        self.ante_margem.registra(self.passageiros,self.ante_pier)
    def recebe(self,elemento):
        self.via.recebe(elemento)


''')

    #print ast.dump(node)

    v = Py2Jeppeto()
    v.visit(node)
