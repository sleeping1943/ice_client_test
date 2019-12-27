import re
from invoke import *
from PyQt5.QtGui import QIcon, QFont, QTextDocument, QTextCursor
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
import time

# 测试用的行数 定位于Login函数
g_test_line = 34
g_total_lines = list()
# ice文件返回的数据类型
func_pre_list = [
    'void',
    'int'
]
# 函数名对应的行数
g_func_name_line_map = dict()
# 函数名
func_param_map = dict()
# 函数参数信息
func_help_param_map = dict()
# 原始的函数帮助信息
origin_func_help_param_map = dict()
# 函数帮助信息
func_help_map = dict()
base_font_size = 14
g_ice_file_path = None

# 颜色主题
dark_theme = {
    'main_color': "#Window{background-color: rgb(45,45,48)}",
    'label_bg_color': 'color:rgb(241,241,241);background-color:rgb(45,45,48);',
    'gbg_color': 'color:rgb(241,241,241);background-color:rgb(30,30,30);font-size:{}px;',
    'group_color': 'color:rgb(241,241,241);background-color:rgb(45,45,48);',
    'btn_color': '''QPushButton{color:rgb(241,241,241)}
                    QPushButton:hover{color:cyan}
                    QPushButton{background-color:rgb(92,97,100)}
                    QPushButton{border:2px}
                    QPushButton{border-radius:10px}
                    QPushButton{padding:2px 4px}'''
}

light_theme = {
    'main_color': "#Window{background-color: rgb(241,241,241)}",
    'label_bg_color': 'color:rgb(45,45,48);background-color:rgb(241,241,241);',
    'gbg_color': 'color:rgb(30,30,30);background-color:rgb(255,255,255);font-size:{}px;',
    'group_color': 'color:rgb(45,45,48);background-color:rgb(241,241,241);',
    'btn_color': '''QPushButton{color:rgb(45,45,48)}
                    QPushButton:hover{color:cyan}
                    QPushButton{background-color:rgb(220,220,220)}
                    QPushButton{border:2px}
                    QPushButton{border-radius:10px}
                    QPushButton{padding:2px 4px}'''
}

cur_theme = light_theme

def help_format(self, state):
    print('help_format:{}'.format(state))
    if self.whole_help_format.isChecked():
        document = QTextDocument(''.join(g_total_lines))
        self.func_params.setDocument(document)
    ui_cb_actived(self, 0)


# 隐藏控制台
def close_console():
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)


def set_window_more_options(widget):
    window = widget.window
    wgt_main = window.widget_main
    wgt_more = window.widget_more
    '''
    main_layout = QGridLayout()
    # 关键性的参数设置
    main_layout.setSizeConstraint(QLayout.SetFixedSize)
    #mainLayout.addLayout(leftLayout, 0, 0)
    main_layout.addWidget(wgt_main, 0, 1)
    main_layout.addWidget(wgt_more, 0, 2, 1, 1)
    main_layout.setColumnStretch(0, 1)
    widget.setLayout(main_layout)
    '''

    #window.hlayout_2.setContentsMargins(0,0,0,0)
    v_layout1 = QVBoxLayout()
    v_layout2 = QVBoxLayout()
    v_layout1.addWidget(wgt_main)
    grid_layout = QGridLayout()
    print('QLayout.SetFixedSize:{}'.format(QLayout.SetFixedSize))
    #grid_layout.setSizeConstraint(QLayout.SetFixedSize)
    grid_layout.addLayout(v_layout1, 0, 0)
    grid_layout.addWidget(wgt_more, 1, 0) #, 1, 1)
    wgt_more.hide()
    widget.setLayout(grid_layout)
    # 函数参数只可读
    window.func_params.setReadOnly(True)


def ui_timer_handler(win):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    str_info = '当前时间:{}'.format(time_now)
    if g_ice_file_path:
        str_info = '{} 文件路径:{}'.format(str_info, g_ice_file_path)
    win.window.te_now.setText(str_info)


def set_window_timer(win):
    win.timer = QTimer(win)
    win.timer.timeout.connect(win.timer_handler)
    win.timer.start(1000) # 每隔一秒执行一次


def set_input_font_size(win, size):
    gbg_color = cur_theme['gbg_color']
    bg_color = gbg_color.format(base_font_size+size)
    # 输入框样式设置
    win.text_params.setStyleSheet(bg_color)
    win.text_result.setStyleSheet(bg_color)
    win.func_params.setStyleSheet(bg_color)
    win.lineEdit_ip.setStyleSheet(bg_color)
    win.lineEdit_port.setStyleSheet(bg_color)
    win.lineEdit_flag.setStyleSheet(bg_color)
    win.lineEdit_func.setStyleSheet(bg_color)

    # 下拉框样式设置
    win.comboBox.setStyleSheet(bg_color)
    win.cb_func_total.setStyleSheet(bg_color)
    win.font_box.setStyleSheet(bg_color)


def ui_value_changed(self, value):
    print('changed_value:{}'.format(value))
    set_input_font_size(self, value)
    pass


def set_window_ui(win):
    global cur_theme
    if win.theme_light.isChecked():
        cur_theme = light_theme
    elif win.theme_dark.isChecked():
        cur_theme = dark_theme
    else:
        cur_theme = dark_theme

    # 隐藏调试按钮
    win.btn_test_invoke.hide()
    # 设置按钮样式
    win.btn_invoke.setStyleSheet(cur_theme['btn_color'])
    # 设置字体
    set_input_font_size(win, 0)
    label_bg_color = cur_theme['label_bg_color']
    # 标签样式设置
    win.label_ip.setStyleSheet(label_bg_color)
    win.label_port.setStyleSheet(label_bg_color)
    win.label_flag.setStyleSheet(label_bg_color)
    win.label_func.setStyleSheet(label_bg_color)
    win.label.setStyleSheet(label_bg_color)
    win.label_2.setStyleSheet(label_bg_color)
    win.label_3.setStyleSheet(label_bg_color)
    win.label_4.setStyleSheet(label_bg_color)
    win.label_5.setStyleSheet(label_bg_color)
    win.te_now.setStyleSheet(label_bg_color)
    win.font_size.setStyleSheet(label_bg_color)
    win.theme_dark.setStyleSheet(label_bg_color)
    win.theme_light.setStyleSheet(label_bg_color)
    win.partial_help_format.setStyleSheet(label_bg_color)
    win.whole_help_format.setStyleSheet(label_bg_color)

    # 主窗口背景色
    win.widget.setStyleSheet(cur_theme['main_color'])
    # 主题box样式
    group_color = cur_theme['group_color']
    win.theme_box.setStyleSheet(group_color)
    win.theme_box_3.setStyleSheet(group_color)
    print('label_bg_size:{}'.format(win.label_2.baseSize().width()))


# 格式化json输出
def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


# 检测ip合法性
def check_ip(str_ip):
    #简单的匹配给定的字符串是否是ip地址,下面的例子它不是IPv4的地址，但是它满足正则表达式
    ret = False
    try:
        if len(str_ip) > 0 and re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", str_ip):
            ret = True
    except Exception as e:
        print(e)
    return ret


# 检测端口合法性
def check_port(str_port):
    ret = False
    try:
        port = int(str_port)
        if 0 < port <= 65535:
            ret = True
    except Exception as e:
        print(e)
    return ret


# 调试测试
def test_invoke(ip, port, flag, params, win):
    if not check_ip(ip):
        print('ip is invalid!')
    else:
        pass
    if not check_port(port):
        print('port is invalid!')
    else:
        pass

    info = 'ip valid:{} port:{} flag:{}'.format(ip, port, flag)
    win.text_params.append(info)
    #dll_file = 'F:/python/gui/test_ice.dll'
    dll_file = './test_ice.dll'

    ice_flag = "SaasService"
    addr = "default -h localhost -p 20071"
    func_name = "Login"
    login_info = {
        'username': 'admin',
        'password': '0192023a7bbd73250516f069df18b500'
    }

    login_str = json.dumps(login_info)
    in_params = login_str
    out_params = {}
    out_params = []
    result = invoce_ice(dll_file, ice_flag, addr, func_name, in_params, out_params)
    str_result = str(out_params[0], encoding="utf-8")
    #result = 'invoce_ice(dll_file, ice_flag, addr, func_name, in_params)'
    win.text_result.append(str_result)


# 调用ice接口
def invoke(ip, port, flag, func, params, win):
    try:
        if not check_ip(ip):
            raise Exception('无效IP')
        elif not check_port(port):
            raise Exception('无效端口')
        elif not flag or len(flag) <= 0:
            raise Exception('Ice标识为空')
        elif not func or len(func) <= 0:
            raise Exception('函数名为空')
        else:
            pass
    except Exception as e:
        win.text_result.append('调用错误:{}'.format(e))
        print(e)
    else:
        dll_file = './test_ice.dll'
        addr = "default -h {} -p {}".format(ip, port)
        out_params = []
        invoce_ice(dll_file, flag, addr, func, params, out_params)

        # 格式化输出返回的json
        if len(out_params) > 0 and len(out_params[0]) > 0:
            json_obj = json.loads(str(out_params[0], encoding="utf-8"))
            js_format = get_pretty_print(json_obj)
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            str_result = '调用时间:{} \n调用函数:{}\nresult:\n{}'\
                .format(time_now, func, js_format)
            win.text_result.clear()
            win.text_result.append(str_result)


# 测试调用
def ui_test_invoke(self):
    ip = self.lineEdit_ip.text()
    port = self.lineEdit_port.text()
    flag = self.lineEdit_flag.text()
    test_invoke(ip, port, flag, '', self)


# 调用接口
def ui_invoke_func(self):
    try:
        ip = self.lineEdit_ip.text()
        port = self.lineEdit_port.text()
        flag = self.lineEdit_flag.text()
        func = self.lineEdit_func.text()
        params = self.text_params.toPlainText()
        invoke(ip, port, flag, func, params, self)
        # 已缓存该函数信息
        if self.comboBox.findText(func) != -1:
            pass
        else:
            self.comboBox.addItem(func)
            func_param_map[func] = params
    except Exception as e:
        print(e)


# 缓存函数选择处理函数
def ui_selection_change(self, index):
    func_name = self.comboBox.currentText()
    func_params = ''
    self.lineEdit_func.setText(func_name)
    # 填充函数名后，若缓存了参数，则一并填充
    if func_name in func_param_map.keys():
        func_params = func_param_map[func_name]
        if not func_params and func_name in func_help_param_map.keys():
            func_params = func_help_param_map[func_name]
        else:
            pass
        if func_params:
            self.text_params.clear()
            self.text_params.setText(func_params)
    else:
        pass
    # 帮助信息全文定位
    if self.partial_help_format.isChecked():
        if func_name in func_help_map.keys():
            func_help_info = func_help_map[func_name]
            self.func_params.clear()
            self.func_params.setText(func_help_info)
        else:
            pass
    else:
        if func_name in g_func_name_line_map.keys():
            line_index = g_func_name_line_map[func_name]
            win_func_params = self.func_params
            tc = win_func_params.textCursor()
            position = win_func_params.document().findBlockByNumber(line_index-1).position()
            tc.setPosition(position,QTextCursor.MoveAnchor)
            win_func_params.setTextCursor(tc)
            print('func_name:{} line_index:{}'.format(func_name, line_index-1))
        else:
            pass


# 初始化参数
def init_params(win):
    conf = {
       "ip":"127.0.0.1",
       "port":"20051",
       "flag":"business"
    }
    with open('./conf.json','r') as f:
        content = f.read()
        conf = json.loads(content)
        print(conf)
        win.lineEdit_ip.setText(conf["ip"])
        win.lineEdit_port.setText(conf["port"])
        win.lineEdit_flag.setText(conf["flag"])
        # 关闭控制台调试
        if 'debug_model' in conf.keys() and conf['debug_model'] is False:
            close_console()


# Ice文件函数选择时处理
def ui_cb_actived(self, index):
    func_name = self.cb_func_total.currentText()
    self.lineEdit_func.setText(func_name)
    if func_name in func_param_map.keys():
        func_params = func_param_map[func_name]
        if not func_params and func_name in func_help_param_map.keys():
            func_params = func_help_param_map[func_name]
        else:
            pass
        if func_params:
            self.text_params.clear()
            self.text_params.setText(func_params)
        else:
            pass
    else:
        pass
    # 帮助信息全文定位
    if self.partial_help_format.isChecked():
        if func_name in func_help_map.keys():
            func_help_info = func_help_map[func_name]
            self.func_params.clear()
            self.func_params.setText(func_help_info)
        else:
            pass
    else:
        if func_name in g_func_name_line_map.keys():
            line_index = g_func_name_line_map[func_name]
            win_func_params = self.func_params
            tc = win_func_params.textCursor()
            position = win_func_params.document().findBlockByNumber(line_index-1).position()
            tc.setPosition(position,QTextCursor.MoveAnchor)
            win_func_params.setTextCursor(tc)
            print('func_name:{} line_index:{}'.format(func_name, line_index-1))
        else:
            pass


# 窗口信号处理
def define_signals(win):
    win.btn_test_invoke.clicked.connect(win.test_invoke)
    win.btn_invoke.clicked.connect(win.invoke_func)
    win.comboBox.currentIndexChanged.connect(win.selection_change)
    win.cb_func_total.activated.connect(win.cb_actived)
    #win.te_now.dateTimeChanged.connect(win.te_dateTimeChanged)
    win.font_box.valueChanged.connect(win.value_changed)
    win.theme_dark.toggled.connect(win.set_window_ui)
    win.theme_light.toggled.connect(win.set_window_ui)
    # 帮助显示样式
    win.partial_help_format.toggled.connect(win.help_format)
    win.whole_help_format.toggled.connect(win.help_format)


# 额外窗口样式设置
def extro_ui(window):
    window.setWindowIcon(QIcon('./resources/ice.png'))
    #window.setStyleSheet("#Window{background-color: lightblue}")
    window.setStyleSheet(cur_theme['main_color'])
    window.setMaximumSize(window.width(), window.height())
    window.setMinimumSize(window.width(), window.height())


# ice文件函数解析
def parse_ice_file(file_path):
    func_names = list()

    with open(file_path, 'r') as fd:
        line_index = 1
        line = fd.readline()
        #global g_total_lines
        g_total_lines.append(line)
        while line:
            g_total_lines.append(line)
            line = line.lstrip()
            # 获取函数的返回类型
            pre_str = line[0:line.find(' ')]
            #print('pre_str1:{}'.format(pre_str))
            if pre_str in func_pre_list and '(' in line:
                func_name = line[len(pre_str)+1:line.index('(')]
                func_names.append(func_name)
                g_func_name_line_map[func_name] = line_index
                #print('pre_str:{}'.format(pre_str))
            line = fd.readline()
            line_index = line_index + 1
        print('total_lines:{}'.format(len(g_total_lines)))
        print('g_func_name_line_map:{}'.format(g_func_name_line_map))
    return func_names


# 从文件获取函数对应的帮助信息
def get_help_infos(file_path):
    func_names = list()
    pre_func_name = None
    cur_func_name = ''
    help_info = ''
    global func_param_map
    help_info_list = list()

    with open(file_path, 'r') as fd:
        origin_line = fd.readline()
        line = origin_line
        while line:
            line = line.lstrip()
            for key in func_param_map.keys():
                if key in line:
                    if not pre_func_name:
                        pre_func_name = key
                    else:
                        cur_func_name = key
                    #print(line)
                    break
            if pre_func_name:
                help_info += origin_line
                help_info_list.append(origin_line)
            # 该函数帮助信息结尾
            if cur_func_name == pre_func_name:
                pre_func_name = None
                global func_help_map
                func_help_map[cur_func_name] = help_info
                global origin_func_help_param_map
                origin_func_help_param_map[cur_func_name] = help_info_list.copy()
                help_info_list[:] = []
                help_info = ''
            line = fd.readline()
            origin_line = line
    return func_names


'''
从帮助信息中提取发送参数
1. 从example开始为参数定义
2. 参数定义在'{}'中
3. 去除定义中'{}'的影响
4. 去除注释性文字
'''
def get_func_help_params():
    split_list = ['必填', '选填']
    for key,value_list in origin_func_help_param_map.items():
        # 初始参数为None,不处理
        help_info_list = list()
        # 第一行的缩进空格数
        blank_count = -1
        # 括号层数
        bracket_level = 0
        is_begin = False
        for line in value_list:
            trim_str = line.strip()
            if is_begin:
                if blank_count == -1:
                    blank_count = (len(line) - len(line.lstrip()))
                left_quot = False
                right_quot = False
                if '{' in trim_str:
                    left_quot = True
                    bracket_level += 1
                if '}' in trim_str:
                    right_quot = True
                    bracket_level -= 1
                    # 消除上一行的','
                    if (not left_quot) and len(help_info_list) > 0:
                        help_info_list[-1] = help_info_list[-1].rstrip(' ,\n')
                        #print('help_info_line[-1]:{}'.format(help_info_list[-1]))

                # 该行字符串没有'{'和'}' 或者同时有'{'和'}'的情况,剔除后面的注释
                if (left_quot^right_quot) == False:
                    for value in split_list:
                        if value in line:
                            line = line[0:line.index(value)]
                            line = line.rstrip()
                        else:
                            pass
                format_line = line
                if blank_count > 0:
                    format_line = line[blank_count:]
                help_info_list.append(format_line)
            elif trim_str.startswith('example'):
                is_begin = True
                continue
            # 括号匹配完，跳出此函数参数解析
            if is_begin and bracket_level == 0:
                temp_help_info = None
                if len(help_info_list) > 2:
                    param_str = help_info_list[-2]
                    help_info_list[-2] = param_str.rstrip(',')
                    temp_help_info_list = help_info_list[1:-1]
                    temp_help_info = '\n'.join(temp_help_info_list)
                    help_info_list[1:-1] = temp_help_info 
                help_info_list.insert(-1, '\n')
                help_info = ''.join(help_info_list)
                try:
                    help_info_obj = json.loads(help_info)
                    func_help_param_map[key] = get_pretty_print(help_info_obj)
                except Exception as e:
                    func_help_param_map[key] = help_info
                    print('get_func_help_params error:{}'.format(e))
                else:
                    func_help_param_map[key] = help_info
                help_info_list.clear()
                break



# 鼠标拖入事件
def ui_drag_enter_event(self, evn):
    # 鼠标放开函数事件
    evn.accept()


# 鼠标放开执行
def ui_drop_event(self, evn):
    file_path = ''
    try:
        # 获取文件路径
        file_path = evn.mimeData().text()
        str_head = 'file:///'
        if file_path.startswith(str_head):
            file_path = file_path[len(str_head):]
        print(file_path)
        self.window.text_params.setText(file_path)
        key_list = parse_ice_file(file_path)

        # 先清空以前的参数信息和帮助信息, comboBox信息等
        global func_param_map
        func_param_map.clear()
        global func_help_param_map
        func_help_param_map.clear()
        global origin_func_help_param_map
        origin_func_help_param_map.clear()
        global func_help_map
        func_help_map.clear()
        self.window.cb_func_total.clear()
        self.window.comboBox.clear()

        #print(key_list)
        if len(key_list) > 0:
            value_list = [None] * len(key_list)
            func_param_map = dict(zip(key_list, value_list))
            self.window.cb_func_total.addItems(key_list)
            #print(func_param_map)

        func_params_list = get_help_infos(file_path)
        get_func_help_params()
        #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&func_help_map:{}".format(func_help_map))
        #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&func_help_params_map:{}".format(func_help_param_map))
        #str_json = json.dumps(func_help_param_map)
        #print("json:{}".format(str_json))
    except Exception as e:
        print('drag event:{}'.format(e))
    else:
        global g_ice_file_path
        g_ice_file_path = file_path


# 鼠标拖拽文件移动
def ui_drag_move_event(self, evn):
    pass