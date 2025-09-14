import os
import base64
import random
from PIL import Image
import streamlit as st
from typing import List, Optional
from config import IMAGES_DIR, DEFAULT_AVATAR

class ImageHandler:
    def __init__(self):
        self.images_dir = IMAGES_DIR
        self.default_avatar = DEFAULT_AVATAR
        self.available_images = self._get_available_images()
    
    def _get_available_images(self) -> List[str]:
        """Get list of available image files"""
        if not os.path.exists(self.images_dir):
            return []
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        images = []
        
        for file in os.listdir(self.images_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                images.append(file)
        
        return images
    
    def get_random_avatar(self) -> str:
        """Get a random avatar from available images"""
        if not self.available_images:
            return self.default_avatar
        
        return random.choice(self.available_images)
    
    def get_avatar_path(self, avatar_name: str) -> Optional[str]:
        """Get full path to avatar image"""
        if avatar_name:
            full_path = os.path.join(self.images_dir, avatar_name)
            if os.path.exists(full_path):
                return full_path
        
        # Try default avatar
        if self.default_avatar:
            default_path = os.path.join(self.images_dir, self.default_avatar)
            if os.path.exists(default_path):
                return default_path
        
        return None
    
    def resize_image(self, image_path: str, size: tuple = (150, 150)) -> Optional[str]:
        """Resize image and return base64 encoded string"""
        try:
            if not os.path.exists(image_path):
                return None
                
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize with high quality
                img = img.resize(size, Image.Resampling.LANCZOS)
                
                # Save to bytes
                import io
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG', quality=95)
                img_bytes = img_bytes.getvalue()
                
                # Encode to base64
                encoded = base64.b64encode(img_bytes).decode()
                return f"data:image/png;base64,{encoded}"
                
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def get_avatar_base64(self, avatar_name: str = None, size: tuple = (150, 150)) -> Optional[str]:
        """Get base64 encoded avatar image"""
        if not avatar_name:
            avatar_name = self.get_random_avatar()
        
        avatar_path = self.get_avatar_path(avatar_name)
        if avatar_path:
            return self.resize_image(avatar_path, size)
        
        return None
    
    def create_avatar_selector(self, current_avatar: str = "") -> str:
        """Create avatar selection interface"""
        if not self.available_images:
            return current_avatar or self.default_avatar
        
        # Create columns for avatar grid
        cols = st.columns(3)
        selected_avatar = current_avatar
        
        for i, avatar in enumerate(self.available_images):
            col = cols[i % 3]
            
            with col:
                avatar_path = self.get_avatar_path(avatar)
                if avatar_path:
                    # Display avatar as selectable option
                    if st.button("", key=f"avatar_{i}", help=avatar):
                        selected_avatar = avatar
                    
                    # Show preview
                    avatar_b64 = self.get_avatar_base64(avatar, (80, 80))
                    if avatar_b64:
                        st.image(avatar_b64, width=60)
                        st.caption(avatar.replace('.jpeg.jpg', '').replace('.jpg', '').replace('_', ' ').title())
        
        return selected_avatar or self.default_avatar
