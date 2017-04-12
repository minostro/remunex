#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This class is under GPL (http://www.gnu.org/copyleft/gpl.html)
# Copyright Benjamin POUSSIN < bpoussin@free.fr >, Sebastien REGNIER < seb.regnier@free.fr >
# Benoît CLOUET < b.clouet@free.fr > 

# Utilise gtk2
import pygtk
pygtk.require('2.0')

import gtk.glade
import gtk
import sys
import os


class GladeConnect:
    """
    permet d'utiliser les fichiers XML générer par glade de facon tres simple.
    Faire hériter une classe de cette classe GladeConnect.
    Dans le constructeur de votre classe faites appelle a
    GladeConnect.__init__(self, "nom du fichier glade").

    Ensuite les objets creer en Glade, peuvent etre utilise dans votre classe
    par self.nom_du_widget
    Il vous faudra aussi creer des methodes ayant le meme nom que les callbacks
    definie en glade, par exemple:
    def callback_declare(self, source=None, event=None):
    """

    def __init__(self, filename, root=None):
	"""
	root vous permet de specifier une fenetre particuliere du fichier
	.glade. Cela est util si vous avez mis plusieurs fenêtres dans le
	même fichier.
	"""
	dirname = os.path.dirname(sys.argv[0])
	if dirname != '':
		dirname = dirname + os.sep

	try:
		os.stat(dirname+filename)
	except:
		dirname = '/opt/pyGestor/'
		
        self.ui = gtk.glade.XML(dirname+filename, root)
        self.connect()
        
    def cree_dico (self):
        dico = {} ## dico vide pour commencer
        self.cree_dico_pour_classe (self.__class__, dico)
        return dico

    def cree_dico_pour_classe (self, une_classe, dico):
        bases = une_classe.__bases__
        for iteration in bases:
            self.cree_dico_pour_classe (iteration, dico) ## Appel recursif
        for iteration in dir(une_classe):
            dico[iteration]=getattr(self,iteration)

    def connect(self):
        self.ui.signal_autoconnect(self) 

    def __getattr__(self, name):
        result = self.ui.get_widget(name)
        if result == None:
            ## On ne le trouve pas sur l'ui, il serait bon de recherche sur
            ## la fenetre de l'ui
            pass
            if result == None:
                raise AttributeError, name
        return result

    def on_exit(self, source=None, event=None):
	try:
		gtk.main_quit()
	except:
		print "Terminando ejecución..."
