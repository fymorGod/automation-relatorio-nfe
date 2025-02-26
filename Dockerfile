FROM python:3.9

RUN apt-get update && apt-get install -y locales && \
    sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

RUN  apt-get install -y libaio1 unzip
COPY instantclient-basic-linux.x64-11.2.0.4.0.zip /opt/oracle/
COPY instantclient-sqlplus-linux.x64-11.2.0.4.0.zip /opt/oracle/
RUN cd /opt/oracle && \
    unzip instantclient-basic-linux.x64-11.2.0.4.0.zip && \
    unzip instantclient-sqlplus-linux.x64-11.2.0.4.0.zip && \
    rm instantclient-basic-linux.x64-11.2.0.4.0.zip instantclient-sqlplus-linux.x64-11.2.0.4.0.zip ; \
    apt install libdbus-1-dev gettext librsync-dev cmake libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 gobject-introspection libgirepository1.0-dev gcc libparted-dev libsystemd-dev -y
ENV LD_LIBRARY_PATH /opt/oracle/instantclient_11_2:$LD_LIBRARY_PATH
ENV PATH /opt/oracle/instantclient_11_2:$PATH

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8

COPY . /home/www/relatorio_notas_fiscais
WORKDIR /home/www/relatorio_notas_fiscais

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
