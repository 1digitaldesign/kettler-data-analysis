#!/usr/bin/env python3
"""
Vertex AI Client
Provides access to Google Cloud Vertex AI services
"""

import os
from typing import Optional, Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# Try to import Vertex AI libraries
try:
    from google.cloud import aiplatform
    from google.oauth2 import service_account
    import google.auth
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    logger.warning("Vertex AI libraries not installed. Install with: pip install google-cloud-aiplatform")

def setup_vertex_ai():
    """Initialize Vertex AI client"""
    if not VERTEX_AI_AVAILABLE:
        raise ImportError("Vertex AI libraries not available")

    # Setup GCP authentication
    from scripts.microservices.gcp_auth import setup_gcp_auth, get_gcp_project_id, get_gcp_region

    if not setup_gcp_auth():
        raise ValueError("GCP credentials not configured")

    project_id = get_gcp_project_id()
    region = get_gcp_region()

    if not project_id:
        raise ValueError("GCP_PROJECT_ID not set")

    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=region)

    logger.info(f"Vertex AI initialized: project={project_id}, region={region}")

    return {
        'project_id': project_id,
        'region': region,
        'initialized': True
    }

class VertexAIClient:
    """Client for Vertex AI services"""

    def __init__(self):
        if not VERTEX_AI_AVAILABLE:
            raise ImportError("Vertex AI libraries not available")

        self.config = setup_vertex_ai()
        self.project_id = self.config['project_id']
        self.region = self.config['region']

    def list_models(self) -> List[Dict]:
        """List available Vertex AI models"""
        try:
            # This is a placeholder - adjust based on your Vertex AI setup
            models = aiplatform.Model.list()
            return [
                {
                    'name': model.display_name,
                    'resource_name': model.resource_name,
                    'create_time': str(model.create_time)
                }
                for model in models
            ]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def predict(self, model_name: str, instances: List[Any]) -> Dict:
        """Make predictions using a Vertex AI model"""
        try:
            # This is a placeholder - adjust based on your model setup
            endpoint = aiplatform.Endpoint(model_name)
            prediction = endpoint.predict(instances=instances)
            return {
                'predictions': prediction.predictions,
                'model': model_name
            }
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise

    def get_endpoint(self, endpoint_name: str):
        """Get a Vertex AI endpoint"""
        try:
            return aiplatform.Endpoint(endpoint_name)
        except Exception as e:
            logger.error(f"Error getting endpoint: {e}")
            raise

def get_vertex_ai_client() -> Optional[VertexAIClient]:
    """Get Vertex AI client instance"""
    if not VERTEX_AI_AVAILABLE:
        return None

    try:
        return VertexAIClient()
    except Exception as e:
        logger.error(f"Could not initialize Vertex AI client: {e}")
        return None

if __name__ == '__main__':
    try:
        client = get_vertex_ai_client()
        if client:
            print(f"✓ Vertex AI client initialized")
            print(f"  Project: {client.project_id}")
            print(f"  Region: {client.region}")
            models = client.list_models()
            print(f"  Available models: {len(models)}")
        else:
            print("⚠ Vertex AI client not available")
    except Exception as e:
        print(f"Error: {e}")
