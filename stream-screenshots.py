#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import socket
import subprocess
import os
import sys

log_path = '/tmp/geckodriver.log'
img_path = '/tmp'
default_port = 6000

url = os.environ.get('URL')
port = os.environ.get('PORT')

if port:
    port = int(port)
    if port < 1025 or port > 65535:
        port = default_port
else:
    port = default_port
if len(url) < 12:
    print("Not a valid URL")
    sys.exit(1)

options = Options()
options.headless = True
options.log.level = "info"
browser = webdriver.Firefox(options=options, service_log_path=log_path)

t0 = int(round(time.time() * 1000))
n = 0

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

ip = get_ip_address()

gstreamer = subprocess.Popen([
    'gst-launch-1.0', '-v', '-e',
    'fdsrc',
    '!', 'pngdec',
    '!', 'videoconvert',
    '!', 'videorate',
    '!', 'video/x-raw,framerate=25/2',
    '!', 'theoraenc',
    '!', 'oggmux',
    '!', 'tcpserversink', 'host=' + ip + '', 'port=' + str(port) + ''
    ], stdin=subprocess.PIPE)

while True:
    browser.get(url)
    filename = img_path + '/image_' + str(n).zfill(4) + '.png'
    browser.save_screenshot(filename)
    t1 = int(round(time.time() * 1000))
    print(ip + ":" + str(port) + " [" + url + "] " + str(t1 - t0) + " ms")
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
