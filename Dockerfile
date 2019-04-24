
FROM python:alpine3.8

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ADD . /portal

RUN pip install -r requirements --user --no-warn-script-location

ENTRYPOINT [ "python3 manage.py runserver"]
