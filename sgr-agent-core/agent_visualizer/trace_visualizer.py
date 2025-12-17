"""
Трейсинг визуализатор в стиле Langfuse для отображения выполнения агента.

Создает древовидное представление с временной линией, метриками и деталями.
"""

from typing import List, Dict, Any, Optional
import streamlit as st
from datetime import datetime
from log_parser import AgentStep, LogParser


class TraceNode:
    """
    Узел дерева трейсинга.
    
    Attributes:
        name: Название узла
        type: Тип (span, event, tool)
        start_time: Время начала
        end_time: Время окончания
        duration_ms: Длительность в миллисекундах
        metadata: Дополнительные данные
        children: Дочерние узлы
        level: Уровень вложенности
    """
    
    def __init__(
        self,
        name: str,
        type: str,
        start_time: str,
        duration_ms: float = 0,
        metadata: Optional[Dict[str, Any]] = None,
        level: int = 0
    ):
        """
        Инициализирует узел трейса.
        
        Args:
            name: Название узла
            type: Тип узла
            start_time: Время начала
            duration_ms: Длительность
            metadata: Дополнительные данные
            level: Уровень вложенности
        """
        self.name = name
        self.type = type
        self.start_time = start_time
        self.duration_ms = duration_ms
        self.metadata = metadata or {}
        self.children: List[TraceNode] = []
        self.level = level
    
    def add_child(self, child: 'TraceNode') -> None:
        """
        Добавляет дочерний узел.
        
        Args:
            child: Дочерний узел для добавления
        """
        child.level = self.level + 1
        self.children.append(child)


class TraceVisualizer:
    """
    Визуализатор трейсинга агента в стиле Langfuse.
    
    Создает красивое древовидное представление с метриками и временной линией.
    """
    
    # Цветовая схема
    COLORS = {
        'step': '#8B5CF6',      # Фиолетовый
        'reasoning': '#EC4899',  # Розовый
        'llm_call': '#3B82F6',  # Синий
        'tool': '#10B981',      # Зеленый
        'search': '#F59E0B',    # Оранжевый
        'extract': '#6366F1',   # Индиго
        'final': '#22C55E'      # Лайм
    }
    
    # Иконки
    ICONS = {
        'step': '📍',
        'reasoning': '🧠',
        'llm_call': '🤖',
        'tool': '🛠️',
        'websearchtool': '🔍',
        'extractpagecontenttool': '📄',
        'finalanswertool': '✅',
        'reasoningtool': '💭'
    }
    
    def build_trace_tree(self, parser: LogParser) -> List[TraceNode]:
        """
        Строит дерево трейсинга из логов в формате:
        LLM Call
          └─ Tool Execution (если есть)
        LLM Call
          └─ Tool Execution (если есть)
        
        Args:
            parser: Парсер логов
            
        Returns:
            Список корневых узлов дерева
        """
        # Получаем все записи из оригинального лога
        log_entries = parser.log_data.get('log', [])
        root_nodes = []
        
        # Группируем записи по шагам
        current_step = None
        current_llm_node = None
        
        for entry in log_entries:
            step_type = entry.get('step_type')
            step_num = entry.get('step_number')
            
            # LLM Call - создаем корневой узел
            if step_type == 'llm_call':
                phase = entry.get('phase', '')
                metrics = entry.get('metrics', {})
                
                # Определяем название
                if phase == 'reasoning_phase':
                    llm_name = f"Step {step_num}: LLM Reasoning"
                    icon = '🧠'
                elif phase == 'action_selection':
                    llm_name = f"Step {step_num}: LLM Action"
                    icon = '🎯'
                else:
                    llm_name = f"Step {step_num}: LLM Call"
                    icon = '🤖'
                
                # Извлекаем tool calls из ответа
                response = entry.get('response', {})
                tool_calls = []
                if 'choices' in response:
                    for choice in response['choices']:
                        message = choice.get('message', {})
                        if 'tool_calls' in message and message['tool_calls']:
                            for tc in message['tool_calls']:
                                func = tc.get('function', {})
                                tool_name = func.get('name')
                                # Убираем дубликаты reasoningtool (он системный)
                                if tool_name and tool_name != 'reasoningtool':
                                    tool_calls.append({
                                        'name': tool_name,
                                        'arguments': func.get('parsed_arguments', {})
                                    })
                
                # Создаем узел LLM вызова
                current_llm_node = TraceNode(
                    name=f"{icon} {llm_name}",
                    type='llm_call',
                    start_time=entry.get('timestamp', ''),
                    duration_ms=metrics.get('duration_ms', 0),
                    metadata={
                        'phase': phase,
                        'tokens': metrics.get('total_tokens', 0),
                        'prompt_tokens': metrics.get('prompt_tokens', 0),
                        'completion_tokens': metrics.get('completion_tokens', 0),
                        'tokens_per_second': metrics.get('tokens_per_second', 0),
                        'step_number': step_num,
                        'tool_calls': tool_calls
                    }
                )
                
                root_nodes.append(current_llm_node)
                current_step = step_num
            
            # Reasoning - добавляем как дочерний элемент к текущему LLM
            elif step_type == 'reasoning' and current_llm_node:
                reasoning = entry.get('agent_reasoning', {})
                reasoning_node = TraceNode(
                    name='Reasoning Result',
                    type='reasoning',
                    start_time=entry.get('timestamp', ''),
                    metadata={
                        'current_situation': reasoning.get('current_situation'),
                        'enough_data': reasoning.get('enough_data'),
                        'task_completed': reasoning.get('task_completed'),
                        'reasoning_steps': reasoning.get('reasoning_steps', []),
                        'remaining_steps': reasoning.get('remaining_steps', [])
                    }
                )
                current_llm_node.add_child(reasoning_node)
            
            # Tool execution - добавляем как дочерний элемент к текущему LLM
            elif step_type == 'tool_execution' and current_llm_node:
                tool_name = entry.get('tool_name', 'unknown')
                
                # Пропускаем reasoningtool (системный)
                if tool_name == 'reasoningtool':
                    continue
                
                tool_context = entry.get('agent_tool_context', {})
                tool_result = entry.get('agent_tool_execution_result', '')
                
                # Иконка для инструмента
                tool_icon = {
                    'websearchtool': '🔍',
                    'extractpagecontenttool': '📄',
                    'finalanswertool': '✅'
                }.get(tool_name, '🔧')
                
                tool_node = TraceNode(
                    name=f'{tool_icon} {tool_name}',
                    type='tool',
                    start_time=entry.get('timestamp', ''),
                    metadata={
                        'tool_name': tool_name,
                        'arguments': tool_context,
                        'result': tool_result[:500] if isinstance(tool_result, str) else str(tool_result)[:500]
                    }
                )
                current_llm_node.add_child(tool_node)
        
        return root_nodes
    
    def render_trace_node(
        self,
        node: TraceNode,
        total_duration: float,
        show_details: bool = True
    ) -> None:
        """
        Отрисовывает узел трейса.
        
        Args:
            node: Узел для отрисовки
            total_duration: Общая длительность для расчета процентов
            show_details: Показывать ли детали
        """
        # Отступ в зависимости от уровня
        indent_html = "　　" * node.level  # Японский пробел для визуального отступа
        
        # Цвет
        color = self.COLORS.get(node.type, self.COLORS['tool'])
        if node.type == 'tool':
            tool_name = node.metadata.get('tool_name', '')
            if 'search' in tool_name:
                color = self.COLORS['search']
            elif 'extract' in tool_name:
                color = self.COLORS['extract']
            elif 'final' in tool_name:
                color = self.COLORS['final']
        
        # Процент от общего времени
        percent = (node.duration_ms / total_duration * 100) if total_duration > 0 and node.duration_ms > 0 else 0
        
        # Контейнер для узла
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                # Имя с иконкой и отступом
                st.markdown(
                    f"{indent_html}<span style='color: {color}; font-weight: 500; font-size: 0.9rem;'>{node.name}</span>",
                    unsafe_allow_html=True
                )
            
            with col2:
                if node.duration_ms > 0:
                    st.markdown(
                        f"<span style='color: #9CA3AF; font-size: 0.8rem;'>⏱ {node.duration_ms:.0f}ms</span>",
                        unsafe_allow_html=True
                    )
            
            with col3:
                # Метрики специфичные для типа
                if node.type == 'llm_call' and node.metadata.get('tokens'):
                    st.markdown(
                        f"<span style='color: #9CA3AF; font-size: 0.8rem;'>🎫 {node.metadata['tokens']}</span>",
                        unsafe_allow_html=True
                    )
                elif percent > 0 and node.level == 0:  # Процент только для корневых
                    st.markdown(
                        f"<span style='color: #9CA3AF; font-size: 0.8rem;'>{percent:.1f}%</span>",
                        unsafe_allow_html=True
                    )
            
            # Детали узла
            if show_details and node.metadata and node.level == 0:  # Детали только для LLM вызовов
                self._render_node_details(node, indent_html)
        
        # Рекурсивно отрисовываем детей
        for child in node.children:
            self.render_trace_node(child, total_duration, show_details)
    
    def _render_node_details(self, node: TraceNode, indent: str) -> None:
        """
        Отрисовывает детали узла (только для LLM вызовов).
        
        Args:
            node: Узел для отрисовки деталей
            indent: Отступ
        """
        metadata = node.metadata
        
        if node.type == 'llm_call':
            # Метрики производительности в одну строку
            metrics_parts = []
            if metadata.get('prompt_tokens'):
                metrics_parts.append(f"📥 {metadata['prompt_tokens']}")
            if metadata.get('completion_tokens'):
                metrics_parts.append(f"📤 {metadata['completion_tokens']}")
            if metadata.get('tokens_per_second'):
                metrics_parts.append(f"⚡ {metadata['tokens_per_second']:.0f}t/s")
            
            if metrics_parts:
                st.markdown(
                    f"{indent}　<span style='color: #9CA3AF; font-size: 0.75rem;'>{' • '.join(metrics_parts)}</span>",
                    unsafe_allow_html=True
                )
    
    def render_trace_tree(self, parser: LogParser) -> None:
        """
        Отрисовывает полное дерево трейсинга.
        
        Args:
            parser: Парсер логов
        """
        # Строим дерево
        root_nodes = self.build_trace_tree(parser)
        
        if not root_nodes:
            st.warning("Нет данных для трейсинга")
            return
        
        # Вычисляем общую длительность
        total_duration = sum([node.duration_ms for node in root_nodes])
        
        # Заголовок таблицы
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown("**Name**")
        with col2:
            st.markdown("**Duration**")
        with col3:
            st.markdown("**Tokens**")
        
        st.divider()
        
        # Отрисовываем узлы
        for node in root_nodes:
            self.render_trace_node(node, total_duration, show_details=True)
        
        st.divider()
        
        # Итоговая статистика
        col1, col2, col3 = st.columns(3)
        
        metrics = parser.get_aggregated_metrics()
        
        with col1:
            st.metric("⏱️ Total Time", f"{total_duration:.0f} ms")
        
        with col2:
            st.metric("🎫 Total Tokens", f"{metrics.get('total_tokens', 0):,}")
        
        with col3:
            st.metric("🤖 LLM Calls", len(root_nodes))

