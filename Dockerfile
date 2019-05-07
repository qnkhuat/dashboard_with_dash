FROM docker.topica.vn/dash:base_1.1

COPY . /app
WORKDIR app

ENTRYPOINT ["python"]
CMD ["index.py"]

