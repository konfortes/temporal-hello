start-temporal:
	@echo "Starting temporal..."
	@docker-compose -f temporal/docker-compose.yml up -d
stop-temporal:
	@echo "Stopping temporal..."
	@docker-compose -f temporal/docker-compose.yml down