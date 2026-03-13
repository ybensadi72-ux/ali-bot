import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- البيانات التي استخرجتها أنت ---
# الصق هنا القيمة الطويلة التي نسختها من المتصفح (xman_t)
XMAN_T_COOKIE = "KoSqRkC+azCffzHCz/FfUwlZksMomuWFz7isGUjR6fwH42iM7bQIdbYFVGu48N8ZAq1ErTXraJcIKIQ1L/idOhWB2W1WIcUnawfEgcx6POpV81ReTj0Mwz3kK8Jp1yo2GdIHKyX0JwvvjBmYwDFRp/kW6drsvwo4ouJgjPNrLO3XQcGCvrs/czo76oQsJpiwbLypil2xa7p/taD2tQwlNclpPusRoFlfUSbY7L2StxjGpkC0sPshSN8B8ZQz99nR12esY52xdj9Z8v1/1YcQIrdCzGrMVyBRzsV926NVw3vo+3PiDdIdeDggZEIZsIObzag6L9d7n6M/Qb2HNFx7eMjNbEzAOJ3/SagLy1Q0Jy5A2QEYcVfxyKWAxl3wNQQjnkXSU3/MKYruiR476NI+HLYkoNYGdXkPAvmb8JZeHs28MhzU582KjfBite2Euh7aGiu3O3eSKN8SkbViOASlFHZWhuE6l+MmsPGEJ+e6QXO411/gv/fAGN7IGZhNclfOIUXF95lMpu1FjujtZ9ES6WyRCheo/S76RMOb+ybf6eJxbjk75NVHISN+h2bOqb14HJJeO39RWNaVDb2bC9I+NazTLH6g2utNxHxZODBssbS4HDB2IxjvGIjmjNGAHN4lrbtcUw1/wX+OAWXX/diWzDOl6rZQcaHGBaxQuVGEOJfCBMcenOQyUVbNSATo+HStuOs8K9vX78M="

BOT_TOKEN = "6529390402:AAHxlLXqrWiMNRqi6E0RXwk1S9GsMqfSAgc"
# ضع هنا رقم الـ Short Key الخاص بك (مثل EuV7EW0)
AFF_SHORT_KEY = "EuV7EW0" 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "aliexpress.com" in url:
        await update.message.reply_text("⏳ يتم التحويل باستخدام هويتك الخاصة...")
        
        # محاكاة المتصفح باستخدام الكوكي الخاصة بك
        headers = {
            'Cookie': f'xman_t={XMAN_T_COOKIE}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            # محاولة الوصول للرابط وتوقيعه
            res = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            final_url = res.url
            
            # استخراج رقم المنتج لبناء رابط الأفيليت
            product_id = re.search(r'item/(\d+)\.html', final_url)
            if product_id:
                pid = product_id.group(1)
                aff_link = f"https://s.click.aliexpress.com/deep_link.htm?aff_short_key={AFF_SHORT_KEY}&dl_target_url=https://www.aliexpress.com/item/{pid}.html"
                await update.message.reply_text(f"✅ تم التحويل بنجاح:\n\n{aff_link}")
            else:
                await update.message.reply_text("❌ لم أتمكن من استخراج رقم المنتج، تأكد أن الرابط لمنتج واحد.")
        except Exception as e:
            await update.message.reply_text(f"⚠️ حدث خطأ أثناء الاتصال: {str(e)}")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن باستخدام نظام الكوكيز الخاص بك...")
    app.run_polling()
