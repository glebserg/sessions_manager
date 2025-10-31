run-app:
	@echo "Запускаю приложение"
	export $$(grep -v '^#' .env | xargs) && \
	cd ./src && \
	poetry run python main.py

install-app:
	@echo "Устанавливаю приложение"
	sudo dpkg -i ./deb-packages/session-manager_0.0.1_all.deb

remove-app:
	@echo "Удаляю приложение"
	sudo apt remove session-manager -y

build-package:
	@echo "Собираю приложение"
	dpkg-buildpackage -us -uc -b && mv ../session-manager_* ./deb-packages
