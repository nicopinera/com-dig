# Detectar el sistema operativo
ifeq ($(OS),Windows_NT)
    ENV_ACTIVATE = venv\Scripts\activate
    PIP = venv\Scripts\pip
    PYTHON = python
else
    ENV_ACTIVATE = venv/bin/activate
    PIP = venv/bin/pip
    PYTHON = python3
endif

# Crear el entorno virtual y activar
python:
	sudo apt update
	sudo apt upgrade -y
	sudo apt install python3 -y
	sudo apt install python3-venv -y
	sudo apt install python3-pip -y
	$(PYTHON) -m venv venv
	@echo "Entorno virtual creado."

# Activar el entorno virtual e instalar dependencias
install:
	@$(PYTHON) -m venv venv && \
	chmod +x $(ENV_ACTIVATE) && \
	$(ENV_ACTIVATE) && \
	$(PYTHON) -m ensurepip --upgrade && \
	$(PYTHON) -m pip install --upgrade pip && \
	$(PYTHON) -m pip install -r requerimientos.txt
	@echo "Dependencias instaladas."