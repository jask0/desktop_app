# -*- coding: utf-8 -*-
import queue

RESPONSE_QUEUE = queue.Queue()

def putInQueue(target, *args):
    ''' puts command into the response queue '''

    global RESPONSE_QUEUE
    # store data
    RESPONSE_QUEUE.put((target, args))

def Response():
    ''' multitasker response queue '''
    return RESPONSE_QUEUE.get(block=False)