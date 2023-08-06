import time

from JuMonC.tasks import taskPool
from JuMonC import settings

def test_taskPool():
    settings.MAX_WORKER_THREADS = 4
    taskPool._task_pool_avaiable=False
    for i in range(8):
        simpleFunc()
    assert(taskPool._thread_pool._work_queue.qsize() == 4)
    time.sleep(0.5)
    assert(taskPool._thread_pool._work_queue.qsize() >= 0)
    time.sleep(0.5)
    assert(taskPool._thread_pool._work_queue.qsize() == 0)
    
@taskPool.executeAsTask
def simpleFunc():
    time.sleep(0.5)