# POC

Uses webdriver https://www.w3.org/TR/webdriver/#take-screenshot to take screenshots of a given URL
and produces a continuous video stream


Build container
```
$ podman build -t firefox-streamer .
```

Run container
```
$ podman run -e URL -v /dev/shm:/dev/shm -ti firefox-streamer
```
