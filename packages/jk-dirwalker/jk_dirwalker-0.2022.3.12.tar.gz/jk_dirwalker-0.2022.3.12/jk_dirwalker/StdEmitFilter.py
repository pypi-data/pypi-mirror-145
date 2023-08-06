


import os
import typing

import jk_typing

from .DirEntryX import DirEntryX
from .EmitFilter import EmitFilter






class StdEmitFilter(EmitFilter):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self,
			emitWalkRoot:bool = True,
			emitDirectories:bool = True,
			emitRegularFiles:bool = True,
			emitSymLinks:bool = True,
			emitBlockDevices:bool = True,
			emitCharacterDevices:bool = True,
			emitSockets:bool = True,
			emitFIFOs:bool = True,
			emitOthers:bool = True,
			emitErrors:bool = True,
		) -> None:

		super().__init__(
			emitWalkRoot = emitWalkRoot,
			emitErrors = emitErrors,
		)

		self.emitDirectories = emitDirectories
		self.emitRegularFiles = emitRegularFiles
		self.emitSymLinks = emitSymLinks
		self.emitBlockDevices = emitBlockDevices
		self.emitCharacterDevices = emitCharacterDevices
		self.emitSockets = emitSockets
		self.emitFIFOs = emitFIFOs
		self.emitOthers = emitOthers
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"emitWalkRoot",
			"emitDirectories",
			"emitRegularFiles",
			"emitSymLinks",
			"emitBlockDevices",
			"emitCharacterDevices",
			"emitSockets",
			"emitFIFOs",
			"emitOthers",
			"emitErrors",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def checkEmit(self, entry:DirEntryX) -> bool:
		if entry.is_dir():
			if self.emitDirectories:
				return entry
		elif entry.is_file():
			if self.emitRegularFiles:
				return entry
		elif entry.is_symlink():
			if self.emitSymLinks:
				return entry
		elif entry.is_blockDev():
			if self.emitBlockDevices:
				return entry
		elif entry.is_charDev():
			if self.emitCharacterDevices:
				return entry
		elif entry.is_sock():
			if self.emitSockets:
				return entry
		elif entry.is_fifo():
			if self.emitFIFOs:
				return entry
		elif entry.is_other():
			if self.emitOthers:
				return entry
		else:
			entry.dump()
			raise Exception()
	#

	@staticmethod
	def newFromDisabled(
			emitWalkRoot:bool = False,
			emitDirectories:bool = False,
			emitRegularFiles:bool = False,
			emitSymLinks:bool = False,
			emitBlockDevices:bool = False,
			emitCharacterDevices:bool = False,
			emitSockets:bool = False,
			emitFIFOs:bool = False,
			emitOthers:bool = False,
			emitErrors:bool = False,
		):

		return StdEmitFilter(
			emitWalkRoot = emitWalkRoot,
			emitDirectories = emitDirectories,
			emitRegularFiles = emitRegularFiles,
			emitSymLinks = emitSymLinks,
			emitBlockDevices = emitBlockDevices,
			emitCharacterDevices = emitCharacterDevices,
			emitSockets = emitSockets,
			emitFIFOs = emitFIFOs,
			emitOthers = emitOthers,
			emitErrors = emitErrors,
		)
	#

#







