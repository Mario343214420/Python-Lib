import subprocess
ffmpeger=subprocess.Popen('ffmpeg -re -i e:/test.mp4 -vcodec libx264 -acodec aac -f flv rtmp://192.168.1.3:9999/hls1/test', shell=True, stdin=subprocess.PIPE)