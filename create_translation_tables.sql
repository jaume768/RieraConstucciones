-- Blog: CategoryTranslation
CREATE TABLE IF NOT EXISTS blog_category_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    master_id INTEGER NOT NULL REFERENCES blog_category(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Blog: TagTranslation
CREATE TABLE IF NOT EXISTS blog_tag_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    name VARCHAR(100) NOT NULL,
    master_id INTEGER NOT NULL REFERENCES blog_tag(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Blog: PostTranslation
CREATE TABLE IF NOT EXISTS blog_post_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    title VARCHAR(200) NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    meta_title VARCHAR(70),
    meta_description TEXT,
    master_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Services: ServiceTranslation
CREATE TABLE IF NOT EXISTS services_service_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    title VARCHAR(200) NOT NULL,
    short_description VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    meta_title VARCHAR(70),
    meta_description TEXT,
    master_id INTEGER NOT NULL REFERENCES services_service(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Core: PageTranslation
CREATE TABLE IF NOT EXISTS core_page_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    meta_title VARCHAR(70),
    meta_description TEXT,
    master_id INTEGER NOT NULL REFERENCES core_page(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Core: TeamMemberTranslation
CREATE TABLE IF NOT EXISTS core_teammember_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    position VARCHAR(200) NOT NULL,
    bio TEXT,
    master_id INTEGER NOT NULL REFERENCES core_teammember(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Core: CompanyValueTranslation
CREATE TABLE IF NOT EXISTS core_companyvalue_translation (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(15) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    master_id INTEGER NOT NULL REFERENCES core_companyvalue(id) ON DELETE CASCADE,
    UNIQUE (language_code, master_id)
);

-- Crear índices
CREATE INDEX IF NOT EXISTS blog_category_translation_language_code ON blog_category_translation(language_code);
CREATE INDEX IF NOT EXISTS blog_tag_translation_language_code ON blog_tag_translation(language_code);
CREATE INDEX IF NOT EXISTS blog_post_translation_language_code ON blog_post_translation(language_code);
CREATE INDEX IF NOT EXISTS services_service_translation_language_code ON services_service_translation(language_code);
CREATE INDEX IF NOT EXISTS core_page_translation_language_code ON core_page_translation(language_code);
CREATE INDEX IF NOT EXISTS core_teammember_translation_language_code ON core_teammember_translation(language_code);
CREATE INDEX IF NOT EXISTS core_companyvalue_translation_language_code ON core_companyvalue_translation(language_code);
