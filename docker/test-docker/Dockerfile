FROM mundialis/actinia:2.5.0
# TODO change to latest docker image if this is fixed
# FROM mundialis/actinia:latest

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia-test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia-test

# # install things only for tests
# RUN apk add redis
# RUN pip3 install iniconfig colorlog pwgen

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

# add data for tests
RUN wget --quiet https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_micro.zip && \
  unzip nc_spm_08_micro.zip && \
  rm -f nc_spm_08_micro.zip && \
  mv nc_spm_08_micro /actinia_core/grassdb/nc_spm_08

# copy needed files and configs for test
COPY docker/test-docker/actinia.cfg /etc/default/actinia
COPY docker/test-docker/actinia.cfg /etc/default/actinia-test

# RUN make install

# ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0

# COPY docker/actinia-parallel-plugin-test/run_integration_tests.sh /usr/bin/run_integration_tests.sh
# RUN chmod a+x /usr/bin/run_integration_tests.sh
# COPY docker/actinia-parallel-plugin-test/run_unittests.sh /usr/bin/run_unittests.sh
# RUN chmod a+x /usr/bin/run_unittests.sh

# RUN make test
