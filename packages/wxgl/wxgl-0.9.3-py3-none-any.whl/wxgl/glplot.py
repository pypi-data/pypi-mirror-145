# -*- coding: utf-8 -*-
#
# MIT License
# 
# Copyright (c) 2021 Tianyuan Langzi
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


"""
WxGL: 基于PyOpenGL的三维数据绘图工具包

以wx为显示后端，提供Matplotlib风格的应用方式
也可以和wxpython无缝结合，在wx的窗体上绘制三维模型
"""


from . figure import Figure


fig = Figure()
create_figure = Figure

show = fig.show
savefig = fig.savefig
capture = fig.capture


def current_axes(func):
    """装饰器函数，检查是否存在当前子图，若无则创建"""
    
    def wrapper(*args, **kwds):
        fig._create_frame()
        if not fig.curr_ax:
            fig.add_axes('111')
        
        func(*args, **kwds)
    
    return wrapper

def figure(**kwds):
    """初始化画布
    
    kwds        - 关键字参数
        proj        - 投影模式，'O' - 正射投影，'P' - 透视投影（默认）
        zoom        - 视口缩放因子，默认1.0
        azim        - 方位角，默认0°
        elev        - 仰角，默认0°
        azim_range  - 方位角限位器，默认-180°~180°
        elev_range  - 仰角限位器，默认-180°~180°
        smooth      - 直线、多边形和点的反走样开关
        style       - 场景风格，默认太空蓝
            'blue'      - 太空蓝
            'gray'      - 国际灰
            'white'     - 珍珠白
            'black'     - 石墨黑
            'royal'     - 宝石蓝
    """
    
    global fig
    fig = Figure(**kwds)

def subplot(pos):
    """添加子图
    
    pos         - 子图在场景中的位置和大小
                    三位数字    - 指定分割画布的行数、列数和子图序号。例如，223表示两行两列的第3个位置
                    四元组      - 以画布左下角为原点，宽度和高度都是1。四元组分别表示子图左下角在画布上的水平、垂直位置和宽度、高度
    """
    
    fig.add_axes(pos)

@current_axes
def cruise(func):
    """设置相机巡航函数"""
    
    fig.curr_ax.cruise(func)

@current_axes
def title(*args, **kwds):
    fig.curr_ax.title(*args, **kwds)

@current_axes
def colorbar(*args, **kwds):
    fig.curr_ax.colorbar(*args, **kwds)

@current_axes
def text(*args, **kwds):
    fig.curr_ax.text(*args, **kwds)

@current_axes
def text3d(*args, **kwds):
    fig.curr_ax.text3d(*args, **kwds)

@current_axes
def line(*args, **kwds):
    fig.curr_ax.line(*args, **kwds)

@current_axes
def point(*args, **kwds):
    fig.curr_ax.point(*args, **kwds)

@current_axes
def surface(*args, **kwds):
    fig.curr_ax.surface(*args, **kwds)

@current_axes
def quad(*args, **kwds):
    fig.curr_ax.quad(*args, **kwds)

@current_axes
def mesh(*args, **kwds):
    fig.curr_ax.mesh(*args, **kwds)

@current_axes
def cylinder(*args, **kwds):
    fig.curr_ax.cylinder(*args, **kwds)

@current_axes
def torus(*args, **kwds):
    fig.curr_ax.torus(*args, **kwds)

@current_axes
def uvsphere(*args, **kwds):
    fig.curr_ax.uvsphere(*args, **kwds)

@current_axes
def isosphere(*args, **kwds):
    fig.curr_ax.isosphere(*args, **kwds)

@current_axes
def circle(*args, **kwds):
    fig.curr_ax.circle(*args, **kwds)

@current_axes
def cone(*args, **kwds):
    fig.curr_ax.cone(*args, **kwds)

@current_axes
def cube(*args, **kwds):
    fig.curr_ax.cube(*args, **kwds)

@current_axes
def isosurface(*args, **kwds):
    fig.curr_ax.isosurface(*args, **kwds)

@current_axes
def grid(*args, **kwds):
    fig.curr_ax.grid(*args, **kwds)

@current_axes
def model(*args, **kwds):
    fig.curr_ax.model(*args, **kwds)

@current_axes
def xrange(xrange):
    fig.curr_ax.xrange(xrange)

@current_axes
def yrange(yrange):
    fig.curr_ax.yrange(yrange)

@current_axes
def zrange(zrange):
    fig.curr_ax.zrange(zrange)
