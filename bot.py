import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# الصق الـ Cookie الخاصة بك هنا
XMAN_T_COOKIE = "KoSqRkC+azCffzHCz/FfUwlZksMomuWFz7isGUjR6fwH42iM7bQIdbYFVGu48N8ZAq1ErTXraJcIKIQ1L/idOhWB2W1WIcUnawfEgcx6POpV81ReTj0Mwz3kK8Jp1yo2GdIHKyX0JwvvjBmYwDFRp/kW6drsvwo4ouJgjPNrLO3XQcGCvrs/czo76oQsJpiwbLypil2xa7p/taD2tQwlNclpPusRoFlfUSbY7L2StxjGpkC0sPshSN8B8ZQz99nR12esY52xdj9Z8v1/1YcQIrdCzGrMVyBRzsV926NVw3vo+3PiDdIdeDggZEIZsIObzag6L9d7n6M/Qb2HNFx7eMjNbEzAOJ3/SagLy1Q0Jy5A2QEYcVfxyKWAxl3wNQQjnkXSU3/MKYruiR476NI+HLYkoNYGdXkPAvmb8JZeHs28MhzU582KjfBite2Euh7aGiu3O3eSKN8SkbViOASlFHZWhuE6l+MmsPGEJ+e6QXO411/gv/fAGN7IGZhNclfOIUXF95lMpu1FjujtZ9ES6WyRCheo/S76RMOb+ybf6eJxbjk75NVHISN+h2bOqb14HJJeO39RWNaVDb2bC9I+NazTLH6g2utNxHxZODBssbS4HDB2IxjvGIjmjNGAHN4lrbtcUw1/wX+OAWXX/diWzDOl6rZQcaHGBaxQuVGEOJfCBMcenOQyUVbNSATo+HStuOs8K9vX78M="

BOT_TOKEN = "6529390402:AAHxlLXqrWiMNRqi6E0RXwk1S9GsMqfSAgc"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_url = update.message.text
    if "aliexpress.com" in user_url:
        await update.message.reply_text("⏳ جاري توليد رابط أفيليت رسمي...")
        
        # الرابط الخاص بـ AliExpress Link Generator API (الداخلي)
        api_url = "https://portals.aliexpress.com/affi/portal/web/link_generator.htm"
        
        headers = {
            'Cookie': f'xman_t={XMAN_T_COOKIE}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://portals.aliexpress.com/affi/portal/web/link_generator.htm'
        }
        
        # إرسال طلب للحصول على الرابط الحقيقي
        params = {
            'memo': user_url,
            'trackingId': 'default'
        }
        
        try:
            # هنا نقوم بمحاكاة الضغط على زر "Get Tracking Link"
            response = requests.get(api_url, headers=headers, params=params, timeout=15)
            
            # البحث عن الرابط المختصر (s.click) في استجابة الصفحة
            short_link = re.search(r'https://s.click.aliexpress.com/e/[a-zA-Z0-9]+', response.text)
            
            if short_link:
                await update.message.reply_text(f"✅ تم التوليد بنجاح:\n\n{short_link.group(0)}")
            else:
                await update.message.reply_text("❌ فشل التوليد. قد تحتاج لتحديث الـ Cookie من المتصفح كما في الفيديو.")
        except Exception as e:
            await update.message.reply_text(f"⚠️ خطأ: {str(e)}")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
