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
	$(PYTHON) -m venv venv
	@echo "Entorno virtual creado."

# Activar el entorno virtual e instalar dependencias
install:
	@$(PYTHON) -m venv venv && \
	$(ENV_ACTIVATE) && \
	$(PYTHON) -m pip install --upgrade pip && \
	$(PYTHON) -m pip install -r requerimientos.txt
	@echo "Dependencias instaladas."