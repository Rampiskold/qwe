"""
Примеры использования Agent Visualizer API для программного доступа к данным.

Демонстрирует работу с парсером логов и визуализаторами
без запуска Streamlit интерфейса.
"""

import json
from pathlib import Path
from log_parser import LogParser
from visualizers import RoadmapVisualizer, MetricsVisualizer, TimelineVisualizer


def load_log_example(log_file_path: str) -> None:
    """
    Пример загрузки и анализа файла логов.
    
    Args:
        log_file_path: Путь к JSON файлу с логами
    """
    print(f"📂 Загрузка логов из: {log_file_path}")
    
    # Загружаем JSON
    with open(log_file_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    print(f"✅ Логи загружены")
    print(f"   ID агента: {log_data.get('id', 'N/A')}")
    print(f"   Задача: {log_data.get('task', 'N/A')}")
    print(f"   Инструменты: {', '.join(log_data.get('toolkit', []))}")
    print()
    
    return log_data


def analyze_steps(parser: LogParser) -> None:
    """
    Анализирует шаги выполнения агента.
    
    Args:
        parser: Инициализированный парсер логов
    """
    print("🔍 Анализ шагов выполнения")
    print("=" * 60)
    
    steps = parser.get_steps()
    print(f"Всего шагов: {len(steps)}\n")
    
    # Группировка по типам
    step_types = {}
    for step in steps:
        step_types[step.step_type] = step_types.get(step.step_type, 0) + 1
    
    print("Распределение по типам:")
    for step_type, count in step_types.items():
        print(f"  - {step_type}: {count}")
    print()
    
    # Детали первых нескольких шагов
    print("Первые 3 шага:")
    for step in steps[:3]:
        print(f"\n  Шаг {step.step_number}: {step.step_type}")
        print(f"    Фаза: {step.phase or 'N/A'}")
        if step.metrics:
            print(f"    Длительность: {step.metrics.get('duration_ms', 'N/A')} мс")
            print(f"    Токены: {step.metrics.get('total_tokens', 'N/A')}")
        if step.reasoning and step.reasoning.get('current_situation'):
            situation = step.reasoning['current_situation'][:80]
            print(f"    Ситуация: {situation}...")
    print()


def analyze_metrics(parser: LogParser) -> None:
    """
    Анализирует метрики производительности.
    
    Args:
        parser: Инициализированный парсер логов
    """
    print("📊 Метрики производительности")
    print("=" * 60)
    
    metrics = parser.get_aggregated_metrics()
    
    print(f"Всего шагов: {metrics['total_steps']}")
    print(f"Общее время: {metrics['total_duration_ms']:.2f} мс ({metrics['total_duration_ms']/1000:.2f} сек)")
    print(f"Среднее время на шаг: {metrics['avg_duration_per_step']:.2f} мс")
    print()
    
    print(f"Всего токенов: {metrics['total_tokens']}")
    print(f"  - Prompt токены: {metrics['total_prompt_tokens']}")
    print(f"  - Completion токены: {metrics['total_completion_tokens']}")
    print(f"Среднее токенов на LLM вызов: {metrics['avg_tokens_per_llm_call']:.2f}")
    print()
    
    print(f"LLM вызовов: {metrics['llm_calls']}")
    print(f"Выполнений инструментов: {metrics['tool_executions']}")
    print()


def analyze_tool_usage(parser: LogParser) -> None:
    """
    Анализирует использование инструментов.
    
    Args:
        parser: Инициализированный парсер логов
    """
    print("🛠️ Использование инструментов")
    print("=" * 60)
    
    tool_stats = parser.get_tool_usage_stats()
    
    if not tool_stats:
        print("Инструменты не использовались")
        return
    
    print(f"Всего вызовов инструментов: {sum(tool_stats.values())}")
    print("\nРаспределение по инструментам:")
    
    # Сортируем по количеству использований
    sorted_tools = sorted(tool_stats.items(), key=lambda x: x[1], reverse=True)
    
    for tool_name, count in sorted_tools:
        percentage = (count / sum(tool_stats.values())) * 100
        print(f"  - {tool_name}: {count} ({percentage:.1f}%)")
    print()


def analyze_reasoning_evolution(parser: LogParser) -> None:
    """
    Анализирует эволюцию reasoning агента.
    
    Args:
        parser: Инициализированный парсер логов
    """
    print("🧠 Эволюция reasoning")
    print("=" * 60)
    
    evolution = parser.get_reasoning_evolution()
    
    if not evolution:
        print("Нет данных о reasoning")
        return
    
    print(f"Всего reasoning шагов: {len(evolution)}\n")
    
    for idx, item in enumerate(evolution, 1):
        print(f"Reasoning шаг {idx} (общий шаг {item['step_number']}):")
        print(f"  Ситуация: {item['current_situation'][:80]}...")
        print(f"  План: {item['plan_status']}")
        print(f"  Достаточно данных: {'✅ Да' if item['enough_data'] else '❌ Нет'}")
        print(f"  Задача завершена: {'✅ Да' if item['task_completed'] else '⏳ В процессе'}")
        
        if item['remaining_steps']:
            print(f"  Оставшиеся шаги ({len(item['remaining_steps'])}):")
            for step in item['remaining_steps'][:2]:  # Показываем первые 2
                print(f"    - {step}")
        print()


def save_visualizations(parser: LogParser, output_dir: str = "output") -> None:
    """
    Сохраняет визуализации в HTML файлы.
    
    Args:
        parser: Инициализированный парсер логов
        output_dir: Директория для сохранения файлов
    """
    print("💾 Сохранение визуализаций")
    print("=" * 60)
    
    # Создаем директорию, если её нет
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    steps = parser.get_steps()
    
    # Создаем визуализаторы
    roadmap_viz = RoadmapVisualizer()
    metrics_viz = MetricsVisualizer()
    timeline_viz = TimelineVisualizer()
    
    # Роудмап
    print("  Создание роудмапа...")
    fig_roadmap = roadmap_viz.create_roadmap(steps)
    fig_roadmap.write_html(output_path / "roadmap.html")
    
    # Метрики
    print("  Создание графиков метрик...")
    fig_duration = metrics_viz.create_duration_chart(steps)
    fig_duration.write_html(output_path / "duration.html")
    
    fig_tokens = metrics_viz.create_tokens_chart(steps)
    fig_tokens.write_html(output_path / "tokens.html")
    
    fig_cumulative = metrics_viz.create_cumulative_timeline(steps)
    fig_cumulative.write_html(output_path / "cumulative.html")
    
    # Использование инструментов
    tool_stats = parser.get_tool_usage_stats()
    if tool_stats:
        fig_tools = metrics_viz.create_tool_usage_pie(tool_stats)
        fig_tools.write_html(output_path / "tool_usage.html")
    
    # Временная линия
    print("  Создание временной линии...")
    fig_timeline = timeline_viz.create_timeline(steps)
    fig_timeline.write_html(output_path / "timeline.html")
    
    print(f"\n✅ Визуализации сохранены в директорию: {output_path.absolute()}")
    print(f"   Открыть роудмап: file://{output_path.absolute()}/roadmap.html")
    print()


def main():
    """
    Главная функция примера использования.
    
    Демонстрирует полный цикл работы с логами агента:
    загрузка, парсинг, анализ и визуализация.
    """
    print("=" * 60)
    print("🤖 SGR Agent Visualizer - Пример использования API")
    print("=" * 60)
    print()
    
    # Путь к файлу логов (замените на свой)
    log_file = "../logs/20251217-070215-russian_deep_research_agent_43092779-2eaa-439d-ba74-8f6eca97b211-log.json"
    
    # Проверяем существование файла
    if not Path(log_file).exists():
        print(f"❌ Файл не найден: {log_file}")
        print("\nИспользование:")
        print("  python example_usage.py")
        print("\nИли укажите путь к вашему файлу в коде.")
        return
    
    # Загружаем логи
    log_data = load_log_example(log_file)
    
    # Создаем парсер
    parser = LogParser(log_data)
    
    # Выполняем различные виды анализа
    analyze_steps(parser)
    analyze_metrics(parser)
    analyze_tool_usage(parser)
    analyze_reasoning_evolution(parser)
    
    # Сохраняем визуализации
    save_visualizations(parser, output_dir="output")
    
    print("=" * 60)
    print("✅ Анализ завершен!")
    print("=" * 60)


if __name__ == "__main__":
    main()

