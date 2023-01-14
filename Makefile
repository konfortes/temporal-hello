start-temporal:
	@echo "Starting temporal..."
	@docker-compose -f temporal/docker-compose.yml up -d
stop-temporal:
	@echo "Stopping temporal..."
	@docker-compose -f temporal/docker-compose.yml down
run-step-0:
	@echo "Running step 0..."
	python step0/main.py
run-step-2:
	@echo "Running step 2..."
	python step2/main.py