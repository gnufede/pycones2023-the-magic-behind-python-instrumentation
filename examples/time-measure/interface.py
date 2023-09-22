#!/usr/bin/env python3
import time


class MeasuredDatabase(object):
    def inner_query(self):
        pass

    def query_wrapper(self):
        start_time = time.time()
        self.inner_query()
        print(time.time() - start_time)
