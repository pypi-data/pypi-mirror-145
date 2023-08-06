import time
import json
import random
import logging
import threading
import platform

from croniter import croniter

from .lock import RedisLock

logger = logging.getLogger(__name__)

class Schedule(object):
    
    def __init__(self,
            conn,
            channel="default",
            schedule_key_prefix="redmq:schedule:channels:",
            schedule_meta_prefix="redmq:schedule:metas:",
            schedule_events_prefix="redmq:schedule:events:",
            ):
        self.conn = conn
        self.channel = channel
        self.schedule_key = schedule_key_prefix + channel
        self.schedule_meta_key = schedule_meta_prefix + channel
        self.schedule_events_prefix = schedule_events_prefix + channel + ":"
    
    def reload_task(self, task_id, task=None, last_schedule_time=None):
        if isinstance(task_id, dict) and task is None:
            task = task_id
            task_id = task_id["id"]
        elif isinstance(task_id, dict):
            task_id = task_id["id"]
        nowtime = int(time.time())
        task = task
        if not task:
            task = self.conn.hget(self.schedule_meta_key, task_id)
            if task:
                task = json.loads(task)
        if not task:
            task = {}
        task["id"] = task_id
        task["schedule_time"] = nowtime
        if not "first_schedule_time" in task:
            task["first_schedule_time"] = nowtime
        if last_schedule_time:
            task["last_execute_time"] = last_schedule_time
        elif "next_schedule_time" in task:
            task["last_schedule_time"] = task["next_schedule_time"]
        else:
            task["last_schedule_time"] = 0
        if "next_schedule_time" in task:
            del task["next_schedule_time"]
        return task

    def add_next_schedule(self, task):
        task_id = task["id"]
        schedule_rule = task["schedule_rule"]
        if schedule_rule["type"] == "interval":
            self.add_interval_task(task_id, schedule_rule["interval"])
        elif schedule_rule["type"] == "crontab":
            self.add_crontab_task(task_id, schedule_rule["rule"])
        elif schedule_rule["type"] == "runonce":
            self.delete_task(task_id)
        else:
            raise NotImplementedError("Unknown schedule_rule...")

    def add_interval_task(self, task_id, interval, task=None, last_schedule_time=None):
        task = self.reload_task(task_id, task, last_schedule_time)
        task["schedule_rule"] = {
            "type": "interval",
            "interval": interval,
        }
        task["next_schedule_time"] = max(task["schedule_time"], task["last_schedule_time"]) + interval
        self.conn.hset(self.schedule_meta_key, task_id, json.dumps(task))
        self.conn.zadd(self.schedule_key, {task_id: task["next_schedule_time"]})
    
    def add_runonce_task(self, task_id, timeout, task=None, last_schedule_time=None):
        task = self.reload_task(task_id, task, last_schedule_time)
        task["schedule_rule"] = {
            "type": "runonce",
            "timeout": timeout,
        }
        task["next_schedule_time"] = max(task["schedule_time"], task["last_schedule_time"]) + timeout
        self.conn.hset(self.schedule_meta_key, task_id, json.dumps(task))
        self.conn.zadd(self.schedule_key, {task_id: task["next_schedule_time"]})
    
    def add_crontab_task(self, task_id, rule, task=None, last_schedule_time=None):
        task = self.reload_task(task_id, task, last_schedule_time)
        task["schedule_rule"] = {
            "type": "crontab",
            "rule": rule,
        }
        cron = croniter(rule, start_time=max(task["schedule_time"], task["last_schedule_time"]))
        task["next_schedule_time"] = int(cron.next())
        self.conn.hset(self.schedule_meta_key, task_id, json.dumps(task))
        self.conn.zadd(self.schedule_key, {task_id: task["next_schedule_time"]})

    def get_wakeup_tasks(self):
        tasks = {}
        nowtime = int(time.time())
        task_ids = self.conn.zrangebyscore(self.schedule_key, 0, nowtime)
        for task_id in task_ids:
            task = self.conn.hget(self.schedule_meta_key, task_id)
            task = task and json.loads(task) or {}
            tasks[task_id] = task
        return tasks

    def get_most_recent_task(self):
        tasks = self.conn.zrange(self.schedule_key, 0, 0, withscores=True)
        if tasks:
            task_id, _ = tasks[0]
            task = self.conn.hget(self.schedule_meta_key, task_id)
            task = task and json.loads(task) or {}
            return task
        else:
            return None
    
    def delete_task(self, task_id):
        if isinstance(task_id, dict):
            task_id = task_id["id"]
        self.conn.zrem(self.schedule_key, task_id)
        self.conn.hdel(self.schedule_meta_key, task_id)

    def add_task_event(self, task_id, event_id):
        if isinstance(task_id, dict):
            task_id = task_id["id"]
        if isinstance(event_id, dict):
            event_id = event_id["id"]
        self.conn.rpush(self.schedule_events_prefix + task_id, event_id)

    def get_task_events_count(self, task_id):
        if isinstance(task_id, dict):
            task_id = task_id["id"]
        return self.conn.llen(self.schedule_events_prefix + task_id)

    def get_task_events(self, task_id, start=0, end=-1):
        return self.conn.lrange(self.schedule_events_prefix + task_id, start, end)

    def get_task(self, task_id):
        if isinstance(task_id, dict):
            task_id = task_id["id"]
        task = self.conn.hget(self.schedule_meta_key, task_id)
        if task:
            task = json.loads(task)
            return task
        else:
            return None

    def get_all_tasks(self):
        tasks = {}
        task_ts = dict(self.conn.zrange(self.schedule_key, 0, -1, withscores=True))
        task_infos = self.conn.hgetall(self.schedule_meta_key)
        print(task_ts, task_infos)
        for task_id, score in task_ts.items():
            task = task_infos.get(task_id, "{}")
            if isinstance(task_id, bytes):
                task_id = task_id.decode("utf-8")
            tasks[task_id] = {
                "score": score,
                "task": json.loads(task),
            }
        return tasks

class Scheduler(object):

    def __init__(self, schedule, mq, max_interval=5):
        self.schedule = schedule
        self.mq = mq
        self.stop_flag = False
        self.max_interval = max_interval
        self.class_name = self.__class__.__name__

    def main_loop(self):
        thread_number = threading.get_ident()
        logger.info(f"{self.class_name} worker starting {thread_number}")
        lock_name = f"{self.class_name}:locks:{self.schedule.channel}"
        while not self.stop_flag:
            try:
                node = platform.node()
                worker_name = f"{self.class_name}:{self.schedule.channel}:{node}"
                lock = RedisLock(self.schedule.conn, lock_name, worker_name=worker_name, timeout=self.max_interval*5)
                with lock as locked:
                    if locked:
                        while not self.stop_flag:
                            tasks = self.schedule.get_wakeup_tasks()
                            wakeup_tasks = len(tasks)
                            logger.info(f"{self.class_name}.get_wakeup_tasks got {wakeup_tasks} tasks.")
                            for _, task in tasks.items():
                                task_event = self.mq.push(task)
                                self.schedule.add_task_event(task, task_event)
                                self.schedule.add_next_schedule(task)
                            lock.renew()
                            if wakeup_tasks < 1:
                                task = self.schedule.get_most_recent_task()
                                if task:
                                    sleep_time = min(task["next_schedule_time"] - time.time(), self.max_interval) - random.random()
                                else:
                                    sleep_time = self.max_interval - random.random()
                                if sleep_time < 0:
                                    sleep_time = 0
                                if sleep_time:
                                    time.sleep(sleep_time)
                    else:
                        logger.info(f"{self.class_name}.main_loop got worker lock failed...")
            except Exception as error:
                logger.exception(f"{self.class_name}.main_loop failed, error_message={error}")
            time.sleep(self.max_interval * random.random())

    def start(self):
        self.stop_flag = False
        self.worker = threading.Thread(target=self.main_loop)
        self.worker.setDaemon(True)
        self.worker.start()

    def stop(self):
        self.stop_flag = True
    
    def wait(self):
        self.worker.join()
