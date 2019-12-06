from view import *
from PyQt5 import QtWidgets
from tools import *


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()

    ''' 窗口类添加其他事件函数 begin'''
    Ui_Window.test_invoke = ui_test_invoke
    Ui_Window.invoke_func = ui_invoke_func

    Ui_Window.widget = widget
    Ui_Window.selection_change = ui_selection_change
    Ui_Window.cb_actived = ui_cb_actived
    Ui_Window.value_changed = ui_value_changed
    Ui_Window.set_window_ui = set_window_ui
    QtWidgets.QWidget.dragEnterEvent = ui_drag_enter_event
    QtWidgets.QWidget.dropEvent = ui_drop_event
    QtWidgets.QWidget.dragMoveEvent = ui_drag_move_event
    QtWidgets.QWidget.timer_handler = ui_timer_handler
    ''' 窗口类添加其他事件函数 end '''
    window = Ui_Window()
    window.setupUi(widget)
    QtWidgets.QWidget.window = window
    #设置窗口定时器
    set_window_timer(widget)
    # 窗口隐藏设置
    window.btn_more.toggled.connect(window.widget_more.setVisible)
    # 设置更多选项
    set_window_more_options(widget)
    # 默认暗黑主题
    window.theme_dark.setChecked(True)
    #设置窗口样式
    set_window_ui(window)

    init_params(window)
    define_signals(window)
    widget.show()
    print('widget.baseSize():{} {}'.format(widget.height(), widget.width()))
    extro_ui(widget)
    #window.widget_more.hide()
    ret = app.exec_()
    sys.exit(ret)


if __name__ == '__main__':
    main()
