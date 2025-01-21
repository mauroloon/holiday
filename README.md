# holiday
Consulta de feriados

# Python version
3.12.4

# Instalar librerías necesarias
pip install -r requirements.txt

# Inicializar DB postgresql !!! Se necesita docker
docker run --name holidaysDB -p 5432:5432 -e POSTGRES_PASSWORD=admin123 -d postgres

# Crear tabla
python db_setup.py

# Poblar tabla
python populate_db.py

# Iniciar fastApi
fastapi dev main.py

# Acceder a swagger
http://127.0.0.1:8000/docs

# Consulta de api a través de curl
curl -X 'GET' \
  'http://127.0.0.1:8000/date/?date=2023-12-25' \
  -H 'accept: application/json'