import os
from contextlib import contextmanager
from gui_handlers import MyFrame
import wx
import wx.lib.mixins.inspection
from pathlib import Path
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


@contextmanager
def cd(newdir):
    """https://stackoverflow.com/a/24176022"""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


class LoguetoolsWxApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """The main application class - added a wxPython inspection tool
    http://wiki.wxpython.org/Widget%20Inspection%20Tool

    """
    def OnInit(self):
        self.Init()  # initialize the inspection tool
        self.m_frame = MyFrame(None)
        self.m_frame.Show()
        self.SetTopWindow(self.m_frame)
        return True


if __name__ == '__main__':
    with cd(Path(__file__).parent):
        app = LoguetoolsWxApp(0)
        app.MainLoop()
