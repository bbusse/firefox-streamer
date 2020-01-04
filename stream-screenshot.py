#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import subprocess

url = 'https://uhr.ptb.de/'
log_path = '/tmp/geckodriver.log'
img_path = '/tmp'
options = Options()
options.headless = True
options.log.level = "info"
browser = webdriver.Firefox(options=options, service_log_path=log_path)

t0 = int(round(time.time() * 1000))
n = 0

gstreamer = subprocess.Popen([
    'gst-launch-1.0', '-v', '-e',
    'fdsrc',
    '!', 'pngdec',
    '!', 'videoconvert',
    '!', 'videorate',
    '!', 'video/x-raw,framerate=25/2',
    '!', 'theoraenc',
    '!', 'oggmux',
    '!', 'tcpserversink', 'host=127.0.0.1', 'port=5000'
    ], stdin=subprocess.PIPE)

while True:
    browser.get(url)
    filename = img_path + '/image_' + str(n).zfill(4) + '.png'
    browser.save_screenshot(filename)
    t1 = int(round(time.time() * 1000))
    print(str(t1 - t0) + " ms")
    t0 = t1

    with open(filename, 'rb') as f:
        content = f.read()
        gstreamer.stdin.write(content)

    if 10 == n:
        n = 0
    else:
        n += 1

gstreamer.stdin.close()
gstreamer.wait()
browser.close()
browser.quit()
