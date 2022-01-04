FROM python:3.9

ENV YG_ENV production

ADD ./backend /app
WORKDIR /app

# HEALTHCHECK --interval=5s --retries=3 CMD python /app/deploy/health_check.py

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /app/deploy/requirements.txt
RUN chmod 755 /app/deploy/entrypoint.sh

# COPY --from=builder /build/dist /app/dist
# COPY --from=builder /app .
EXPOSE 8000

ENTRYPOINT /app/deploy/entrypoint.sh