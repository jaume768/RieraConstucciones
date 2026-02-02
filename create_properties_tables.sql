-- Script para crear tablas de properties manualmente
-- Solución al bug de django-parler con migraciones

-- Tabla principal Property
CREATE TABLE IF NOT EXISTS properties_property (
    id BIGSERIAL PRIMARY KEY,
    slug VARCHAR(200) UNIQUE NOT NULL,
    property_type VARCHAR(20) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    surface_area INTEGER NOT NULL,
    bedrooms INTEGER NOT NULL DEFAULT 0,
    bathrooms INTEGER NOT NULL DEFAULT 0,
    location VARCHAR(200) NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    is_sold BOOLEAN NOT NULL DEFAULT FALSE,
    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de traducciones PropertyTranslation
CREATE TABLE IF NOT EXISTS properties_property_translation (
    id BIGSERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    short_description TEXT NOT NULL,
    features TEXT,
    meta_title VARCHAR(70),
    meta_description TEXT,
    master_id BIGINT NOT NULL,
    CONSTRAINT properties_property_translation_master_fk 
        FOREIGN KEY (master_id) REFERENCES properties_property(id) ON DELETE CASCADE,
    CONSTRAINT properties_property_translation_unique 
        UNIQUE (language_code, master_id)
);

-- Índice para language_code
CREATE INDEX IF NOT EXISTS properties_property_translation_language_code_idx 
    ON properties_property_translation(language_code);

-- Índice para master_id
CREATE INDEX IF NOT EXISTS properties_property_translation_master_id_idx 
    ON properties_property_translation(master_id);

-- Tabla PropertyImage
CREATE TABLE IF NOT EXISTS properties_propertyimage (
    id BIGSERIAL PRIMARY KEY,
    image VARCHAR(100) NOT NULL,
    "order" INTEGER NOT NULL DEFAULT 0,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    property_id BIGINT NOT NULL,
    CONSTRAINT properties_propertyimage_property_fk 
        FOREIGN KEY (property_id) REFERENCES properties_property(id) ON DELETE CASCADE
);

-- Índice para property_id
CREATE INDEX IF NOT EXISTS properties_propertyimage_property_id_idx 
    ON properties_propertyimage(property_id);

-- Registrar migración como aplicada
INSERT INTO django_migrations (app, name, applied)
VALUES ('properties', '0001_initial', CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;
