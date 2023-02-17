# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
#ARG VARIANT="3.10-bullseye"
#FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
#ARG NODE_VERSION="none"
#RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi
FROM python:3
WORKDIR /LIVE-CAPTURE
COPY . .

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#     && rm -rf /tmp/pip-tmp

#RUN pip3 uninstall python-telegram-bot
# RUN apt-get update \
#   && apt-get -y install tesseract-ocr \
#   && apt-get -y install tesseract-ocr-vie
  #&& apt-get install -y python3 python3-distutils python3-pip \
  #&& cd /usr/local/bin \
  #&& ln -s /usr/bin/python3 python \
  #&& pip3 --no-cache-dir install --upgrade pip \
  #&& rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install python-telegram-bot
RUN pip3 install mplfinance
#RUN pip3 install tesseract
#RUN pip3 install pytesseract
#RUN pip3 install selenium
RUN pip3 install APScheduler
RUN pip3 install requests
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install seaborn
RUN pip3 install lxml
RUN pip3 install tabulate
RUN pip3 install vnstock
RUN pip3 install openpyxl
RUN pip3 install markdown
RUN pip3 install python-wordpress-xmlrpc
RUN pip3 install wolframalpha
RUN pip3 install html5lib
RUN pip3 install translate
RUN pip3 install langdetect
RUN pip3 install pymongo
RUN pip3 install beautifulsoup4

#RUN pip3 install htmldocx
#RUN pip3 install json-normalize

#RUN sudo apt-get install tesseract-ocr-vie
#RUN brew install tesseract

CMD ["python","./bot.py"]
#CMD ["python","./bot.py;./bot2.py"]

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1