FROM python:3.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY . .
CMD ["python3",  "adapter.py"]
