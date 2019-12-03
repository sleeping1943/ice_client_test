
from view import *
from PyQt5 import QtWidgets
from tools import *


# 隐藏控制台
def close_console():
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    extro_ui(widget)

    ''' 窗口类添加其他事件函数 begin'''
    Ui_Window.test_invoke = ui_test_invoke
    Ui_Window.invoke_func = ui_invoke_func

    Ui_Window.selection_change = ui_selection_change
    Ui_Window.cb_actived = ui_cb_actived
    Ui_Window.te_dateTimeChanged = ui_te_datetime_changed
    QtWidgets.QWidget.dragEnterEvent = ui_drag_enter_event
    QtWidgets.QWidget.dropEvent = ui_drop_event
    QtWidgets.QWidget.dragMoveEvent = ui_drag_move_event
    ''' 窗口类添加其他事件函数 end '''

    window = Ui_Window()
    window.setupUi(widget)
    QtWidgets.QWidget.window = window

    widget.setFont(QFont("Roman times", 5.5))
    #设置窗口样式
    set_window_ui(window)

    init_params(window)
    define_signals(window)
    close_console()
    widget.show()

    ret = app.exec_()
    sys.exit(ret)


if __name__ == '__main__':
    main()
