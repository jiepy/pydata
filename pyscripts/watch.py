#!/usr/bin/env python
# ---------------------------------------
# author : Geng Jie
# email  : gengjie@outlook.com
#
# Create Time: 2016/3/23 08:03
# ----------------------------------------
from os import path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Watcher(FileSystemEventHandler):
    def __init__(self, filename, matcher):
        # 得到文件的绝对路径
        self.filename = path.abspath(filename)
        self.matcher = matcher
        self.observer = Observer
        self.fd = None
        self.offset = 0
        # 判断是文件则打开
        if path.isfile(self.filename):
            self.fd = open(self.filename)
            # 获取文件大小
            self.offset = path.getsize(self.filename)

    def on_moved(self, event):
        if path.abspath(event.src_path) == self.filename:
            self.fd.close()
        if path.abspath(event.dest_path) == self.filename and path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)

    def on_deleted(self, event):
        if path.abspath(event.src_path) == self.filename:
            self.fd.close()

    def on_created(self, event):
        if path.abspath(event.src_path) == self.filename and path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)

    def on_modified(self, event):
        if path.abspath(event.src_path) == self.filename:
            # 将文件指针跳到文件末尾
            self.fd.seek(self.offset, 0)
            match = getattr(self.matcher, 'match', lambda x: False)
            for line in self.fd:
                line = line.rsplit('\n')
                if match(line):
                    print('matched {0}'.format(line))
            self.offset = self.fd.tell()

    def start(self):
        # 启动observer
        self.observer.schedule(self, path.dirname(self.filename), recursive=False)
        self.observer.start()
        self.observer.join()

    def stop(self):
        # 停止observer
        self.observer._stop()
        if self.fd is not None and not self.fd.closed:
            self.fd.close()


if __name__ == '__main__':
    import sys


    class match:
        def match(self, line):
            return True


    w = Watcher(sys.argv[1], match())

    try:
        w.start()
    except KeyboardInterrupt:
        w.stop()