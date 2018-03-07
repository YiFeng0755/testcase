import os
import time

def screen_record():
    for i in range(1,25):
        cmd='adb shell screenrecord '+"/sdcard/testui"+ str(i) +".mp4"
        os.system(cmd)
        time.sleep(3)

#screen_record()
