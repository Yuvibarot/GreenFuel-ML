
import os
import subprocess
import json

# Change to the project directory
os.chdir('greenfuel-ml-frontend')

# Initialize git repo
try:
    subprocess.run(['git', 'init'], capture_output=True, check=True)
    print("✓ Git repository initialized")
except Exception as e:
    print(f"✗ Git init error: {e}")

# Configure git
try:
    subprocess.run(['git', 'config', 'user.name', 'GreenFuel-Deploy'], capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'greenfuel@noreply.github.com'], capture_output=True)
    print("✓ Git configured")
except Exception as e:
    print(f"Git config warning: {e}")

# Add all files
try:
    subprocess.run(['git', 'add', '-A'], capture_output=True, check=True)
    print("✓ Files staged for commit")
    
    # Show what will be committed
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    files = result.stdout.strip().split('\n')
    print(f"\n📦 Files to commit ({len(files)}):")
    for f in files[:10]:  # Show first 10
        print(f"   {f}")
    if len(files) > 10:
        print(f"   ... and {len(files) - 10} more files")
except Exception as e:
    print(f"✗ Git add error: {e}")

# Create initial commit
try:
    subprocess.run(['git', 'commit', '-m', 
                   'Initial commit: GreenFuel-ML Full Stack Application\n\n- Frontend: Professional web interface\n- Backend: Flask API with ML model\n- Deployment: AWS SAM, Docker, GitHub Pages\n- Features: Real-time predictions, Model info, Responsive design'], 
                  capture_output=True, check=True)
    print("\n✓ Initial commit created")
except Exception as e:
    print(f"✗ Commit error: {e}")

# Add remote
try:
    # First, remove any existing remote
    subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
except:
    pass

try:
    # Use HTTPS with token
    remote_url = 'https://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@github.com/Yuvibarot/GreenFuel-ML.git'
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], capture_output=True, check=True)
    print("✓ Remote repository configured")
except Exception as e:
    print(f"✗ Remote add error: {e}")

# Create main branch
try:
    subprocess.run(['git', 'branch', '-M', 'main'], capture_output=True)
    print("✓ Main branch created")
except Exception as e:
    print(f"✗ Branch error: {e}")

os.chdir('..')

print("\n" + "="*60)
print("✅ LOCAL SETUP COMPLETE - READY FOR GITHUB PUSH")
print("="*60)
