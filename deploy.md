# 🚀 Deploy Raman - AI Companion

## Quick Deployment Guide

### Option 1: Streamlit Cloud (Recommended)

1. **Create GitHub Repository**
   - Go to [GitHub](https://github.com)
   - Create new repository
   - Upload all your bot files

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file to `app.py`
   - Add your API key in secrets

3. **Add Secrets in Streamlit Cloud**
   ```
   OPENAI_API_KEY = "sk-or-v1-your-api-key-here"
   ```

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Railway

1. **Connect GitHub to Railway**
2. **Set environment variables**
3. **Deploy automatically**

## 📁 Files Needed for Deployment

- `app.py` (main app)
- `config.py` (configuration)
- `openai_client.py` (AI client)
- `database.py` (memory)
- `image_handler.py` (images)
- `theme_handler.py` (themes)
- `requirements.txt` (dependencies)
- `images_/` folder (your images)

## 🔒 Environment Variables

Set these in your deployment platform:
- `OPENAI_API_KEY`: Your OpenRouter API key
- `OPENROUTER_SITE_URL`: Your site URL (optional)
- `OPENROUTER_SITE_NAME`: Your site name (optional)

## 🎉 After Deployment

Your Raman bot will be live and accessible to anyone with the URL!
