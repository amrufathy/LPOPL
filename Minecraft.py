import pygame, sys
import numpy as np
import atexit
import random
import time
import math
from math import fabs
import TaskExecutor
from TaskExecutor import *

black = [0, 0, 0]
white = [255, 255, 255]
grey = [180, 180, 180]
dgrey = [120, 120, 120]
orange = [180, 100, 20]
green = [0, 200, 0]
lgreen = [60, 250, 60]
dgreen = [0, 100, 0]
blue = [0, 0, 250]
lblue = [80, 200, 200]
brown = [140, 100, 40]
dbrown = [100, 80, 0]
gold = [230, 215, 80]

ACTION_NAMES = ['<-', '->', '^', 'v', 'g', 'u', 'b', 'x']
# 0: left, 1: right, 2: up, 3: down, 4: get, 5: use, 6, 7: use crafted tools

MAP_ACTIONS = {5: 'get', 6: 'use', 7: 'usetool_bridge', 8: 'usetool_axe'}

RESOURCES = ['wood', 'grass', 'iron', 'gold', 'gem']  # for get actions
TOOLS = ['toolshed', 'workbench', 'factory', 'bridge', 'axe']  # for use actions
CRAFT = ['plank', 'stick', 'cloth', 'rope', 'bridge', 'bed', 'axe', 'shears']  # makeable tools

CRAFTEDTOOLS = ['bridge', 'axe']  # usable and crafted tools

LOCATIONS = [('wood', brown, 1, 1), ('grass', green, 4, 3), ('iron', grey, 5, 5),
             ('gold', gold, 1, 6), ('gem', lblue, 6, 1), ('toolshed', dbrown, 2, 4),
             ('workbench', dgreen, 0, 3), ('factory', dgrey, 4, 6)]

TASKS = {
    # 'make_plank': [['get_wood', 'use_toolshed']],
    # 'make_stick': [['get_wood', 'use_workbench']],
    # 'make_cloth': [['get_grass', 'use_factory']],
    # 'make_rope': [['get_grass', 'use_toolshed']],
    'make_bridge': [['get_iron', 'get_wood', 'use_factory']],
    # 'make_bed': [['get_wood', 'use_toolshed', 'get_grass', 'use_workbench']],
    # 'make_axe': [['get_wood', 'use_workbench', 'get_iron', 'use_toolshed']],
    # 'make_shears': [['get_wood', 'use_workbench', 'get_iron', 'use_workbench']],
    'get_gold': [['get_iron', 'get_wood', 'use_factory', 'use_bridge']],
    # 'get_gem': [['get_wood', 'use_workbench', 'get_iron', 'use_toolshed', 'use_axe']]
}

REWARD_STATES = {
    'Init': 0,
    'Alive': 0,
    'Dead': -1,
    'Score': 1000,
    'Hit': 0,
    'Forward': 0,
    'Turn': 0,
    'BadGet': 0,
    'BadUse': 0,
    'TaskProgress': 10,
    'TaskComplete': 50
}


class Minecraft(TaskExecutor):

    def __init__(self, rows=7, cols=7, trainsessionname='test'):
        global ACTION_NAMES, LOCATIONS, TASKS, REWARD_STATES
        TaskExecutor.__init__(self, rows, cols, trainsessionname)
        self.locations = LOCATIONS
        self.action_names = ACTION_NAMES
        self.tasks = TASKS
        self.reward_states = REWARD_STATES
        self.maxitemsheld = 10
        self.map_actionfns = {4: self.doget, 5: self.douse,
                              6: self.dousebridge, 7: self.douseaxe}

    def doget(self):
        what = self.itemat(self.pos_x, self.pos_y)
        if what is not None and not self.isAuto:
            print("get: ", what)
            print("has: ", self.has)
            print("maxitem: ", self.maxitemsheld)
        if what is None:
            r = self.reward_states['BadGet']
        elif len(self.has) == self.maxitemsheld:
            r = self.reward_states['BadGet']
        else:
            if not what in self.has:
                self.has.append(what)
            r = self.check_action_task('get', what)
        return r

    def douse(self):
        what = self.itemat(self.pos_x, self.pos_y)
        if what is not None and not self.isAuto:
            print("use: ", what)
        if what is None:
            r = self.reward_states['BadUse']
        else:
            r = self.check_action_task('use', what)
        return r

    def dousebridge(self):
        return self.dousetool('bridge')

    def douseaxe(self):
        return self.dousetool('axe')

    def dousetool(self, what):
        tt = 'make_%s' % what
        if not self.isAuto:
            print("use: ", what)
        if not tt in self.taskscompleted:
            r = self.reward_states['BadUse']
        else:
            r = self.check_action_task('use', what)
        return r


