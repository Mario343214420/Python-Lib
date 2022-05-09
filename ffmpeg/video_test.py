import subprocess
import time
ffmpeger=subprocess.Popen('ffmpeg -thread_queue_size 16 -f gdigrab -i desktop -s 1280*720 -vcodec libx264 -y test2.mp4', shell=True, stdin=subprocess.PIPE)
time.sleep(10)
ffmpeger.stdin.write('q'.encode("GBK"))
ffmpeger.communicate()