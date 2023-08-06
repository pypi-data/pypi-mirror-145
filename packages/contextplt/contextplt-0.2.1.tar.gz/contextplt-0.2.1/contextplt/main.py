from typing import Union, Optional, List, Dict, Tuple, Any

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.dates as mdates

class Single():
    """Create one figure. Adjust figure with arguments. 

    Examples: 
        Basic usage. 

        >>> import contextplt
        >>> x = [1,2,3]
        >>> y = [1,2,3]
        >>> with contextplt.Single() as p:
        >>>     p.ax.plot(x,y)

        With parameter version.

        >>> with contextplt.Single(xlim=[0,5], ylim=[0,5], xlabel="xlabel", ylabel="ylabel",
        ...         title="title", figsize=(6,6), dpi=150) as p:
        >>>     p.ax.plot(x,y)

        Can use variadic keyword arguments to share the same keyword arguments. 

        >>> kargs = dict(xlim=[0,5], ylim=[0,5], xlabel="xlabel", ylabel="ylabel",
        ...         title="title", figsize=(6,6), dpi=150)
        >>> with contextplt.Single(**kargs) as p:
        >>>     p.ax.plot(x,y)
    """
    def __init__(
        self, 
        xlim : Optional[List[float]] = None, 
        ylim : Optional[List[float]] = None, 
        xlabel : Optional[str] = None, 
        ylabel : Optional[str] = None,
        xlabelfontsize : Optional[float] = None,
        ylabelfontsize : Optional[float] = None,
        xtickfontsize : Optional[float] = None,
        ytickfontsize : Optional[float] = None,
        title : Optional[str] =None,
        titlefontsize : Optional[float] = None,
        tight : bool =True,
        rotation : Optional[int] = None, 
        save_path : Optional[str] =None, 
        figsize : Tuple[float, float] =(5,3), 
        dpi : int =150,
        savefig_kargs : dict = {}
    ):
        """Set various parameters. 

        Attributes:
            ax : axis. 
            save_path (str) : path to save.
            title (str) : title.
            tight (bool) : tight_layout or not.
        """
        vars_ = locals()
        for k,v in vars_.items():
            setattr(self, k, v)

        self.fig = plt.figure(figsize=figsize,dpi=dpi)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xlim(xlim) if xlim else None
        self.ax.set_ylim(ylim) if ylim else None

    def __enter__(self):
        return(self)

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.option()

        self.ax.set_xlabel(self.xlabel, fontsize=self.xlabelfontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.ylabelfontsize)
        self.ax.tick_params(axis='x', which='major', labelsize=self.xtickfontsize, 
                            rotation=self.rotation)
        self.ax.tick_params(axis='y', which='major', labelsize=self.ytickfontsize)
        plt.title(self.title, fontsize=self.titlefontsize)
        plt.tight_layout() if self.tight else None
        if self.save_path:
            plt.savefig(self.save_path, **self.savefig_kargs)
        plt.show()

    def option(self):
        '''This method is for additional graphic setting. 
        See DatePlot for example.'''
        pass

class Date(Single):
    def __init__(self,rotation=90,x_fontsize=10,**kargs):
        super().__init__(**kargs)
        self.rotation = rotation
        self.x_fontsize = x_fontsize

    def option(self):
        self.ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=1, tz=None))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=self.rotation,fontsize=self.x_fontsize)

class Multiple():
    """Create multiple figures in one picture with arguments. 

    Examples:
        Basic usage. 
        
        >>> import numpy as np
        >>> import contextplt
        >>> x1, x2, y1, y2= np.random.rand(4, 100)
        >>> with contextplt.Single(grid=(2,1),figsize=(4,4), dpi=150) as p:
        >>>     ax = p.set_ax(1, title="title1")
        >>>     ax.plot(x1,y1)
        >>>     ax = p.set_ax(2, title="title2")
        >>>     ax.plot(x2,y2)

        Various options. Label_outer only leaves the outside of ticks and labels. 

        >>> with contextplt.Single(grid=(2,2),figsize=(6,4), dpi=150,
        ...         suptitle="super title", label_outer=True) as p:
        >>>     for i in range(4):
        >>>         ax = p.set_ax(i + 1, xlabel=f"xlabel{i+1}", ylabel=f"ylabel{i+1}")
        >>>         x, y = np.random.rand(2,100)
        >>>         ax.plot(x,y)
    """
    def __init__(self, figsize=(8,6), dpi=150,grid=(2,2) ,suptitle="",
            save_path=None,show=True, tight=True, label_outer=False,
            savefig_kargs : dict = {}):
        self.fig = plt.figure(figsize=figsize,dpi=dpi)
        self.grid = grid
        self.save_path = save_path
        self.show = show
        self.tight = tight
        self.label_outer = label_outer
        self.savefig_kargs = savefig_kargs

        plt.suptitle(suptitle)

    def set_ax(self,index,xlim=None, ylim=None, 
               xlabel="", ylabel="",title="", rotation : int = 0):
        """Return axis object. 

        Args: 
            index (int) : index of which axes object is pointed at. 
        """
        ax = self.fig.add_subplot(*self.grid,index)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim) if xlim else None
        ax.set_ylim(ylim) if ylim else None
        ax.set_title(title)
        plt.xticks(rotation=rotation)
        return(ax)

    def __enter__(self):
        return(self)

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.option()
        if self.label_outer:
            for ax in self.fig.get_axes():
                ax.label_outer()
        plt.tight_layout() if self.tight else None
        plt.savefig(self.save_path, **self.savefig_kargs) if self.save_path else None
        plt.show() if self.show else None

    def option(self):
        """This method is for additional graphic setting. 
        See DatePlot for example."""
        pass


