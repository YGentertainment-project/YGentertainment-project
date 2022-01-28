FROM python:3.9

ENV YG_ENV production

ADD ./backend /app
WORKDIR /app

# HEALTHCHECK --interval=5s --retries=3 CMD python /app/deploy/health_check.py
RUN apt install unzip wget
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && apt-get install -yqq unzip curl \
    && rm -rf /var/lib/apt/lists/*


## install the latest version google-chrome binary
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | \
    tee -a /etc/apt/sources.list.d/google.list && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | \
    apt-key add - && \
    apt-get update && \
    apt-get install -y google-chrome-stable libxss1

# install the chromedriver dependent on installed google-chrome
RUN BROWSER_MAJOR=$(google-chrome --version | sed 's/Google Chrome \([0-9]*\).*/\1/g') && \
    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${BROWSER_MAJOR} -O chrome_version && \
    wget https://chromedriver.storage.googleapis.com/`cat chrome_version`/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    DRIVER_MAJOR=$(chromedriver --version | sed 's/ChromeDriver \([0-9]*\).*/\1/g') && \
    echo "chrome version: $BROWSER_MAJOR" && \
    echo "chromedriver version: $DRIVER_MAJOR" && \
    if [ $BROWSER_MAJOR != $DRIVER_MAJOR ]; then echo "VERSION MISMATCH"; exit 1; fi

RUN pip install --no-cache-dir -r /app/deploy/requirements.txt

ARG DATA=/data
RUN mkdir -p ${DATA}/log ${DATA}/config ${DATA}/public/avatar ${DATA}/public/website
RUN mkdir -p ${DATA}/log/server ${DATA}/log/user ${DATA}/log/crawler
RUN if [ ! -f "${DATA}/config/secret.key" ] ; then echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > "${DATA}/config/secret.key" ; fi

# COPY --from=builder /build/dist /app/dist
# COPY --from=builder /app .
EXPOSE 8000
EXPOSE 5555
#RUN chmod 755 /app/deploy/entrypoint.sh
#ENTRYPOINT /app/deploy/entrypoint.sh
