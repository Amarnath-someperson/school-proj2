FROM python:3

COPY requirements.txt .

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["venv/bin/flask", "run", "--host=0.0.0.0", "--port=8000"]
CMD ["venv/bin/python", "app.py"]