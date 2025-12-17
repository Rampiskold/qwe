"""
Интерактивный Streamlit интерфейс для визуализации трейсинга агента.

Модуль создает роудмап работы агента на основе JSON логов,
чтобы отобразить шаги выполнения, reasoning, вызовы инструментов и метрики.
"""

import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from log_parser import LogParser, AgentStep
from visualizers import RoadmapVisualizer, MetricsVisualizer, TimelineVisualizer
from trace_visualizer import TraceVisualizer
import json


def load_log_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Загружает JSON файл с логами агента.
    
    Args:
        file_path: Путь к файлу с логами
        
    Returns:
        Словарь с данными логов или None при ошибке
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {e}")
        return None


def get_available_logs(logs_dir: str = "logs") -> List[Path]:
    """
    Получает список доступных файлов логов в директории.
    
    Args:
        logs_dir: Директория с логами
        
    Returns:
        Список путей к файлам логов
    """
    logs_path = Path(logs_dir)
    if not logs_path.exists():
        return []
    
    return sorted(
        logs_path.glob("*.json"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )


def render_agent_info(log_data: Dict[str, Any]) -> None:
    """
    Отображает основную информацию об агенте и задаче.
    
    Args:
        log_data: Данные из файла логов
    """
    st.header("🤖 Информация об агенте")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("ID агента", log_data.get('id', 'N/A').split('_')[-1][:8])
        st.metric("Модель", log_data.get('model_config', {}).get('model', 'N/A'))
    
    with col2:
        st.metric("Температура", log_data.get('model_config', {}).get('temperature', 'N/A'))
        st.metric("Max tokens", log_data.get('model_config', {}).get('max_tokens', 'N/A'))
    
    with col3:
        toolkit = log_data.get('toolkit', [])
        st.metric("Количество инструментов", len(toolkit))
        
    st.subheader("📋 Задача")
    st.info(log_data.get('task', 'Задача не указана'))
    
    st.subheader("🛠️ Набор инструментов")
    cols = st.columns(4)
    for idx, tool in enumerate(toolkit):
        with cols[idx % 4]:
            st.code(tool, language=None)


def render_roadmap(parser: LogParser, visualizer: RoadmapVisualizer) -> None:
    """
    Отображает роудмап работы агента.
    
    Args:
        parser: Парсер логов с обработанными данными
        visualizer: Визуализатор роудмапа
    """
    st.header("🗺️ Роудмап выполнения")
    
    steps = parser.get_steps()
    
    if not steps:
        st.warning("Нет данных для отображения роудмапа")
        return
    
    # Создаем визуализацию роудмапа
    fig = visualizer.create_roadmap(steps)
    st.plotly_chart(fig, width='stretch')
    
    # Показываем детали каждого шага - группируем reasoning и execution
    st.subheader("📝 Детали шагов")
    
    # Группируем шаги по номеру
    steps_grouped = {}
    for step in steps:
        if step.step_number not in steps_grouped:
            steps_grouped[step.step_number] = []
        steps_grouped[step.step_number].append(step)
    
    # Отображаем сгруппированные шаги
    for step_num in sorted(steps_grouped.keys()):
        render_step_group(step_num, steps_grouped[step_num])


def render_step_group(step_num: int, steps: List[AgentStep]) -> None:
    """
    Отображает группу шагов с одним номером (reasoning + execution).
    
    Args:
        step_num: Номер шага
        steps: Список шагов с одинаковым номером
    """
    # Находим reasoning и execution шаги
    reasoning_step = None
    execution_steps = []
    llm_calls = []
    
    for step in steps:
        if step.step_type == 'reasoning':
            reasoning_step = step
        elif step.step_type == 'tool_execution':
            execution_steps.append(step)
        elif step.step_type == 'llm_call':
            llm_calls.append(step)
    
    # Считаем реальное количество операций
    total_ops = len([s for s in steps if s.step_type in ['reasoning', 'tool_execution']])
    
    # Определяем цвет и иконку на основе типа шага
    if reasoning_step and reasoning_step.reasoning.get('task_completed'):
        icon = "✅"
        color = "green"
    elif execution_steps:
        # Проверяем тип инструмента
        tool_names = [e.tool_calls[0]['name'] if e.tool_calls else 'unknown' for e in execution_steps]
        if 'finalanswertool' in tool_names:
            icon = "✅"
        else:
            icon = "🛠️"
        color = "blue"
    else:
        icon = "🤔"
        color = "orange"
    
    # Формируем описание шага
    step_desc = []
    if reasoning_step:
        step_desc.append("reasoning")
    if execution_steps:
        for exec_step in execution_steps:
            if exec_step.tool_calls:
                tool_name = exec_step.tool_calls[0].get('name', 'unknown')
                step_desc.append(tool_name)
    
    desc_text = " + ".join(step_desc) if step_desc else f"{len(steps)} операций"
    
    with st.expander(f"{icon} **Шаг {step_num}** - {desc_text}", expanded=False):
        
        # Reasoning блок
        if reasoning_step:
            st.markdown("### 🧠 Reasoning")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if reasoning_step.reasoning.get('current_situation'):
                    st.info(f"**Ситуация:** {reasoning_step.reasoning['current_situation']}")
                
                if reasoning_step.reasoning.get('plan_status'):
                    st.write(f"**План:** {reasoning_step.reasoning['plan_status']}")
            
            with col2:
                col_status1, col_status2 = st.columns(2)
                with col_status1:
                    if 'enough_data' in reasoning_step.reasoning:
                        status = "✅" if reasoning_step.reasoning['enough_data'] else "❌"
                        st.metric("Данных достаточно", status)
                with col_status2:
                    if 'task_completed' in reasoning_step.reasoning:
                        status = "✅" if reasoning_step.reasoning['task_completed'] else "⏳"
                        st.metric("Задача", status)
            
            # Шаги рассуждения
            if reasoning_step.reasoning.get('reasoning_steps'):
                st.markdown("**💭 Шаги рассуждения:**")
                for idx, r_step in enumerate(reasoning_step.reasoning['reasoning_steps'], 1):
                    st.markdown(f"{idx}. {r_step}")
            
            # Оставшиеся шаги
            if reasoning_step.reasoning.get('remaining_steps'):
                st.markdown("**📋 Что нужно сделать:**")
                for r_step in reasoning_step.reasoning['remaining_steps']:
                    st.markdown(f"- {r_step}")
            
            st.divider()
        
        # LLM Calls блок
        if llm_calls:
            st.markdown("### 🤖 LLM вызовы")
            
            for llm_step in llm_calls:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        phase_emoji = {"reasoning_phase": "🧠", "action_selection": "🎯", "execution": "⚡"}.get(llm_step.phase, "📞")
                        st.write(f"{phase_emoji} **Фаза:** {llm_step.phase or 'N/A'}")
                    
                    with col2:
                        if 'duration_ms' in llm_step.metrics:
                            st.metric("⏱️ Время", f"{llm_step.metrics['duration_ms']:.0f} мс")
                    
                    with col3:
                        if 'total_tokens' in llm_step.metrics:
                            st.metric("🎫 Токены", llm_step.metrics['total_tokens'])
                    
                    # Tool calls из LLM ответа
                    if llm_step.tool_calls:
                        st.markdown("**Запрошенные инструменты:**")
                        for tool_call in llm_step.tool_calls:
                            st.code(f"📞 {tool_call['name']}", language=None)
            
            st.divider()
        
        # Tool Execution блок
        if execution_steps:
            st.markdown("### 🛠️ Выполнение инструментов")
            
            for exec_step in execution_steps:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        if exec_step.tool_calls:
                            for tool_call in exec_step.tool_calls:
                                tool_name = tool_call.get('name', 'unknown')
                                tool_emoji = {
                                    'websearchtool': '🔍',
                                    'extractpagecontenttool': '📄',
                                    'finalanswertool': '✅',
                                    'reasoningtool': '🧠'
                                }.get(tool_name, '🔧')
                                
                                st.markdown(f"**{tool_emoji} {tool_name}**")
                                
                                # Аргументы
                                args = tool_call.get('arguments', {})
                                if args:
                                    with st.expander("Аргументы", expanded=False):
                                        st.json(args)
                    
                    with col2:
                        if 'duration_ms' in exec_step.metrics:
                            st.metric("⏱️ Время", f"{exec_step.metrics['duration_ms']:.0f} мс")
                    
                    # Результаты поиска
                    if exec_step.search_results:
                        st.markdown(f"**🔍 Найдено результатов: {len(exec_step.search_results)}**")
                        
                        with st.expander(f"Показать {len(exec_step.search_results)} результатов", expanded=False):
                            for idx, result in enumerate(exec_step.search_results, 1):
                                st.markdown(f"**{idx}. {result.get('title', 'N/A')}**")
                                st.markdown(f"🔗 [{result.get('url', 'N/A')}]({result.get('url', '#')})")
                                if result.get('content'):
                                    st.caption(result['content'][:150] + "...")
                                st.divider()
                    
                    st.markdown("---")


def render_metrics(parser: LogParser, metrics_viz: MetricsVisualizer) -> None:
    """
    Отображает метрики производительности агента.
    
    Args:
        parser: Парсер логов с обработанными данными
        metrics_viz: Визуализатор метрик
    """
    st.header("📊 Метрики производительности")
    
    metrics = parser.get_aggregated_metrics()
    
    if not metrics:
        st.warning("Нет данных о метриках")
        return
    
    # Общие метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Всего шагов", metrics['total_steps'])
    
    with col2:
        st.metric("Общее время (мс)", f"{metrics['total_duration_ms']:.2f}")
    
    with col3:
        st.metric("Всего токенов", metrics['total_tokens'])
    
    with col4:
        st.metric("LLM вызовов", metrics['llm_calls'])
    
    # Детальные графики
    tab1, tab2, tab3 = st.tabs(["⏱️ Время выполнения", "🎫 Использование токенов", "📈 Динамика"])
    
    with tab1:
        fig_duration = metrics_viz.create_duration_chart(parser.get_steps())
        st.plotly_chart(fig_duration, width='stretch')
    
    with tab2:
        fig_tokens = metrics_viz.create_tokens_chart(parser.get_steps())
        st.plotly_chart(fig_tokens, width='stretch')
    
    with tab3:
        fig_timeline = metrics_viz.create_cumulative_timeline(parser.get_steps())
        st.plotly_chart(fig_timeline, width='stretch')


def render_simple_trace(log_data: Dict[str, Any]) -> None:
    """
    Отображение трейсинга с визуальной иерархией (лесенкой).
    
    Args:
        log_data: Данные из файла логов
    """
    log_entries = log_data.get('log', [])
    
    if not log_entries:
        st.warning("Нет записей в логе")
        return
    
    current_step = None
    indent_level = 0
    
    for i, entry in enumerate(log_entries, 1):
        step_num = entry.get('step_number')
        step_type = entry.get('step_type')
        phase = entry.get('phase', '')
        tool_name = entry.get('tool_name', '')
        
        # Определяем уровень отступа
        if step_num != current_step:
            current_step = step_num
            indent_level = 0
        else:
            # Внутри одного шага - делаем отступ
            if step_type == 'reasoning':
                indent_level = 1
            elif step_type == 'llm_call' and phase == 'action_selection':
                indent_level = 0
            elif step_type == 'tool_execution':
                indent_level = 1
        
        # Иконки
        icon = {
            'llm_call': '🤖',
            'reasoning': '🧠',
            'tool_execution': '🛠️'
        }.get(step_type, '📝')
        
        # Формируем название
        parts = [f"Step {step_num}"]
        
        if step_type == 'llm_call':
            if phase == 'reasoning_phase':
                parts.append("LLM Reasoning")
            elif phase == 'action_selection':
                parts.append("LLM Action")
            else:
                parts.append("LLM Call")
        elif step_type == 'reasoning':
            parts.append("→ Reasoning Result")
        elif step_type == 'tool_execution':
            tool_icon = {
                'websearchtool': '🔍',
                'extractpagecontenttool': '📄',
                'finalanswertool': '✅',
                'reasoningtool': '💭'
            }.get(tool_name, '🔧')
            parts.append(f"→ {tool_icon} {tool_name}")
        
        title = f"{icon} {' · '.join(parts)}"
        
        # Метрики для краткости
        metrics_str = ""
        if step_type == 'llm_call':
            metrics = entry.get('metrics', {})
            duration = metrics.get('duration_ms', 0)
            tokens = metrics.get('total_tokens', 0)
            if duration > 0:
                metrics_str = f" ⏱ {duration:.0f}ms"
            if tokens > 0:
                metrics_str += f" 🎫 {tokens}"
        
        # Создаем отступ с помощью columns
        if indent_level == 0:
            # Без отступа
            with st.expander(f"{title}{metrics_str}", expanded=False):
                st.json(entry)
        else:
            # С отступом - используем columns
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.write("")  # Пустая колонка для отступа
            with col2:
                with st.expander(f"{title}{metrics_str}", expanded=False):
                    st.json(entry)


def render_raw_json(log_data: Dict[str, Any]) -> None:
    """
    Отображает Raw JSON логов в удобном формате.
    
    Args:
        log_data: Данные из файла логов
    """
    st.header("📋 Raw JSON - Порядок выполнения")
    
    st.markdown("""
    Показывает все записи лога в порядке выполнения агента.
    Каждая запись содержит полную информацию о шаге.
    """)
    
    log_entries = log_data.get('log', [])
    
    if not log_entries:
        st.warning("Нет записей в логе")
        return
    
    # Группируем по шагам для удобства
    st.subheader(f"📊 Всего записей: {len(log_entries)}")
    
    for i, entry in enumerate(log_entries, 1):
        step_num = entry.get('step_number')
        step_type = entry.get('step_type')
        phase = entry.get('phase', '')
        tool_name = entry.get('tool_name', '')
        timestamp = entry.get('timestamp', '')
        
        # Формируем заголовок
        title_parts = [f"[{i}] Шаг {step_num}"]
        
        # Иконка по типу
        icon = {
            'llm_call': '🤖',
            'reasoning': '🧠',
            'tool_execution': '🛠️'
        }.get(step_type, '📝')
        
        title_parts.append(f"{icon} {step_type}")
        
        if phase:
            phase_emoji = {
                'reasoning_phase': '💭',
                'action_selection': '🎯'
            }.get(phase, '')
            title_parts.append(f"{phase_emoji} {phase}")
        
        if tool_name:
            tool_emoji = {
                'websearchtool': '🔍',
                'extractpagecontenttool': '📄',
                'finalanswertool': '✅',
                'reasoningtool': '🧠'
            }.get(tool_name, '🔧')
            title_parts.append(f"{tool_emoji} {tool_name}")
        
        title = " - ".join(title_parts)
        
        with st.expander(title, expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.caption(f"⏰ {timestamp}")
            
            with col2:
                # Метрики если есть
                if 'metrics' in entry:
                    metrics = entry['metrics']
                    if 'duration_ms' in metrics:
                        st.metric("⏱️ Время", f"{metrics['duration_ms']:.0f} мс")
            
            # Ключевая информация в зависимости от типа
            if step_type == 'reasoning':
                reasoning = entry.get('agent_reasoning', {})
                
                st.markdown("### 🧠 Reasoning")
                
                if reasoning.get('current_situation'):
                    st.info(reasoning['current_situation'])
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.write(f"**Достаточно данных:** {'✅' if reasoning.get('enough_data') else '❌'}")
                with col_r2:
                    st.write(f"**Задача завершена:** {'✅' if reasoning.get('task_completed') else '⏳'}")
                
                if reasoning.get('reasoning_steps'):
                    st.markdown("**Шаги рассуждения:**")
                    for idx, step in enumerate(reasoning['reasoning_steps'], 1):
                        st.markdown(f"{idx}. {step}")
                
                if reasoning.get('remaining_steps'):
                    st.markdown("**Оставшиеся шаги:**")
                    for step in reasoning['remaining_steps']:
                        st.markdown(f"- {step}")
            
            elif step_type == 'tool_execution':
                context = entry.get('agent_tool_context', {})
                result = entry.get('agent_tool_execution_result', '')
                
                st.markdown(f"### 🛠️ {tool_name}")
                
                st.markdown("**Контекст вызова:**")
                st.json(context)
                
                if tool_name == 'websearchtool':
                    st.markdown("**Результаты поиска:**")
                    st.text(result[:1000] + "..." if len(result) > 1000 else result)
                
                elif tool_name == 'extractpagecontenttool':
                    st.markdown("**Извлеченный контент:**")
                    st.text(result[:500] + "..." if len(result) > 500 else result)
                
                elif tool_name == 'finalanswertool':
                    st.markdown("**Финальный ответ:**")
                    try:
                        result_json = json.loads(result)
                        st.json(result_json)
                    except:
                        st.text(result)
            
            elif step_type == 'llm_call':
                st.markdown(f"### 🤖 LLM Call - {phase}")
                
                if 'metrics' in entry:
                    metrics = entry['metrics']
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("⏱️ Длительность", f"{metrics.get('duration_ms', 0):.0f} мс")
                    with col_m2:
                        st.metric("🎫 Токены", metrics.get('total_tokens', 0))
                    with col_m3:
                        st.metric("📊 Токены/сек", f"{metrics.get('tokens_per_second', 0):.1f}")
                
                # Показываем tool calls из ответа
                if 'response' in entry:
                    response = entry['response']
                    if 'choices' in response:
                        for choice in response['choices']:
                            message = choice.get('message', {})
                            if 'tool_calls' in message and message['tool_calls']:
                                st.markdown("**Вызванные инструменты:**")
                                for tool_call in message['tool_calls']:
                                    func = tool_call.get('function', {})
                                    st.markdown(f"- `{func.get('name')}`")
            
            # Полный JSON для экспертов
            with st.expander("🔍 Полный JSON", expanded=False):
                st.json(entry)


def render_timeline(parser: LogParser, timeline_viz: TimelineVisualizer) -> None:
    """
    Отображает временную линию выполнения агента.
    
    Args:
        parser: Парсер логов с обработанными данными
        timeline_viz: Визуализатор временной линии
    """
    st.header("⏳ Временная линия")
    
    steps = parser.get_steps()
    
    if not steps:
        st.warning("Нет данных для временной линии")
        return
    
    fig = timeline_viz.create_timeline(steps)
    st.plotly_chart(fig, width='stretch')


def main() -> None:
    """
    Главная функция приложения Streamlit.
    
    Инициализирует интерфейс и управляет отображением компонентов.
    """
    st.set_page_config(
        page_title="SGR Agent Visualizer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 SGR Agent Trace Visualizer")
    st.markdown("*Интерактивная визуализация работы агента на основе Schema-Guided Reasoning*")
    
    # Sidebar для выбора файла
    st.sidebar.title("⚙️ Настройки")
    
    # Выбор способа загрузки
    load_method = st.sidebar.radio(
        "Способ загрузки логов:",
        ["Выбрать из директории", "Загрузить файл"]
    )
    
    log_data = None
    
    if load_method == "Выбрать из директории":
        logs_dir = st.sidebar.text_input(
            "Путь к директории с логами:",
            value="../logs"
        )
        
        available_logs = get_available_logs(logs_dir)
        
        if available_logs:
            selected_log = st.sidebar.selectbox(
                "Выберите файл лога:",
                options=available_logs,
                format_func=lambda x: f"{x.name} ({datetime.fromtimestamp(x.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')})"
            )
            
            if selected_log:
                log_data = load_log_file(str(selected_log))
        else:
            st.sidebar.warning(f"Логи не найдены в директории: {logs_dir}")
    
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Загрузите JSON файл с логами:",
            type=['json']
        )
        
        if uploaded_file:
            try:
                log_data = json.load(uploaded_file)
            except Exception as e:
                st.error(f"Ошибка при чтении файла: {e}")
    
    # Если данные загружены, отображаем визуализацию
    if log_data:
        # Инициализация парсера и визуализаторов
        parser = LogParser(log_data)
        roadmap_viz = RoadmapVisualizer()
        metrics_viz = MetricsVisualizer()
        timeline_viz = TimelineVisualizer()
        trace_viz = TraceVisualizer()
        
        # Основная информация
        render_agent_info(log_data)
        
        st.divider()
        
        # Простое отображение трейсинга
        st.header("🔍 Trace")
        render_simple_trace(log_data)
    
    else:
        st.info("👈 Выберите или загрузите файл с логами для начала визуализации")
        
        # Показываем пример структуры
        with st.expander("ℹ️ Информация о формате логов"):
            st.markdown("""
            Ожидаемая структура JSON файла с логами:
            
            ```json
            {
                "id": "agent_id",
                "model_config": {
                    "model": "model_name",
                    "temperature": 0.2,
                    "max_tokens": 8000
                },
                "task": "Описание задачи",
                "toolkit": ["tool1", "tool2"],
                "log": [
                    {
                        "step_number": 1,
                        "timestamp": "2025-12-17T07:02:00.240803",
                        "step_type": "llm_call",
                        "phase": "reasoning_phase",
                        ...
                    }
                ]
            }
            ```
            """)


if __name__ == "__main__":
    main()

