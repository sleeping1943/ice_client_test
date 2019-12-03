import sys
from ctypes import *
import json

'''
 ctypes 使用说明URL:
 http://blog.timd.cn/python-ctypes/
'''

def invoce_ice(dll_file, ice_flag, addr, func_name, in_params, out_params, is_print=False):
    '''
    指定 函数的参数类型
    注：虽然delete_str的参数和invoke的返回指针为char*,但是执行后不知为何指针地址会改变，
    都改为void*后无此问题，很是奇怪
    '''
    if is_print:
        print('load dll{} begin'.format(dll_file))
    p_dll = CDLL(dll_file)
    if is_print:
        print('load dll{} over'.format(dll_file))
    p_dll.invoke.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_bool]
    p_dll.delete_str.argtypes = [c_void_p]
    '''
    参数
    '''
    arg1 = c_char_p(bytes(ice_flag, 'utf-8'))
    arg2 = c_char_p(bytes(addr, 'utf-8'))
    arg3 = c_char_p(bytes(func_name, 'utf-8'))
    arg4 = c_char_p(bytes(in_params, 'utf-8'))
    arg5 = c_bool(is_print)

    '''
    指定 函数的返回类型
    '''
    p_dll.invoke.restype = c_void_p
    p_dll.delete_str.restype = None
    ########### 调用动态链接库函数 ##################
    if is_print:
        print('login_str:{}'.format(in_params))
    p_ret_str = p_dll.invoke(arg1, arg2, arg3, arg4, arg5)
    result = cast(p_ret_str, c_char_p).value
    if is_print:
        print('result:{}-----'.format(result))
    p_dll.delete_str(p_ret_str)
    out_params.append(result)

if __name__ == '__main__':
    login_info = {
        'username':'admin',
        'password':'0192023a7bbd73250516f069df18b500'
    }

    login_str = json.dumps(login_info)
    dll_file = './test_ice.dll'

    ice_flag = "SaasBackend"
    addr = "default -h localhost -p 20071"
    func_name = "Login"
    in_params = login_str
    out_params = []
    invoce_ice(dll_file, ice_flag, addr, func_name, in_params, out_params, True)