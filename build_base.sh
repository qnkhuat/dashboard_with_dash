docker build -t dash:base -f Dockerfile_base .
docker tag dash:base docker.topica.vn/dash:base_1.1
docker push docker.topica.vn/dash:base_1.1
