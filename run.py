#!/usr/bin/env python3
"""
Raman - Your Personal AI Companion
Launch script for the adorable chatbot
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import openai
        import PIL
        import sqlite3
        print("✅ All requirements are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_images():
    """Check if images directory exists and has images"""
    images_dir = "images_"
    if not os.path.exists(images_dir):
        print(f"❌ Images directory '{images_dir}' not found!")
        return False
    
    images = [f for f in os.listdir(images_dir) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
    
    if not images:
        print(f"❌ No images found in '{images_dir}' directory!")
        print("Please add some images to use as avatars.")
        return False
    
    print(f"✅ Found {len(images)} images in '{images_dir}' directory!")
    return True

def main():
    """Main launch function"""
    print("🇮🇳 Raman - Your AI Companion 🇮🇳")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check images
    if not check_images():
        print("⚠️  Warning: No images found. Raman will use default avatar.")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY") and "sk-or-v1-" not in open("config.py").read():
        print("⚠️  Warning: No API key found. Please set OPENAI_API_KEY in .env file or config.py")
    
    print("\n🚀 Launching Raman...")
    print("📱 The app will open in your browser automatically!")
    print("🇮🇳 Enjoy chatting with Raman in English or Hinglish!")
    print("=" * 50)
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for chatting with Raman! 🇮🇳")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
