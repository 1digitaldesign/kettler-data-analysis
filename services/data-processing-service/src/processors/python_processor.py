"""
Python Data Processor
Handles data transformation and processing
"""

import pandas as pd
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PythonProcessor:
    """Process and transform data using Python"""

    def __init__(self):
        logger.info("Python Processor initialized")

    async def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform data based on input
        """
        try:
            # Handle different input types
            if isinstance(data, dict):
                if 'dataframe' in data:
                    # Process DataFrame
                    df = pd.DataFrame(data['dataframe'])
                    result = self._process_dataframe(df, data.get('operations', []))
                    return {"result": result.to_dict('records')}
                elif 'json' in data:
                    # Process JSON
                    json_data = json.loads(data['json']) if isinstance(data['json'], str) else data['json']
                    result = self._process_json(json_data, data.get('operations', []))
                    return {"result": result}
                else:
                    # Process dict directly
                    return {"result": self._process_dict(data)}
            else:
                raise ValueError("Unsupported data type")

        except Exception as e:
            logger.error(f"Error transforming data: {e}")
            raise

    def _process_dataframe(self, df: pd.DataFrame, operations: List[str]) -> pd.DataFrame:
        """Process DataFrame with operations"""
        result_df = df.copy()

        for operation in operations:
            if operation == 'clean':
                result_df = result_df.dropna()
            elif operation == 'deduplicate':
                result_df = result_df.drop_duplicates()
            elif operation.startswith('filter:'):
                # Format: filter:column=value
                parts = operation.split(':', 1)[1].split('=')
                if len(parts) == 2:
                    column, value = parts
                    result_df = result_df[result_df[column] == value]

        return result_df

    def _process_json(self, json_data: Any, operations: List[str]) -> Any:
        """Process JSON data"""
        result = json_data

        for operation in operations:
            if operation == 'normalize':
                if isinstance(result, list):
                    result = [self._normalize_dict(item) if isinstance(item, dict) else item for item in result]
                elif isinstance(result, dict):
                    result = self._normalize_dict(result)

        return result

    def _normalize_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize dictionary keys"""
        return {k.lower().replace(' ', '_'): v for k, v in d.items()}

    def _process_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process dictionary"""
        return self._normalize_dict(data)
