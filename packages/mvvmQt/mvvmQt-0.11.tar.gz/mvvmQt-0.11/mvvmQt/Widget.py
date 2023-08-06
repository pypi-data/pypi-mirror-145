from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from mvvmQt.Observable import ObservableBase

class Widget(QWidget):
    def showType(self, isFull):
        if isFull:
            return super().showFullScreen()
        else:
            return super().show()

class Window(QMainWindow):
    def showType(self, isFull):
        if isFull:
            return super().showFullScreen()
        else:
            return super().show()

# class Widget(QWidget):
#     def __init__(self, parser):
#         super().__init__()
#         self.parser = parser
#         self.desktop = QApplication.desktop()
#         self.attrs = []
#         self.hasTitle = False

#     def adapter(self, attrs):
#         for attr in attrs:
#             self.useAttr(attr)

#     def changeValue(self, c, v):
#         if type(c) is list:
#             if type(v) is not c[-1]:
#                 for _ in c:
#                     v = _(v)
#         else:
#             v = c(v)
#         return v

#     def useQtFunc(self, f, params):
#         if type(params) == list:
#             getattr(self, f)(*params)
#         else:
#             getattr(self, f)(params)

#     def addSubscribe(self, ob, c):
#         if type(c[1]) is str:
#             ob.subscribe(lambda v: self.useQtFunc(c[0], c[1] % v), init=True)
#         else:
#             ob.subscribe(lambda v: self.useQtFunc(c[0], self.changeValue(c[1], v)), init=True)

#     def useAttr(self, attr):
#         k = attr.key
#         v = attr.value
#         if k == 'width' and v == '100%':
#             v = self.desktop.width()
#         if k == 'height' and v == '100%':
#             v = self.desktop.height()
#         if k == 'title':
#             self.hasTitle = True
#         if k not in self.parser.ElementAttrConfig['widget'].keys():
#             return
#         _ = [*self.parser.ElementAttrConfig['widget'][k]]
#         if isinstance(v, ObservableBase):
#             if attr.dom.attr('format'):
#                 _[1] = attr.dom.attr('format')
#             self.addSubscribe(v, _)
#         else:
#             self.useQtFunc(_[0], self.changeValue(_[1], v))

#     def run(self):
#         if self.hasTitle:
#             self.show()
#         else:
#             self.showFullScreen()
#         self.adapter(self.attrs)