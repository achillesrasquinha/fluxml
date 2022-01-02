FROM  python:3.9-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV FLUXML_PATH=/usr/local/src/fluxml \
    DIAMOND_VERSION=2.0.13

RUN apk add --no-cache \
        bash \
        git \
        g++ \
        make \
        boost-dev && \
    git clone https://github.com/Gaius-Augustus/Augustus.git /Augustus --depth 1 && \
    cd /Augustus && \
    make install && \
    wget http://github.com/bbuchfink/diamond/releases/download/v${DIAMOND_VERSION}/diamond-linux64.tar.gz && \
    mkdir -p $FLUXML_PATH && \
    apk remove .build-deps && \
    rm -rf /Augustus

COPY . $FLUXML_PATH
COPY ./docker/entrypoint.sh /entrypoint.sh

WORKDIR $FLUXML_PATH

RUN pip install -r ./requirements.txt && \
    python setup.py install

ENTRYPOINT ["/entrypoint.sh"]

CMD ["fluxml"]