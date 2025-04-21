# drone_fleet/Dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y openssh-server apache2 net-tools iputils-ping curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m drone && echo "drone:drone" | chpasswd && adduser drone sudo

RUN mkdir /var/run/sshd
EXPOSE 22 80

# 미끼 서비스용 가짜 힌트 파일 생성
RUN echo "hint: password is not 1234" > /home/drone/hint.txt

CMD ["/usr/sbin/sshd", "-D"]
