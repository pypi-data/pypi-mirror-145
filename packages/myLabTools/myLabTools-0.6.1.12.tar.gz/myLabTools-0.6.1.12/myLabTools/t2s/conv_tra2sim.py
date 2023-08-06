from .langconv import *
"""将sentence中的繁体字转为简体字
"""
def Traditional2Simplified(sentence):
    """将sentence中的繁体字转为简体字

    Args:
        sentence (_type_): 待转换的句子

    Returns:
        _type_: 将句子中繁体字转换为简体字之后的句子
    """    
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

if __name__=="__main__":
    traditional_sentence = '憂郁的臺灣烏龜'
    simplified_sentence = Traditional2Simplified(traditional_sentence)
    print(simplified_sentence)

    '''
    输出结果：
        忧郁的台湾乌龟
    '''