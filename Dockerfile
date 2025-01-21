FROM postgres:15-alpine

# Variables de entorno para la configuración inicial
ENV POSTGRES_DB=holidaydb

# Puerto por defecto de PostgreSQL
EXPOSE 5432

# Volumen para persistir los datos
VOLUME /var/lib/postgresql/data
