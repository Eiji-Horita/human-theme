#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os, sys


class TestWin(Gtk.ApplicationWindow):

	def __init__(self, app, color):
		super().__init__(name='test', application=app)
		name = 'test-40f4o'

		css = Gtk.CssProvider()
		css.load_from_data(f'@define-color {name} {color};'.encode())
		Gtk.StyleContext.add_provider_for_screen(
			self.get_screen(), css,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION )

		color = self.get_style_context().lookup_color(name)
		assert color[0], f'Test-color {name!r} lookup failed'
		r, g, b, a = (round(c * 255) for c in color[1])
		color_str = f'#{r:02x}{g:02x}{b:02x}'
		if a != 255: color_str += f'{a:02x}'
		print(color_str)


class TestApp(Gtk.Application):

	def __init__(self, color):
		super().__init__()
		self.color = color

	def do_activate(self):
		win = TestWin(self, self.color)
		self.quit()


def main(args=None):
	import argparse
	parser = argparse.ArgumentParser(
		description='Translate specified color via GTK3 CSS system to #RRGGBB[AA] value.')
	parser.add_argument('color',
		help='GTK3 color specification. Can include any color expressions or theme color refs.')
	opts = parser.parse_args(sys.argv[1:] if args is None else args)
	TestApp(opts.color).run()


if __name__ == '__main__':
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	sys.exit(main())
