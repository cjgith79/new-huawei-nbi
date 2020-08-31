#!/bin/sh
# Inicia un container docker con mysql:5.7 con un volumen persistente

docker run --name mysql-test -e MYSQL_ROOT_PASSWORD=my-secret-pw \
	--mount src=mysql-test-data,dst=/var/lib/mysql \
	-e MYSQL_DATABASE=mytestdb -e MYSQL_USER=testuser \
	-e MYSQL_PASSWORD=testpassword --publish 33060:3306 -d mysql:5.7

# Para entrar a la consola mysql con el usuario testuser:
# $ ./privileges_to_testuser.sh
# docker exec -it mysql-test mysql -u testuser -ptestpassword
