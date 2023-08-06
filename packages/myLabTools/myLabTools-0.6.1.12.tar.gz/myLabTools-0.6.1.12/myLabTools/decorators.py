from line_profiler import LineProfiler
from functools import wraps
import time

def get_now():
    """获取当前时间

    Returns:
        _type_: _description_
    """    
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

def code_ana(func,args = None):
    """代码分析

    Args:
        func (_type_): _description_
        args (_type_, optional): _description_. Defaults to None.
    """    
    lp = LineProfiler()#实例化
    #测试jc函数性能
    lp_wrapper = lp(func) #输入函数
    if not args is None:
        lp_wrapper(*args) #输入函数参数
    lp.print_stats()

def func_line_time(f):
    """代码运行效率装饰器

    Args:
        f (_type_): 函数

    Returns:
        _type_: _description_
    """    
    @wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(f)
        lp_wrap(*args, **kwargs) 
        lp.print_stats() 
        return func_return 
    return decorator

def logit(logfile='out.log'):
    """日志包装器

    Args:
        logfile (str, optional): 日志的保存路径. Defaults to 'out.log'.
    """    
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string =  get_now() + " == " + func.__name__ + " start "
            print(log_string)
            # 打开logfile，并写入内容
            opened_file = open(logfile, 'w',encoding="utf-8") 
                # 现在将日志打到指定的logfile
            opened_file.write(log_string + '\n')
            kwargs["log_file"] = opened_file
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator