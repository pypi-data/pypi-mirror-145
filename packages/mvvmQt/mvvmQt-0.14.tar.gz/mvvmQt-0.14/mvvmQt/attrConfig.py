from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFrame, QTabWidget

def toList(t):
    def f(s):
        s = s.split(',')
        arr = []
        for i, j in enumerate(s):
            if type(t) == list:
                arr.append(t[i](j.strip()))
            else:
                arr.append(t(j.strip()))
        return arr
    return f

def cvImg(img):
    import cv2
    qimageformat = QImage.Format_Indexed8
    if len(img.shape)==3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        qimageformat = QImage.Format_RGBA8888
    q_img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qimageformat)
    q_img = q_img.rgbSwapped()
    return QPixmap.fromImage(q_img)

def cvPathImg(path):
    import cv2
    img = cv2.imread(path)
    return cvImg(img)

def frameShape(style: str):
    style = style.lower()
    d = {
        'none': QFrame.NoFrame,  # QFrame什么都没画
        'box': QFrame.Box,      # QFrame围绕其内容绘制一个框
        'panel': QFrame.Panel,    # QFrame绘制一个面板，使内容显得凸起或凹陷
        'vline': QFrame.VLine,    # QFrame绘制一条无框架的垂直线（用作分隔符）
        'style': QFrame.StyledPanel,  # 绘制一个矩形面板，其外观取决于当前的GUI样式。它可以升起或凹陷。
        'hline': QFrame.HLine
    }
    if style not in d.keys():
        style = 'none'
    return d[style]

def frameShadow(shadow: str):
    shadow = shadow.lower()
    d = {
        'plain': QFrame.Plain,  # 框架和内容与周围环境呈现水平;（没有任何3D效果）
        'raised': QFrame.Raised, # 框架和内容出现; 使用当前颜色组的浅色和深色绘制3D凸起线
        'sunken': QFrame.Sunken, # 框架和内容出现凹陷; 使用当前颜色组的浅色和深色绘制3D凹陷线
    }
    if shadow not in d.keys():
        shadow = 'plain'
    return d[shadow]

def tabPosition(pos: str):
    pos = pos.lower()
    d = {
        'north': QTabWidget.North,
        'south': QTabWidget.South,
        'west': QTabWidget.West,
        'east': QTabWidget.East
    }
    return d[pos]

"""
结构格式为key: [qt function name or callable function, type]
如果为callable function, 最后一个参数必然为Element对象
"""

size = {
    'maxHeight': ['setMaximumHeight', int],
    'maxWidth': ['setMaximumWidth', int],
    'minHeight': ['setMinimumHeight', int],
    'minWidth': ['setMinimumWidth', int],
    'width': ['setFixedWidth', int],
    'height': ['setFixedHeight', int],
    'visible': ['setVisible', bool]
}

common = {
    'text': ['setText', str],
    'enable': ['setEnabled', bool]
}

ElementAttr = {
    'widget': {
        **size,
        'title': ['setWindowTitle', str],
        'pos': ['move', toList(int)],
        'full': ['showType', [int, bool]]
    },
    'frame': {
        **size,
        'shape': ['setFrameShape', frameShape],
        'shadow': ['setFrameShadow', frameShadow],
        'linew': ['setLineWidth', int],
        'lineMw': ['setMidLineWidth', int],
    },
    'grid': {
        'spacing': ['setSpacing', int],
        'vspacing': ['setVerticalSpacing', int],
        'hspacing': ['setHorizontalSpacing', int]
    },
    'button': {
        **size,
        **common,
        'shortcut': ['setShortcut', str],
        'tooltip': ['setToolTip', str],
        'checkable': ['setCheckable', bool],
        'icon': ['setIcon', str],
        'repeat': ['setAutoRepeat', [int, bool]],
        'repeatDelay': ['setAutoRepeatDelay', int],
        'repeatInterval': ['setAutoRepeatInterval', int]
    },
    'label': {
        **size, **common,
        'cv': ['setPixmap', cvImg],
        'cvPath': ['setPixmap', [str, cvPathImg]]
    },
    'tab': {
        'pos': ['setTabPosition', tabPosition],
        'name': ['setTabText', toList([int, str])]
    },
    'status': {
        'msg': ['showMessage', str]
    }
}

ElementAttr['window'] = {
    **ElementAttr['widget']
}