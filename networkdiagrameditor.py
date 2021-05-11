
# Copyright 2021 Alekz.Net <alekz.net@gmail.com>
# (Pretty much copied from diagrameditor.py)


from zim.plugins import PluginClass
from zim.plugins.base.imagegenerator import ImageGeneratorClass, BackwardImageGeneratorObjectType

from zim.fs import File, TmpFile
from zim.applications import Application, ApplicationError
import os.path


# TODO put these commands in preferences
font="/usr/share/fonts/truetype/msttcorefonts/arial.ttf"
if os.path.exists(font):
	diagcmd = ('nwdiag', '-a', '--font='+font, '-o')
else:
	diagcmd = ('nwdiag', '-a', '-o')

class InsertSequenceDiagramPlugin(PluginClass):

	plugin_info = {
		'name': _('Insert Network Diagram'), # T: plugin name
		'description': _('''\
This plugin provides a network diagram editor for zim based on nwdiag.
It allows easy editing of network diagrams.
'''), # T: plugin description
		'help': 'Plugins:Network Diagram Editor',
		'author': 'Alekz.Net',
	}

	@classmethod
	def check_dependencies(klass):
		has_diagcmd = Application(diagcmd).tryexec()
		return has_diagcmd, [("nwdiag", has_diagcmd, True)]


class BackwardSequenceDiagramImageObjectType(BackwardImageGeneratorObjectType):

	name = 'image+nwdiagram'
	label = _('Network Diagram') # T: menu item
	syntax = None
	scriptname = 'nwdiagram.diag'
	imagefile_extension = '.png'


class SequenceDiagramGenerator(ImageGeneratorClass):

	def __init__(self, plugin, notebook, page):
		ImageGeneratorClass.__init__(self, plugin, notebook, page)
		self.diagfile = TmpFile('nwdiagram.diag')
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
