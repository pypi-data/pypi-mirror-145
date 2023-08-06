from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from .kpath import kpath
import os
class mma:
    """Usage:
    >>> from pywmma import mma
    >>> with mma("YOUR_PATH\\WolframKernel.exe") as Eval:
    ...     print(Eval("a=1;1+a"))
    ... 
    2
    >>> """
    def __init__(self,kernel=kpath):
        if kernel==None:
            raise Exception("No kernel path given!")
        elif kernel!=kpath:
            with open(os.path.join(os.path.dirname(__file__),"kpath.py"),"w",encoding="utf-8") as f:
                f.write("kpath="+repr(kernel))
        self.session=WolframLanguageSession(kernel)
        self.wl=wl
        pass
    def __enter__(self):
        self.session.start()
        return lambda expr:self.session.evaluate(wlexpr(expr))
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.stop()

if __name__=="__main__":
    with mma() as Eval:
        print(Eval("3*78"))