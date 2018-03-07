#!/usr/bin/env/ python
#-*-coding:utf-8-*-
class EnumDirection(object):
    '''
    元素滑动方向  手机左上角坐标为(0,0)

    # Left：向左滑动  y不变，x减小
    # Right：向右滑动 y不变，x增大
    # Up：向上滑      x不变，y减小
    # Down：向下滑    x不变，y增大
    '''
    Left, Right, Up, Down = ('Left', 'Right', 'Up', "Down")


class EnumItemCount(object):
    '''
    各列表一页显示item个数

    # Rank_Item_Count：排行榜列表每页显示item个数
'''

class EnumSceneType():
    '''
    场景类型
    '''
    Start, Stop = ("start", "stop")


class EnumSceneName():
    '''
    场景名
    '''
    ThreeRoom,LaiziRoom,DoublelaiziRoom,FourRoom = (
    "threeroom","laiziroom","doublelaiziroom","fourroom")