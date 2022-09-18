#!/usr/bin/env python3
import configargparse
import logging
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
public_probe_ip = "9.9.9.9"
sources = ["static-images", "v4l2loopback"]


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((public_probe_ip, 80))
    return s.getsockname()[0]


def setup_gstreamer(source, ip, port):
    if source == "static-images":
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

    elif source == "v4l2loopback":
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

    return gstreamer


def stream_images(browser, url, gstreamer):
    t0 = int(round(time.time() * 1000))
    n = 0

    while True:
        browser.get(url)
        filename = img_path + '/image_' + str(n).zfill(4) + '.png'
        browser.save_screenshot(filename)
        t1 = int(round(time.time() * 1000))
        logging.info(ip + ":" + str(port) + " [" + url + "] " + str(t1 - t0) + " ms")
        t0 = t1

        with open(filename, 'rb') as f:
            content = f.read()
            gstreamer.stdin.write(content)

        if 10 == n:
            n = 0
        else:
            n += 1


def stream_v4l2():
    return False


if __name__ == '__main__':

    parser = configargparse.ArgParser( description="")
    parser.add_argument('--logfile', dest='logfile', env_var='LOGFILE', help="Path to optional logfile", type=str)
    parser.add_argument('--loglevel', dest='loglevel', env_var='LOGLEVEL', help="Loglevel, default: INFO", type=str, default='INFO')

    args = parser.parse_args()
    logfile = args.logfile
    loglevel = args.loglevel

    # Optional File Logging
    if logfile:
        tlog = logfile.rsplit('/', 1)
        logpath = tlog[0]
        logfile = tlog[1]
        if not os.access(logpath, os.W_OK):
            # Our logger is not set up yet, so we use print here
            print("Logging: Can not write to directory. Skippking filelogging handler")
        else:
            fn = logpath + '/' + logfile
            file_handler = logging.FileHandler(filename=fn)
            # Our logger is not set up yet, so we use print here
            print("Logging: Logging to " + fn)

    stdout_handler = logging.StreamHandler(sys.stdout)

    if 'file_handler' in locals():
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [stdout_handler]

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )

    logger = logging.getLogger(__name__)
    level = logging.getLevelName(loglevel)
    logger.setLevel(level)

    url = os.environ.get('URL')
    port = os.environ.get('PORT')
    source = os.environ.get('STREAM_SOURCE')

    if port:
        port = int(port)
        if port < 1025 or port > 65535:
            port = default_port
    else:
        port = default_port
        logging.info("Using default port")

    if len(url) < 12:
        logging.error("Not a valid URL, aborting..")
        sys.exit(1)

    if not source:
        logging.error("No source defined")
        sys.exit(1)

    if not source in sources:
        logging.error("Invalid source, aborting..")
        logging.info("Possible choices are: " + sources)
        sys.exit(1)

    ip = get_ip_address()

    if source == "static-images":
        options = Options()
        options.headless = True
        options.log.level = "info"
        browser = webdriver.Firefox(options=options, service_log_path=log_path)
        gstreamer = setup_gstreamer(source, ip, port)
        stream_images(browser, url, gstreamer)
        gstreamer.stdin.close()
        gstreamer.wait()
        browser.close()
        browser.quit()
    elif source == "v4l2loopback":
        options = Options()
        options.headless = True
        options.log.level = "info"
        browser = webdriver.Firefox(options=options, service_log_path=log_path)
        browser.close()
        browser.quit()
    else:
        logging.error("Missing streaming source configuration. Exiting.")
        sys.exit(1)
