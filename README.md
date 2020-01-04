# POC

Build container
```
$ podman build -t firefox-streamer .
```

Run container
```
$ podman run -v /dev/shm:/dev/shm -ti firefox-streamer
```
