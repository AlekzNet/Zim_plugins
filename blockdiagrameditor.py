# Copyright 2021 Alekz.Net <alekz.net@gmail.com>
# (Pretty much copied from diagrameditor.py)


from zim.plugins import PluginClass
from zim.plugins.base.imagegenerator import ImageGeneratorClass, BackwardImageGeneratorObjectType

from zim.fs import File, TmpFile
from zim.applications import Application, ApplicationError


# TODO put these commands in preferences
diagcmd = ('blockdiag', '-a', '--font=/usr/share/fonts/truetype/msttcorefonts/arial.ttf', '-o')


class InsertSequenceDiagramPlugin(PluginClass):

	plugin_info = {
		'name': _('Insert Block Diagram'), # T: plugin name
		'description': _('''\
This plugin provides a block diagram editor for zim based on blockdiag.
It allows easy editing of network diagrams.
'''), # T: plugin description
		'help': 'Plugins:Block Diagram Editor',
		'author': 'Alekz.Net',
	}

	@classmethod
	def check_dependencies(klass):
		has_diagcmd = Application(diagcmd).tryexec()
		return has_diagcmd, [("blockdiag", has_diagcmd, True)]


class BackwardSequenceDiagramImageObjectType(BackwardImageGeneratorObjectType):

	name = 'image+blockdiagram'
	label = _('Block Diagram') # T: menu item
	syntax = None
	scriptname = 'blockdiagram.diag'
	imagefile_extension = '.png'


class SequenceDiagramGenerator(ImageGeneratorClass):

	def __init__(self, plugin, notebook, page):
		ImageGeneratorClass.__init__(self, plugin, notebook, page)
		self.diagfile = TmpFile('blockdiagram.diag')
		self.diagfile.touch()
		self.pngfile = File(self.diagfile.path[:-5] + '.png') # len('.diag') == 5

	def generate_image(self, text):
		# Write to tmp file
		self.diagfile.write(text)

		# Call seqdiag
		try:
			diag = Application(diagcmd)
			diag.run((self.pngfile, self.diagfile))
		except ApplicationError:
			return None, None # Sorry, no log
		else:
			return self.pngfile, None

	def cleanup(self):
		self.diagfile.remove()
		self.pngfile.remove()
