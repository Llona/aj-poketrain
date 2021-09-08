# _*_ coding:utf-8 _*_

import time
import configparser
import os
from multiprocessing import Process
import threading
import json
from threading import Timer


class CreateEmptyThread(threading.Thread):
    def __init__(self, queue, stop_str):
        threading.Thread.__init__(self)
        self.thread_queue = queue
        self.stop_str = stop_str
        # self.thread_queue = queue.Queue()

    def run(self):
        try:
            while True:
                msg = self.thread_queue.get()
                print('get stop event: {}'.format(msg))
                if msg == self.stop_str:
                    print('stop thread: {}'.format(msg))
                    return
                time.sleep(0.2)
        except Exception as e:
            print('get queue fail: {}'.format(e))


class CreateTimer(object):
    def __init__(self):
        self.timer_h = None

    def is_timer_running(self):
        if self.timer_h and self.timer_h.isAlive():
            return True
        return False

    def start_count_timer(self, sec, callback, args='', repeat=False):
        # print('start timer')
        self.stop_count_timer()
        self.timer_h = Timer(sec, self.timer_count_expired, (callback, args, repeat, ))
        self.timer_h.start()

    def stop_count_timer(self):
        # print('stop timer')
        if self.is_timer_running():
            self.timer_h.cancel()

    def timer_count_expired(self, callback, args, repeat):
        if args:
            callback(args)
        else:
            callback()

        if repeat:
            self.start_count_timer(0.2, callback, args, repeat)
        else:
            self.stop_count_timer()


def create_process(process_list, args_list):
    process_ll = []
    count = 0

    for process_f in process_list:
        process_ll.append(Process(target=process_f, args=args_list[count]))
        count += 1

    for process in process_ll:
        process.start()

    for process in process_ll:
        process.join()


class JsonControl(object):
    def __init__(self, json_full_path):
        self.json_full_path = json_full_path
        self.json_format = 'utf8'
        self.format_list = ['utf8', 'utf-8-sig', 'utf16', None, 'big5', 'gbk', 'gb2312']
        if os.path.exists(self.json_full_path):
            self.try_ini_format()

    def try_ini_format(self):
        for file_format in self.format_list:
            try:
                with open(self.json_full_path, 'r', encoding=file_format) as file:
                    json_dic = json.load(file)
                self.json_format = file_format
                print('find correct format {} in json file: {}'.format(file_format, self.json_full_path))
                return
            except Exception as e:
                print('checking {} format: {}'.format(self.json_full_path, file_format))
                str(e)

    def read_config(self):
        try:
            with open(self.json_full_path, 'r', encoding=self.json_format) as file:
                return json.load(file)
        except Exception as e:
            print("Error! 讀取cfg設定檔發生錯誤!: {} {}".format(self.json_full_path, e))
            raise

    def write_config(self, json_content):
        try:
            with open(self.json_full_path, 'w', encoding=self.json_format) as file:
                json.dump(json_content, file, ensure_ascii=False, indent=4, separators=(',', ':'))
        except Exception as e:
            print("Error! 寫入cfg設定檔發生錯誤! {} {}".format(self.json_full_path, e))
            # str(e)
            raise


class IniControl(object):
    def __init__(self, ini_full_path):
        self.ini_full_path = ini_full_path
        self.ini_format = 'utf8'
        self.format_list = ['utf8', 'utf-8-sig', 'utf16', None, 'big5', 'gbk', 'gb2312']
        self.try_ini_format()

    def try_ini_format(self):
        for file_format in self.format_list:
            try:
                config_lh = configparser.ConfigParser()
                with open(self.ini_full_path, 'r', encoding=file_format) as file:
                    config_lh.read_file(file)
                self.ini_format = file_format
                print('find correct format {} in ini file: {}'.format(file_format, self.ini_full_path))
                return
            except Exception as e:
                print('checking {} format: {}'.format(self.ini_full_path, file_format))
                str(e)

    def read_config(self, section, key):
        try:
            config_lh = configparser.ConfigParser()
            file_ini_lh = open(self.ini_full_path, 'r', encoding=self.ini_format)
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()
            return config_lh.get(section, key)
        except Exception as e:
            print("Error! 讀取ini設定檔發生錯誤! " + self.ini_full_path)
            str(e)
            raise

    def write_config(self, sections, key, value):
        try:
            config_lh = configparser.ConfigParser()
            config_lh.optionxform = str
            file_ini_lh = open(self.ini_full_path, 'r', encoding=self.ini_format)
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()

            file_ini_lh = open(self.ini_full_path, 'w', encoding=self.ini_format)
            config_lh.set(sections, key, value)
            config_lh.write(file_ini_lh)
            file_ini_lh.close()
        except Exception as e:
            print("Error! 寫入ini設定檔發生錯誤! " + self.ini_full_path)
            str(e)
            raise
