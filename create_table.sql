-- Crear usuario si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'admin') THEN
        CREATE USER admin WITH PASSWORD 'adminpass';
    END IF;
END
$$;

-- Dar privilegios al usuario
GRANT ALL PRIVILEGES ON DATABASE holidaydb TO admin;

-- Extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS holidays (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    type VARCHAR(100),
    description TEXT,
    day_week VARCHAR(20)
);
