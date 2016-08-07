#encoding=utf-8
################################################
#   由于Queue.Queue get()和 qsize() 不是原子操作,
#   所以这里做简单封装
##################################################

import Queue


class ShareQueue(Queue.Queue):
    def get_one(self):
        '''
            非阻塞获取队列中的数据
        '''
        x = None
        self.mutex.acquire()

        n = self._qsize()
        if n > 0:
            x = self._get()
        else:
            x = None

        self.mutex.release()

        return x