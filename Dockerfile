FROM https://github.com/alragi0/Booot.git

RUN git clone https://github.com/alragi0/Booot.git /root/mover

WORKDIR /root/mover

RUN apt update
RUN apt-get install screen
RUN apt install python3-pip

ENV PATH="/home/mover/bin:$PATH"

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["sh", "run.sh"]
