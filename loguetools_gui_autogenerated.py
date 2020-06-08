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

        bSizer = wx.BoxSizer( wx.VERTICAL )

        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.toolbar = wx.ToolBar( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
        self.toolbar.Realize()

        bSizer5.Add( self.toolbar, 0, wx.EXPAND, 0 )


        self.m_panel3.SetSizer( bSizer5 )
        self.m_panel3.Layout()
        bSizer5.Fit( self.m_panel3 )
        gSizer1.Add( self.m_panel3, 1, wx.EXPAND, 0 )

        self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_toolBar_options = wx.ToolBar( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
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

        bSizer4.Add( self.m_toolBar_options, 0, wx.EXPAND, 0 )


        self.m_panel4.SetSizer( bSizer4 )
        self.m_panel4.Layout()
        bSizer4.Fit( self.m_panel4 )
        gSizer1.Add( self.m_panel4, 1, wx.EXPAND, 0 )


        bSizer.Add( gSizer1, 0, wx.EXPAND, 5 )

        fgSizer1 = wx.FlexGridSizer( 1, 2, 0, 0 )
        fgSizer1.AddGrowableCol( 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.AddGrowableRow( 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
        self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
        self.m_splitter2.SetMinimumPaneSize( 40 )

        self.m_panel1 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.listCtrl = wx.ListCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
        bSizer2.Add( self.listCtrl, 1, wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        self.m_panel2 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrlOut = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
        bSizer3.Add( self.m_textCtrlOut, 2, wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer3 )
        self.m_panel2.Layout()
        bSizer3.Fit( self.m_panel2 )
        self.m_splitter2.SplitVertically( self.m_panel1, self.m_panel2, 510 )
        fgSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )


        bSizer.Add( fgSizer1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer )
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
        self.listCtrl.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.OnPatchDeselected )
        self.listCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnPatchSelected )
        self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_menuItem21.GetId() )
        self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_menuItem2.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnPatchDeselected( self, event ):
        event.Skip()

    def OnPatchSelected( self, event ):
        event.Skip()

    def OnExit( self, event ):
        event.Skip()

    def OnAbout( self, event ):
        event.Skip()

    def m_splitter2OnIdle( self, event ):
    	self.m_splitter2.SetSashPosition( 510 )
    	self.m_splitter2.Unbind( wx.EVT_IDLE )


