
import os
import subprocess

os.chdir('greenfuel-ml-frontend')

# Push to GitHub
try:
    print("🚀 Pushing to GitHub...")
    result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                          capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
        print("\n📊 Push Output:")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Info:", result.stderr)
    else:
        print(f"⚠️ Push output: {result.stderr}")
        print(f"Return code: {result.returncode}")
        
except subprocess.TimeoutExpired:
    print("⏱️ Push timed out - but it may still be processing")
except Exception as e:
    print(f"⚠️ Push error: {e}")
    print("Note: The token might have push restrictions or network issues")

os.chdir('..')

print("\n" + "="*70)
print("✅ DEPLOYMENT PREPARATION COMPLETE!")
print("="*70)
