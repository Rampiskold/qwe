-- =====================================================
-- Детальная отчетность за месяц (Январь 2025)
-- Реалистичные данные для демонстрации системы
-- =====================================================

-- Очищаем существующие тестовые данные (опционально)
-- TRUNCATE TABLE budget_actuals CASCADE;
-- TRUNCATE TABLE capex_it_budget CASCADE;

-- =====================================================
-- CAPEX IT БЮДЖЕТ НА 2025 ГОД
-- =====================================================

-- Проект 1: Модернизация серверной инфраструктуры
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by, metadata
) VALUES
    (
        '00398', 'Capex IT', '$1706',
        'Capex IT. Реализация инициативы', 'Реализация инициативы',
        'Оплата закупа серверного оборудования с Решения С.А.',
        'Иванов С.А.', 'Цифровая рубля', 'CAPEX-SRV-001', 'Development', 'Цифровая рубля',
        228.16, 'RUB', TRUE,
        19.03, 19.03, 19.03,
        19.03, 19.03, 19.03,
        19.03, 19.03, 19.03,
        19.03, 19.03, 19.03,
        2025, 'admin',
        '{"project_code": "PRJ-2025-001", "priority": "high", "department": "Infrastructure"}'::jsonb
    ),
    (
        '00391', 'Capex IT', '$1706',
        'Capex IT. Реализация инициативы', 'Реализация инициативы',
        'Оплата закупа серверного оборудования с Решения С.А.',
        'Петров А.И.', 'Цифровая рубля', 'CAPEX-SRV-002', 'Development', 'Цифровая рубля',
        54.14, 'RUB', TRUE,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 54.14,
        2025, 'admin',
        '{"project_code": "PRJ-2025-002", "priority": "medium", "department": "Infrastructure"}'::jsonb
    );

-- Проект 2: Системы хранения данных
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by, metadata
) VALUES
    (
        '00392', 'Capex IT', '$1706',
        'Capex IT. Сопровождение и развитие АБС ЦРТ', 'АБС ЦРТ',
        'Оплата услуг по сопровождению и развитию АБС ЦРТ с Решения С.А.',
        'Сидоров В.П.', 'Цифровая рубля', 'CAPEX-ABS-001', 'Development', 'Цифровая рубля',
        14.16, 'RUB', TRUE,
        6.41, 6.41, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 1.34,
        2025, 'admin',
        '{"project_code": "PRJ-2025-003", "priority": "high", "department": "Development"}'::jsonb
    ),
    (
        '00395', 'Capex IT', '$1706',
        'Capex IT. Сопровождение и развитие АБС ЦРТ', 'АБС ЦРТ',
        'Оплата регуляторных требований с Решения С.А.',
        'Козлов Д.М.', 'Цифровая рубля', 'CAPEX-ABS-002', 'License', 'Цифровая рубля',
        10.00, 'RUB', FALSE,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        2.30, 2.30, 0.00,
        0.00, 0.00, 5.40,
        2025, 'admin',
        '{"project_code": "PRJ-2025-004", "priority": "critical", "department": "Compliance"}'::jsonb
    );

-- Проект 3: Модернизация АБС
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by, metadata
) VALUES
    (
        '00344', 'Capex IT', '$1706',
        'АБС ЦРТ. Сопровождение и развитие АБС ЦРТ', 'АБС ЦРТ',
        'Оплата работы по модернизации АБС с Борисов Е.',
        'Морозов К.С.', 'Цифровая рубля', 'CAPEX-MOD-001', 'Development', 'Цифровая рубля',
        93.32, 'RUB', FALSE,
        7.61, 7.61, 7.61,
        7.61, 7.61, 7.61,
        7.61, 7.61, 7.61,
        7.61, 7.61, 7.82,
        2025, 'admin',
        '{"project_code": "PRJ-2025-005", "priority": "high", "department": "Core Banking"}'::jsonb
    ),
    (
        '00350', 'Capex IT', '$1706',
        'АБС ЦРТ. Сопровождение и развитие АБС ЦРТ', 'АБС ЦРТ',
        'Оплата работы по интеграции с АБС с Борисов Е.',
        'Волков А.Н.', 'Цифровая рубля', 'CAPEX-MOD-002', 'IT Networking', 'Цифровая рубля',
        3.36, 'RUB', FALSE,
        3.36, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        2025, 'admin',
        '{"project_code": "PRJ-2025-006", "priority": "medium", "department": "Integration"}'::jsonb
    );

-- Проект 4: Цифровая рубля
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by, metadata
) VALUES
    (
        '00056', 'Capex IT', '$1706',
        'Цифровая рубля', 'Цифровая рубля',
        'Оплата разработки платформы цифрового рубля с Решения С.А.',
        'Новиков П.Л.', 'Цифровая рубля', 'CAPEX-DR-001', 'Development', 'Цифровая рубля',
        14.16, 'RUB', FALSE,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 14.16,
        2025, 'admin',
        '{"project_code": "PRJ-2025-007", "priority": "critical", "department": "Digital Currency"}'::jsonb
    ),
    (
        '00134', 'Capex IT', '$1706',
        'Цифровая рубля', 'Цифровая рубля',
        'Оплата интеграции с ЦБ РФ с Решения С.А.',
        'Соколов М.В.', 'Цифровая рубля', 'CAPEX-DR-002', 'IT Networking', 'Цифровая рубля',
        10.00, 'RUB', FALSE,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 10.00,
        2025, 'admin',
        '{"project_code": "PRJ-2025-008", "priority": "critical", "department": "Digital Currency"}'::jsonb
    );

-- Проект 5: Модернизация ЖБС
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by, metadata
) VALUES
    (
        '00074', 'Capex IT', '$1706',
        'Модернизация ЖБС. Внедрение новых услуг ЖБС', 'Внедрение новых услуг ЖБС',
        'Оплата работы по модернизации ЖБС с Борисов Е.',
        'Лебедев Н.Г.', 'Цифровая рубля', 'CAPEX-JBS-001', 'Development', 'Цифровая рубля',
        14.45, 'RUB', FALSE,
        0.00, 5.44, 5.44,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 3.57,
        2025, 'admin',
        '{"project_code": "PRJ-2025-009", "priority": "high", "department": "Housing Services"}'::jsonb
    );

-- Проект 6: Облачная инфраструктура
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by, metadata
) VALUES
    (
        '00093', 'Capex IT', '$1706',
        'Модернизация ЖБС. Облачная инфраструктура', 'Облачная инфраструктура',
        'Оплата облачных услуг AWS для ЖБС',
        'Егоров Р.Т.', 'Цифровая рубля', 'CAPEX-CLOUD-001', 'IT Networking', 'Цифровая рубля',
        100.00, 'RUB', TRUE,
        7.60, 7.60, 8.40,
        8.40, 8.40, 8.40,
        8.40, 8.40, 8.40,
        8.40, 8.40, 9.20,
        2025, 'admin',
        '{"project_code": "PRJ-2025-010", "priority": "high", "department": "Cloud Infrastructure", "provider": "AWS"}'::jsonb
    );


-- =====================================================
-- ФАКТИЧЕСКИЕ ДАННЫЕ ЗА ЯНВАРЬ 2025
-- =====================================================

-- Capex IT - Серверная инфраструктура
INSERT INTO budget_actuals (
    f_lvl_1, f_lvl_2, tribe_name, pl_line,
    name_eng_4, name_eng_5, name_eng_6,
    cfo_code, cfo_name,
    period_act, f_summa, p_summa, dev_summ, dev_percent,
    metadata
) VALUES
    (
        'Capex IT', 'Capex IT', 'Platform', 'CAPEX',
        'IT Equipment', 'Servers', 'Server Hardware Purchase',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 18.50, 19.03, -0.53, 97.21,
        '{"vendor": "Решения С.А.", "budget_id": "00398", "invoice_number": "INV-2025-001"}'::jsonb
    ),
    (
        'Capex IT', 'Capex IT', 'Infrastructure', 'CAPEX',
        'IT Equipment', 'Storage', 'Storage Systems',
        'CFO002', 'ЦФО Инфраструктура',
        '2025-01-31', 6.20, 6.41, -0.21, 96.72,
        '{"vendor": "Решения С.А.", "budget_id": "00392", "invoice_number": "INV-2025-002"}'::jsonb
    ),
    (
        'Capex IT', 'Capex IT', 'Core Banking', 'CAPEX',
        'Software Development', 'ABS Modernization', 'ABS Core Development',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 7.80, 7.61, 0.19, 102.50,
        '{"vendor": "Борисов Е.", "budget_id": "00344", "invoice_number": "INV-2025-003"}'::jsonb
    ),
    (
        'Capex IT', 'Capex IT', 'Integration', 'CAPEX',
        'Software Development', 'Integration', 'ABS Integration Services',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 3.36, 3.36, 0.00, 100.00,
        '{"vendor": "Борисов Е.", "budget_id": "00350", "invoice_number": "INV-2025-004"}'::jsonb
    );

-- Capex IT - Облачные сервисы (январь)
INSERT INTO budget_actuals (
    f_lvl_1, f_lvl_2, tribe_name, pl_line,
    name_eng_4, name_eng_5, name_eng_6,
    cfo_code, cfo_name,
    period_act, f_summa, p_summa, dev_summ, dev_percent,
    metadata
) VALUES
    (
        'Capex IT', 'Capex IT', 'Cloud Infrastructure', 'CAPEX',
        'Cloud Services', 'AWS', 'AWS Compute EC2',
        'CFO002', 'ЦФО Инфраструктура',
        '2025-01-31', 7.45, 7.60, -0.15, 98.03,
        '{"vendor": "AWS", "budget_id": "00093", "service": "EC2", "region": "eu-central-1"}'::jsonb
    );

-- Дополнительные записи для детализации
INSERT INTO budget_actuals (
    f_lvl_1, f_lvl_2, tribe_name, pl_line,
    name_eng_4, name_eng_5, name_eng_6,
    cfo_code, cfo_name,
    period_act, f_summa, p_summa, dev_summ, dev_percent,
    metadata
) VALUES
    -- Сетевое оборудование
    (
        'Capex IT', 'Capex IT', 'Network', 'CAPEX',
        'IT Equipment', 'Network', 'Switches and Routers',
        'CFO002', 'ЦФО Инфраструктура',
        '2025-01-31', 12.30, 15.00, -2.70, 82.00,
        '{"vendor": "Cisco", "budget_id": "NET-001", "delivery_status": "partial"}'::jsonb
    ),
    -- Лицензии ПО
    (
        'Capex IT', 'Capex IT', 'Platform', 'CAPEX',
        'Software Licenses', 'Database', 'Oracle Database Enterprise',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 45.00, 50.00, -5.00, 90.00,
        '{"vendor": "Oracle", "budget_id": "LIC-001", "license_type": "Enterprise", "users": 500}'::jsonb
    ),
    -- Системы мониторинга
    (
        'Capex IT', 'Capex IT', 'DevOps', 'CAPEX',
        'Monitoring Systems', 'APM', 'Application Performance Monitoring',
        'CFO003', 'ЦФО Аналитика',
        '2025-01-31', 8.90, 10.00, -1.10, 89.00,
        '{"vendor": "Datadog", "budget_id": "MON-001", "hosts": 150}'::jsonb
    ),
    -- Системы безопасности
    (
        'Capex IT', 'Capex IT', 'Security', 'CAPEX',
        'Security Systems', 'SIEM', 'Security Information and Event Management',
        'CFO004', 'ЦФО Поддержка',
        '2025-01-31', 22.50, 25.00, -2.50, 90.00,
        '{"vendor": "Splunk", "budget_id": "SEC-001", "log_volume_gb": 500}'::jsonb
    ),
    -- Резервное копирование
    (
        'Capex IT', 'Capex IT', 'Infrastructure', 'CAPEX',
        'Backup Systems', 'Storage', 'Backup and Recovery Solutions',
        'CFO002', 'ЦФО Инфраструктура',
        '2025-01-31', 14.80, 15.00, -0.20, 98.67,
        '{"vendor": "Veeam", "budget_id": "BAK-001", "capacity_tb": 100}'::jsonb
    ),
    -- Виртуализация
    (
        'Capex IT', 'Capex IT', 'Infrastructure', 'CAPEX',
        'Virtualization', 'VMware', 'VMware vSphere Enterprise Plus',
        'CFO002', 'ЦФО Инфраструктура',
        '2025-01-31', 32.10, 35.00, -2.90, 91.71,
        '{"vendor": "VMware", "budget_id": "VIR-001", "hosts": 50}'::jsonb
    ),
    -- Контейнеризация
    (
        'Capex IT', 'Capex IT', 'DevOps', 'CAPEX',
        'Container Platform', 'Kubernetes', 'Red Hat OpenShift',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 18.75, 20.00, -1.25, 93.75,
        '{"vendor": "Red Hat", "budget_id": "CON-001", "nodes": 30}'::jsonb
    ),
    -- CI/CD инструменты
    (
        'Capex IT', 'Capex IT', 'DevOps', 'CAPEX',
        'DevOps Tools', 'CI/CD', 'GitLab Ultimate',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 9.20, 10.00, -0.80, 92.00,
        '{"vendor": "GitLab", "budget_id": "DEV-001", "users": 200}'::jsonb
    ),
    -- Системы аналитики
    (
        'Capex IT', 'Capex IT', 'Data', 'CAPEX',
        'Analytics Platform', 'BI', 'Tableau Server',
        'CFO003', 'ЦФО Аналитика',
        '2025-01-31', 16.50, 18.00, -1.50, 91.67,
        '{"vendor": "Tableau", "budget_id": "ANA-001", "users": 100}'::jsonb
    ),
    -- Тестирование
    (
        'Capex IT', 'Capex IT', 'QA', 'CAPEX',
        'Testing Tools', 'Automation', 'Test Automation Platform',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 7.30, 8.00, -0.70, 91.25,
        '{"vendor": "Selenium Grid", "budget_id": "QA-001", "concurrent_tests": 50}'::jsonb
    );


-- =====================================================
-- ДОПОЛНИТЕЛЬНЫЕ СПРАВОЧНЫЕ ДАННЫЕ
-- =====================================================

-- Добавляем недостающие трайбы
INSERT INTO dict_tribes (tribe_name, description) VALUES
    ('Core Banking', 'Команда разработки основного банковского функционала'),
    ('Integration', 'Команда интеграционных решений'),
    ('Cloud Infrastructure', 'Команда облачной инфраструктуры'),
    ('Network', 'Команда сетевой инфраструктуры'),
    ('Security', 'Команда информационной безопасности'),
    ('QA', 'Команда обеспечения качества'),
    ('Housing Services', 'Команда жилищно-коммунальных услуг'),
    ('Digital Currency', 'Команда цифровой валюты')
ON CONFLICT (tribe_name) DO NOTHING;

-- Добавляем недостающие ЦФО
INSERT INTO dict_cfo (cfo_code, cfo_name, description) VALUES
    ('$1706', 'ЦФО IT Департамент', 'Основной ЦФО IT департамента')
ON CONFLICT (cfo_code) DO NOTHING;

-- Добавляем статьи затрат
INSERT INTO dict_expense_items (pl_line, name_eng_4, name_eng_5, name_eng_6, item_code) VALUES
    ('CAPEX', 'IT Equipment', 'Servers', 'Server Hardware Purchase', 'CAPEX-SRV-001'),
    ('CAPEX', 'IT Equipment', 'Storage', 'Storage Systems', 'CAPEX-STR-001'),
    ('CAPEX', 'IT Equipment', 'Network', 'Switches and Routers', 'CAPEX-NET-001'),
    ('CAPEX', 'Software Development', 'ABS Modernization', 'ABS Core Development', 'CAPEX-ABS-001'),
    ('CAPEX', 'Software Development', 'Integration', 'ABS Integration Services', 'CAPEX-INT-001'),
    ('CAPEX', 'Software Licenses', 'Database', 'Oracle Database Enterprise', 'CAPEX-LIC-001'),
    ('CAPEX', 'Monitoring Systems', 'APM', 'Application Performance Monitoring', 'CAPEX-MON-001'),
    ('CAPEX', 'Security Systems', 'SIEM', 'Security Information and Event Management', 'CAPEX-SEC-001'),
    ('CAPEX', 'Backup Systems', 'Storage', 'Backup and Recovery Solutions', 'CAPEX-BAK-001'),
    ('CAPEX', 'Virtualization', 'VMware', 'VMware vSphere Enterprise Plus', 'CAPEX-VIR-001'),
    ('CAPEX', 'Container Platform', 'Kubernetes', 'Red Hat OpenShift', 'CAPEX-CON-001'),
    ('CAPEX', 'DevOps Tools', 'CI/CD', 'GitLab Ultimate', 'CAPEX-DEV-001'),
    ('CAPEX', 'Analytics Platform', 'BI', 'Tableau Server', 'CAPEX-ANA-001'),
    ('CAPEX', 'Testing Tools', 'Automation', 'Test Automation Platform', 'CAPEX-QA-001'),
    ('CAPEX', 'Cloud Services', 'AWS', 'AWS Compute EC2', 'CAPEX-CLOUD-001')
ON CONFLICT DO NOTHING;


-- =====================================================
-- АНАЛИТИЧЕСКИЕ ЗАПРОСЫ ДЛЯ ПРОВЕРКИ
-- =====================================================

-- Логируем загрузку данных
INSERT INTO app_logs (log_level, message, operation, metadata) 
VALUES (
    'INFO', 
    'Загружена детальная отчетность за январь 2025', 
    'SEED',
    jsonb_build_object(
        'period', '2025-01',
        'capex_records', (SELECT COUNT(*) FROM capex_it_budget WHERE fiscal_year = 2025),
        'actuals_records', (SELECT COUNT(*) FROM budget_actuals WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01'),
        'total_budget_mln', (SELECT ROUND(SUM(total_current_mln_rub)::numeric, 2) FROM capex_it_budget WHERE fiscal_year = 2025),
        'total_fact_jan_mln', (SELECT ROUND(SUM(f_summa)::numeric, 2) FROM budget_actuals WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01')
    )
);

-- Выводим статистику
DO $$
DECLARE
    v_capex_count INTEGER;
    v_actuals_count INTEGER;
    v_total_budget NUMERIC;
    v_total_fact NUMERIC;
    v_avg_execution NUMERIC;
BEGIN
    SELECT COUNT(*) INTO v_capex_count 
    FROM capex_it_budget WHERE fiscal_year = 2025;
    
    SELECT COUNT(*) INTO v_actuals_count 
    FROM budget_actuals 
    WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01';
    
    SELECT ROUND(SUM(total_current_mln_rub)::numeric, 2) INTO v_total_budget 
    FROM capex_it_budget WHERE fiscal_year = 2025;
    
    SELECT ROUND(SUM(f_summa)::numeric, 2) INTO v_total_fact 
    FROM budget_actuals 
    WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01';
    
    SELECT ROUND(AVG(dev_percent)::numeric, 2) INTO v_avg_execution 
    FROM budget_actuals 
    WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01';
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'ОТЧЕТНОСТЬ ЗА ЯНВАРЬ 2025 ЗАГРУЖЕНА';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'CAPEX бюджетов на 2025: %', v_capex_count;
    RAISE NOTICE 'Фактических записей за январь: %', v_actuals_count;
    RAISE NOTICE 'Общий бюджет на год: % млн руб', v_total_budget;
    RAISE NOTICE 'Факт за январь: % млн руб', v_total_fact;
    RAISE NOTICE 'Среднее исполнение: %%%', v_avg_execution;
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Доступные представления для анализа:';
    RAISE NOTICE '  - v_capex_monthly_analysis';
    RAISE NOTICE '  - v_budget_execution_summary';
    RAISE NOTICE '========================================';
END $$;
