"""Configuration template for Compel Classics Pipeline

Copy this file to config.py and fill in your actual values.
config.py is gitignored for security.
"""

CONFIG = {
    # ====================
    # LOCAL AI SETUP
    # ====================
    'LOCAL_AI': {
        'provider': 'anthropic',  # or 'local_llm'
        'api_key': 'your_anthropic_api_key_here',
        'model': 'claude-sonnet-4.5',
        'max_tokens': 4000,
        'temperature': 0.3,  # Lower for more consistent analysis
    },
    
    # ====================
    # ELEVENLABS
    # ====================
    'ELEVENLABS': {
        'api_key': 'your_elevenlabs_api_key',
        'use_flash_models': True,  # 50% cheaper, good quality
        
        # Voice IDs - get these from ElevenLabs voice library
        'voices': {
            'narrator_primary': {
                'voice_id': 'adam_voice_id',
                'name': 'Adam',
                'settings': {
                    'stability': 0.75,
                    'similarity_boost': 0.75,
                    'style': 0.5
                }
            },
            'male_british_young': {
                'voice_id': 'george_voice_id',
                'name': 'George',
                'settings': {'stability': 0.7, 'similarity_boost': 0.8}
            },
            'male_british_mature': {
                'voice_id': 'brian_voice_id',
                'name': 'Brian',
                'settings': {'stability': 0.8, 'similarity_boost': 0.75}
            },
            'female_british_young': {
                'voice_id': 'charlotte_voice_id',
                'name': 'Charlotte',
                'settings': {'stability': 0.7, 'similarity_boost': 0.8}
            },
        }
    },
    
    # ====================
    # IMAGE GENERATION
    # ====================
    'IMAGE_GEN': {
        'provider': 'comfyui',  # or 'stable_diffusion_api'
        'api_url': 'http://localhost:8188',  # ComfyUI default
        'workflow_path': 'workflows/victorian_illustration.json',
        
        # Style settings
        'style': 'victorian_illustrations',
        'resolution': '1024x1024',
        'steps': 30,
        'cfg_scale': 7.5,
    },
    
    # ====================
    # STORAGE
    # ====================
    'STORAGE': {
        # Local storage
        'local_archive': '/path/to/14tb/drive/compel-archives',
        'working_dir': './working',
        'output_dir': './output',
        
        # Cloud storage (Google Cloud Storage)
        'cloud_storage': {
            'bucket': 'compel-classics',
            'project_id': 'your-gcp-project-id',
            'credentials_file': '/path/to/service-account-key.json',
        },
        
        # CDN settings
        'cdn_base_url': 'https://cdn.compel-english.com',
    },
    
    # ====================
    # DATABASE (Web App)
    # ====================
    'DATABASE': {
        'host': 'your-cloud-sql-host',
        'port': 5432,
        'database': 'compel_english',
        'user': 'your_db_user',
        'password': 'your_db_password',
        'ssl': True,
    },
    
    # ====================
    # PROCESSING OPTIONS
    # ====================
    'PROCESSING': {
        # Text cleaning
        'ocr_fixes': {
            'rn': 'm',
            'vv': 'w',
            'l1': 'll',
            'cl': 'd',
        },
        
        # AI analysis
        'chunk_size': 5000,  # chars per API call
        'confidence_threshold': 0.85,  # minimum to auto-approve
        
        # Audio generation
        'audio_format': 'mp3',
        'audio_bitrate': '128k',
        'add_pauses': True,  # Add 0.5s between sentences
        
        # Image generation
        'scenes_per_book': 10,  # Target number of illustrations
        'generate_variations': 3,  # Generate 3 per scene, pick best
    },
    
    # ====================
    # COST TRACKING
    # ====================
    'COSTS': {
        'elevenlabs_per_1k_chars': 0.20,
        'image_gen_per_image': 0.75,
        'anthropic_per_1k_tokens': 0.003,
    },
    
    # ====================
    # PATHS
    # ====================
    'PATHS': {
        'input': './input',
        'working': './working',
        'output': './output',
        'archive': '/path/to/14tb/drive',
        'logs': './logs',
        'database': './pipeline.db',
    }
}

# Validation
def validate_config():
    """Validate configuration has required fields"""
    required = [
        ('LOCAL_AI', 'api_key'),
        ('ELEVENLABS', 'api_key'),
        ('STORAGE', 'local_archive'),
    ]
    
    for section, key in required:
        if not CONFIG.get(section, {}).get(key):
            raise ValueError(f"Missing required config: {section}.{key}")
    
    print("✓ Configuration valid")

if __name__ == '__main__':
    validate_config()
