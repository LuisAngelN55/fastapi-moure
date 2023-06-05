# fastapi-moure

docker run --name tryhard-postgres -e POSTGRES_USER=zuntrix -e POSTGRES_PASSWORD=zuntrix -p 5432:5432 -v /Users/luisangel/Documents/LuisAngel/Postgres/data -d postgres

/Users/luisangel/Documents/LuisAngel/Postgres/data

PostgreSQL is the name of the Docker Container.
-e POSTGRES_USER is the parameter that sets a unique username to the Postgres database.
-e POSTGRES_PASSWORD is the parameter that allows you to set the password of the Postgres database.
-p 5432:5432 is the parameter that establishes a connection between the Host Port and Docker Container Port. In this case, both ports are given as 5432, which indicates requests sent to the Host Ports will automatically redirect to the Docker Container Port. In addition, 5432 is also the same port where PostgreSQL will be accepting requests from the client.
-v is the parameter that synchronizes the Postgres data with the local folder. This ensures that Postgres data will be safely present within the Home Directory even if the Docker Container is terminated.
-d is the parameter that runs the Docker Container in the detached mode, i.e., in the background. If you accidentally close or terminate the Command Prompt, the Docker Container will still run in the background.
Postgres is the name of the Docker image that was previously downloaded to run the Docker Container.




docker pull dpage/pgadmin4:latest

After downloading the image, run the container by executing the command given below.

docker run --name tryhard-pgadmin -p 82:80 -e 'PGADMIN_DEFAULT_EMAIL=zuntrixit@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=zuntrix' -d dpage/pgadmin4

In the above-given command, my-pgadmin is the name of the Docker PostgreSQL PGAdmin Container. PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD are the username and passwords for the Docker PostgreSQL container, respectively.