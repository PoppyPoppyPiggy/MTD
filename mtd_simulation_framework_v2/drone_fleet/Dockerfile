# drone_fleet/Dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y openssh-server apache2 net-tools iputils-ping curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 사용자 및 SSH 설정
RUN useradd -m drone && echo "drone:drone" | chpasswd && mkdir /var/run/sshd
EXPOSE 22 80

# 기본 파일 삽입
RUN echo "hint: try admin123" > /home/drone/hint.txt && \
    echo "Fake Apache Log - GET /flag" > /var/log/apache2/access.log

CMD ["/usr/sbin/sshd", "-D"]
