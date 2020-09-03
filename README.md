# new-huawei-nbi

DESCRIPCIÓN

  Este desarrollo provee un ambiente "local" para la ejecución de sets de
  comandos en el U2020 y su adecuado registro.

AMBIENTE LOCAL

  Este ambiente local está compuesto de:

  - Una aplicación servidora (NBI) que recibe los sets de comandos enviados
    por aplicaciones cliente.

  - Un cluster Kafka que provee la infraestructura necesaria para el intercambio
    de mensajes entre las aplicaciones cliente y el servidor NBI

  - Un ejemplo de aplicación cliente, que envía un set de comandos al servidor NBI
    y que recibe respuesta de la ejecución de los mismos.

  - Una base de datos MySQL donde queda registro de los sets de comandos enviados
    y del resultado de su proceso.

  Notas:
        - La arquitectura de implementación es tal que se pueden instalar los componentes
          en distintos hosts.
        - A modo de ejemplo se podría tener un servidor NBI en un host que atendiera a todas
          las aplicaciones clientes.

DESARROLLO EN PYTHON

  Todo el desarrollo fue realizado en python 3.6 y todas las librerías utilizadas son estandar.

USO DE DOCKER-COMPOSE

  Dos de las componentes de la solución no fueron producto de este desarrollo:
  - la base de datos MySQL
  - el cluster Kafka

  En ambos casos se recurrió al uso de Docker-Compose para:

  - no tener que instalar ambos productos en el host local, lo que siempre
    es riesgoso en términos de las librerías que se descargan y que pueden
    desestabilizar el entorno local.

  - proveer de manera simple volúmenes persistentes que pueden ser administrados
    separadamente.

  - contar con un cluster Kafka, lo que garantiza persistencia y escalabilidad de procesos.

SISTEMAS OPERATIVOS EN QUE SE PUEDEN INSTALAR LOS COMPONENTES DE LA SOLUCIÓN

  El server NBI, debe tener comunicación telnet y ftp al U2020, esto fuerza que esté dentro de la 
  VPN de Huawei, esta VPN sólo puede ser levantada en Windows. Por lo que el server NBI debe estar
  instalado en Windows.

  Las aplicaciones cliente pueden correr en Windows o Linux.

DIRECTIVAS DE IMPLEMENTACIÓN

  La cola de respuestas es única, esto implica que todos los clientes, reciben
  todas las respuestas enviadas por el server NBI y no sólo las propias.

  Nota:
      - Lo anterior es manejado por la implementación cliente realizada, en que en forma
        transparente, mete en "un sobre con id único" el set de comandos que envía
        al server NBI, de modo de reconocer la respuesta asociada.
      
PREVIO A LA INSTALACIÓN DE LA SOLUCIÓN EN WINDOWS

  Instalar Docker-Compose
    https://docs.docker.com/docker-for-windows/install/

INSTALACIÓN DE LA SOLUCIÓN

  https://github.com/cjgith79/new-huawei-nbi.git

ESTRUCTURA DE LA SOLUCIÓN

  new-huawei-nbi
  ├── app-nbi
  │   ├── .env
  │   ├── client.conf
  │   ├── conector_telnet.py
  │   ├── conf.py
  │   ├── db.py
  │   ├── db_entry.py
  │   ├── encpass.py
  │   ├── event.conf
  │   ├── event.py
  │   ├── gestor_ftp.py
  │   ├── kafka.conf
  │   ├── kafka_client.py
  │   ├── kafka_nbi.py
  │   ├── mysql.conf
  │   ├── mysql-notes.txt
  │   ├── process_command_file.py
  │   ├── process_result_file.py
  │   ├── requirements.txt
  │   ├── result_mml.py
  │   ├── secrets
  │   │   └── confu_arlos.p
  │   ├── temps
  │   │   ├── result_u2020
  │   │   └── script_u2020
  │   └── utils.py
  ├── kafka-docker
  │   ├── docker-compose.yml
  │   └── Dockerfile
  └── mysql-docker
      ├── create_volume_mysql.sh
      ├── delete_volume_mysql.sh
      ├── privileges_to_testuser.sh
      ├── start_mysql.sh
      └── stop_mysql.sh

USO DE LA SOLUCIÓN

  Cluster Kafka (comandos útiles)
  
    En kafka-docker:
    
      $ docker ps -a
      $ docker-compose ps
      $ docker-compose up -d
      $ docker-compose stop
      $ docker rm $(docker ps -a -q -f status=exited)

  MySQL (comandos útiles)
  
    En mysql-docker:
    
      $ ./delete_volume_mysql.sh
      $ ./create_volume_mysql.sh
      $ ./stop_mysql.sh
      $ ./start_mysql.sh
    
      # Para entrar a la consola mysql con el usuario testuser
      $ docker exec -it mysql-test mysql -u testuser -ptestpassword
      mysql> show databases;
      mysql> use mytestdb;
      mysql> show tables;
      mysql> describe file;
      mysql> describe result;
      mysql> select * from file;
      mysql> select * from result;
      mysql> quit
    
  CONDA
  
    En app-nbi:
  
    >conda deactivate
    >conda info --envs
    >conda activate base
    >python kafka_nbi.py
    >python kafka_client.py <-- en otra Anaconda Prompt
    
