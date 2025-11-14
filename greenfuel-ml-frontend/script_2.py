
# Create requirements.txt for backend
requirements = '''Flask==2.3.2
Flask-CORS==4.0.0
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==2.3.7
'''

with open('greenfuel-ml-frontend/requirements.txt', 'w') as f:
    f.write(requirements)

print("✓ Created requirements.txt")

# Create .gitignore
gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Flask
instance/
.webassets-cache

# Environment
.env
.env.local

# Pickle files (model files can be large)
*.pkl
*.pickle

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
'''

with open('greenfuel-ml-frontend/.gitignore', 'w') as f:
    f.write(gitignore)

print("✓ Created .gitignore")
