# polygon.py
"""
名称	类型	默认值	描述
opts	Object	 	配置项，继承得到的配置项参见 zrender.Displayable。
opts.shape	Object	 	形状属性。
opts.shape.points	number[][]	0	每个元素是一个横纵坐标的数组。
opts.shape.smooth	number|string	0	圆滑程度，取值范围为 0 到 1 之间的数字，0 表示不圆滑；也可以是特殊字符串 'spline' 表示用 Catmull-Rom spline 插值算法，否则默认用贝塞尔曲线插值算法。
opts.shape.smoothConstraint	number[][]	0	将计算出来的控制点约束在一个包围盒内。比如 [[0, 0], [100, 100]]，这个包围盒会与整个折线的包围盒做一个并集用来约束控制点。
"""

