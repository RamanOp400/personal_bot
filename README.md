# 🇮🇳 Raman - Your AI Companion

The most intelligent and friendly chatbot you'll ever meet! Built with love using Python, Streamlit, and OpenAI's GPT-4 via OpenRouter. Speaks both English and Hinglish fluently!

## ✨ Features

- 🎨 **Beautiful, Modern UI**: The most attractive chat interface with Indian vibes
- 🧠 **Perfect Memory**: Never forgets your conversations using SQLite database
- 🖼️ **Custom Avatars**: Uses your personal images as avatars
- 📱 **Mobile Responsive**: Works perfectly on any device
- 🇮🇳 **Multi-language Support**: Speaks both English and Hinglish naturally
- 🎭 **Smart Personality**: Raman adapts to your language and remembers you
- 🔄 **Real-time Chat**: Instant responses with smooth animations
- ⚙️ **Customizable**: Personalize your experience with settings

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API Key**
   - Copy `.env.example` to `.env`
   - Add your OpenRouter API key to the `.env` file

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

4. **Enjoy!** 🎉
   - Open your browser to the provided URL
   - Start chatting with Raman!

## 📁 Project Structure

```
bot_/
├── app.py              # Main Streamlit application
├── config.py           # Configuration settings
├── database.py         # Memory and database management
├── openai_client.py    # OpenAI API integration with multi-language support
├── image_handler.py    # Avatar and image processing
├── requirements.txt    # Python dependencies
├── images_/           # Your custom avatar images
└── chat_memory.db     # SQLite database (created automatically)
```

## 🎨 Customization

### Changing Bot Personality
Edit `config.py` to modify Raman's personality:
```python
BOT_PERSONALITY = "your custom personality description with multi-language capabilities"
```

### Adding New Avatars
Simply add your images to the `images_` folder and they'll automatically appear as avatar options!

### Styling
The app uses custom CSS for the adorable pink theme. You can modify colors in `app.py` by changing the CSS variables.

## 🔧 Technical Details

- **Backend**: Python with SQLite for memory
- **Frontend**: Streamlit with custom CSS
- **AI**: OpenAI GPT-4 via OpenRouter
- **Database**: SQLite for conversation history
- **Images**: Pillow for image processing

## 💡 Features in Detail

### Memory System
- Stores all conversations in SQLite database
- Remembers user preferences and settings
- Provides context for more natural conversations
- Persistent across sessions

### Avatar System
- Automatically detects images in `images_` folder
- Supports multiple formats (JPG, PNG, GIF, etc.)
- Random avatar selection
- Custom avatar picker in sidebar

### Responsive Design
- Mobile-first approach
- Adaptive layout for all screen sizes
- Touch-friendly interface
- Optimized for both desktop and mobile

## 🎯 Usage Tips

1. **First Time**: Raman will ask for your name to personalize the experience
2. **Language**: Type in English or Hinglish - Raman will respond in the same style
3. **Avatar Selection**: Use the sidebar to choose your favorite avatar
4. **Conversation History**: All chats are automatically saved
5. **Settings**: Customize your experience in the sidebar

## 🔒 Privacy & Security

- All conversations are stored locally in SQLite
- No data is sent to external servers except for AI processing
- API key is kept secure in environment variables

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your OpenRouter API key is correct
2. **Images Not Showing**: Check that images are in the `images_` folder
3. **Database Issues**: Delete `chat_memory.db` to reset memory

### Getting Help

If you encounter any issues:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure your API key is valid

## 🎉 Enjoy Your Chat!

Raman is designed to be your perfect AI companion - smart, helpful, and always there for you. Have fun chatting in English or Hinglish! 🇮🇳

---

*Made with 🇮🇳 and lots of love for the most intelligent chatbot experience ever!*
