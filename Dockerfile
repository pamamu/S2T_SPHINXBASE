FROM pablomacias/s2t_main-controller

WORKDIR /srv/S2T/S2T_SPHINXBASE

ADD . .

RUN apk add --update libtool automake autoconf bison
RUN lib/sphinxbase/autogen.sh
RUN lib/sphinxbase/configure
RUN make -C lib/sphinxbase
RUN make install -C lib/sphinxbase

RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]


