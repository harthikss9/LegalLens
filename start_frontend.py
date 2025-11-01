#!/usr/bin/env python3
"""
Startup script for LegalLens Frontend
"""
import subprocess
import sys
import os

def main():
    """Start the Next.js frontend development server."""
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found!")
        return False
    
    print("🚀 Starting LegalLens Frontend...")
    print("=" * 40)
    
    try:
        # Change to frontend directory and start Next.js
        subprocess.run([
            "npm", "run", "dev"
        ], cwd=frontend_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped by user")
        return True
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
