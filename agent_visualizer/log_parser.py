"""
Парсер JSON логов агента для извлечения структурированной информации.

Модуль обрабатывает JSON логи и преобразует их в удобные структуры данных
для последующей визуализации.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentStep:
    """
    Представление одного шага выполнения агента.
    
    Attributes:
        step_number: Номер шага в последовательности выполнения
        timestamp: Временная метка выполнения шага
        step_type: Тип шага (llm_call, reasoning, tool_execution и т.д.)
        phase: Фаза выполнения (reasoning_phase, action_selection и т.д.)
        metrics: Метрики производительности (время, токены)
        reasoning: Информация о рассуждениях агента
        tool_calls: Список вызванных инструментов
        search_results: Результаты веб-поиска
        raw_data: Исходные данные из лога
    """
    step_number: int
    timestamp: str
    step_type: str
    phase: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    reasoning: Dict[str, Any] = field(default_factory=dict)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    search_results: List[Dict[str, Any]] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


class LogParser:
    """
    Парсер для обработки JSON логов агента.
    
    Класс извлекает и структурирует информацию из логов,
    чтобы подготовить данные для визуализации.
    """
    
    def __init__(self, log_data: Dict[str, Any]) -> None:
        """
        Инициализирует парсер с данными логов.
        
        Args:
            log_data: Словарь с данными из JSON файла логов
        """
        self.log_data = log_data
        self.steps: List[AgentStep] = []
        self._parse_logs()
    
    def _parse_logs(self) -> None:
        """
        Парсит логи и создает список объектов AgentStep.
        
        Обрабатывает каждую запись в логах, чтобы извлечь
        информацию о шагах, reasoning, метриках и результатах.
        """
        log_entries = self.log_data.get('log', [])
        
        current_step_data = {}
        
        for entry in log_entries:
            step_num = entry.get('step_number')
            step_type = entry.get('step_type')
            
            # Группируем записи по номеру шага
            if step_num not in current_step_data:
                current_step_data[step_num] = {
                    'step_number': step_num,
                    'timestamp': entry.get('timestamp'),
                    'step_type': step_type,
                    'phase': entry.get('phase'),
                    'metrics': {},
                    'reasoning': {},
                    'tool_calls': [],
                    'search_results': [],
                    'raw_entries': []
                }
            
            step_data = current_step_data[step_num]
            step_data['raw_entries'].append(entry)
            
            # Извлекаем метрики
            if 'metrics' in entry:
                step_data['metrics'].update(entry['metrics'])
            
            # Извлекаем reasoning
            if step_type == 'reasoning' and 'agent_reasoning' in entry:
                step_data['reasoning'] = entry['agent_reasoning']
            
            # Извлекаем tool calls из LLM ответов
            if step_type == 'llm_call' and 'response' in entry:
                response = entry['response']
                if 'choices' in response:
                    for choice in response['choices']:
                        message = choice.get('message', {})
                        if 'tool_calls' in message and message['tool_calls']:
                            for tool_call in message['tool_calls']:
                                func = tool_call.get('function', {})
                                step_data['tool_calls'].append({
                                    'id': tool_call.get('id'),
                                    'name': func.get('name'),
                                    'arguments': func.get('parsed_arguments', {})
                                })
            
            # Для tool_execution также добавляем информацию о вызове
            if step_type == 'tool_execution':
                tool_name = entry.get('tool_name')
                if tool_name:
                    step_data['tool_calls'].append({
                        'name': tool_name,
                        'arguments': entry.get('agent_tool_context', {})
                    })
            
            # Извлекаем результаты поиска из tool_execution
            if step_type == 'tool_execution':
                tool_name = entry.get('tool_name')
                
                # Для websearchtool парсим результаты из строки
                if tool_name == 'websearchtool':
                    result_str = entry.get('agent_tool_execution_result', '')
                    if result_str and isinstance(result_str, str):
                        # Парсим результаты поиска из текста
                        import re
                        # Находим все результаты в формате [N] Title - URL
                        pattern = r'\[(\d+)\]\s+(.+?)\s+-\s+(https?://[^\s]+)\s*\n(.+?)(?=\n\[|\n\n|$)'
                        matches = re.findall(pattern, result_str, re.DOTALL)
                        
                        for match in matches:
                            step_data['search_results'].append({
                                'title': match[1].strip(),
                                'url': match[2].strip(),
                                'content': match[3].strip()
                            })
                
                # Сохраняем контекст и результат выполнения
                step_data['tool_context'] = entry.get('agent_tool_context', {})
                step_data['tool_result'] = entry.get('agent_tool_execution_result', '')
        
        # Создаем объекты AgentStep
        for step_num in sorted(current_step_data.keys()):
            data = current_step_data[step_num]
            step = AgentStep(
                step_number=data['step_number'],
                timestamp=data['timestamp'],
                step_type=data['step_type'],
                phase=data['phase'],
                metrics=data['metrics'],
                reasoning=data['reasoning'],
                tool_calls=data['tool_calls'],
                search_results=data['search_results'],
                raw_data=data
            )
            self.steps.append(step)
    
    def get_steps(self) -> List[AgentStep]:
        """
        Возвращает список всех обработанных шагов.
        
        Returns:
            Список объектов AgentStep
        """
        return self.steps
    
    def get_step_by_number(self, step_number: int) -> Optional[AgentStep]:
        """
        Находит шаг по его номеру.
        
        Args:
            step_number: Номер шага для поиска
            
        Returns:
            Объект AgentStep или None, если шаг не найден
        """
        for step in self.steps:
            if step.step_number == step_number:
                return step
        return None
    
    def get_steps_by_type(self, step_type: str) -> List[AgentStep]:
        """
        Фильтрует шаги по типу.
        
        Args:
            step_type: Тип шага для фильтрации
            
        Returns:
            Список шагов указанного типа
        """
        return [step for step in self.steps if step.step_type == step_type]
    
    def get_steps_by_phase(self, phase: str) -> List[AgentStep]:
        """
        Фильтрует шаги по фазе выполнения.
        
        Args:
            phase: Фаза для фильтрации
            
        Returns:
            Список шагов в указанной фазе
        """
        return [step for step in self.steps if step.phase == phase]
    
    def get_aggregated_metrics(self) -> Dict[str, Any]:
        """
        Агрегирует метрики по всем шагам.
        
        Вычисляет общие показатели производительности,
        чтобы предоставить сводную статистику.
        
        Returns:
            Словарь с агрегированными метриками
        """
        total_duration = 0
        total_tokens = 0
        total_prompt_tokens = 0
        total_completion_tokens = 0
        llm_calls = 0
        tool_executions = 0
        
        for step in self.steps:
            if step.metrics:
                # Суммируем длительность
                if 'duration_ms' in step.metrics:
                    total_duration += step.metrics['duration_ms']
                
                # Суммируем токены
                if 'total_tokens' in step.metrics:
                    total_tokens += step.metrics['total_tokens']
                if 'prompt_tokens' in step.metrics:
                    total_prompt_tokens += step.metrics['prompt_tokens']
                if 'completion_tokens' in step.metrics:
                    total_completion_tokens += step.metrics['completion_tokens']
            
            # Подсчитываем типы операций
            if step.step_type == 'llm_call':
                llm_calls += 1
            elif step.step_type == 'tool_execution':
                tool_executions += 1
        
        return {
            'total_steps': len(self.steps),
            'total_duration_ms': total_duration,
            'total_tokens': total_tokens,
            'total_prompt_tokens': total_prompt_tokens,
            'total_completion_tokens': total_completion_tokens,
            'llm_calls': llm_calls,
            'tool_executions': tool_executions,
            'avg_duration_per_step': total_duration / len(self.steps) if self.steps else 0,
            'avg_tokens_per_llm_call': total_tokens / llm_calls if llm_calls > 0 else 0
        }
    
    def get_tool_usage_stats(self) -> Dict[str, int]:
        """
        Подсчитывает статистику использования инструментов.
        
        Returns:
            Словарь с количеством вызовов каждого инструмента
        """
        tool_stats = {}
        
        for step in self.steps:
            for tool_call in step.tool_calls:
                tool_name = tool_call.get('name', 'unknown')
                tool_stats[tool_name] = tool_stats.get(tool_name, 0) + 1
        
        return tool_stats
    
    def get_timeline_data(self) -> List[Dict[str, Any]]:
        """
        Подготавливает данные для временной линии.
        
        Форматирует информацию о шагах для отображения
        на временной шкале с метками времени.
        
        Returns:
            Список словарей с данными временной линии
        """
        timeline = []
        
        for step in self.steps:
            timeline.append({
                'step_number': step.step_number,
                'timestamp': step.timestamp,
                'step_type': step.step_type,
                'phase': step.phase,
                'duration_ms': step.metrics.get('duration_ms', 0),
                'description': self._generate_step_description(step)
            })
        
        return timeline
    
    def _generate_step_description(self, step: AgentStep) -> str:
        """
        Генерирует краткое описание шага для отображения.
        
        Args:
            step: Объект шага для описания
            
        Returns:
            Строка с описанием шага
        """
        if step.step_type == 'reasoning':
            if step.reasoning.get('current_situation'):
                return step.reasoning['current_situation'][:100]
        
        elif step.step_type == 'llm_call':
            phase_names = {
                'reasoning_phase': 'Фаза рассуждения',
                'action_selection': 'Выбор действия',
                'execution': 'Выполнение'
            }
            return phase_names.get(step.phase, step.phase or 'LLM вызов')
        
        elif step.step_type == 'tool_execution':
            if step.tool_calls:
                tool_names = [tc.get('name', 'unknown') for tc in step.tool_calls]
                return f"Выполнение: {', '.join(tool_names)}"
        
        return f"{step.step_type} - {step.phase or 'N/A'}"
    
    def get_reasoning_evolution(self) -> List[Dict[str, Any]]:
        """
        Отслеживает эволюцию reasoning агента по шагам.
        
        Собирает информацию о том, как менялись планы
        и рассуждения агента в процессе выполнения.
        
        Returns:
            Список словарей с эволюцией reasoning
        """
        reasoning_steps = self.get_steps_by_type('reasoning')
        
        evolution = []
        for step in reasoning_steps:
            evolution.append({
                'step_number': step.step_number,
                'timestamp': step.timestamp,
                'current_situation': step.reasoning.get('current_situation'),
                'plan_status': step.reasoning.get('plan_status'),
                'enough_data': step.reasoning.get('enough_data', False),
                'task_completed': step.reasoning.get('task_completed', False),
                'reasoning_steps': step.reasoning.get('reasoning_steps', []),
                'remaining_steps': step.reasoning.get('remaining_steps', [])
            })
        
        return evolution

