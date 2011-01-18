# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008, 2009, 2010 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

from __future__ import unicode_literals

"""
Base class and stubs and logic for Panels (QDockWidgets).

When the panel must be shown its widget is instantiated.
"""

import weakref

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDockWidget, QKeySequence, QLabel

import actioncollection
import app
import plugin


def manager(mainwindow):
    return PanelManager.instance(mainwindow)
    

class PanelManager(plugin.MainWindowPlugin):
    def __init__(self, mainwindow):
        # instantiate the panel stubs here
        self.quickinsert = QuickInsertPanel(mainwindow)
        
        self.createActions()

    def createActions(self):
        self.actionCollection = Actions(self)
        self.mainwindow().addActionCollection(self.actionCollection)

    def addActionsToMenu(self, menu):
        """Adds all toggleViewActions to the given menu."""
        menu.addAction(self.actionCollection.panel_quickinsert)
        
        

class Actions(actioncollection.ActionCollection):
    """Manages the keyboard shortcuts to hide/show the plugins."""
    name = "panels"
    
    def createActions(self, manager):
        # add the actions for the plugins
        self.panel_quickinsert = manager.quickinsert.toggleViewAction()
        



class Panel(QDockWidget):
    """Base class for Panels.
    
    You should implement __init__(), createWidget() and translateUI().
    On the first call to sizeHint() our widget is created.
    
    """
    def __init__(self, mainwindow):
        """You should implement this method to set a title and add yourself to the mainwindow.
        
        First call this super method as it calls the Qt constructor.
        
        """
        super(Panel, self).__init__(mainwindow)
        app.translateUI(self)
    
    def mainwindow(self):
        return self.parentWidget()
        
    def sizeHint(self):
        """This is always called when the panel needs to be shown. Instantiate if not already done."""
        self.widget()
        return super(Panel, self).sizeHint()
    
    def widget(self):
        """Ensures that our widget() is created and returns it."""
        w = super(Panel, self).widget()
        if not w:
            w = self.createWidget()
            self.setWidget(w)
        return w
        
    def createWidget(self):
        """Re-implement this to return the widget for this tool."""
        return QLabel("<test>", self)
        

# stubs here
class QuickInsertPanel(Panel):
    def __init__(self, mainwindow):
        super(QuickInsertPanel, self).__init__(mainwindow)
        self.hide()
        self.toggleViewAction().setShortcut(QKeySequence("Meta+Alt+I"))
        mainwindow.addDockWidget(Qt.LeftDockWidgetArea, self)
        self.actionCollection = QuickInsertActions(self)
        mainwindow.addActionCollection(self.actionCollection)
    
    def translateUI(self):
        self.setWindowTitle(_("Quick Insert"))
        self.toggleViewAction().setText(_("Quick &Insert"))
        
    def createWidget(self):
        import quickinsert
        return quickinsert.QuickInsert(self)


class QuickInsertActions(actioncollection.ShortcutCollection):
    """Manages keyboard shortcuts for the QuickInsert module."""
    name = "quickinsert"
    def __init__(self, panel):
        super(QuickInsertActions, self).__init__(panel.mainwindow())
        self.panel = weakref.ref(panel)
    
    def createDefaultShortcuts(self):
        self.setDefaultShortcuts('slur', [QKeySequence('Ctrl+0')])

    def realAction(self, name):
        return self.panel().widget().actionForName(name)
        
    def title(self):
        return _("Quick Insert")
    

