# Hugging Face Token Configuration

## Overview

Hugging Face tokens have been configured for authenticated access to models and the Hugging Face Hub.

## Tokens Configured

- **Write Token**: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (for uploading models/data) - **Set in .env file**
- **Read Token**: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (for downloading models/data) - **Set in .env file**

## Configuration Files

### `.env` File
The tokens are stored in `.env` file (gitignored for security):
```
HF_WRITE_TOKEN=your_write_token_here
HF_READ_TOKEN=your_read_token_here
```

### `.env.example` File
Template file showing required environment variables (safe to commit):
```
HF_WRITE_TOKEN=your_write_token_here
HF_READ_TOKEN=your_read_token_here
```

## Integration Points

### Docker Compose
The `docker-compose.yml` has been updated to:
- Load environment variables from `.env` file
- Pass tokens to containers via `env_file` and `environment` sections
- Make tokens available to all Python services

### Python Services
- **Vector Embeddings** (`scripts/etl/vector_embeddings.py`): Uses tokens for model downloads
- **ETL Pipeline** (`scripts/etl/etl_pipeline.py`): Authenticates before processing
- **Hugging Face Auth** (`scripts/etl/huggingface_auth.py`): Helper module for authentication

## Usage

### Automatic Authentication
Tokens are automatically loaded from `.env` file when:
- Starting Docker Compose services
- Running Python scripts in containers
- Using the ETL pipeline

### Manual Testing
Test authentication:
```bash
# In Docker container
docker-compose exec python-etl python scripts/etl/huggingface_auth.py

# Or locally (if .env is loaded)
python scripts/etl/huggingface_auth.py
```

### Using Tokens in Code
```python
import os
from huggingface_hub import login

# Token is automatically available from environment
token = os.getenv('HF_WRITE_TOKEN')
if token:
    login(token=token)
```

## Security

✅ **Tokens are gitignored** - `.env` file is in `.gitignore`
✅ **Example file provided** - `.env.example` shows structure without tokens
✅ **Environment variables** - Tokens passed via environment, not hardcoded
✅ **Container isolation** - Tokens only available in containers that need them

## Services Using Tokens

1. **Python ETL Service**
   - Downloads models from Hugging Face Hub
   - Uses read token for model access
   - Uses write token for uploading embeddings/models

2. **Vector API Service**
   - May need tokens for custom model downloads
   - Inherits tokens from environment

## Verification

Check if tokens are loaded:
```bash
# Check environment variables in container
docker-compose exec python-etl env | grep HF_

# Test authentication
docker-compose exec python-etl python scripts/etl/huggingface_auth.py
```

## Troubleshooting

### Tokens Not Working
1. Verify `.env` file exists and contains tokens
2. Check Docker Compose is loading `.env`:
   ```bash
   docker-compose config | grep HF_
   ```
3. Restart services:
   ```bash
   docker-compose restart python-etl vector-api
   ```

### Authentication Errors
- Verify tokens are valid
- Check token permissions (read vs write)
- Ensure `huggingface-hub` package is installed

## Next Steps

1. **Test Authentication**: Run `python scripts/etl/huggingface_auth.py`
2. **Download Models**: Models will authenticate automatically
3. **Upload Embeddings**: Use write token for uploading to Hub (if needed)

## Token Management

### For Team Members
1. Copy `.env.example` to `.env`
2. Add your Hugging Face tokens
3. Never commit `.env` to git

### For CI/CD
Set tokens as secrets/environment variables:
```yaml
env:
  HF_WRITE_TOKEN: ${{ secrets.HF_WRITE_TOKEN }}
  HF_READ_TOKEN: ${{ secrets.HF_READ_TOKEN }}
```
