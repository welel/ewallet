dev:
	docker compose -f ./docker-compose.dev.yml --env-file .env --env-file .env.db up -d

dev-build:
	docker compose -f ./docker-compose.dev.yml --env-file .env --env-file .env.db up -d --build

dev-build-no-cache:
	docker compose -f ./docker-compose.dev.yml --env-file .env --env-file .env.db build --no-cache

dev-down:
	docker compose -f ./docker-compose.dev.yml --env-file .env --env-file .env.db down
