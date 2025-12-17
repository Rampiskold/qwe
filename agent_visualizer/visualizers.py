"""
Визуализаторы для создания интерактивных графиков и диаграмм.

Модуль содержит классы для построения различных видов визуализаций:
роудмапов, метрик, временных линий и других графических представлений.
"""

from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from log_parser import AgentStep


class RoadmapVisualizer:
    """
    Визуализатор роудмапа выполнения агента.
    
    Создает интерактивную диаграмму, показывающую последовательность
    шагов и фаз выполнения задачи агентом.
    """
    
    # Цветовая схема для разных типов шагов
    STEP_COLORS = {
        'llm_call': '#3498db',          # Синий
        'reasoning': '#e74c3c',         # Красный
        'tool_execution': '#2ecc71',    # Зеленый
        'final_answer': '#f39c12',      # Оранжевый
        'default': '#95a5a6'            # Серый
    }
    
    # Иконки для разных типов шагов
    STEP_ICONS = {
        'llm_call': '🤖',
        'reasoning': '🧠',
        'tool_execution': '🛠️',
        'final_answer': '✅',
        'default': '⚙️'
    }
    
    def create_roadmap(self, steps: List[AgentStep]) -> go.Figure:
        """
        Создает визуализацию роудмапа в виде Sankey диаграммы.
        
        Args:
            steps: Список шагов агента для визуализации
            
        Returns:
            Plotly Figure объект с роудмапом
        """
        if not steps:
            return self._create_empty_figure("Нет данных для роудмапа")
        
        # Создаем граф потока выполнения
        fig = go.Figure()
        
        # Подготавливаем данные для графика
        x_positions = []
        y_positions = []
        colors = []
        sizes = []
        text_labels = []
        hover_texts = []
        
        for idx, step in enumerate(steps):
            x_positions.append(idx)
            y_positions.append(0)
            
            # Определяем цвет на основе типа шага
            color = self.STEP_COLORS.get(step.step_type, self.STEP_COLORS['default'])
            colors.append(color)
            
            # Размер пропорционален длительности
            duration = step.metrics.get('duration_ms', 100)
            sizes.append(max(20, min(60, duration / 50)))
            
            # Создаем метку
            icon = self.STEP_ICONS.get(step.step_type, self.STEP_ICONS['default'])
            label = f"{icon} {step.step_number}"
            text_labels.append(label)
            
            # Создаем hover текст
            hover = self._create_hover_text(step)
            hover_texts.append(hover)
        
        # Добавляем узлы шагов
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_positions,
            mode='markers+text',
            marker=dict(
                size=sizes,
                color=colors,
                line=dict(width=2, color='white')
            ),
            text=text_labels,
            textposition='top center',
            hovertext=hover_texts,
            hoverinfo='text',
            name='Шаги'
        ))
        
        # Добавляем линии связи между шагами
        for i in range(len(steps) - 1):
            fig.add_trace(go.Scatter(
                x=[i, i + 1],
                y=[0, 0],
                mode='lines',
                line=dict(
                    color='lightgray',
                    width=2
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Настраиваем layout
        fig.update_layout(
            title="Роудмап выполнения агента",
            xaxis=dict(
                title="Прогресс",
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[-1, 1]
            ),
            height=400,
            hovermode='closest',
            showlegend=False,
            plot_bgcolor='white'
        )
        
        return fig
    
    def create_phase_flow(self, steps: List[AgentStep]) -> go.Figure:
        """
        Создает визуализацию потока фаз выполнения.
        
        Args:
            steps: Список шагов агента
            
        Returns:
            Plotly Figure с Sankey диаграммой фаз
        """
        if not steps:
            return self._create_empty_figure("Нет данных для потока фаз")
        
        # Подсчитываем переходы между фазами
        phase_transitions = {}
        prev_phase = None
        
        for step in steps:
            phase = step.phase or step.step_type
            
            if prev_phase:
                key = (prev_phase, phase)
                phase_transitions[key] = phase_transitions.get(key, 0) + 1
            
            prev_phase = phase
        
        # Создаем уникальный список фаз
        all_phases = set()
        for source, target in phase_transitions.keys():
            all_phases.add(source)
            all_phases.add(target)
        
        phase_list = list(all_phases)
        phase_indices = {phase: idx for idx, phase in enumerate(phase_list)}
        
        # Подготавливаем данные для Sankey
        sources = []
        targets = []
        values = []
        
        for (source, target), count in phase_transitions.items():
            sources.append(phase_indices[source])
            targets.append(phase_indices[target])
            values.append(count)
        
        # Создаем Sankey диаграмму
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=phase_list,
                color="lightblue"
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])
        
        fig.update_layout(
            title="Поток фаз выполнения",
            height=400
        )
        
        return fig
    
    def _create_hover_text(self, step: AgentStep) -> str:
        """
        Создает текст для hover подсказки шага.
        
        Args:
            step: Объект шага агента
            
        Returns:
            Форматированный текст подсказки
        """
        lines = [
            f"<b>Шаг {step.step_number}</b>",
            f"Тип: {step.step_type}",
        ]
        
        if step.phase:
            lines.append(f"Фаза: {step.phase}")
        
        if step.metrics:
            if 'duration_ms' in step.metrics:
                lines.append(f"Длительность: {step.metrics['duration_ms']:.2f} мс")
            if 'total_tokens' in step.metrics:
                lines.append(f"Токены: {step.metrics['total_tokens']}")
        
        if step.reasoning and step.reasoning.get('current_situation'):
            situation = step.reasoning['current_situation'][:100]
            lines.append(f"<br>Ситуация: {situation}...")
        
        return "<br>".join(lines)
    
    def _create_empty_figure(self, message: str) -> go.Figure:
        """
        Создает пустую фигуру с сообщением.
        
        Args:
            message: Сообщение для отображения
            
        Returns:
            Пустая Plotly Figure с текстом
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        return fig


class MetricsVisualizer:
    """
    Визуализатор метрик производительности агента.
    
    Создает графики и диаграммы для анализа производительности,
    использования ресурсов и эффективности работы агента.
    """
    
    def create_duration_chart(self, steps: List[AgentStep]) -> go.Figure:
        """
        Создает график длительности выполнения шагов.
        
        Args:
            steps: Список шагов агента
            
        Returns:
            Plotly Figure с графиком длительности
        """
        if not steps:
            return self._create_empty_figure("Нет данных о длительности")
        
        step_numbers = []
        durations = []
        step_types = []
        
        for step in steps:
            if 'duration_ms' in step.metrics:
                step_numbers.append(step.step_number)
                durations.append(step.metrics['duration_ms'])
                step_types.append(step.step_type)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=step_numbers,
            y=durations,
            marker=dict(
                color=durations,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="мс")
            ),
            text=[f"{d:.2f} мс" for d in durations],
            textposition='auto',
            hovertemplate='<b>Шаг %{x}</b><br>Длительность: %{y:.2f} мс<extra></extra>'
        ))
        
        fig.update_layout(
            title="Длительность выполнения шагов",
            xaxis_title="Номер шага",
            yaxis_title="Длительность (мс)",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_tokens_chart(self, steps: List[AgentStep]) -> go.Figure:
        """
        Создает график использования токенов по шагам.
        
        Args:
            steps: Список шагов агента
            
        Returns:
            Plotly Figure с графиком токенов
        """
        if not steps:
            return self._create_empty_figure("Нет данных о токенах")
        
        step_numbers = []
        prompt_tokens = []
        completion_tokens = []
        
        for step in steps:
            if 'total_tokens' in step.metrics:
                step_numbers.append(step.step_number)
                prompt_tokens.append(step.metrics.get('prompt_tokens', 0))
                completion_tokens.append(step.metrics.get('completion_tokens', 0))
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Prompt токены',
            x=step_numbers,
            y=prompt_tokens,
            marker_color='lightblue',
            hovertemplate='<b>Шаг %{x}</b><br>Prompt: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Completion токены',
            x=step_numbers,
            y=completion_tokens,
            marker_color='lightcoral',
            hovertemplate='<b>Шаг %{x}</b><br>Completion: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Использование токенов по шагам",
            xaxis_title="Номер шага",
            yaxis_title="Количество токенов",
            barmode='stack',
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_cumulative_timeline(self, steps: List[AgentStep]) -> go.Figure:
        """
        Создает график накопительной динамики токенов и времени.
        
        Args:
            steps: Список шагов агента
            
        Returns:
            Plotly Figure с накопительным графиком
        """
        if not steps:
            return self._create_empty_figure("Нет данных для динамики")
        
        step_numbers = []
        cumulative_tokens = []
        cumulative_duration = []
        
        total_tokens = 0
        total_duration = 0
        
        for step in steps:
            step_numbers.append(step.step_number)
            
            if 'total_tokens' in step.metrics:
                total_tokens += step.metrics['total_tokens']
            cumulative_tokens.append(total_tokens)
            
            if 'duration_ms' in step.metrics:
                total_duration += step.metrics['duration_ms']
            cumulative_duration.append(total_duration)
        
        # Создаем фигуру с двумя осями Y
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=step_numbers,
            y=cumulative_tokens,
            name='Накопленные токены',
            mode='lines+markers',
            line=dict(color='blue', width=3),
            marker=dict(size=8),
            yaxis='y1'
        ))
        
        fig.add_trace(go.Scatter(
            x=step_numbers,
            y=cumulative_duration,
            name='Накопленное время (мс)',
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Накопительная динамика выполнения",
            xaxis=dict(title="Номер шага"),
            yaxis=dict(
                title=dict(text="Накопленные токены", font=dict(color="blue")),
                tickfont=dict(color="blue")
            ),
            yaxis2=dict(
                title=dict(text="Накопленное время (мс)", font=dict(color="red")),
                tickfont=dict(color="red"),
                overlaying='y',
                side='right'
            ),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_tool_usage_pie(self, tool_stats: Dict[str, int]) -> go.Figure:
        """
        Создает круговую диаграмму использования инструментов.
        
        Args:
            tool_stats: Словарь с количеством вызовов каждого инструмента
            
        Returns:
            Plotly Figure с круговой диаграммой
        """
        if not tool_stats:
            return self._create_empty_figure("Нет данных об инструментах")
        
        labels = list(tool_stats.keys())
        values = list(tool_stats.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Вызовов: %{value}<br>Процент: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Распределение использования инструментов",
            height=400
        )
        
        return fig
    
    def _create_empty_figure(self, message: str) -> go.Figure:
        """
        Создает пустую фигуру с сообщением.
        
        Args:
            message: Сообщение для отображения
            
        Returns:
            Пустая Plotly Figure с текстом
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        return fig


class TimelineVisualizer:
    """
    Визуализатор временной линии выполнения агента.
    
    Создает интерактивную временную шкалу с отображением
    всех событий и их длительности.
    """
    
    def create_timeline(self, steps: List[AgentStep]) -> go.Figure:
        """
        Создает временную линию выполнения шагов агента.
        
        Args:
            steps: Список шагов агента
            
        Returns:
            Plotly Figure с временной линией
        """
        if not steps:
            return self._create_empty_figure("Нет данных для временной линии")
        
        # Подготавливаем данные для Gantt chart
        tasks = []
        
        for idx, step in enumerate(steps):
            # Парсим timestamp
            try:
                start_time = datetime.fromisoformat(step.timestamp.replace('Z', '+00:00'))
            except:
                start_time = datetime.now()
            
            # Вычисляем конечное время на основе длительности
            duration_ms = step.metrics.get('duration_ms', 1000)
            
            task_name = f"Шаг {step.step_number}: {step.step_type}"
            
            tasks.append(dict(
                Task=task_name,
                Start=start_time,
                Finish=start_time,
                Resource=step.step_type,
                Duration=duration_ms
            ))
        
        # Создаем цветовую схему
        color_map = {
            'llm_call': 'rgb(52, 152, 219)',
            'reasoning': 'rgb(231, 76, 60)',
            'tool_execution': 'rgb(46, 204, 113)',
            'final_answer': 'rgb(243, 156, 18)'
        }
        
        fig = go.Figure()
        
        for task in tasks:
            color = color_map.get(task['Resource'], 'rgb(149, 165, 166)')
            
            fig.add_trace(go.Scatter(
                x=[task['Start']],
                y=[task['Task']],
                mode='markers',
                marker=dict(
                    size=max(10, min(30, task['Duration'] / 100)),
                    color=color,
                    line=dict(width=2, color='white')
                ),
                name=task['Resource'],
                showlegend=False,
                hovertemplate=f"<b>{task['Task']}</b><br>Время: {task['Start']}<br>Длительность: {task['Duration']:.2f} мс<extra></extra>"
            ))
        
        fig.update_layout(
            title="Временная линия выполнения",
            xaxis_title="Время",
            yaxis_title="Шаги",
            height=max(400, len(tasks) * 30),
            showlegend=False,
            hovermode='closest'
        )
        
        return fig
    
    def _create_empty_figure(self, message: str) -> go.Figure:
        """
        Создает пустую фигуру с сообщением.
        
        Args:
            message: Сообщение для отображения
            
        Returns:
            Пустая Plotly Figure с текстом
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        return fig

