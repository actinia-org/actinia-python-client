# SPDX-FileCopyrightText: (c) 2022-2025 by mundialis GmbH & Co. KG
# SPDX-License-Identifier: GPL-3.0-or-later

FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install \
    git \
    python3 \
    python3-pip \
    python3.8-venv \
    -y
# RUN python3.8-venv libgdal-dev -y
RUN pip3 install build twine
RUN pip3 install --upgrade setuptools
