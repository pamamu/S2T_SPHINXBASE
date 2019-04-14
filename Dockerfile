FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG SPHINXBASE_NAME
ENV SPHINXBASE_NAME = $SPHINXBASE_NAME

WORKDIR /srv/S2T/S2T_SPHINXBASE

ADD . .

RUN apk add --update libtool automake autoconf bison swig perl linux-headers

WORKDIR /srv/S2T/S2T_SPHINXBASE/lib/sphinxbase
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
#RUN make clean
#RUN make distclean
#
WORKDIR /srv/S2T/S2T_SPHINXBASE/lib/sphinxtrain
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
#RUN make clean
#RUN make distclean
##
WORKDIR /srv/S2T/S2T_SPHINXBASE/lib/pocketsphinx
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
#RUN make clean
#RUN make distclean

WORKDIR /srv/S2T/S2T_SPHINXBASE
RUN pip install -r requirements.txt

CMD python src/app.py $SPHINXBASE_NAME $SHARED_FOLDER



