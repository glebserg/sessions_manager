#format:
#	poetry run pre-commit run --all-files

#prod:
#	poetry install --only main && \
#	chmod 664 ./fc-agent.service && \
#	cp ./fc-agent.service /etc/systemd/system/fc-agent.service && \
#	systemctl daemon-reload && \
#	systemctl enable --now fc-agent && \
#	systemctl restart fc-agent

run:
	export $$(grep -v '^#' .env | xargs) && \
	cd ./src && \
	poetry run python main.py

#update:
#	git pull
#
#reload: update prod