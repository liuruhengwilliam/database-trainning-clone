#coding=utf-8


import threading
import time
import sys

event = threading.Event()

def func(count):
    print 'hello timer'+'%s' % count+'!\n'
    event.set()
    #yield

def timer_control(timerRange):
    for i in timerRange:
        print "xrange is %d" % i + "!\n"
        timer = threading.Timer(1, func,'%s'%i)
        yield timer.start()

def timer_demo(timerCnt,function,arg):
    #timer_control(xrange(9))
    #timer.start()
    #time.sleep(1)
    timer = threading.Timer(timerCnt, function,'%s'%arg)
    timer.start()
    print "Timer%d"%timerCnt+" start!\n"
    event.wait()
    print "event waited!\n"

def test():
    for i in xrange(9):
        timer_demo(i,func,i)

#if __name__ == '__main__':
    #test()
    #p = test()
    #while True:
    #    try:
    #        p.next()
    #    except StopIteration:
    #        sys.exit(0)


class LoopTimer(threading._Timer):
    """Call a function after a specified number of seconds:


            t = LoopTimer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting
    """
    def __init__(self, interval, function, args=[], kwargs={}):
        threading._Timer.__init__(self, interval, function, args=[], kwargs={})

    def run(self):
        '''override run function'''
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)

def testlooptimer():
    print("I am loop timer.")

def LoopTimerDemo():
    t = LoopTimer(2,testlooptimer)
    t.start()

class IntervalTimer(threading._Timer):
    """Call a function after a specified number of seconds:


            t = LoopTimer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting
    """
    def __init__(self, interval, function, args=[], kwargs={}):
        threading._Timer.__init__(self, interval, function, args=[], kwargs={})
        self.timerTuple = args
        for i in list(self.timerTuple):
            print i


    def run(self):
        '''override run function'''
        try:
            for i in list(self.timerTuple):
                #print "run %d"%i
                self.finished.wait(i)
                if self.finished.is_set():
                    self.finished.set()
                    break
                self.function(*self.args, **self.kwargs)
        except Exception,e:
            print "Exception: "+e.Message

if __name__ == '__main__':
    t = IntervalTimer(2,testlooptimer,args=[1,3,5])
    t.start()