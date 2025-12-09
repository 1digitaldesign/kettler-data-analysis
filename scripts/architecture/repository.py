#!/usr/bin/env python3
"""
Repository Pattern Implementation
Data Access Layer for Data-Intensive Applications
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Any, TypeVar, Generic
from abc import ABC, abstractmethod
import logging

from .base import BaseRepository
from .models import Firm, Connection, Violation, Evidence, PropertyRecord
import sys
from pathlib import Path

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

T = TypeVar('T')


class DataRepository(BaseRepository, Generic[T]):
    """
    Generic Repository Pattern
    Provides data access abstraction
    """
    
    def __init__(self, data_source: Path):
        self.data_source = Path(data_source)
        self.cache: Dict[str, T] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Load data into cache"""
        pass
    
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find entity by ID"""
        return self.cache.get(entity_id)
    
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """Find all entities matching filters"""
        results = list(self.cache.values())
        
        if filters:
            results = self._apply_filters(results, filters)
        
        return results
    
    def _apply_filters(self, entities: List[T], filters: Dict[str, Any]) -> List[T]:
        """Apply filters to entities"""
        filtered = entities
        
        for key, value in filters.items():
            filtered = [e for e in filtered if self._matches_filter(e, key, value)]
        
        return filtered
    
    def _matches_filter(self, entity: T, key: str, value: Any) -> bool:
        """Check if entity matches filter"""
        if hasattr(entity, key):
            attr_value = getattr(entity, key)
            return attr_value == value
        return False
    
    def save(self, entity: T) -> T:
        """Save entity"""
        if hasattr(entity, 'firm_id'):
            self.cache[entity.firm_id] = entity
        elif hasattr(entity, 'connection_id'):
            self.cache[entity.connection_id] = entity
        elif hasattr(entity, 'violation_id'):
            self.cache[entity.violation_id] = entity
        elif hasattr(entity, 'evidence_id'):
            self.cache[entity.evidence_id] = entity
        elif hasattr(entity, 'record_id'):
            self.cache[entity.record_id] = entity
        
        return entity
    
    def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        if entity_id in self.cache:
            del self.cache[entity_id]
            return True
        return False


class FirmRepository(DataRepository[Firm]):
    """Repository for Firm entities"""
    
    def __init__(self, data_source: Path):
        super().__init__(data_source)
    
    def _load_cache(self) -> None:
        """Load firms from data source"""
        try:
            if self.data_source.suffix == '.json':
                with open(self.data_source, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    firms_data = data
                elif isinstance(data, dict) and 'firms' in data:
                    firms_data = data['firms']
                else:
                    firms_data = []
                
                for firm_data in firms_data:
                    if isinstance(firm_data, dict):
                        firm = Firm(
                            firm_id=firm_data.get('Firm.ID', firm_data.get('firm_id', '')),
                            firm_name=firm_data.get('Firm.Name', firm_data.get('firm_name', '')),
                            address=firm_data.get('Address', firm_data.get('address', '')),
                            principal_broker=firm_data.get('Principal.Broker', firm_data.get('principal_broker')),
                            license_number=firm_data.get('License.Number', firm_data.get('license_number')),
                            state=firm_data.get('State', firm_data.get('state')),
                            phone=firm_data.get('Phone', firm_data.get('phone')),
                            email=firm_data.get('Email', firm_data.get('email')),
                            metadata=firm_data
                        )
                        self.cache[firm.firm_id] = firm
            
            elif self.data_source.suffix == '.csv':
                df = pd.read_csv(self.data_source)
                for _, row in df.iterrows():
                    firm = Firm(
                        firm_id=str(row.get('Firm.ID', row.get('firm_id', ''))),
                        firm_name=str(row.get('Firm.Name', row.get('firm_name', ''))),
                        address=str(row.get('Address', row.get('address', ''))),
                        principal_broker=str(row.get('Principal.Broker', row.get('principal_broker', ''))) if pd.notna(row.get('Principal.Broker', row.get('principal_broker'))) else None,
                        license_number=str(row.get('License.Number', row.get('license_number', ''))) if pd.notna(row.get('License.Number', row.get('license_number'))) else None,
                        state=str(row.get('State', row.get('state', ''))) if pd.notna(row.get('State', row.get('state'))) else None,
                        phone=str(row.get('Phone', row.get('phone', ''))) if pd.notna(row.get('Phone', row.get('phone'))) else None,
                        email=str(row.get('Email', row.get('email', ''))) if pd.notna(row.get('Email', row.get('email'))) else None,
                        metadata=row.to_dict()
                    )
                    self.cache[firm.firm_id] = firm
        
        except Exception as e:
            logger.error(f"Error loading firms: {e}")
    
    def find_by_principal_broker(self, broker_name: str) -> List[Firm]:
        """Find firms by principal broker"""
        return [firm for firm in self.cache.values() if firm.principal_broker == broker_name]
    
    def find_by_address(self, address: str) -> List[Firm]:
        """Find firms by address"""
        address_lower = address.lower()
        return [firm for firm in self.cache.values() if address_lower in firm.address.lower()]


class FileRepository(BaseRepository):
    """
    File-based repository for general data
    """
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Find entity by ID from file"""
        file_path = self.base_path / f"{entity_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None
    
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Find all entities from files"""
        results = []
        for file_path in self.base_path.glob("*.json"):
            with open(file_path, 'r') as f:
                data = json.load(f)
                if filters:
                    if all(data.get(k) == v for k, v in filters.items()):
                        results.append(data)
                else:
                    results.append(data)
        return results
    
    def save(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Save entity to file"""
        entity_id = entity.get('id', entity.get('_id', 'unknown'))
        file_path = self.base_path / f"{entity_id}.json"
        with open(file_path, 'w') as f:
            json.dump(entity, f, indent=2, default=str)
        return entity
    
    def delete(self, entity_id: str) -> bool:
        """Delete entity file"""
        file_path = self.base_path / f"{entity_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False


class VectorRepository(BaseRepository):
    """
    Vector database repository for embeddings
    """
    
    def __init__(self, vector_store_path: Path):
        self.vector_store_path = Path(vector_store_path)
        self.index = None
        self.metadata = {}
        self._load_vector_store()
    
    def _load_vector_store(self) -> None:
        """Load vector store"""
        try:
            import faiss
            index_path = self.vector_store_path / "vector_index.faiss"
            metadata_path = self.vector_store_path / "metadata.json"
            
            if index_path.exists():
                self.index = faiss.read_index(str(index_path))
            
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
        except ImportError:
            logger.warning("FAISS not available")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Find entity by ID"""
        return self.metadata.get(entity_id)
    
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Find all entities"""
        results = list(self.metadata.values())
        
        if filters:
            results = [r for r in results if all(r.get(k) == v for k, v in filters.items())]
        
        return results
    
    def save(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Save entity"""
        entity_id = entity.get('id', entity.get('_id', 'unknown'))
        self.metadata[entity_id] = entity
        return entity
    
    def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        if entity_id in self.metadata:
            del self.metadata[entity_id]
            return True
        return False
    
    def search_similar(self, query_vector: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        if self.index is None:
            return []
        
        import numpy as np
        query_array = np.array([query_vector], dtype='float32')
        distances, indices = self.index.search(query_array, top_k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                result = list(self.metadata.values())[idx].copy()
                result['similarity'] = float(1 / (1 + dist))  # Convert distance to similarity
                result['distance'] = float(dist)
                results.append(result)
        
        return results
