import re
from invoke import *
from PyQt5.QtGui import QIcon, QFont
import time

func_param_map = dict()
func_help_param_map = dict()
origin_func_help_param_map = dict()
func_help_map = dict()


def set_window_ui(win):
    # 隐藏调试按钮
    win.btn_test_invoke.hide()
    # 设置字体
    #win.setFont(QFont("Roman times", 10.5))
    label_bg_color = "color:{};background-color: {};".format('rgb(241,241,241)','rgb(45,45,48)')
    bg_color = "color:{};background-color: {};{}".format('rgb(241,241,241)','rgb(30,30,30)', 'font-size:20px;')
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


#格式化json输出
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
    if func_name in func_help_map.keys():
        func_help_info = func_help_map[func_name]
        self.func_params.clear()
        self.func_params.setText(func_help_info)


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


# Ice文件函数选择时处理
def ui_cb_actived(self, index):
    func_name = self.cb_func_total.currentText()
    self.lineEdit_func.setText(func_name)
    if func_name in func_param_map.keys():
        func_params = func_param_map[func_name]
        if not func_params:
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
    if func_name in func_help_map.keys():
        func_help_info = func_help_map[func_name]
        self.func_params.clear()
        self.func_params.setText(func_help_info)


# 窗口信号处理
def define_signals(win):
    win.btn_test_invoke.clicked.connect(win.test_invoke)
    win.btn_invoke.clicked.connect(win.invoke_func)
    win.comboBox.currentIndexChanged.connect(win.selection_change)
    win.cb_func_total.activated.connect(win.cb_actived)
    win.te_now.dateTimeChanged.connect(win.te_dateTimeChanged)


# 额外窗口样式设置
def extro_ui(window):
    window.setWindowIcon(QIcon('./resources/ice.png'))
    #window.setStyleSheet("#Window{background-color: lightblue}")
    window.setStyleSheet("#Window{background-color: rgb(45,45,48)}")


# ice文件函数解析
def parse_ice_file(file_path):
    func_names = list()
    with open(file_path, 'r') as fd:
        line = fd.readline()
        while line:
            line = line.lstrip()
            pre_str = 'void '
            if line.startswith(pre_str) and '(' in line:
                line = line[len(pre_str):line.index('(')]
                func_names.append(line)
            line = fd.readline()
    return func_names


# 从文件获取函数对应的帮助信息
def get_func_params(file_path):
    func_names = list()
    pre_func_name = None
    cur_func_name = ''
    help_info = ''
    global func_param_map
    help_info_list = list()
    with open(file_path, 'r') as fd:
        line = fd.readline()
        while line:
            line = line.lstrip()
            for key in func_param_map.keys():
                if key in line:
                    #print('key:{} in line:{}'.format(key, line))
                    if not pre_func_name:
                        pre_func_name = key
                    else:
                        cur_func_name = key
                    #print(line)
                    break
            if pre_func_name:
                help_info += line
                help_info_list.append(line)
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
        # 括号层数
        bracket_level = 0
        is_begin = False
        for line in value_list:
            trim_str = line.strip()
            if is_begin:
                if trim_str[0] == '{':
                    bracket_level += 1
                elif trim_str[-1] == '}':
                    bracket_level -= 1
                    # {}在同一行的情况
                    if len(trim_str) >= 2 and trim_str[-2] == '{':
                        bracket_level += 1
                    else:
                        pass
                # 结尾不是'{' or '}'的情况,剔除后面的注释
                else:
                    for value in split_list:
                        if value in line:
                            line = line[0:line.index(value)]
                            line = line.rstrip()
                        else:
                            pass
                help_info_list.append(line)
            elif trim_str.startswith('example'):
                is_begin = True
                continue
            # 括号匹配完，跳出此函数参数解析
            if is_begin and bracket_level == 0:
                if len(help_info_list) >= 2:
                    param_str = help_info_list[-2]
                    help_info_list[-2] = param_str.rstrip(',')
                help_info = '\n'.join(help_info_list)
                func_help_param_map[key] = help_info
                help_info_list.clear()
                break



# 鼠标拖入事件
def ui_drag_enter_event(self, evn):
    # 鼠标放开函数事件
    evn.accept()


# 鼠标放开执行
def ui_drop_event(self, evn):
    # 获取文件路径
    file_path = evn.mimeData().text()
    str_head = 'file:///'
    if file_path.startswith(str_head):
        file_path = file_path[len(str_head):]
    print(file_path)
    self.window.text_params.setText(file_path)
    key_list = parse_ice_file(file_path)

    print(key_list)
    if len(key_list) > 0:
        value_list = [None] * len(key_list)
        global func_param_map
        func_param_map = dict(zip(key_list, value_list))
        self.window.cb_func_total.addItems(key_list)
        #print(func_param_map)
    func_params_list = get_func_params(file_path)
    get_func_help_params()
    #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&func_help_map:{}".format(func_help_map))
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&func_help_params_map:{}".format(func_help_param_map))
    str_json = json.dumps(func_help_param_map)
    print("json:{}".format(str_json))


# 鼠标拖拽文件移动
def ui_drag_move_event(self, evn):
    pass


def ui_te_datetime_changed(self, datetime):
    self.te_now.setDateTime(datetime)
    pass
