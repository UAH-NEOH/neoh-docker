docker build --no-cache -t neoh-dockers .
docker stop neoh-dockers-container
docker rm neoh-dockers-container
docker run -d --name neoh-dockers-container -p80:80 neoh-dockers

#docker rm $(docker ps --filter status=exited -q)
#docker run -d --name neoh-docker-container -p80:80 neoh-docker

