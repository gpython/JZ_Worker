#encoding:utf-8

import Queue

class Chat(object):
  def __init__(self):
    self.msg_queue = Queue.Queue()

  def get_qmsg(self, request):
    new_msgs = []
    if self.msg_queue.qsize() > 0:
      for msg in range(self.msg_queue.qsize()):
        new_msgs.append(self.msg_queue.get_nowait())
      return new_msgs
    else:
      try:
        print "--------------------Queue-----------------------"
        new_msgs.append(self.msg_queue.get())
        print "Queue Found new message: ", new_msgs
      except Queue.Empty:
        print "Queue Timeout no new message"
    print "Queue length: ", len(new_msgs)
    return new_msgs
