


import os
import stat
import typing

import jk_typing
import jk_prettyprintobj








@typing.final
class DirEntryX(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param	str absBaseDirPath		The base directory of the scanning process
	# @param	str relFilePath			The path of the element relative to the base directory path.
	# @param	os.DirEntry fe			The file entry object.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			nLevel:int,
			absBaseDirPath:str,
			relPath:str,
			fileName:str,
			absPath:str,
			statResult:os.stat_result,
			exception:Exception = None,
		):

		self.absBaseDirPath = absBaseDirPath
		self.nLevel = nLevel
		self.exception = exception
		self.__statResult = statResult
		self.name = fileName
		self.fileName = fileName
		self.path = absPath
		self.absPath = absPath
		self.relPath = relPath
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def isError(self) -> bool:
		return bool(self.exception)
	#

	@property
	def isWalkRoot(self) -> bool:
		return not self.relPath
	#

	@property
	def ctime(self) -> float:
		return self.__statResult.st_ctime
	#

	@property
	def mtime(self) -> float:
		return self.__statResult.st_mtime
	#

	@property
	def uid(self) -> int:
		return self.__statResult.st_uid
	#

	@property
	def gid(self) -> int:
		return self.__statResult.st_gid
	#

	@property
	def size(self) -> int:
		return self.__statResult.st_size
	#

	@property
	def isFile(self) -> bool:
		return stat.S_ISREG(self.__statResult.st_mode)
	#

	@property
	def isDir(self) -> bool:
		return stat.S_ISDIR(self.__statResult.st_mode)
	#

	@property
	def isSymLink(self) -> bool:
		return stat.S_ISLNK(self.__statResult.st_mode)
	#

	@property
	def isBlockDev(self) -> bool:
		return stat.S_ISBLK(self.__statResult.st_mode)
	#

	@property
	def isFIFO(self) -> bool:
		return stat.S_ISFIFO(self.__statResult.st_mode)
	#

	@property
	def isCharDev(self) -> bool:
		return stat.S_ISCHR(self.__statResult.st_mode)
	#

	@property
	def isSock(self) -> bool:
		return stat.S_ISSOCK(self.__statResult.st_mode)
	#

	@property
	def isOther(self) -> bool:
		m = self.__statResult.st_mode
		return not stat.S_ISREG(m) \
			and not stat.S_ISDIR(m) \
			and not stat.S_ISLNK(m) \
			and not stat.S_ISBLK(m) \
			and not stat.S_ISFIFO(m) \
			and not stat.S_ISSOCK(m) \
			and not stat.S_ISCHR(m)
	#

	@property
	def typeStr(self) -> str:
		m = self.__statResult.st_mode
		if stat.S_ISDIR(m):
			return "dir"
		elif stat.S_ISREG(m):
			return "file"
		elif stat.S_ISLNK(m):
			return "symlink"
		elif stat.S_ISBLK(m):
			return "blockdev"
		elif stat.S_ISSOCK(m):
			return "sock"
		elif stat.S_ISFIFO(m):
			return "fifo"
		elif stat.S_ISCHR(m):
			return "chardev"
		else:
			return "other"
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"absFilePath",
			"absBaseDirPath",
			"relFilePath",
			"fileName",
			"typeStr",
			"nLevel",
			"size",
			"uid",
			"gid",
			"ctime",
			"mtime",
			"isFile",
			"isDir",
			"isSymLink",
			"isBlockDev",
			"isCharDev",
			"isFIFO",
			"isSock",
			"isOther",
			"exception",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __repr__(self):
		if self.exception:
			return self.__class__.__name__ + "<( ERROR {}, {}, {} )>".format(self.typeStr, repr(self.relPath), repr(self.exception))
		else:
			return self.__class__.__name__ + "<( {:>8}, {} )>".format(self.typeStr, repr(self.relPath))
	#

	def __str__(self):
		return self.relPath
	#

	def stat(self) -> os.stat_result:
		return self.__statResult
	#

	def is_file(self) -> bool:
		return stat.S_ISREG(self.__statResult.st_mode)
	#

	def is_dir(self) -> bool:
		return stat.S_ISDIR(self.__statResult.st_mode)
	#

	def is_symlink(self) -> bool:
		return stat.S_ISLNK(self.__statResult.st_mode)
	#

	def is_blockDev(self) -> bool:
		return stat.S_ISBLK(self.__statResult.st_mode)
	#

	def is_fifo(self) -> bool:
		return stat.S_ISFIFO(self.__statResult.st_mode)
	#

	def is_charDev(self) -> bool:
		return stat.S_ISCHR(self.__statResult.st_mode)
	#

	def is_sock(self) -> bool:
		return stat.S_ISSOCK(self.__statResult.st_mode)
	#

	def is_other(self) -> bool:
		m = self.__statResult.st_mode
		return not stat.S_ISREG(m) \
			and not stat.S_ISDIR(m) \
			and not stat.S_ISLNK(m) \
			and not stat.S_ISBLK(m) \
			and not stat.S_ISFIFO(m) \
			and not stat.S_ISSOCK(m) \
			and not stat.S_ISCHR(m)
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	def fromOSDirEntry(nLevel:int, absBaseDirPath:str, relPath:str, fe:os.DirEntry, exception:Exception = None):
		return DirEntryX(
			nLevel = nLevel,
			absBaseDirPath = absBaseDirPath,
			relPath = relPath,
			fileName = fe.name,
			absPath = fe.path,
			statResult = fe.stat(follow_symlinks=False),
			exception = exception,
		)
	#

	def fromPath(nLevel:int, absBaseDirPath:str, absFilePath:str):
		if not absBaseDirPath.endswith(os.sep):
			_baseDirPath2 = absBaseDirPath + os.sep
		else:
			_baseDirPath2 = absBaseDirPath

		return DirEntryX(
			nLevel = nLevel,
			absBaseDirPath = absBaseDirPath,
			relPath = absFilePath[len(_baseDirPath2):],
			fileName = os.path.basename(absFilePath),
			absPath = absFilePath,
			statResult = os.stat(absFilePath, follow_symlinks=False),
			exception = None,
		)
	#

#



