-- =====================================================
-- ПРИМЕРЫ АНАЛИТИЧЕСКИХ ЗАПРОСОВ
-- Для работы с отчетностью за январь 2025
-- =====================================================

-- =====================================================
-- 1. ОБЩАЯ СТАТИСТИКА ПО БЮДЖЕТУ
-- =====================================================

-- Общий бюджет CAPEX на 2025 год
SELECT 
    COUNT(*) as total_budget_lines,
    ROUND(SUM(total_current_mln_rub)::numeric, 2) as total_budget_mln_rub,
    ROUND(AVG(total_current_mln_rub)::numeric, 2) as avg_budget_per_line,
    ROUND(SUM(jan_current_mln)::numeric, 2) as january_plan_mln
FROM capex_it_budget
WHERE fiscal_year = 2025;


-- =====================================================
-- 2. ИСПОЛНЕНИЕ БЮДЖЕТА ЗА ЯНВАРЬ 2025
-- =====================================================

-- Сводка исполнения за январь
SELECT 
    COUNT(*) as total_records,
    ROUND(SUM(p_summa)::numeric, 2) as total_plan_mln,
    ROUND(SUM(f_summa)::numeric, 2) as total_fact_mln,
    ROUND(SUM(dev_summ)::numeric, 2) as total_deviation_mln,
    ROUND(AVG(dev_percent)::numeric, 2) as avg_execution_percent,
    ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as overall_execution_percent
FROM budget_actuals
WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01';


-- =====================================================
-- 3. АНАЛИЗ ПО ТРАЙБАМ
-- =====================================================

-- Исполнение бюджета по трайбам за январь
SELECT 
    tribe_name,
    COUNT(*) as records_count,
    ROUND(SUM(p_summa)::numeric, 2) as plan_mln,
    ROUND(SUM(f_summa)::numeric, 2) as fact_mln,
    ROUND(SUM(dev_summ)::numeric, 2) as deviation_mln,
    ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as execution_percent
FROM budget_actuals
WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01'
GROUP BY tribe_name
ORDER BY fact_mln DESC;


-- =====================================================
-- 4. АНАЛИЗ ПО ЦФО
-- =====================================================

-- Исполнение бюджета по ЦФО за январь
SELECT 
    cfo_code,
    cfo_name,
    COUNT(*) as records_count,
    ROUND(SUM(p_summa)::numeric, 2) as plan_mln,
    ROUND(SUM(f_summa)::numeric, 2) as fact_mln,
    ROUND(SUM(dev_summ)::numeric, 2) as deviation_mln,
    ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as execution_percent
FROM budget_actuals
WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01'
GROUP BY cfo_code, cfo_name
ORDER BY fact_mln DESC;


-- =====================================================
-- 5. АНАЛИЗ ПО СТАТЬЯМ ЗАТРАТ
-- =====================================================

-- Топ-10 статей затрат по факту за январь
SELECT 
    name_eng_4,
    name_eng_5,
    name_eng_6,
    COUNT(*) as records_count,
    ROUND(SUM(p_summa)::numeric, 2) as plan_mln,
    ROUND(SUM(f_summa)::numeric, 2) as fact_mln,
    ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as execution_percent
FROM budget_actuals
WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01'
GROUP BY name_eng_4, name_eng_5, name_eng_6
ORDER BY fact_mln DESC
LIMIT 10;


-- =====================================================
-- 6. АНАЛИЗ ПО ФУНКЦИЯМ
-- =====================================================

-- Исполнение по функциям (F_LVL_1 и F_LVL_2)
SELECT 
    f_lvl_1,
    f_lvl_2,
    COUNT(*) as records_count,
    ROUND(SUM(p_summa)::numeric, 2) as plan_mln,
    ROUND(SUM(f_summa)::numeric, 2) as fact_mln,
    ROUND(SUM(dev_summ)::numeric, 2) as deviation_mln,
    ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as execution_percent
FROM budget_actuals
WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01'
GROUP BY f_lvl_1, f_lvl_2
ORDER BY fact_mln DESC;


-- =====================================================
-- 7. ДЕТАЛЬНЫЙ АНАЛИЗ CAPEX БЮДЖЕТА
-- =====================================================

-- Бюджеты с наибольшими суммами
SELECT 
    budget_id,
    group_initiatives_project,
    description_expense_ru,
    article,
    expense_type,
    ROUND(total_current_mln_rub::numeric, 2) as total_budget_mln,
    ROUND(jan_current_mln::numeric, 2) as jan_plan_mln,
    budgetline_author,
    created_at
FROM capex_it_budget
WHERE fiscal_year = 2025
ORDER BY total_current_mln_rub DESC
LIMIT 10;


-- =====================================================
-- 8. АНАЛИЗ ОТКЛОНЕНИЙ
-- =====================================================

-- Записи с наибольшими отклонениями (недовыполнение)
SELECT 
    tribe_name,
    name_eng_6,
    cfo_name,
    ROUND(p_summa::numeric, 2) as plan_mln,
    ROUND(f_summa::numeric, 2) as fact_mln,
    ROUND(dev_summ::numeric, 2) as deviation_mln,
    ROUND(dev_percent::numeric, 2) as execution_percent,
    metadata->>'vendor' as vendor
FROM budget_actuals
WHERE period_act >= '2025-01-01' 
    AND period_act < '2025-02-01'
    AND dev_percent < 100
ORDER BY dev_summ ASC
LIMIT 10;

-- Записи с перевыполнением бюджета
SELECT 
    tribe_name,
    name_eng_6,
    cfo_name,
    ROUND(p_summa::numeric, 2) as plan_mln,
    ROUND(f_summa::numeric, 2) as fact_mln,
    ROUND(dev_summ::numeric, 2) as deviation_mln,
    ROUND(dev_percent::numeric, 2) as execution_percent,
    metadata->>'vendor' as vendor
FROM budget_actuals
WHERE period_act >= '2025-01-01' 
    AND period_act < '2025-02-01'
    AND dev_percent > 100
ORDER BY dev_percent DESC;


-- =====================================================
-- 9. АНАЛИЗ ПО ВЕНДОРАМ (из metadata)
-- =====================================================

-- Расходы по вендорам
SELECT 
    metadata->>'vendor' as vendor,
    COUNT(*) as transactions_count,
    ROUND(SUM(p_summa)::numeric, 2) as plan_mln,
    ROUND(SUM(f_summa)::numeric, 2) as fact_mln,
    ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as execution_percent
FROM budget_actuals
WHERE period_act >= '2025-01-01' 
    AND period_act < '2025-02-01'
    AND metadata ? 'vendor'
GROUP BY metadata->>'vendor'
ORDER BY fact_mln DESC;


-- =====================================================
-- 10. ИСПОЛЬЗОВАНИЕ ПРЕДСТАВЛЕНИЙ
-- =====================================================

-- Анализ по месяцам и кварталам (используя представление)
SELECT 
    budget_id,
    article,
    expense_type,
    ROUND(total_current_mln_rub::numeric, 2) as total_year,
    ROUND(q1_total::numeric, 2) as q1_total,
    ROUND(q2_total::numeric, 2) as q2_total,
    ROUND(q3_total::numeric, 2) as q3_total,
    ROUND(q4_total::numeric, 2) as q4_total
FROM v_capex_monthly_analysis
ORDER BY total_current_mln_rub DESC
LIMIT 10;

-- Сводка исполнения (используя представление)
SELECT 
    f_lvl_1,
    tribe_name,
    pl_line,
    TO_CHAR(period_month, 'YYYY-MM') as period,
    ROUND(total_plan::numeric, 2) as plan_mln,
    ROUND(total_fact::numeric, 2) as fact_mln,
    ROUND(total_deviation::numeric, 2) as deviation_mln,
    execution_percent
FROM v_budget_execution_summary
WHERE period_month >= '2025-01-01'
ORDER BY total_fact DESC;


-- =====================================================
-- 11. ПОИСК ПО ОПИСАНИЮ (полнотекстовый поиск)
-- =====================================================

-- Поиск проектов по ключевым словам
SELECT 
    budget_id,
    group_initiatives_project,
    description_expense_ru,
    article,
    ROUND(total_current_mln_rub::numeric, 2) as budget_mln
FROM capex_it_budget
WHERE description_expense_ru ILIKE '%модернизация%'
    OR group_initiatives_project ILIKE '%модернизация%'
ORDER BY total_current_mln_rub DESC;


-- =====================================================
-- 12. АНАЛИЗ МЕТАДАННЫХ
-- =====================================================

-- Проекты с высоким приоритетом
SELECT 
    budget_id,
    group_initiatives_project,
    description_expense_ru,
    ROUND(total_current_mln_rub::numeric, 2) as budget_mln,
    metadata->>'priority' as priority,
    metadata->>'department' as department
FROM capex_it_budget
WHERE metadata->>'priority' IN ('high', 'critical')
ORDER BY 
    CASE metadata->>'priority'
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        ELSE 3
    END,
    total_current_mln_rub DESC;


-- =====================================================
-- 13. СРАВНЕНИЕ ПЛАНА И ФАКТА ПО МЕСЯЦАМ
-- =====================================================

-- Сравнение январского плана из CAPEX с фактом из actuals
WITH capex_plan AS (
    SELECT 
        budget_id,
        article,
        jan_current_mln as plan_from_capex
    FROM capex_it_budget
    WHERE fiscal_year = 2025
),
actuals_fact AS (
    SELECT 
        metadata->>'budget_id' as budget_id,
        SUM(f_summa) as fact_from_actuals
    FROM budget_actuals
    WHERE period_act >= '2025-01-01' 
        AND period_act < '2025-02-01'
        AND metadata ? 'budget_id'
    GROUP BY metadata->>'budget_id'
)
SELECT 
    cp.budget_id,
    cp.article,
    ROUND(cp.plan_from_capex::numeric, 2) as plan_mln,
    ROUND(COALESCE(af.fact_from_actuals, 0)::numeric, 2) as fact_mln,
    ROUND((COALESCE(af.fact_from_actuals, 0) - cp.plan_from_capex)::numeric, 2) as deviation_mln,
    ROUND((COALESCE(af.fact_from_actuals, 0) / NULLIF(cp.plan_from_capex, 0) * 100)::numeric, 2) as execution_percent
FROM capex_plan cp
LEFT JOIN actuals_fact af ON cp.budget_id = af.budget_id
WHERE cp.plan_from_capex > 0
ORDER BY cp.plan_from_capex DESC;


-- =====================================================
-- 14. ЭКСПОРТ ДЛЯ ОТЧЕТОВ
-- =====================================================

-- Полная детализация для Excel-отчета
SELECT 
    ba.period_act as "Дата",
    ba.f_lvl_1 as "Функция (уровень 1)",
    ba.f_lvl_2 as "Функция (уровень 2)",
    ba.tribe_name as "Трайб",
    ba.pl_line as "Линия затрат",
    ba.name_eng_4 as "Статья (уровень 4)",
    ba.name_eng_5 as "Статья (уровень 5)",
    ba.name_eng_6 as "Статья (уровень 6)",
    ba.cfo_code as "Код ЦФО",
    ba.cfo_name as "Название ЦФО",
    ROUND(ba.p_summa::numeric, 2) as "План (млн руб)",
    ROUND(ba.f_summa::numeric, 2) as "Факт (млн руб)",
    ROUND(ba.dev_summ::numeric, 2) as "Отклонение (млн руб)",
    ROUND(ba.dev_percent::numeric, 2) as "Исполнение (%)",
    ba.metadata->>'vendor' as "Поставщик",
    ba.metadata->>'invoice_number' as "Номер счета"
FROM budget_actuals ba
WHERE ba.period_act >= '2025-01-01' AND ba.period_act < '2025-02-01'
ORDER BY ba.f_summa DESC;


-- =====================================================
-- 15. DASHBOARD МЕТРИКИ
-- =====================================================

-- Ключевые метрики для дашборда
WITH metrics AS (
    SELECT 
        COUNT(*) as total_transactions,
        ROUND(SUM(p_summa)::numeric, 2) as total_plan,
        ROUND(SUM(f_summa)::numeric, 2) as total_fact,
        ROUND(SUM(dev_summ)::numeric, 2) as total_deviation,
        ROUND((SUM(f_summa) / NULLIF(SUM(p_summa), 0) * 100)::numeric, 2) as execution_rate,
        COUNT(DISTINCT tribe_name) as active_tribes,
        COUNT(DISTINCT cfo_code) as active_cfos,
        COUNT(CASE WHEN dev_percent < 90 THEN 1 END) as underperforming_items,
        COUNT(CASE WHEN dev_percent > 110 THEN 1 END) as overperforming_items
    FROM budget_actuals
    WHERE period_act >= '2025-01-01' AND period_act < '2025-02-01'
)
SELECT 
    'Январь 2025' as period,
    total_transactions as "Всего транзакций",
    total_plan as "План (млн руб)",
    total_fact as "Факт (млн руб)",
    total_deviation as "Отклонение (млн руб)",
    execution_rate as "Процент исполнения",
    active_tribes as "Активных трайбов",
    active_cfos as "Активных ЦФО",
    underperforming_items as "Недовыполнение (<90%)",
    overperforming_items as "Перевыполнение (>110%)"
FROM metrics;
