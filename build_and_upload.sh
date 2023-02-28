docker build  -t neoh-docker .
docker stop neoh-docker-container
docker rm neoh-docker-container
docker run -d --name neoh-docker-container -p80:80 neoh-docker

