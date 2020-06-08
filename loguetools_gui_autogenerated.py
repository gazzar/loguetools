# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"loguetools", pos = wx.DefaultPosition, size = wx.Size( 1029,509 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        MainFrameSizer = wx.BoxSizer( wx.VERTICAL )

        toolbarSizer = wx.GridSizer( 0, 2, 0, 0 )

        self.toolbarPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        toolbarPanelSizer = wx.BoxSizer( wx.VERTICAL )

        self.toolbar = wx.ToolBar( self.toolbarPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
        self.toolbar.Realize()

        toolbarPanelSizer.Add( self.toolbar, 0, wx.ALL|wx.EXPAND, 0 )


        self.toolbarPanel.SetSizer( toolbarPanelSizer )
        self.toolbarPanel.Layout()
        toolbarPanelSizer.Fit( self.toolbarPanel )
        toolbarSizer.Add( self.toolbarPanel, 1, wx.EXPAND, 0 )

        self.checkboxPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        checkboxPanelSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_toolBar_options = wx.ToolBar( self.checkboxPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
        self.m_checkBox_id = wx.CheckBox( self.m_toolBar_options, wx.ID_ANY, u"id", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_id.SetToolTip( u"Prepend id to filename" )

        self.m_toolBar_options.AddControl( self.m_checkBox_id )
        self.m_checkBox_md5 = wx.CheckBox( self.m_toolBar_options, wx.ID_ANY, u"md5:4", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_md5.SetToolTip( u"Append md5 checksum to filename" )

        self.m_toolBar_options.AddControl( self.m_checkBox_md5 )
        self.m_checkBox_version = wx.CheckBox( self.m_toolBar_options, wx.ID_ANY, u"ver", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_version.SetToolTip( u"Append loguetools version to filename" )

        self.m_toolBar_options.AddControl( self.m_checkBox_version )
        self.m_checkBox_inits = wx.CheckBox( self.m_toolBar_options, wx.ID_ANY, u"Inits", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_inits.SetToolTip( u"Include patches named Init Program" )

        self.m_toolBar_options.AddControl( self.m_checkBox_inits )
        self.m_toolBar_options.Realize()

        checkboxPanelSizer.Add( self.m_toolBar_options, 0, wx.ALL|wx.EXPAND, 0 )


        self.checkboxPanel.SetSizer( checkboxPanelSizer )
        self.checkboxPanel.Layout()
        checkboxPanelSizer.Fit( self.checkboxPanel )
        toolbarSizer.Add( self.checkboxPanel, 1, wx.EXPAND, 0 )


        MainFrameSizer.Add( toolbarSizer, 0, wx.EXPAND, 0 )

        displaySizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        displaySizer.AddGrowableCol( 0 )
        displaySizer.AddGrowableCol( 1 )
        displaySizer.AddGrowableRow( 0 )
        displaySizer.SetFlexibleDirection( wx.BOTH )
        displaySizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.displaySplitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
        self.displaySplitter.Bind( wx.EVT_IDLE, self.displaySplitterOnIdle )
        self.displaySplitter.SetMinimumPaneSize( 40 )

        self.patchListPanel = wx.Panel( self.displaySplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        patchListPanelSizer = wx.BoxSizer( wx.VERTICAL )

        self.listCtrl = wx.ListCtrl( self.patchListPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
        patchListPanelSizer.Add( self.listCtrl, 1, wx.EXPAND, 5 )


        self.patchListPanel.SetSizer( patchListPanelSizer )
        self.patchListPanel.Layout()
        patchListPanelSizer.Fit( self.patchListPanel )
        self.stdoutPanel = wx.Panel( self.displaySplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        stdoutPanelSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrlOut = wx.TextCtrl( self.stdoutPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
        stdoutPanelSizer.Add( self.m_textCtrlOut, 2, wx.EXPAND, 5 )


        self.stdoutPanel.SetSizer( stdoutPanelSizer )
        self.stdoutPanel.Layout()
        stdoutPanelSizer.Fit( self.stdoutPanel )
        self.displaySplitter.SplitVertically( self.patchListPanel, self.stdoutPanel, 510 )
        displaySizer.Add( self.displaySplitter, 1, wx.EXPAND, 5 )


        MainFrameSizer.Add( displaySizer, 1, wx.EXPAND, 0 )


        self.SetSizer( MainFrameSizer )
        self.Layout()
        self.statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu21 = wx.Menu()
        self.m_menuItem21 = wx.MenuItem( self.m_menu21, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu21.Append( self.m_menuItem21 )

        self.m_menubar1.Append( self.m_menu21, u"File" )

        self.m_menu2 = wx.Menu()
        self.m_menuItem2 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"About..."+ u"\t" + u"F1", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem2 )

        self.m_menubar1.Append( self.m_menu2, u"Help" )

        self.SetMenuBar( self.m_menubar1 )


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_checkBox_id.Bind( wx.EVT_MOTION, self.OnMouseoverId )
        self.m_checkBox_md5.Bind( wx.EVT_MOTION, self.OnMouseoverMd5 )
        self.m_checkBox_version.Bind( wx.EVT_MOTION, self.OnMouseoverVer )
        self.m_checkBox_inits.Bind( wx.EVT_MOTION, self.OnMouseoverInits )
        self.listCtrl.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.OnPatchDeselected )
        self.listCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnPatchSelected )
        self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_menuItem21.GetId() )
        self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_menuItem2.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnMouseoverId( self, event ):
        event.Skip()

    def OnMouseoverMd5( self, event ):
        event.Skip()

    def OnMouseoverVer( self, event ):
        event.Skip()

    def OnMouseoverInits( self, event ):
        event.Skip()

    def OnPatchDeselected( self, event ):
        event.Skip()

    def OnPatchSelected( self, event ):
        event.Skip()

    def OnExit( self, event ):
        event.Skip()

    def OnAbout( self, event ):
        event.Skip()

    def displaySplitterOnIdle( self, event ):
    	self.displaySplitter.SetSashPosition( 510 )
    	self.displaySplitter.Unbind( wx.EVT_IDLE )


