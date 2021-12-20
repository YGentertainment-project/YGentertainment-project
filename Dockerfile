# Build Stage
# FROM node:14-alpine AS builder

# ADD ./frontend /build
# WORKDIR /build

# RUN yarn install && \
#     yarn build

#Deploy Stage
FROM python:3.9

ENV YG_ENV production
# ENV NODE_ENV production

ADD ./backend /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python /app/deploy/health_check.py

# RUN apk add --update --no-cache build-base curl unzip jpeg-dev zlib-dev mariadb-dev freetype-dev && \
#     apk del build-base --purge

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r /app/deploy/requirements.txt
RUN chmod 755 /app/deploy/entrypoint.sh

# COPY --from=builder /build/dist /app/dist
# COPY --from=builder /app .
EXPOSE 8000

ENTRYPOINT /app/deploy/entrypoint.sh
# FROM python:3.9

# ENV YG_ENV production
# ENV PYTHONUNBUFFERED 1

# ADD ./backend /app
# WORKDIR /app

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#        postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install -r /app/deploy/requirements.txt
# RUN chmod 755 /app/deploy/entrypoint.sh

# EXPOSE 8000

# ENTRYPOINT /app/deploy/entrypoint.sh