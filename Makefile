# Docker Makefile
.PHONY: start
start:
	docker-compose --env-file ./.env -f ./postgres-docker-compose.yaml  up -d
	docker-compose -f airflow-docker-compose.yaml up -d

down:
	docker-compose -f postgres-docker-compose.yaml down  --remove-orphans
	docker-compose -f airflow-docker-compose.yaml down  --remove-orphans

cleanup:
	docker-compose -f postgres-docker-compose.yaml down --volumes --rmi all
	docker-compose -f airflow-docker-compose.yaml down --volumes --rmi all
