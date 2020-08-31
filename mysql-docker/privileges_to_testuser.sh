#!/bin/sh
# Inicia un container docker con mysql:5.7 con un volumen persistente

docker exec -it mysql-test mysql -u root -p -e 'grant ALL PRIVILEGES ON *.* TO 'testuser';'
docker exec -it mysql-test mysql -u root -p -e 'flush privileges;'

# Para entrar a la consola mysql con el usuario testuser
# docker exec -it mysql-test mysql -u testuser -ptestpassword
