sudo docker build -t reddit-service . ;
sudo docker run --restart=always -d reddit-service ;