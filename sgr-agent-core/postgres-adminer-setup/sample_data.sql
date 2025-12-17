-- =====================================================
-- Тестовые данные для демонстрации работы системы
-- =====================================================

-- Вставляем тестовые функции
INSERT INTO dict_functions (f_lvl_1, f_lvl_2, description) VALUES
    ('Capex IT', 'Capex IT', 'Капитальные затраты на IT инфраструктуру'),
    ('IT', 'Development', 'Разработка программного обеспечения'),
    ('IT', 'Infrastructure', 'IT инфраструктура и поддержка'),
    ('Finance', 'Accounting', 'Бухгалтерский учет'),
    ('Finance', 'Planning', 'Финансовое планирование')
ON CONFLICT (f_lvl_1, f_lvl_2) DO NOTHING;

-- Вставляем тестовые трайбы
INSERT INTO dict_tribes (tribe_name, description) VALUES
    ('Platform', 'Платформенные решения'),
    ('Data', 'Работа с данными и аналитика'),
    ('Mobile', 'Мобильная разработка'),
    ('Web', 'Веб-разработка'),
    ('DevOps', 'DevOps и инфраструктура')
ON CONFLICT (tribe_name) DO NOTHING;

-- Вставляем тестовые ЦФО
INSERT INTO dict_cfo (cfo_code, cfo_name, description) VALUES
    ('CFO001', 'ЦФО Разработка', 'Центр финансовой ответственности разработки'),
    ('CFO002', 'ЦФО Инфраструктура', 'Центр финансовой ответственности инфраструктуры'),
    ('CFO003', 'ЦФО Аналитика', 'Центр финансовой ответственности аналитики'),
    ('CFO004', 'ЦФО Поддержка', 'Центр финансовой ответственности поддержки')
ON CONFLICT (cfo_code) DO NOTHING;

-- Вставляем тестовые статьи затрат
INSERT INTO dict_expense_items (pl_line, name_eng_4, name_eng_5, name_eng_6, item_code, description) VALUES
    ('CAPEX', 'IT Equipment', 'Servers', 'Server Hardware', 'CAPEX-001', 'Серверное оборудование'),
    ('CAPEX', 'IT Equipment', 'Network', 'Network Equipment', 'CAPEX-002', 'Сетевое оборудование'),
    ('CAPEX', 'Software', 'Licenses', 'Enterprise Licenses', 'CAPEX-003', 'Корпоративные лицензии'),
    ('OPEX', 'Cloud Services', 'AWS', 'AWS Compute', 'OPEX-001', 'Вычислительные ресурсы AWS'),
    ('OPEX', 'Cloud Services', 'AWS', 'AWS Storage', 'OPEX-002', 'Хранилище AWS'),
    ('OPEX', 'Personnel', 'Salaries', 'Developer Salaries', 'OPEX-003', 'Зарплаты разработчиков'),
    ('PEREX', 'Training', 'Courses', 'Online Courses', 'PEREX-001', 'Онлайн курсы для сотрудников')
ON CONFLICT DO NOTHING;

-- Вставляем тестовые данные CAPEX IT бюджета
INSERT INTO capex_it_budget (
    budget_id, function_customer, cfo_customer,
    group_initiatives_project, consolidator_initiatives, description_expense_ru,
    budgetline_author, article, article_code, expense_type, consumer_donor,
    total_current_mln_rub, group_15_currency, vat,
    jan_current_mln, feb_current_mln, mar_current_mln,
    apr_current_mln, may_current_mln, jun_current_mln,
    jul_current_mln, aug_current_mln, sep_current_mln,
    oct_current_mln, nov_current_mln, dec_current_mln,
    fiscal_year, created_by
) VALUES
    (
        'BDG-2025-001', 'Capex IT', 'CFO001',
        'Модернизация ЦОД', 'АБС ЦРТ', 'Закупка серверного оборудования для модернизации ЦОД',
        'Иванов И.И.', 'Серверное оборудование', 'CAPEX-001', 'Development', 'IT Infrastructure',
        120.50, 'RUB', TRUE,
        10.00, 10.00, 10.00,
        10.00, 10.00, 10.00,
        10.00, 10.00, 10.00,
        10.00, 10.00, 10.50,
        2025, 'admin'
    ),
    (
        'BDG-2025-002', 'Capex IT', 'CFO002',
        'Обновление сетевой инфраструктуры', 'Сетевая инфраструктура', 'Закупка коммутаторов и маршрутизаторов',
        'Петров П.П.', 'Сетевое оборудование', 'CAPEX-002', 'IT Networking', 'Network Team',
        85.30, 'RUB', TRUE,
        0.00, 0.00, 15.00,
        15.00, 15.00, 10.00,
        10.00, 10.00, 5.30,
        5.00, 0.00, 0.00,
        2025, 'admin'
    ),
    (
        'BDG-2025-003', 'Capex IT', 'CFO001',
        'Лицензии Oracle', 'Корпоративные лицензии', 'Продление корпоративных лицензий Oracle Database',
        'Сидоров С.С.', 'Лицензии ПО', 'CAPEX-003', 'License', 'Database Team',
        250.00, 'RUB', FALSE,
        0.00, 0.00, 0.00,
        0.00, 0.00, 250.00,
        0.00, 0.00, 0.00,
        0.00, 0.00, 0.00,
        2025, 'admin'
    );

-- Вставляем тестовые фактические данные
INSERT INTO budget_actuals (
    f_lvl_1, f_lvl_2, tribe_name, pl_line,
    name_eng_4, name_eng_5, name_eng_6,
    cfo_code, cfo_name,
    period_act, f_summa, p_summa, dev_summ, dev_percent
) VALUES
    (
        'Capex IT', 'Capex IT', 'Platform', 'CAPEX',
        'IT Equipment', 'Servers', 'Server Hardware',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 9.50, 10.00, -0.50, 95.00
    ),
    (
        'Capex IT', 'Capex IT', 'Platform', 'CAPEX',
        'IT Equipment', 'Servers', 'Server Hardware',
        'CFO001', 'ЦФО Разработка',
        '2025-02-28', 10.20, 10.00, 0.20, 102.00
    ),
    (
        'Capex IT', 'Capex IT', 'DevOps', 'CAPEX',
        'IT Equipment', 'Network', 'Network Equipment',
        'CFO002', 'ЦФО Инфраструктура',
        '2025-03-31', 14.80, 15.00, -0.20, 98.67
    ),
    (
        'IT', 'Development', 'Data', 'OPEX',
        'Cloud Services', 'AWS', 'AWS Compute',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 45.30, 50.00, -4.70, 90.60
    ),
    (
        'IT', 'Development', 'Data', 'OPEX',
        'Cloud Services', 'AWS', 'AWS Storage',
        'CFO001', 'ЦФО Разработка',
        '2025-01-31', 23.10, 25.00, -1.90, 92.40
    );

-- Логируем добавление тестовых данных
INSERT INTO app_logs (log_level, message, operation, metadata) 
VALUES (
    'INFO', 
    'Добавлены тестовые данные в базу', 
    'SEED',
    '{"records_inserted": {"functions": 5, "tribes": 5, "cfo": 4, "expense_items": 7, "capex_budget": 3, "actuals": 5}}'::jsonb
);

-- Выводим статистику
DO $$
DECLARE
    v_functions_count INTEGER;
    v_tribes_count INTEGER;
    v_cfo_count INTEGER;
    v_expense_items_count INTEGER;
    v_capex_count INTEGER;
    v_actuals_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_functions_count FROM dict_functions;
    SELECT COUNT(*) INTO v_tribes_count FROM dict_tribes;
    SELECT COUNT(*) INTO v_cfo_count FROM dict_cfo;
    SELECT COUNT(*) INTO v_expense_items_count FROM dict_expense_items;
    SELECT COUNT(*) INTO v_capex_count FROM capex_it_budget;
    SELECT COUNT(*) INTO v_actuals_count FROM budget_actuals;
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Тестовые данные успешно загружены!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Функций: %', v_functions_count;
    RAISE NOTICE 'Трайбов: %', v_tribes_count;
    RAISE NOTICE 'ЦФО: %', v_cfo_count;
    RAISE NOTICE 'Статей затрат: %', v_expense_items_count;
    RAISE NOTICE 'CAPEX бюджетов: %', v_capex_count;
    RAISE NOTICE 'Фактических записей: %', v_actuals_count;
    RAISE NOTICE '========================================';
END $$;
