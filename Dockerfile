FROM python:3.12

RUN apt-get update

COPY . .

RUN python -m venv /opt/venv
RUN /bin/bash -c "source /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

ENV PATH="/opt/venv/bin:$PATH"
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]