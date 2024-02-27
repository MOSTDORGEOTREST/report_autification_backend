docker system prune -a -f
docker rm $(docker ps -a -q) -f
docker rmi $(docker images -a -q) -f
cd /root/projects/report_autification_backend
git pull
sudo service docker restart
docker-compose up