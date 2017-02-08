from __future__ import division
from __future__ import print_function

import numpy as np
import math
import os
import random

from action_space.continuous_action_space import Continuous_Action_Space
from base_environment import Environment
from observation_space import ???#TODO

PI = math.pi

class No_Ped_v0(Environment):
    def __init__(self, step_time, field_size, background_path, nmap_path):
        # action range
        act_low = np.array([0.,-PI])
        act_high = np.array([2.,PI])

        # basic environment setting
        Environment.__init__(self, step_time, field_size)
        self._step_time = step_time
        self._W, self._H = field_size
        self._action_space = Continuous_Action_Space(act_low, act_high)

        # navigation map used for reward from environment
        self._nmap = np.load(nmap_path)

        #TODO: use pygame to load image
        self._background_raw = some_function(background_path)
        assert self._background_raw.shape[0:2]==field_size, 'Loaded background should be the same size as field_size'

        # start and destination
        self._start = self._random_sample_pos() #[y,x]
        self._destination = self._random_sample_pos()
        self._dest_hw = 10 # half window for destination
        self._dest_color = (0,255,0)

        self._background = self._background_raw.copy()
        y_min = max(0, self._destination[0]-self._dest_hw)
        y_max = min(self._H, self._destination[0]+self._dest_hw)
        x_min = max(0, self._destination[1]-self._dest_hw)
        x_max = min(self._W, self._destination[1]+self._dest_hw)
        self._background[y_min:y_max, x_min:x_max, :] = self._dest_color

        # agent information, should be integers in range (H,W)
        self._x = 0
        self._y = 0
        self._color = (255,0,0)

    def step(self, action):
        # update agent position
        hor_step = action[0] * math.cos(action[1])
        vert_step = action[1] * math.sin(action[1])
        self._x += hor_step
        self._y += vert_step

        # observation, background + agent + destination
        obs = self._background.copy()
        obs[self._y,self._x,:] = self._agent_color

        # reward and terminal
        if self._x, self._y  out_of_bound:
            # agent hit the wall
            r = -1000
            t = True
        elif: self._x, self._y reach destination:
            # agent reach destination
            r = 1000
            t = True
        else:
            # agent keep wandering
            r = -1 + self._nmap[self._y,self._x]*5
            t = False

        return obs, r, t

    def display(self):
        #TODO: use pygame to display background + agent + destination
        pass

    def reset(self):
        # add destination, background_raw --> background
        self._background = self._background_raw.copy()
        self._background[?,?,:] = self._dest_color

        # add agent to background
        self._y, self._x = self._start
        obs = self._background.copy()
        obs[self._y, self._x, :] = self._agent_color

        return obs

    def set_params(self, params):
        self._start = params['start']
        self._destination = params['destination']

    def _random_sample_pos(self):
        pos_map_x, pos_map_y = np.meshgrid(np.arange(self._W), np.arange(self._H))
        valid_pos = self._nmap < 0.8
        pos_map_x = pos_map_x[valid_pos]
        pos_map_y = pos_map_y[valid_pos]
        pos = np.array([random.sample(pos_map_y,1), random.sample(pos_map_x,1)])

        return pos #(y,x)

    def __str__(self):
        des = '?'
        
        return des
        
