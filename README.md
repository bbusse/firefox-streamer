# POC

Uses webdriver https://www.w3.org/TR/webdriver/#take-screenshot to take screenshots of given URL
and produces a continuous video stream


Build container
```
$ podman build -t firefox-streamer .
```

Run container
```
$ podman run -v /dev/shm:/dev/shm -ti firefox-streamer -e URL
```
