# smishing 

강의를 위한 스미싱을 차단하기 위해한 서버 및 안드로이드 앱 개발.

#### To build Dockerfile
```
docker build -t smishing .
```


#### To run DockerImage
```
docker run -d --name smishing -p 8080:80 smishing
```


#### Build & run docker-compose
```
docker-compose up -d 
```
or

#### To rebuild and rerun.
```
docker-compose up -d --build   
```


