#!/usr/bin/env python3
"""
Setup script for Raman - Your Personal AI Companion
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements!")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("# OpenAI Configuration (OpenRouter)\n")
            f.write("OPENAI_API_KEY=your_api_key_here\n\n")
            f.write("# Optional: Customize your bot\n")
            f.write("BOT_NAME=Raman\n")
            f.write("BOT_PERSONALITY=a cute, friendly, and helpful assistant who loves to chat and help with anything\n")
        print("✅ .env file created! Please edit it with your API key.")
    else:
        print("✅ .env file already exists!")

def check_images():
    """Check if images directory has images"""
    images_dir = "images_"
    if os.path.exists(images_dir):
        images = [f for f in os.listdir(images_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
        if images:
            print(f"✅ Found {len(images)} images in '{images_dir}' directory!")
            return True
    
    print(f"⚠️  No images found in '{images_dir}' directory!")
    print("   Raman will use a default avatar.")
    return False

def main():
    """Main setup function"""
    print("💕 Raman Setup - Your Personal AI Companion 💕")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Check images
    check_images()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your OpenRouter API key")
    print("2. Add images to the 'images_' folder for custom avatars (optional)")
    print("3. Run: python run.py")
    print("4. Or double-click: launch.bat (Windows)")
    print("\n💕 Enjoy chatting with Raman!")
    print("=" * 60)

if __name__ == "__main__":
    main()
