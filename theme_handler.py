import os
import base64
import random
from PIL import Image
import streamlit as st
from typing import List, Optional
from config import IMAGES_DIR

class ThemeHandler:
    def __init__(self):
        self.images_dir = IMAGES_DIR
        self.available_images = self._get_available_images()
        self.current_theme_image = None
    
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
    
    def get_random_theme_image(self) -> str:
        """Get a random theme image from available images"""
        if not self.available_images:
            return None
        
        return random.choice(self.available_images)
    
    def get_theme_image_path(self, image_name: str) -> Optional[str]:
        """Get full path to theme image"""
        if image_name:
            full_path = os.path.join(self.images_dir, image_name)
            if os.path.exists(full_path):
                return full_path
        return None
    
    def resize_image_for_background(self, image_path: str, size: tuple = (1200, 800)) -> Optional[str]:
        """Resize image for background and return base64 encoded string"""
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
                img.save(img_bytes, format='JPEG', quality=85)
                img_bytes = img_bytes.getvalue()
                
                # Encode to base64
                encoded = base64.b64encode(img_bytes).decode()
                return f"data:image/jpeg;base64,{encoded}"
                
        except Exception as e:
            print(f"Error processing theme image {image_path}: {e}")
            return None
    
    def get_theme_background_css(self, image_name: str = None) -> str:
        """Get CSS for theme background"""
        if not image_name:
            image_name = self.get_random_theme_image()
        
        if not image_name:
            return ""
        
        image_path = self.get_theme_image_path(image_name)
        if not image_path:
            return ""
        
        background_b64 = self.resize_image_for_background(image_path)
        if not background_b64:
            return ""
        
        return f"""
        body {{
            background-image: url('{background_b64}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        
        .main .block-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .main-header {{
            background: rgba(255, 107, 157, 0.9) !important;
            backdrop-filter: blur(10px);
        }}
        
        .chat-container {{
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px);
        }}
        
        .stSidebar {{
            background: rgba(248, 187, 217, 0.9) !important;
            backdrop-filter: blur(10px);
        }}
        """
    
    def create_theme_selector(self, current_theme: str = "") -> str:
        """Create theme selection interface"""
        if not self.available_images:
            return current_theme
        
        # Create columns for theme grid
        cols = st.columns(3)
        selected_theme = current_theme
        
        for i, image in enumerate(self.available_images):
            col = cols[i % 3]
            
            with col:
                image_path = self.get_theme_image_path(image)
                if image_path:
                    # Display theme as selectable option
                    if st.button("", key=f"theme_{i}", help=f"Use {image} as theme"):
                        selected_theme = image
                    
                    # Show preview
                    theme_b64 = self.resize_image_for_background(image, (150, 100))
                    if theme_b64:
                        st.image(theme_b64, width=120)
                        st.caption(image.replace('.jpeg.jpg', '').replace('.jpg', '').replace('_', ' ').title())
        
        return selected_theme or self.get_random_theme_image()
    
    def apply_theme_to_page(self, image_name: str = None):
        """Apply theme to the entire page with multiple images as background"""
        if image_name:
            theme_css = self.get_theme_background_css(image_name)
        else:
            theme_css = self.get_multi_image_background_css()
        
        if theme_css:
            st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)
    
    def get_multi_image_background_css(self) -> str:
        """Create amazing background using multiple images"""
        if not self.available_images:
            return ""
        
        # Use multiple images for a stunning background
        background_images = []
        for i, image in enumerate(self.available_images[:4]):  # Use up to 4 images
            image_path = self.get_theme_image_path(image)
            if image_path and os.path.exists(image_path):
                try:
                    bg_b64 = self.resize_image_for_background(image_path, (800, 600))
                    if bg_b64:
                        background_images.append(f"url('{bg_b64}')")
                except Exception as e:
                    print(f"Error processing {image}: {e}")
                    continue
        
        if not background_images:
            return ""
        
        # Create CSS with multiple background layers
        background_layers = ', '.join(background_images)
        
        return f"""
        body {{
            background-image: {background_layers};
            background-size: cover, cover, cover, cover;
            background-position: center, top left, bottom right, center;
            background-attachment: fixed, fixed, fixed, fixed;
            background-repeat: no-repeat, no-repeat, no-repeat, no-repeat;
            background-blend-mode: overlay, multiply, screen, normal;
        }}
        
        .main .block-container {{
            background: rgba(255, 255, 255, 0.92);
            border-radius: 25px;
            padding: 2rem;
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            position: relative;
        }}
        
        .main .block-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, 
                rgba(255, 107, 157, 0.1) 0%, 
                rgba(248, 187, 217, 0.1) 50%, 
                rgba(196, 69, 105, 0.1) 100%);
            border-radius: 25px;
            pointer-events: none;
        }}
        
        .main-header {{
            background: rgba(255, 107, 157, 0.9) !important;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}
        
        .chat-container {{
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 107, 157, 0.2);
        }}
        
        .stSidebar {{
            background: rgba(248, 187, 217, 0.9) !important;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}
        
        /* Add some magical sparkle effects */
        .main .block-container::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255, 107, 157, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(248, 187, 217, 0.3) 0%, transparent 50%);
            border-radius: 25px;
            pointer-events: none;
        }}
        """
