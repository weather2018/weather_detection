from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from collect import crawling_day, crawling_min, simulator
import time
from datetime import datetime, timedelta


class Scheduler(object):

    def __init__(self, hh=9, mm=20):
        now = str(datetime.now() - timedelta(days=1))
        now = now.split(' ')
        yyyymmdd = now[0].replace('-', '')
        hhmmss = now[1].split('.')[0].split(':')[:2]
        self.timeDic = {'yyyy': yyyymmdd[0:4],
                        'mm': yyyymmdd[4:6],  # str(int(yyyymmdd[4:6]) - 1),
                        'dd': yyyymmdd[6:8],  # str(int()),
                        'hhmm': hhmmss[0] + hhmmss[1]}

        self.sched = BackgroundScheduler()
        self.sched.start()
        # self.hh = hh
        # self.mm = mm

        # 테스트 용이성 위해 사용
        self.hh = int(self.timeDic['hhmm'][0:2])
        self.mm = int(self.timeDic['hhmm'][2:4])+1
        self.job_id = ''

    # 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
    def __del__(self):
        self.shutdown()

    # 모든 job들을 종료시켜주는 함수입니다.
    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self,job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print('fail to stop scheduler: %s'% err)
            return

    def scheduler(self, type, job_id):
        print("%s scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))
        if type =='interval':
            self.sched.add_job(simulator.main,
                               trigger=type,
                               seconds=60,
                               id=job_id,
                               args=(self.timeDic['yyyy'],
                                     self.timeDic['mm'],
                                     self.timeDic['dd'],
                                     self.timeDic['hhmm']))
            # self.sched.add_job(self.hello, type, seconds=300, id=job_id, args=(type, job_id))

        elif (type == 'cron' and  job_id=='2'):
            print("%s scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))
            self.sched.add_job(crawling_min.main,
                               trigger=type,
                               day_of_week='mon-sun',
                               hour=self.hh, minute=self.mm,
                               id=job_id,
                               args=(self.timeDic['yyyy'],
                                     self.timeDic['mm'],
                                     self.timeDic['dd']
                                     ))

        elif (type == 'cron' and  job_id=='3'):
            print("%s scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))
            self.sched.add_job(crawling_day.main,
                               trigger=type,
                               day_of_week='mon-sun',
                               hour=self.hh, minute=self.mm,
                               id=job_id
                               )

    def test(self):
        print('[%s] Schedule TEST call def ' % str(time.localtime()))

def main(hh,ss):
    sched = Scheduler(hh,ss)
    sched.scheduler(type='interval',job_id='1')
    sched.scheduler(type='cron',job_id='2')
    sched.scheduler(type='cron',job_id='3')
    while True:
        time.sleep(1)

if __name__=='__main__':
    sched = Scheduler()
    sched.scheduler(type='interval',job_id='1')
    #sched.scheduler(type='cron',job_id='2')
    # sched.scheduler(type='cron',job_id='3')
    while True:
        time.sleep(1)