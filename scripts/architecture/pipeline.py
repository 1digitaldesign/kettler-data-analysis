#!/usr/bin/env python3
"""
Pipeline Pattern Implementation
For ETL and data processing workflows
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from .base import BaseProcessor
import logging

logger = logging.getLogger(__name__)


class PipelineStage(ABC):
    """
    Pipeline Stage - Chain of Responsibility Pattern
    """

    def __init__(self, name: str):
        self.name = name
        self.next_stage: Optional['PipelineStage'] = None

    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute stage processing"""
        pass

    def set_next(self, stage: 'PipelineStage') -> 'PipelineStage':
        """Set next stage in pipeline"""
        self.next_stage = stage
        return stage

    def run(self, data: Any) -> Any:
        """Execute this stage and pass to next"""
        result = self.execute(data)

        if self.next_stage:
            return self.next_stage.run(result)

        return result


class DataPipeline:
    """
    Pipeline Pattern: Sequential data processing
    """

    def __init__(self, name: str):
        self.name = name
        self.stages: List[PipelineStage] = []
        self.results: Dict[str, Any] = {}

    def add_stage(self, stage: PipelineStage) -> 'DataPipeline':
        """Add stage to pipeline"""
        if self.stages:
            self.stages[-1].set_next(stage)
        self.stages.append(stage)
        return self

    def execute(self, initial_data: Any) -> Any:
        """Execute entire pipeline"""
        if not self.stages:
            return initial_data

        result = self.stages[0].run(initial_data)
        self.results['final_result'] = result
        return result

    def get_results(self) -> Dict[str, Any]:
        """Get pipeline results"""
        return self.results


class ETLPipeline(DataPipeline):
    """
    Extract, Transform, Load Pipeline
    """

    def __init__(self, name: str = "ETL Pipeline"):
        super().__init__(name)
        self.extract_stage = None
        self.transform_stage = None
        self.load_stage = None

    def extract(self, source: Any) -> Any:
        """Extract data from source"""
        if self.extract_stage:
            return self.extract_stage.execute(source)
        return source

    def transform(self, data: Any) -> Any:
        """Transform data"""
        if self.transform_stage:
            return self.transform_stage.execute(data)
        return data

    def load(self, data: Any, destination: Any) -> Any:
        """Load data to destination"""
        if self.load_stage:
            return self.load_stage.execute({'data': data, 'destination': destination})
        return data

    def run_etl(self, source: Any, destination: Any) -> Dict[str, Any]:
        """Run complete ETL pipeline"""
        extracted = self.extract(source)
        transformed = self.transform(extracted)
        loaded = self.load(transformed, destination)

        return {
            'extracted': extracted,
            'transformed': transformed,
            'loaded': loaded,
            'status': 'completed'
        }


class AnalysisPipeline(DataPipeline):
    """
    Analysis Pipeline with multiple strategies
    """

    def __init__(self, name: str = "Analysis Pipeline"):
        super().__init__(name)
        self.strategies: List[Any] = []

    def add_strategy(self, strategy: Any) -> 'AnalysisPipeline':
        """Add analysis strategy"""
        self.strategies.append(strategy)
        return self

    def execute_all(self, data: Any) -> Dict[str, Any]:
        """Execute all strategies"""
        results = {}

        for strategy in self.strategies:
            try:
                strategy_result = strategy.analyze(data)
                results[strategy.get_strategy_name()] = strategy_result
            except Exception as e:
                logger.error(f"Error in strategy {strategy.get_strategy_name()}: {e}")
                results[strategy.get_strategy_name()] = {'error': str(e)}

        return results
