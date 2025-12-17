-- =====================================================
-- Инициализация базы данных SGR Memory Vault
-- Система учета бюджетов и финансовой аналитики
-- =====================================================

-- Включаем UUID расширение для генерации уникальных идентификаторов
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Включаем расширение для полнотекстового поиска
CREATE EXTENSION IF NOT EXISTS "pg_trgm";


-- =====================================================
-- СПРАВОЧНИКИ (DICTIONARIES)
-- =====================================================

-- Справочник функций (SMT Functions)
CREATE TABLE IF NOT EXISTS dict_functions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    f_lvl_1 VARCHAR(255) NOT NULL,
    f_lvl_2 VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(f_lvl_1, f_lvl_2)
);

COMMENT ON TABLE dict_functions IS 'Справочник функций SMT для ролевой модели';
COMMENT ON COLUMN dict_functions.f_lvl_1 IS 'Группировка функций (верхний уровень)';
COMMENT ON COLUMN dict_functions.f_lvl_2 IS 'Наименование функции SMT (детальный уровень)';


-- Справочник трайбов
CREATE TABLE IF NOT EXISTS dict_tribes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tribe_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dict_tribes IS 'Справочник трайбов';
COMMENT ON COLUMN dict_tribes.tribe_name IS 'Наименование трайба';


-- Справочник ЦФО (Cost Centers)
CREATE TABLE IF NOT EXISTS dict_cfo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cfo_code VARCHAR(50) NOT NULL UNIQUE,
    cfo_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dict_cfo IS 'Справочник центров финансовой ответственности';
COMMENT ON COLUMN dict_cfo.cfo_code IS 'Код ЦФО';
COMMENT ON COLUMN dict_cfo.cfo_name IS 'Наименование ЦФО';


-- Справочник статей затрат
CREATE TABLE IF NOT EXISTS dict_expense_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pl_line VARCHAR(50) NOT NULL,
    name_eng_4 VARCHAR(255),
    name_eng_5 VARCHAR(255),
    name_eng_6 VARCHAR(255) NOT NULL,
    item_code VARCHAR(100),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dict_expense_items IS 'Справочник статей затрат с иерархией';
COMMENT ON COLUMN dict_expense_items.pl_line IS 'Линия затрат (OPEX, CAPEX, PEREX)';
COMMENT ON COLUMN dict_expense_items.name_eng_4 IS 'Группировка статей 4-ого уровня';
COMMENT ON COLUMN dict_expense_items.name_eng_5 IS 'Группировка статей 5-ого уровня';
COMMENT ON COLUMN dict_expense_items.name_eng_6 IS 'Наименование статьи затрат (детальный слой)';


-- Справочник валют
CREATE TABLE IF NOT EXISTS dict_currencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    currency_code VARCHAR(10) NOT NULL UNIQUE,
    currency_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dict_currencies IS 'Справочник валют';

-- Вставляем базовые валюты
INSERT INTO dict_currencies (currency_code, currency_name, symbol) VALUES
    ('RUB', 'Российский рубль', '₽'),
    ('USD', 'Доллар США', '$'),
    ('EUR', 'Евро', '€')
ON CONFLICT (currency_code) DO NOTHING;


-- =====================================================
-- ОСНОВНЫЕ ТАБЛИЦЫ (MAIN TABLES)
-- =====================================================

-- Таблица CAPEX IT бюджетов
CREATE TABLE IF NOT EXISTS capex_it_budget (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Идентификация и классификация
    budget_id VARCHAR(100) NOT NULL,
    function_customer VARCHAR(255),
    cfo_customer VARCHAR(100),
    
    -- Группировка проектов
    group_initiatives_project TEXT,
    consolidator_initiatives TEXT,
    description_expense_ru TEXT,
    
    -- Автор и категоризация
    budgetline_author VARCHAR(255),
    article VARCHAR(255),
    article_code VARCHAR(100),
    expense_type VARCHAR(100),
    consumer_donor VARCHAR(255),
    
    -- Финансовые данные
    total_current_mln_rub NUMERIC(15, 2) DEFAULT 0.00,
    group_15_currency VARCHAR(10) DEFAULT 'RUB',
    vat BOOLEAN DEFAULT FALSE,
    
    -- Помесячная разбивка (в млн)
    jan_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    feb_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    mar_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    apr_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    may_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    jun_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    jul_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    aug_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    sep_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    oct_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    nov_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    dec_current_mln NUMERIC(15, 2) DEFAULT 0.00,
    
    total_current_mln_currency NUMERIC(15, 2) DEFAULT 0.00,
    
    -- Метаданные
    fiscal_year INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    updated_by VARCHAR(255),
    
    -- Дополнительные данные в JSON
    metadata JSONB,
    
    CONSTRAINT fk_currency FOREIGN KEY (group_15_currency) 
        REFERENCES dict_currencies(currency_code)
);

COMMENT ON TABLE capex_it_budget IS 'Таблица бюджетов CAPEX IT с помесячной разбивкой';
COMMENT ON COLUMN capex_it_budget.budget_id IS 'Уникальный идентификатор бюджета';
COMMENT ON COLUMN capex_it_budget.fiscal_year IS 'Финансовый год';
COMMENT ON COLUMN capex_it_budget.metadata IS 'Дополнительные метаданные в формате JSON';


-- Таблица фактических данных по бюджету
CREATE TABLE IF NOT EXISTS budget_actuals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Классификация
    f_lvl_1 VARCHAR(255),
    f_lvl_2 VARCHAR(255),
    tribe_name VARCHAR(255),
    pl_line VARCHAR(50),
    
    -- Статьи затрат (иерархия)
    name_eng_4 VARCHAR(255),
    name_eng_5 VARCHAR(255),
    name_eng_6 VARCHAR(255),
    
    -- ЦФО
    cfo_code VARCHAR(50),
    cfo_name VARCHAR(255),
    
    -- Период и суммы
    period_act DATE NOT NULL,
    f_summa NUMERIC(15, 2) DEFAULT 0.00,
    p_summa NUMERIC(15, 2) DEFAULT 0.00,
    dev_summ NUMERIC(15, 2) DEFAULT 0.00,
    dev_percent NUMERIC(5, 2) DEFAULT 0.00,
    
    -- Метаданные
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Дополнительные данные
    metadata JSONB,
    
    -- Внешние ключи
    CONSTRAINT fk_cfo FOREIGN KEY (cfo_code) 
        REFERENCES dict_cfo(cfo_code)
);

COMMENT ON TABLE budget_actuals IS 'Таблица фактических данных по бюджету с планом и отклонениями';
COMMENT ON COLUMN budget_actuals.f_lvl_1 IS 'Группировка функций (верхний уровень)';
COMMENT ON COLUMN budget_actuals.f_lvl_2 IS 'Наименование функции SMT';
COMMENT ON COLUMN budget_actuals.tribe_name IS 'Наименование трайба';
COMMENT ON COLUMN budget_actuals.pl_line IS 'Линия затрат (OPEX, CAPEX, PEREX)';
COMMENT ON COLUMN budget_actuals.name_eng_4 IS 'Группировка статей 4-ого уровня';
COMMENT ON COLUMN budget_actuals.name_eng_5 IS 'Группировка статей 5-ого уровня';
COMMENT ON COLUMN budget_actuals.name_eng_6 IS 'Наименование статьи затрат';
COMMENT ON COLUMN budget_actuals.cfo_code IS 'Код ЦФО';
COMMENT ON COLUMN budget_actuals.cfo_name IS 'Наименование ЦФО';
COMMENT ON COLUMN budget_actuals.period_act IS 'Отчетная дата';
COMMENT ON COLUMN budget_actuals.f_summa IS 'Сумма фактических затрат';
COMMENT ON COLUMN budget_actuals.p_summa IS 'Сумма плана бюджета';
COMMENT ON COLUMN budget_actuals.dev_summ IS 'Исполнение бюджета, руб';
COMMENT ON COLUMN budget_actuals.dev_percent IS 'Исполнение бюджета, проценты';


-- Таблица для логирования
CREATE TABLE IF NOT EXISTS app_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    log_level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    user_id VARCHAR(255),
    table_name VARCHAR(100),
    operation VARCHAR(50),
    metadata JSONB
);

COMMENT ON TABLE app_logs IS 'Таблица для хранения логов приложения и аудита';
COMMENT ON COLUMN app_logs.log_level IS 'Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL';
COMMENT ON COLUMN app_logs.operation IS 'Тип операции: INSERT, UPDATE, DELETE, SELECT';


-- =====================================================
-- ИНДЕКСЫ ДЛЯ ОПТИМИЗАЦИИ ЗАПРОСОВ
-- =====================================================

-- Индексы для capex_it_budget
CREATE INDEX IF NOT EXISTS idx_capex_budget_id ON capex_it_budget(budget_id);
CREATE INDEX IF NOT EXISTS idx_capex_fiscal_year ON capex_it_budget(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_capex_article_code ON capex_it_budget(article_code);
CREATE INDEX IF NOT EXISTS idx_capex_expense_type ON capex_it_budget(expense_type);
CREATE INDEX IF NOT EXISTS idx_capex_created_at ON capex_it_budget(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_capex_metadata ON capex_it_budget USING gin(metadata);

-- Индексы для budget_actuals
CREATE INDEX IF NOT EXISTS idx_actuals_period ON budget_actuals(period_act DESC);
CREATE INDEX IF NOT EXISTS idx_actuals_cfo_code ON budget_actuals(cfo_code);
CREATE INDEX IF NOT EXISTS idx_actuals_f_lvl_1 ON budget_actuals(f_lvl_1);
CREATE INDEX IF NOT EXISTS idx_actuals_f_lvl_2 ON budget_actuals(f_lvl_2);
CREATE INDEX IF NOT EXISTS idx_actuals_tribe ON budget_actuals(tribe_name);
CREATE INDEX IF NOT EXISTS idx_actuals_pl_line ON budget_actuals(pl_line);
CREATE INDEX IF NOT EXISTS idx_actuals_name_eng_6 ON budget_actuals(name_eng_6);
CREATE INDEX IF NOT EXISTS idx_actuals_metadata ON budget_actuals USING gin(metadata);

-- Составные индексы для частых запросов
CREATE INDEX IF NOT EXISTS idx_actuals_period_cfo ON budget_actuals(period_act, cfo_code);
CREATE INDEX IF NOT EXISTS idx_actuals_period_tribe ON budget_actuals(period_act, tribe_name);

-- Индексы для справочников
CREATE INDEX IF NOT EXISTS idx_dict_functions_active ON dict_functions(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_dict_tribes_active ON dict_tribes(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_dict_cfo_active ON dict_cfo(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_dict_expense_active ON dict_expense_items(is_active) WHERE is_active = TRUE;

-- Индексы для полнотекстового поиска
CREATE INDEX IF NOT EXISTS idx_capex_description_trgm ON capex_it_budget USING gin(description_expense_ru gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_capex_project_trgm ON capex_it_budget USING gin(group_initiatives_project gin_trgm_ops);

-- Индексы для логов
CREATE INDEX IF NOT EXISTS idx_app_logs_created_at ON app_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_app_logs_level ON app_logs(log_level);
CREATE INDEX IF NOT EXISTS idx_app_logs_table ON app_logs(table_name);
CREATE INDEX IF NOT EXISTS idx_app_logs_user ON app_logs(user_id);


-- =====================================================
-- ТРИГГЕРЫ ДЛЯ АВТОМАТИЧЕСКОГО ОБНОВЛЕНИЯ TIMESTAMPS
-- =====================================================

-- Функция для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Применяем триггер к таблицам
CREATE TRIGGER update_capex_it_budget_updated_at
    BEFORE UPDATE ON capex_it_budget
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_budget_actuals_updated_at
    BEFORE UPDATE ON budget_actuals
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dict_functions_updated_at
    BEFORE UPDATE ON dict_functions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dict_tribes_updated_at
    BEFORE UPDATE ON dict_tribes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dict_cfo_updated_at
    BEFORE UPDATE ON dict_cfo
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dict_expense_items_updated_at
    BEFORE UPDATE ON dict_expense_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- =====================================================
-- ПРЕДСТАВЛЕНИЯ (VIEWS) ДЛЯ АНАЛИТИКИ
-- =====================================================

-- Представление для анализа исполнения бюджета по месяцам
CREATE OR REPLACE VIEW v_capex_monthly_analysis AS
SELECT 
    budget_id,
    fiscal_year,
    article,
    expense_type,
    total_current_mln_rub,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    (jan_current_mln + feb_current_mln + mar_current_mln) AS q1_total,
    (apr_current_mln + may_current_mln + jun_current_mln) AS q2_total,
    (jul_current_mln + aug_current_mln + sep_current_mln) AS q3_total,
    (oct_current_mln + nov_current_mln + dec_current_mln) AS q4_total
FROM capex_it_budget
WHERE fiscal_year >= EXTRACT(YEAR FROM CURRENT_DATE) - 1;

COMMENT ON VIEW v_capex_monthly_analysis IS 'Представление для анализа CAPEX по месяцам и кварталам';


-- Представление для сводки по исполнению бюджета
CREATE OR REPLACE VIEW v_budget_execution_summary AS
SELECT 
    ba.f_lvl_1,
    ba.f_lvl_2,
    ba.tribe_name,
    ba.cfo_code,
    ba.cfo_name,
    ba.pl_line,
    DATE_TRUNC('month', ba.period_act) AS period_month,
    SUM(ba.p_summa) AS total_plan,
    SUM(ba.f_summa) AS total_fact,
    SUM(ba.dev_summ) AS total_deviation,
    CASE 
        WHEN SUM(ba.p_summa) > 0 
        THEN ROUND((SUM(ba.f_summa) / SUM(ba.p_summa) * 100)::numeric, 2)
        ELSE 0 
    END AS execution_percent
FROM budget_actuals ba
GROUP BY 
    ba.f_lvl_1, ba.f_lvl_2, ba.tribe_name, 
    ba.cfo_code, ba.cfo_name, ba.pl_line,
    DATE_TRUNC('month', ba.period_act);

COMMENT ON VIEW v_budget_execution_summary IS 'Сводка по исполнению бюджета с процентами выполнения';


-- =====================================================
-- ФУНКЦИИ ДЛЯ РАБОТЫ С ДАННЫМИ
-- =====================================================

-- Функция для расчета общей суммы по месяцам в CAPEX
CREATE OR REPLACE FUNCTION calculate_capex_monthly_total(capex_row capex_it_budget)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        COALESCE(capex_row.jan_current_mln, 0) +
        COALESCE(capex_row.feb_current_mln, 0) +
        COALESCE(capex_row.mar_current_mln, 0) +
        COALESCE(capex_row.apr_current_mln, 0) +
        COALESCE(capex_row.may_current_mln, 0) +
        COALESCE(capex_row.jun_current_mln, 0) +
        COALESCE(capex_row.jul_current_mln, 0) +
        COALESCE(capex_row.aug_current_mln, 0) +
        COALESCE(capex_row.sep_current_mln, 0) +
        COALESCE(capex_row.oct_current_mln, 0) +
        COALESCE(capex_row.nov_current_mln, 0) +
        COALESCE(capex_row.dec_current_mln, 0)
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION calculate_capex_monthly_total IS 'Функция для расчета суммы всех месяцев в CAPEX бюджете';


-- Функция для логирования операций
CREATE OR REPLACE FUNCTION log_operation(
    p_log_level VARCHAR,
    p_message TEXT,
    p_user_id VARCHAR DEFAULT NULL,
    p_table_name VARCHAR DEFAULT NULL,
    p_operation VARCHAR DEFAULT NULL,
    p_metadata JSONB DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_log_id UUID;
BEGIN
    INSERT INTO app_logs (log_level, message, user_id, table_name, operation, metadata)
    VALUES (p_log_level, p_message, p_user_id, p_table_name, p_operation, p_metadata)
    RETURNING id INTO v_log_id;
    
    RETURN v_log_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION log_operation IS 'Функция для добавления записей в лог с возвратом ID записи';


-- =====================================================
-- НАЧАЛЬНЫЕ ДАННЫЕ (SEED DATA)
-- =====================================================

-- Логируем успешную инициализацию
INSERT INTO app_logs (log_level, message, operation) 
VALUES ('INFO', 'База данных успешно инициализирована', 'INIT');

-- Выводим информацию о созданных объектах
DO $$
BEGIN
    RAISE NOTICE 'База данных SGR Memory Vault успешно инициализирована!';
    RAISE NOTICE 'Создано таблиц: 9';
    RAISE NOTICE 'Создано представлений: 2';
    RAISE NOTICE 'Создано функций: 3';
    RAISE NOTICE 'Создано индексов: 25+';
END $$;
