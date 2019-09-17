#!/usr/bin/env python
from enum import Enum


class simState(Enum):
    Paused = 0
    Play = 1
    Step = 2
    StepGame = 3

class playerState(Enum):
    Out = 0
    In = 1
