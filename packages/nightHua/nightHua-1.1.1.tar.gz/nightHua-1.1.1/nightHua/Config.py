#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/4 15:09
# @Author : NightHua
# @Email : lirui001002@163.com
# @File : Config.py
# @Project : 我的pip模块

def getConfig(text,minLength=0,maxLength=99,needKeys=[]):
    '''
    解析配置文本，行首#为注释，;;;为分隔符\n
    逐行解析\n
    :param text: 配置文本内容
    :param minLength:列表项的最小长度 ，默认值0
    :param maxLength: 列表项的最大长度，默认值99
    :param needKeys: 必需的键值，列表形式传入
    :return: 字典形式的解析结果
    '''
    data={
        'data':{},
        'list':[],
    }
    line=0
    for i in text.splitlines():
        line+=1
        print('\n第%d行'%line,i)
        #跳过空行
        if i.strip()=='':
            continue
        #跳过#开头的注释行
        if i.strip().startswith('#'):
            continue
        #单行参数以;;;分割
        paramList=[j.strip() for j in i.split(';;;')]
        #参数解析赋值
        if paramList[0].startswith('@'):
            if paramList[0] =='@set':
                #参数数量检查
                if len(paramList) != 3:
                    raise ValueError('第%d行：%s应设置%d个参数，实际赋予%d个参数。'%(line,paramList[0],2,len(paramList)-1))
                #参数重复检查
                if paramList[1] in data['data'].keys():
                    raise ValueError('第%d行：%s键%s重复。' % (line, paramList[0], paramList[1]))
                data['data'][paramList[1]]=paramList[2]
            else:
                raise ValueError('第%d行：关键词错误%s。'%(line,paramList[0]))
            #检查必需的键值
            for l in needKeys:
                if l not in data['data'].keys():
                    raise ValueError('第%d行：必需的参数%s未赋值。' % (line, l))
        #参数列表解析
        else:
            #检测参数列表长度
            if len(paramList)<minLength or len(paramList)>maxLength:
                raise ValueError('第%d行：%s应设置%d-%d个参数，实际赋予%d个参数。' % (line, paramList[0], minLength,maxLength, len(paramList)))
            data['list'].append(paramList)
    return data





if __name__ == '__main__':
    getConfig('\n #asdasdasd  ;;;asdasd;;;s d;;; asd\nasd;;;\n@set;;;asd;;;123\n@set;;;123;;;123\n',minLength=0,maxLength=2,needKeys=['asd'])