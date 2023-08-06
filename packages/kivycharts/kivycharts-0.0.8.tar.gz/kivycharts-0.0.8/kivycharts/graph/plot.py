
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.properties import NumericProperty, BooleanProperty,\
	BoundedNumericProperty, StringProperty, ListProperty, ObjectProperty,\
	DictProperty, AliasProperty
from kivy.clock import Clock
from kivy.graphics import Mesh, Color, Rectangle, Point
from kivy.graphics import Fbo
from kivy.graphics.texture import Texture
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.logger import Logger
from kivy import metrics
from math import log10, floor, ceil
from decimal import Decimal
from itertools import chain
try:
	import numpy as np
except ImportError as e:
	np = None

class Plot(EventDispatcher):
	'''Plot class, see module documentation for more information.

	:Events:
		`on_clear_plot`
			Fired before a plot updates the display and lets the fbo know that
			it should clear the old drawings.

	..versionadded:: 0.4
	'''

	__events__ = ('on_clear_plot', )

	# most recent values of the params used to draw the plot
	params = DictProperty({'xlog': False, 'xmin': 0, 'xmax': 100,
						   'ylog': False, 'ymin': 0, 'ymax': 100,
						   'size': (0, 0, 0, 0)})

	color = ListProperty([1, 1, 1, 1])
	'''Color of the plot.
	'''

	points = ListProperty([])
	'''List of (x, y) points to be displayed in the plot.

	The elements of points are 2-tuples, (x, y). The points are displayed
	based on the mode setting.

	:data:`points` is a :class:`~kivy.properties.ListProperty`, defaults to
	[].
	'''

	x_axis = NumericProperty(0)
	'''Index of the X axis to use, defaults to 0
	'''

	y_axis = NumericProperty(0)
	'''Index of the Y axis to use, defaults to 0
	'''

	def __init__(self, **kwargs):
		super(Plot, self).__init__(**kwargs)
		self.ask_draw = Clock.create_trigger(self.draw)
		self.bind(params=self.ask_draw, points=self.ask_draw)
		self._drawings = self.create_drawings()

	def funcx(self):
		"""Return a function that convert or not the X value according to plot
		prameters"""
		return log10 if self.params["xlog"] else lambda x: x

	def funcy(self):
		"""Return a function that convert or not the Y value according to plot
		prameters"""
		return log10 if self.params["ylog"] else lambda y: y

	def x_px(self):
		"""Return a function that convert the X value of the graph to the
		pixel coordinate on the plot, according to the plot settings and axis
		settings. It's relative to the graph pos.
		"""
		funcx = self.funcx()
		params = self.params
		size = params["size"]
		xmin = funcx(params["xmin"])
		xmax = funcx(params["xmax"])
		ratiox = (size[2] - size[0]) / float(xmax - xmin)
		return lambda x: (funcx(x) - xmin) * ratiox + size[0]

	def y_px(self):
		"""Return a function that convert the Y value of the graph to the
		pixel coordinate on the plot, according to the plot settings and axis
		settings. The returned value is relative to the graph pos.
		"""
		funcy = self.funcy()
		params = self.params
		size = params["size"]
		ymin = funcy(params["ymin"])
		ymax = funcy(params["ymax"])
		ratioy = (size[3] - size[1]) / float(ymax - ymin)
		return lambda y: (funcy(y) - ymin) * ratioy + size[1]

	def unproject(self, x, y):
		"""Return a function that unproject a pixel to a X/Y value on the plot
		(works only for linear, not log yet). `x`, `y`, is relative to the
		graph pos, so the graph's pos needs to be subtracted from x, y before
		passing it in.
		"""
		params = self.params
		size = params["size"]
		xmin = params["xmin"]
		xmax = params["xmax"]
		ymin = params["ymin"]
		ymax = params["ymax"]
		ratiox = (size[2] - size[0]) / float(xmax - xmin)
		ratioy = (size[3] - size[1]) / float(ymax - ymin)
		x0 = (x - size[0]) / ratiox + xmin
		y0 = (y - size[1]) / ratioy + ymin
		return x0, y0

	def get_px_bounds(self):
		"""Returns a dict containing the pixels bounds from the plot parameters.
		 The returned values are relative to the graph pos.
		"""
		params = self.params
		x_px = self.x_px()
		y_px = self.y_px()
		return {
			"xmin": x_px(params["xmin"]),
			"xmax": x_px(params["xmax"]),
			"ymin": y_px(params["ymin"]),
			"ymax": y_px(params["ymax"]),
		}

	def update(self, xlog, xmin, xmax, ylog, ymin, ymax, size):
		'''Called by graph whenever any of the parameters
		change. The plot should be recalculated then.
		log, min, max indicate the axis settings.
		size a 4-tuple describing the bounding box in which we can draw
		graphs, it's (x0, y0, x1, y1), which correspond with the bottom left
		and top right corner locations, respectively.
		'''
		self.params.update({
			'xlog': xlog, 'xmin': xmin, 'xmax': xmax, 'ylog': ylog,
			'ymin': ymin, 'ymax': ymax, 'size': size})

	def get_group(self):
		'''returns a string which is unique and is the group name given to all
		the instructions returned by _get_drawings. Graph uses this to remove
		these instructions when needed.
		'''
		return ''

	def get_drawings(self):
		'''returns a list of canvas instructions that will be added to the
		graph's canvas.
		'''
		if isinstance(self._drawings, (tuple, list)):
			return self._drawings
		return []

	def create_drawings(self):
		'''called once to create all the canvas instructions needed for the
		plot
		'''
		pass

	def draw(self, *largs):
		'''draw the plot according to the params. It dispatches on_clear_plot
		so derived classes should call super before updating.
		'''
		self.dispatch('on_clear_plot')

	def iterate_points(self):
		'''Iterate on all the points adjusted to the graph settings
		'''
		x_px = self.x_px()
		y_px = self.y_px()
		for x, y in self.points:
			yield x_px(x), y_px(y)

	def on_clear_plot(self, *largs):
		pass

	# compatibility layer
	_update = update
	_get_drawings = get_drawings
	_params = params


class MeshLinePlot(Plot):
	'''MeshLinePlot class which displays a set of points similar to a mesh.
	'''

	def _set_mode(self, value):
		if hasattr(self, '_mesh'):
			self._mesh.mode = value

	mode = AliasProperty(lambda self: self._mesh.mode, _set_mode)
	'''VBO Mode used for drawing the points. Can be one of: 'points',
	'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'.
	See :class:`~kivy.graphics.Mesh` for more details.

	Defaults to 'line_strip'.
	'''

	def create_drawings(self):
		self._color = Color(*self.color)
		self._mesh = Mesh(mode='line_strip')
		self.bind(
			color=lambda instr, value: setattr(self._color, "rgba", value))
		return [self._color, self._mesh]

	def draw(self, *args):
		super(MeshLinePlot, self).draw(*args)
		self.plot_mesh()

	def plot_mesh(self):
		points = [p for p in self.iterate_points()]
		mesh, vert, _ = self.set_mesh_size(len(points))
		for k, (x, y) in enumerate(points):
			vert[k * 4] = x
			vert[k * 4 + 1] = y
		mesh.vertices = vert

	def set_mesh_size(self, size):
		mesh = self._mesh
		vert = mesh.vertices
		ind = mesh.indices
		diff = size - len(vert) // 4
		if diff < 0:
			del vert[4 * size:]
			del ind[size:]
		elif diff > 0:
			ind.extend(range(len(ind), len(ind) + diff))
			vert.extend([0] * (diff * 4))
		mesh.vertices = vert
		return mesh, vert, ind


class MeshStemPlot(MeshLinePlot):
	'''MeshStemPlot uses the MeshLinePlot class to draw a stem plot. The data
	provided is graphed from origin to the data point.
	'''

	def plot_mesh(self):
		points = [p for p in self.iterate_points()]
		mesh, vert, _ = self.set_mesh_size(len(points) * 2)
		y0 = self.y_px()(0)
		for k, (x, y) in enumerate(self.iterate_points()):
			vert[k * 8] = x
			vert[k * 8 + 1] = y0
			vert[k * 8 + 4] = x
			vert[k * 8 + 5] = y
		mesh.vertices = vert


class LinePlot(Plot):
	"""LinePlot draws using a standard Line object.
	"""

	line_width = NumericProperty(1)

	def create_drawings(self):
		from kivy.graphics import Line, RenderContext

		self._grc = RenderContext(
				use_parent_modelview=True,
				use_parent_projection=True)
		with self._grc:
			self._gcolor = Color(*self.color)
			self._gline = Line(
				points=[], cap='none',
				width=self.line_width, joint='round')

		return [self._grc]

	def draw(self, *args):
		super(LinePlot, self).draw(*args)
		# flatten the list
		points = []
		for x, y in self.iterate_points():
			points += [x, y]
		self._gline.points = points

	def on_line_width(self, *largs):
		if hasattr(self, "_gline"):
			self._gline.width = self.line_width


class SmoothLinePlot(Plot):
	'''Smooth Plot class, see module documentation for more information.
	This plot use a specific Fragment shader for a custom anti aliasing.
	'''

	SMOOTH_FS = '''
	$HEADER$

	void main(void) {
		float edgewidth = 0.015625 * 64.;
		float t = texture2D(texture0, tex_coord0).r;
		float e = smoothstep(0., edgewidth, t);
		gl_FragColor = frag_color * vec4(1, 1, 1, e);
	}
	'''

	# XXX This gradient data is a 64x1 RGB image, and
	# values goes from 0 -> 255 -> 0.
	GRADIENT_DATA = (
		b"\x00\x00\x00\x07\x07\x07\x0f\x0f\x0f\x17\x17\x17\x1f\x1f\x1f"
		b"'''///777???GGGOOOWWW___gggooowww\x7f\x7f\x7f\x87\x87\x87"
		b"\x8f\x8f\x8f\x97\x97\x97\x9f\x9f\x9f\xa7\xa7\xa7\xaf\xaf\xaf"
		b"\xb7\xb7\xb7\xbf\xbf\xbf\xc7\xc7\xc7\xcf\xcf\xcf\xd7\xd7\xd7"
		b"\xdf\xdf\xdf\xe7\xe7\xe7\xef\xef\xef\xf7\xf7\xf7\xff\xff\xff"
		b"\xf6\xf6\xf6\xee\xee\xee\xe6\xe6\xe6\xde\xde\xde\xd5\xd5\xd5"
		b"\xcd\xcd\xcd\xc5\xc5\xc5\xbd\xbd\xbd\xb4\xb4\xb4\xac\xac\xac"
		b"\xa4\xa4\xa4\x9c\x9c\x9c\x94\x94\x94\x8b\x8b\x8b\x83\x83\x83"
		b"{{{sssjjjbbbZZZRRRJJJAAA999111)))   \x18\x18\x18\x10\x10\x10"
		b"\x08\x08\x08\x00\x00\x00")

	def create_drawings(self):
		from kivy.graphics import Line, RenderContext

		# very first time, create a texture for the shader
		if not hasattr(SmoothLinePlot, '_texture'):
			tex = Texture.create(size=(1, 64), colorfmt='rgb')
			tex.add_reload_observer(SmoothLinePlot._smooth_reload_observer)
			SmoothLinePlot._texture = tex
			SmoothLinePlot._smooth_reload_observer(tex)

		self._grc = RenderContext(
			fs=SmoothLinePlot.SMOOTH_FS,
			use_parent_modelview=True,
			use_parent_projection=True)
		with self._grc:
			self._gcolor = Color(*self.color)
			self._gline = Line(
				points=[], cap='none', width=2.,
				texture=SmoothLinePlot._texture)

		return [self._grc]

	@staticmethod
	def _smooth_reload_observer(texture):
		texture.blit_buffer(SmoothLinePlot.GRADIENT_DATA, colorfmt="rgb")

	def draw(self, *args):
		super(SmoothLinePlot, self).draw(*args)
		# flatten the list
		points = []
		for x, y in self.iterate_points():
			points += [x, y]
		self._gline.points = points


class ContourPlot(Plot):
	"""
	ContourPlot visualizes 3 dimensional data as an intensity map image.
	The user must first specify 'xrange' and 'yrange' (tuples of min,max) and
	then 'data', the intensity values.
	`data`, is a MxN matrix, where the first dimension of size M specifies the
	`y` values, and the second dimension of size N specifies the `x` values.
	Axis Y and X values are assumed to be linearly spaced values from
	xrange/yrange and the dimensions of 'data', `MxN`, respectively.
	The color values are automatically scaled to the min and max z range of the
	data set.
	"""
	_image = ObjectProperty(None)
	data = ObjectProperty(None, force_dispatch=True)
	xrange = ListProperty([0, 100])
	yrange = ListProperty([0, 100])

	def __init__(self, **kwargs):
		super(ContourPlot, self).__init__(**kwargs)
		self.bind(data=self.ask_draw, xrange=self.ask_draw,
				  yrange=self.ask_draw)

	def create_drawings(self):
		self._image = Rectangle()
		self._color = Color([1, 1, 1, 1])
		self.bind(
			color=lambda instr, value: setattr(self._color, 'rgba', value))
		return [self._color, self._image]

	def draw(self, *args):
		super(ContourPlot, self).draw(*args)
		data = self.data
		xdim, ydim = data.shape

		# Find the minimum and maximum z values
		zmax = data.max()
		zmin = data.min()
		rgb_scale_factor = 1.0 / (zmax - zmin) * 255
		# Scale the z values into RGB data
		buf = np.array(data, dtype=float, copy=True)
		np.subtract(buf, zmin, out=buf)
		np.multiply(buf, rgb_scale_factor, out=buf)
		# Duplicate into 3 dimensions (RGB) and convert to byte array
		buf = np.asarray(buf, dtype=np.uint8)
		buf = np.expand_dims(buf, axis=2)
		buf = np.concatenate((buf, buf, buf), axis=2)
		buf = np.reshape(buf, (xdim, ydim, 3))

		charbuf = bytearray(np.reshape(buf, (buf.size)))
		self._texture = Texture.create(size=(xdim, ydim), colorfmt='rgb')
		self._texture.blit_buffer(charbuf, colorfmt='rgb', bufferfmt='ubyte')
		image = self._image
		image.texture = self._texture

		x_px = self.x_px()
		y_px = self.y_px()
		bl = x_px(self.xrange[0]), y_px(self.yrange[0])
		tr = x_px(self.xrange[1]), y_px(self.yrange[1])
		image.pos = bl
		w = tr[0] - bl[0]
		h = tr[1] - bl[1]
		image.size = (w, h)


class BarPlot(Plot):
	'''BarPlot class which displays a bar graph.
	'''

	bar_width = NumericProperty(1)
	bar_spacing = NumericProperty(1.)
	graph = ObjectProperty(allownone=True)

	def __init__(self, *ar, **kw):
		super(BarPlot, self).__init__(*ar, **kw)
		self.bind(bar_width=self.ask_draw)
		self.bind(points=self.update_bar_width)
		self.bind(graph=self.update_bar_width)

	def update_bar_width(self, *ar):
		if not self.graph:
			return
		if len(self.points) < 2:
			return
		if self.graph.xmax == self.graph.xmin:
			return

		point_width = (
			len(self.points) *
			float(abs(self.graph.xmax) + abs(self.graph.xmin)) /
			float(abs(max(self.points)[0]) + abs(min(self.points)[0])))

		if not self.points:
			self.bar_width = 1
		else:
			self.bar_width = (
				(self.graph.width - self.graph.padding) /
				point_width * self.bar_spacing)

	def create_drawings(self):
		self._color = Color(*self.color)
		self._mesh = Mesh()
		self.bind(
			color=lambda instr, value: setattr(self._color, 'rgba', value))
		return [self._color, self._mesh]

	def draw(self, *args):
		super(BarPlot, self).draw(*args)
		points = self.points

		# The mesh only supports (2^16) - 1 indices, so...
		if len(points) * 6 > 65535:
			Logger.error(
				"BarPlot: cannot support more than 10922 points. "
				"Ignoring extra points.")
			points = points[:10922]

		point_len = len(points)
		mesh = self._mesh
		mesh.mode = 'triangles'
		vert = mesh.vertices
		ind = mesh.indices
		diff = len(points) * 6 - len(vert) // 4
		if diff < 0:
			del vert[24 * point_len:]
			del ind[point_len:]
		elif diff > 0:
			ind.extend(range(len(ind), len(ind) + diff))
			vert.extend([0] * (diff * 4))

		bounds = self.get_px_bounds()
		x_px = self.x_px()
		y_px = self.y_px()
		ymin = y_px(0)

		bar_width = self.bar_width
		if bar_width < 0:
			bar_width = x_px(bar_width) - bounds["xmin"]

		for k in range(point_len):
			p = points[k]
			x1 = x_px(p[0])
			x2 = x1 + bar_width
			y1 = ymin
			y2 = y_px(p[1])

			idx = k * 24
			# first triangle
			vert[idx] = x1
			vert[idx + 1] = y2
			vert[idx + 4] = x1
			vert[idx + 5] = y1
			vert[idx + 8] = x2
			vert[idx + 9] = y1
			# second triangle
			vert[idx + 12] = x1
			vert[idx + 13] = y2
			vert[idx + 16] = x2
			vert[idx + 17] = y2
			vert[idx + 20] = x2
			vert[idx + 21] = y1
		mesh.vertices = vert

	def _unbind_graph(self, graph):
		graph.unbind(width=self.update_bar_width,
					 xmin=self.update_bar_width,
					 ymin=self.update_bar_width)

	def bind_to_graph(self, graph):
		old_graph = self.graph

		if old_graph:
			# unbind from the old one
			self._unbind_graph(old_graph)

		# bind to the new one
		self.graph = graph
		graph.bind(width=self.update_bar_width,
				   xmin=self.update_bar_width,
				   ymin=self.update_bar_width)

	def unbind_from_graph(self):
		if self.graph:
			self._unbind_graph(self.graph)


class HBar(MeshLinePlot):
	'''HBar draw horizontal bar on all the Y points provided
	'''

	def plot_mesh(self, *args):
		points = self.points
		mesh, vert, ind = self.set_mesh_size(len(points) * 2)
		mesh.mode = "lines"

		bounds = self.get_px_bounds()
		px_xmin = bounds["xmin"]
		px_xmax = bounds["xmax"]
		y_px = self.y_px()
		for k, y in enumerate(points):
			y = y_px(y)
			vert[k * 8] = px_xmin
			vert[k * 8 + 1] = y
			vert[k * 8 + 4] = px_xmax
			vert[k * 8 + 5] = y
		mesh.vertices = vert


class VBar(MeshLinePlot):
	'''VBar draw vertical bar on all the X points provided
	'''

	def plot_mesh(self, *args):
		points = self.points
		mesh, vert, ind = self.set_mesh_size(len(points) * 2)
		mesh.mode = "lines"

		bounds = self.get_px_bounds()
		px_ymin = bounds["ymin"]
		px_ymax = bounds["ymax"]
		x_px = self.x_px()
		for k, x in enumerate(points):
			x = x_px(x)
			vert[k * 8] = x
			vert[k * 8 + 1] = px_ymin
			vert[k * 8 + 4] = x
			vert[k * 8 + 5] = px_ymax
		mesh.vertices = vert


class ScatterPlot(Plot):
	"""
	ScatterPlot draws using a standard Point object.
	The pointsize can be controlled with :attr:`point_size`.

	>>> plot = ScatterPlot(color=[1, 0, 0, 1], point_size=5)
	"""

	point_size = NumericProperty(1)
	"""The point size of the scatter points. Defaults to 1.
	"""

	def create_drawings(self):
		from kivy.graphics import Point, RenderContext

		self._points_context = RenderContext(
				use_parent_modelview=True,
				use_parent_projection=True)
		with self._points_context:
			self._gcolor = Color(*self.color)
			self._gpts = Point(points=[], pointsize=self.point_size)

		return [self._points_context]

	def draw(self, *args):
		super(ScatterPlot, self).draw(*args)
		# flatten the list
		self._gpts.points = list(chain(*self.iterate_points()))

	def on_point_size(self, *largs):
		if hasattr(self, "_gpts"):
			self._gpts.pointsize = self.point_size


class PointPlot(Plot):
	'''Displays a set of points.
	'''

	point_size = NumericProperty(1)
	'''
	Defaults to 1.
	'''

	_color = None

	_point = None

	def __init__(self, **kwargs):
		super(PointPlot, self).__init__(**kwargs)

		def update_size(*largs):
			if self._point:
				self._point.pointsize = self.point_size
		self.fbind('point_size', update_size)

		def update_color(*largs):
			if self._color:
				self._color.rgba = self.color
		self.fbind('color', update_color)

	def create_drawings(self):
		self._color = Color(*self.color)
		self._point = Point(pointsize=self.point_size)
		return [self._color, self._point]

	def draw(self, *args):
		super(PointPlot, self).draw(*args)
		self._point.points = [v for p in self.iterate_points() for v in p]


if __name__ == '__main__':
	import itertools
	from math import sin, cos, pi
	from random import randrange
	from kivy.utils import get_color_from_hex as rgb
	from kivy.uix.boxlayout import BoxLayout
	from kivy.app import App

	class TestApp(App):

		def build(self):
			b = BoxLayout(orientation='vertical')
			# example of a custom theme
			colors = itertools.cycle([
				rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])
			graph_theme = {
				'label_options': {
					'color': rgb('444444'),  # color of tick labels and titles
					'bold': True},
				'background_color': rgb('f8f8f2'),  # canvas background color
				'tick_color': rgb('808080'),  # ticks and grid
				'border_color': rgb('808080')}  # border drawn around each graph

			graph = Graph(
				xlabel='Cheese',
				ylabel='Apples',
				x_ticks_minor=5,
				x_ticks_major=25,
				y_ticks_major=1,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				xmin=-50,
				xmax=50,
				ymin=-1,
				ymax=1,
				**graph_theme)

			plot = SmoothLinePlot(color=next(colors))
			plot.points = [(x / 10., sin(x / 50.)) for x in range(-500, 501)]
			# for efficiency, the x range matches xmin, xmax
			graph.add_plot(plot)

			plot = MeshLinePlot(color=next(colors))
			plot.points = [(x / 10., cos(x / 50.)) for x in range(-500, 501)]
			graph.add_plot(plot)
			self.plot = plot  # this is the moving graph, so keep a reference

			plot = MeshStemPlot(color=next(colors))
			graph.add_plot(plot)
			plot.points = [(x, x / 50.) for x in range(-50, 51)]

			plot = BarPlot(color=next(colors), bar_spacing=.72)
			graph.add_plot(plot)
			plot.bind_to_graph(graph)
			plot.points = [(x, .1 + randrange(10) / 10.) for x in range(-50, 1)]

			Clock.schedule_interval(self.update_points, 1 / 60.)

			graph2 = Graph(
				xlabel='Position (m)',
				ylabel='Time (s)',
				x_ticks_minor=0,
				x_ticks_major=1,
				y_ticks_major=10,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				xmin=0,
				ymin=0,
				**graph_theme)
			b.add_widget(graph)

			if np is not None:
				(xbounds, ybounds, data) = self.make_contour_data()
				# This is required to fit the graph to the data extents
				graph2.xmin, graph2.xmax = xbounds
				graph2.ymin, graph2.ymax = ybounds

				plot = ContourPlot()
				plot.data = data
				plot.xrange = xbounds
				plot.yrange = ybounds
				plot.color = [1, 0.7, 0.2, 1]
				graph2.add_plot(plot)

				b.add_widget(graph2)
				self.contourplot = plot

				Clock.schedule_interval(self.update_contour, 1 / 60.)

			# Test the scatter plot
			plot = ScatterPlot(color=next(colors), point_size=5)
			graph.add_plot(plot)
			plot.points = [(x, .1 + randrange(10) / 10.) for x in range(-50, 1)]
			return b

		def make_contour_data(self, ts=0):
			omega = 2 * pi / 30
			k = (2 * pi) / 2.0

			ts = sin(ts * 2) + 1.5  # emperically determined 'pretty' values
			npoints = 100
			data = np.ones((npoints, npoints))

			position = [ii * 0.1 for ii in range(npoints)]
			time = [(ii % 100) * 0.6 for ii in range(npoints)]

			for ii, t in enumerate(time):
				for jj, x in enumerate(position):
					data[ii, jj] = sin(
						k * x + omega * t) + sin(-k * x + omega * t) / ts
			return (0, max(position)), (0, max(time)), data

		def update_points(self, *args):
			self.plot.points = [
				(x / 10., cos(Clock.get_time() + x / 50.))
				for x in range(-500, 501)]

		def update_contour(self, *args):
			_, _, self.contourplot.data[:] = self.make_contour_data(
				Clock.get_time())
			# this does not trigger an update, because we replace the
			# values of the arry and do not change the object.
			# However, we cannot do "...data = make_contour_data()" as
			# kivy will try to check for the identity of the new and
			# old values.  In numpy, 'nd1 == nd2' leads to an error
			# (you have to use np.all).  Ideally, property should be patched
			# for this.
			self.contourplot.ask_draw()

	TestApp().run()
