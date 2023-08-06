FROM python:3.8

RUN pip3 install sphinx sphinx-rtd-theme

ADD . /dev-center

# This ENV needed to hack around the git toolchain being
# unavailable to the setuptools_scm plugin. It has no
# effect on the generated docs.
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0

RUN pip3 install /dev-center/clients/python
