#
# 이미지 출처 : https://github.com/tiangolo/uwsgi-nginx-docker
#
FROM tiangolo/uwsgi-nginx:python3.7-alpine3.8

# 작성 및 유지 보수.
# LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
#
LABEL maintainer="Gordon Ahn <tuxxon@nate.com>"

#
# Flask 설치
#
RUN pip install flask

#
# 환경변수 설정
# nginx 정적 웹문서 경로 그리고 절대경로
#
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

#
# STATIC_INDEX is 1 이면 index.html을 지정함
#
ENV STATIC_INDEX 0

#
# 서버용 앱 위치 지정함
#
COPY ./app /app
WORKDIR /app


#
# /app을 Python에서 사용가능하도록
#
ENV PYTHONPATH=/app

# 
# 콘테이너 내에서 실행가능하게 설치하는 중. 
#
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#
# 시작시, 반드시 실행.
#
ENTRYPOINT ["/entrypoint.sh"]

#
# docker run 수행시 매개변수 받을 수 있음
# 서버 실행가능
#
CMD ["/start.sh"]
