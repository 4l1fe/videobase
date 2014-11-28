# sshd
#

FROM ubuntu:14.04

RUN echo "deb http://ppa.launchpad.net/chris-lea/node.js/ubuntu trusty main" >> /etc/apt/sources.list
RUN echo "deb-src http://ppa.launchpad.net/chris-lea/node.js/ubuntu trusty main" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y --force-yes openssh-server nginx supervisor postgresql pyp nodejs
RUN mkdir /var/run/sshd
RUN echo 'root:test' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN mkdir /var/www/

COPY id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
COPY known_hosts /root/.ssh/known_hosts
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

RUN mkdir /root/configs/
COPY db.ini /root/configs/db.ini
COPY email.ini /root/configs/email.ini
COPY uwsgi.ini /root/configs/uwsgi.ini


# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Set the locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 



EXPOSE 22
EXPOSE 80
CMD ["/usr/sbin/sshd", "-D"]