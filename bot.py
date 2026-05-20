import os
import telebot
import requests

# Securely read your Telegram Bot Token from Railway's variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "Welcome to Julia's AI Sanctuary! ⚡\n\n"
        "To generate a stunning cinematic image, type:\n"
        "`/imagine your prompt here`"
    )

@bot.message_handler(commands=['imagine'])
def generate_image(message):
    # This strips away the '/imagine ' part to grab your actual prompt
    prompt = message.text[9:].strip()
    
    if not prompt:
        bot.reply_to(message, "Please provide a prompt! Example: `/imagine a mechanical chrome skull, 8k`")
        return
    
    # Send a quick text back so you know the bot is working in the background
    status_message = bot.reply_to(message, "🎨 Creating your masterpiece... hold on a few seconds.")
    
    try:
        # We sanitize the prompt text so it safely works as a link URL
        sanitized_prompt = requests.utils.quote(prompt)
        image_url = f"https://image.pollinations.ai/p/{sanitized_prompt}?width=1024&height=1024&model=flux&enhance=true"
        
        # Download the live image data from the free cluster
        image_response = requests.get(image_url, timeout=45)
        
        if image_response.status_code == 200:
            # Deliver the gorgeous high-res picture directly into your chat
            bot.send_photo(message.chat.id, image_response.content, caption=f"✨ \"{prompt}\"")
            # Clear out the "Creating..." message to keep the chat looking flawless
            bot.delete_message(message.chat.id, status_message.message_id)
        else:
            bot.edit_message_text("❌ The engine is temporarily busy. Try hitting submit again!", message.chat.id, status_message.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ Connection error: {str(e)}", message.chat.id, status_message.message_id)

# Start the continuous background listener loop
if __name__ == "__main__":
    print("Your AI Bot is online and running flawlessly...")
    bot.infinity_polling()
  
