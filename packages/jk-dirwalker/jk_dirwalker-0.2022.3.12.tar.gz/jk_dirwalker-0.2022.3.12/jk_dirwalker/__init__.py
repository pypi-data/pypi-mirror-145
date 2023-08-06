


__version__ = "0.2022.3.12"



from .DirEntryX import DirEntryX
from .DescendFilter import DescendFilter
from .EmitFilter import EmitFilter
from .StdEmitFilter import StdEmitFilter

from .DirWalker import DirWalker



def scandir(
		dirPath:str,
		*,
		emitFilter:EmitFilter = None,
		descendFilter:DescendFilter = None,
	):
	yield from DirWalker(
		emitFilter=emitFilter,
		descendFilter=descendFilter,
	).scandir(dirPath)
#

def listdir(
		dirPath:str,
		*,
		emitFilter:EmitFilter = None,
		descendFilter:DescendFilter = None,
	):
	yield from DirWalker(
		emitFilter=emitFilter,
		descendFilter=descendFilter,
	).listdir(dirPath)
#



