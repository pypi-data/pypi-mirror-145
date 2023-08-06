import time
import os
import platform
from functools import partial

import numpy as np
np.seterr(all='ignore')

import wx
import wx.grid as wxgrid

from larch import Group
from larch.wxlib import (BitmapButton, SetTip, GridPanel, FloatCtrl,
                         FloatSpin, FloatSpinWithPin, get_icon, SimpleText,
                         pack, Button, HLine, Choice, Check, MenuItem,
                         GUIColors, CEN, LEFT, FRAMESTYLE, Font, FileSave,
                         FileOpen, FONTSIZE)

from larch.wxlib.plotter import _getDisplay
from larch.utils import group2dict

LEFT = wx.ALIGN_LEFT
CEN |=  wx.ALL

def autoset_fs_increment(wid, value):
    """set increment for floatspin to be
    1, 2, or 5 x 10^(integer) and ~0.02 X current value
    """
    if abs(value) < 1.e-20:
        return
    ndig = int(1-round(np.log10(abs(value*0.5))))
    wid.SetDigits(ndig+1)
    c, inc = 0, 10.0**(-ndig)
    while (inc/abs(value) > 0.02):
        scale = 0.5 if (c % 2 == 0) else 0.4
        inc *= scale
        c += 1
    wid.SetIncrement(inc)

class DataTable(wxgrid.GridTableBase):
    def __init__(self, nrows=50, collabels=['a', 'b'],
                 datatypes=['str', 'float:12,4'],
                 defaults=[None, None]):

        wxgrid.GridTableBase.__init__(self)

        self.ncols = len(collabels)
        self.nrows = nrows
        self.colLabels = collabels
        self.dataTypes = []
        for i, d in enumerate(datatypes):
            if d.lower().startswith('str'):
                self.dataTypes.append(wxgrid.GRID_VALUE_STRING)
                defval = ''
            elif d.lower().startswith('float:'):
                xt, opt = d.split(':')
                self.dataTypes.append(wxgrid.GRID_VALUE_FLOAT+':%s' % opt)
                defval = 0.0
            if defaults[i] is None:
                defaults[i] = defval

        self.data = []
        for i in range(self.nrows):
            self.data.append(defaults)

    def GetNumberRows(self):
        return self.nrows

    def GetNumberCols(self):
        return self.ncols

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return "%d" % (row+1)

    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

class DataTableGrid(wxgrid.Grid):
    def __init__(self, parent, nrows=50, rowlabelsize=35, collabels=['a', 'b'],
                 datatypes=['str', 'float:12,4'],
                 defaults=[None, None],
                 colsizes=[200, 100]):

        wxgrid.Grid.__init__(self, parent, -1)

        self.table = DataTable(nrows=nrows, collabels=collabels,
                                datatypes=datatypes, defaults=defaults)

        self.SetTable(self.table, True)
        self.SetRowLabelSize(rowlabelsize)
        self.SetMargins(10, 10)
        self.EnableDragRowSize()
        self.EnableDragColSize()
        self.AutoSizeColumns(False)
        for i, csize in enumerate(colsizes):
            self.SetColSize(i, csize)

        self.Bind(wxgrid.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)

    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()


class TaskPanel(wx.Panel):
    """generic panel for main tasks.
    meant to be subclassed
    """
    def __init__(self, parent, controller, xasmain=None, title='Generic Panel',
                 configname='task_config', config=None, **kws):
        wx.Panel.__init__(self, parent, -1, size=(550, 625), **kws)
        self.parent = parent
        self.xasmain = xasmain or parent
        self.controller = controller
        self.larch = controller.larch
        self.title = title
        self.configname = configname
        if config is not None:
            self.set_defaultconfig(config)
        self.wids = {}
        self.timers = {'pin': wx.Timer(self)}
        self.Bind(wx.EVT_TIMER, self.onPinTimer, self.timers['pin'])
        self.cursor_dat = {}
        self.subframes = {}
        self.command_hist = []
        self.SetFont(Font(FONTSIZE))
        self.titleopts = dict(font=Font(FONTSIZE+2),
                              colour='#AA0000', style=LEFT)

        self.panel = GridPanel(self, ncols=7, nrows=10, pad=2, itemstyle=LEFT)
        self.panel.sizer.SetVGap(5)
        self.panel.sizer.SetHGap(5)
        self.skip_process = True
        self.skip_plotting = False
        self.build_display()
        self.skip_process = False

    def show_subframe(self, name, frameclass, **opts):
        shown = False
        if name in self.subframes:
            try:
                self.subframes[name].Raise()
                shown = True
            except:
                del self.subframes[name]
        if not shown:
            self.subframes[name] = frameclass(self, **opts)

    def onPanelExposed(self, **kws):
        # called when notebook is selected
        fname = self.controller.filelist.GetStringSelection()
        if fname in self.controller.file_groups:
            gname = self.controller.file_groups[fname]
            dgroup = self.controller.get_group(gname)
            self.fill_form(dgroup)
            self.process(dgroup=dgroup)

    def write_message(self, msg, panel=0):
        self.controller.write_message(msg, panel=panel)

    def larch_eval(self, cmd):
        """eval"""
        self.command_hist.append(cmd)
        return self.controller.larch.eval(cmd)

    def _plain_larch_eval(self, cmd):
        return self.controller.larch._larch.eval(cmd)

    def get_session_history(self):
        """return full session history"""
        larch = self.controller.larch
        return getattr(larch.input, 'hist_buff',
                       getattr(larch.parent, 'hist_buff', []))

    def larch_get(self, sym):
        """get value from larch symbol table"""
        return self.controller.larch.symtable.get_symbol(sym)

    def build_display(self):
        """build display"""

        self.panel.Add(SimpleText(self.panel, self.title, **titleopts),
                       dcol=7)
        self.panel.Add(SimpleText(self.panel, ' coming soon....'),
                       dcol=7, newrow=True)
        self.panel.pack()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.LEFT|wx.CENTER, 3)
        pack(self, sizer)

    def set_defaultconfig(self, config):
        """set the default configuration for this session"""
        conf = self.controller.larch.symtable._sys.xas_viewer
        setattr(conf, self.configname, {key:val for key, val in config.items()})

    def get_defaultconfig(self):
        """get the default configuration for this session"""
        conf = self.controller.larch.symtable._sys.xas_viewer
        defconf = getattr(conf, self.configname, {})
        return {key:val for key, val in defconf.items()}

    def get_config(self, dgroup=None):
        """get and set processing configuration for a group"""
        if dgroup is None:
            dgroup = self.controller.get_group()
        conf = getattr(dgroup, self.configname, self.get_defaultconfig())
        if dgroup is not None:
            setattr(dgroup, self.configname, conf)
        return conf

    def update_config(self, config, dgroup=None):
        """set/update processing configuration for a group"""
        if dgroup is None:
            dgroup = self.controller.get_group()
        conf = getattr(dgroup, self.configname, self.get_defaultconfig())
        conf.update(config)
        if dgroup is not None:
            setattr(dgroup, self.configname, conf)

    def fill_form(self, dat):
        if isinstance(dat, Group):
            dat = group2dict(dat)

        for name, wid in self.wids.items():
            if isinstance(wid, FloatCtrl) and name in dat:
                wid.SetValue(dat[name])

    def read_form(self):
        "read for, returning dict of values"
        dgroup = self.controller.get_group()
        form_opts = {'groupname': dgroup.groupname}
        for name, wid in self.wids.items():
            val = None
            for method in ('GetValue', 'GetStringSelection', 'IsChecked',
                           'GetLabel'):
                meth = getattr(wid, method, None)
                if callable(meth):
                    try:
                        val = meth()
                    except TypeError:
                        pass
                if val is not None:
                    break
            form_opts[name] = val
        return form_opts

    def process(self, dgroup=None, **kws):
        """override to handle data process step"""
        if self.skip_process:
            return
        self.skip_process = True

    def add_text(self, text, dcol=1, newrow=True):
        self.panel.Add(SimpleText(self.panel, text),
                       dcol=dcol, newrow=newrow)

    def add_floatspin(self, name, value, with_pin=True, relative_e0=False,
                      **kws):
        """create FloatSpin with Pin button for onSelPoint"""
        if with_pin:
            pin_action = partial(self.onSelPoint, opt=name,
                                 relative_e0=relative_e0)
            fspin, bb = FloatSpinWithPin(self.panel, value=value,
                                         pin_action=pin_action, **kws)
        else:
            fspin = FloatSpin(self.panel, value=value, **kws)
            bb = (1, 1)

        self.wids[name] = fspin
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(fspin)
        sizer.Add(bb)
        return sizer

    def onPlot(self, evt=None):
        pass

    def onPlotOne(self, evt=None, dgroup=None, **kws):
        pass

    def onPlotSel(self, evt=None, groups=None, **kws):
        pass

    def onProcess(self, evt=None, **kws):
        pass
                     
    def onPinTimer(self, event=None):
        if 'start' not in self.cursor_dat:
            self.cursor_dat['xsel'] = None
            self.onPinTimerComplete(reason="bad")
           
        curhist_name = self.cursor_dat['name']
        cursor_hist = getattr(self.larch.symtable._plotter, curhist_name, [])
        if len(cursor_hist) > self.cursor_dat['nhist']: # got new data!
            self.cursor_dat['xsel'] = cursor_hist[0][0]
            self.cursor_dat['ysel'] = cursor_hist[0][1]
            if time.time() > 3.0 + self.cursor_dat['start']:
                self.timers['pin'].Stop()
                self.onPinTimerComplete(reason="new")                
        elif time.time() > 15.0 + self.cursor_dat['start']:
            self.onPinTimerComplete(reason="timeout")

        if 'win' in self.cursor_dat and 'xsel' in self.cursor_dat:
            time_remaining = 15+self.cursor_dat['start']-time.time()
            msg = 'Select Point from Plot #%d' % (self.cursor_dat['win'])
            if self.cursor_dat['xsel'] is not None:
                msg = '%s, [current value=%.1f]' % (msg, self.cursor_dat['xsel'])
            msg = '%s, expiring in %.0f sec' % (msg, time_remaining)
            self.write_message(msg)
            
    def onPinTimerComplete(self, reason=None, **kws):
        self.timers['pin'].Stop()
        if reason != "bad":
            msg = 'Selected Point at %.1f' % self.cursor_dat['xsel']        
            if reason == 'timeout':
                msg = msg + '(timed-out)'
            wx.CallAfter(self.write_message, msg)
            
            if self.cursor_dat['xsel'] is not None:
                self.pin_callback(**self.cursor_dat)
            time.sleep(0.05)
        self.cursor_dat = {}
        
    def pin_callback(self, opt='__', xsel=None, relative_e0=False, **kws):
        """
        called to do reprocessing after a point is selected as from Pin / Plot
        """
        if xsel is None or opt not in self.wids:
            return
        if relative_e0 and 'e0' in self.wids:
            xsel -= self.wids['e0'].GetValue()
        self.wids[opt].SetValue(xsel)
        time.sleep(0.01)
        wx.CallAfter(self.onProcess)

    def onSelPoint(self, evt=None, opt='__', relative_e0=True, win=None):    
        """
        get last selected point from a specified plot window
        and fill in the value for the widget defined by `opt`.

        start Pin Timer to get last selected point from a specified plot window
        and fill in the value for the widget defined by `opt`.
        """
        if opt not in self.wids:
            return None
        if win is None:
            win = 1
        display = _getDisplay(win=win, _larch=self.larch)
        display.Raise()
        msg = 'Select Point from Plot #%d' % win
        self.write_message(msg)

        now = time.time()
        curhist_name = 'plot%d_cursor_hist' % win
        cursor_hist = getattr(self.larch.symtable._plotter, curhist_name, [])
       
        self.cursor_dat = dict(relative_e0=relative_e0, opt=opt,
                               start=now, xsel=None, ysel=None,
                               win=win, name=curhist_name,
                               nhist=len(cursor_hist))

        if len(cursor_hist) > 2:  # purge old cursor history
            setattr(self.larch.symtable._plotter, curhist_name, cursor_hist[:2])
            
        if len(cursor_hist) > 0:
            x, y, t = cursor_hist[0]
            if now < (t + 30.0): # last cursor position was less than 30 seconds ago
                self.cursor_dat['xsel'] = x
                self.cursor_dat['ysel'] = y
        self.timers['pin'].Start(500)
