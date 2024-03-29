# firefox-streamer
Headless browser content streaming  
  
Uses webdriver https://www.w3.org/TR/webdriver/#take-screenshot to take screenshots of a given URL
and produces a continuous video stream


## Build container
```
$ podman build -t firefox-streamer .
```

## Run container
```
$ podman run -e STREAM_SOURCE="static-images" -e URL -v /dev/shm:/dev/shm -ti firefox-streamer
```
or
```
$ ./run.sh
```

## Open network stream with media player
Use your media player of choice to play back the network video stream
```
# mpv/mplayer/(c)vlc tcp://ip:port
$ mpv tcp://localhost:6000
```
Default port is 6000, can be overridden by env var PORT

## Issues
[firefox geckodriver issue 1577](https://github.com/mozilla/geckodriver/issues/1577)  
[firefox issue 1412061](https://bugzilla.mozilla.org/show_bug.cgi?id=1412061)  
[w3c webdriver issue 893](https://github.com/w3c/webdriver/issues/893)  
[w3c webdriver issue 895](https://github.com/w3c/webdriver/issues/895)  
[w3c issue 1088](https://github.com/w3c/csswg-drafts/issues/1088)  
