# PROPRIETARY LIBS
import sys,time
from decentralizedroutines.RoutineScheduler import RoutineScheduler
from datetime import datetime

from SharedData.Logger import Logger
logger = Logger(__file__)

sched = RoutineScheduler()
sched.LoadSchedule()
sched.RefreshLogs()
sched.getPendingRoutines()

while(True):
    print('',end='\r')
    print('Running Schedule %s' % (str(datetime.now())),end='')
    if sched.schedule['Run Times'][0].date()<datetime.now().date():
        print('')
        print('Reloading Schedule %s' % (str(datetime.now())))
        print('')
        sched.LoadSchedule()
        sched.RefreshLogs()
        sched.getPendingRoutines()

    sched.RefreshLogs()
    sched.getPendingRoutines()
    sched.RunPendingRoutines()    
    time.sleep(15) 