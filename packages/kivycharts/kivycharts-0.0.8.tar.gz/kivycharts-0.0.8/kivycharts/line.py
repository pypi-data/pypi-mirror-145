from kivy.properties import DictProperty, ListProperty, \
		StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.utils import get_color_from_hex as rgb

from kivyblocks.scrollpanel import ScrollPanel
from kivyblocks.utils import SUPER, CSize
from kivyblocks.threadcall import HttpClient
from kivyblocks.baseWidget import VBox

from .graph import Graph
from .graph import Plot, LinePlot, SmoothLinePlot

build_plots = {
	'fold-line':LinePlot,
	'smooth-line':SmoothLinePlot
}

class LineChart(VBox):
	"""
	series = [
		{
			yfield:xxxx,
			charttype:smooth-line, fold-line, ...
			color:
		}
	]
	"""
	dataurl = StringProperty(None)
	params = DictProperty({})
	method = StringProperty('get')
	xlabel = StringProperty(None)
	ylabel = StringProperty(None)
	xfield = StringProperty(None)
	x_ticks_angle = NumericProperty(45)
	series = ListProperty(None)
	data = ListProperty(None)
	def __init__(self, **kw):
		self.graph = None
		SUPER(LineChart, self, kw)

	def on_dataurl(self, o, url=None):
		if not self.dataurl:
			return
		hc = HttpClient()
		x = hc(self.dataurl,
				method=self.method,
				params=self.params)
		self.data = x['rows']
		self.url_call = True

	def on_params(self, o, params=None):
		if not self.url_call:
			return
		self.on_dataurl(None, None)

	def build_plot(self, serie):
		type = serie.get('charttype', 'smooth-line')
		plotKlass = build_plots.get(type)
		p = plotKlass(color=serie['color'])
		return p

	def on_data(self, o, data=None):
		graph_theme = {
			'label_options': {
				'color': rgb('444444'),  # color of tick labels and titles
				'bold': True},
			'background_color': rgb('f8f8f2'),  # canvas background color
			'tick_color': rgb('808080'),  # ticks and grid
			'border_color': rgb('808080')}  # border drawn around each graph

		xcnt = len(self.data)
		ymin, ymax = 9999999999999999, 0
		xlabel_text = [ r.get(self.xfield) for r in self.data ]
		xlabel_text.insert(0,'0')
		for s in self.series:
			points = [ (i, r.get(s['yfield'])) \
							for i,r in enumerate(self.data) ]
			min1 = min([p[1] for p in points])
			max1 = max([p[1] for p in points])
			if max1 >ymax:
				ymax = max1
			if min1 < ymin:
				ymin = min1
			s['points'] = points
		yadd = int((ymax - ymin) / 8)
		ymin = int(ymin - yadd)
		ymax = int(ymax + yadd)
		y_ticks_major = int((ymax-ymin)/4)
		x_ticks_major = int(xcnt/10)
		xlabel = self.xlabel or self.xfield
		ylabel = self.ylabel

		if not self.graph:
			self.graph = Graph(
				xlabel = self.xlabel or self.xfield,
				ylabel = self.ylabel,
				y_ticks_major = int((ymax-ymin)/4),
				x_ticks_major = int(xcnt/10),
				ymin = ymin,
				ymax = ymax,
				xmin = 0,
				xmax = xcnt,
				y_grid_label=True,
				x_grid_label=True,
				xlog = False,
				ylog = False,
				x_grid = True,
				y_grid = True,
				padding = 5,
				**graph_theme)
			self.add_widget(self.graph)
		else:
			self.graph.xlabel = xlabel
			self.graph.ylabel = ylabel
			self.graph.ymin = ymin
			self.graph.ymax = ymax
			self.graph.xmin = 0
			self.graph.xmax = xmax
			self.graph.y_ticks_major = y_ticks_major
			self.graph.x_ticks_major = x_ticks_major

		for s in self.series:
			s['plot'] = self.build_plot(s)
			s['plot'].points = s['points']
			self.graph.add_plot(s['plot'])
		self.graph.x_grid_texts = xlabel_text
		self.graph.x_ticks_angle = self.x_ticks_angle

Factory.register('LineChart', LineChart)
