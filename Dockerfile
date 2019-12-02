FROM ubuntu

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV PYTHON_VERSION 3.6.7
ENV HOME /root
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
ENV PYENV_ROOT $HOME/.pyenv

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
        git \
        make \
        sqlite3 \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        vim \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev \
&& git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
&& $PYENV_ROOT/plugins/python-build/install.sh \
&& /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT \
&& rm -rf $PYENV_ROOT

RUN pyenv install 3.6.7 && \
    pyenv global 3.6.7

RUN pip install flask jupyter 
