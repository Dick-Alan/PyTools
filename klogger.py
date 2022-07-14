#!/usr/bin/env python
import klog
import time

my_klog = klog.Klog(120, "<gmail>", "<gmail password>")
time.sleep(30)
my_klog.start()