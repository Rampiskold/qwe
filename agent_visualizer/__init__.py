"""
Agent Visualizer - интерактивная визуализация трейсинга агентов SGR.

Пакет для анализа и визуализации логов работы агентов на базе
Schema-Guided Reasoning (SGR) подхода.
"""

__version__ = "1.0.0"
__author__ = "SGR Team"

from .log_parser import LogParser, AgentStep
from .visualizers import RoadmapVisualizer, MetricsVisualizer, TimelineVisualizer

__all__ = [
    'LogParser',
    'AgentStep',
    'RoadmapVisualizer',
    'MetricsVisualizer',
    'TimelineVisualizer'
]

