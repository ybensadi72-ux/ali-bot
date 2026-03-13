import requests
import re
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- [إعدادات الهوية - COOKIE] ---
XMAN_T_COOKIE = "KoSqRkC+azCffzHCz/FfUwlZksMomuWFz7isGUjR6fwH42iM7bQIdbYFVGu48N8ZAq1ErTXraJcIKIQ1L/idOhWB2W1WIcUnawfEgcx6POpV81ReTj0Mwz3kK8Jp1yo2GdIHKyX0JwvvjBmYwDFRp/kW6drsvwo4ouJgjPNrLO3XQcGCvrs/czo76oQsJpiwbLypil2xa7p/taD2tQwlNclpPusRoFlfUSbY7L2StxjGpkC0sPshSN8B8ZQz99nR12esY52xdj9Z8v1/1YcQIrdCzGrMVyBRzsV926NVw3vo+3PiDdIdeDggZEIZsIObzag6L9d7n6M/Qb2HNFx7eMjNbEzAOJ3/SagLy1Q0Jy5A2QEYcVfxyKWAxl3wNQQjnkXSU3/MKYruiR476NI+HLYkoNYGdXkPAvmb8JZeHs28MhzU582KjfBite2Euh7aGiu3O3eSKN8SkbViOASlFHZWhuE6l+MmsPGEJ+e6QXO411/gv/fAGN7IGZhNclfOIUXF95lMpu1FjujtZ9ES6WyRCheo/S76RMOb+ybf6eJxbjk75NVHISN+h2bOqb14HJJeO39RWNaVDb2bC9I+NazTLH6g2utNxHxZODBssbS4HDB2IxjvGIjmjNGAHN4lrbtcUw1/wX+OAWXX/diWzDOl6rZQcaHGBaxQuVGEOJfCBMcenOQyUVbNSATo+HStuOs8K9vX78M="

AFF_SHORT_KEY = "EuV7EW0" 
BOT_TOKEN = "6529390402:AAHxlLXqrWiMNRqi6E0RXwk1S9GsMqfSAgc"

async def convert_via_cookie(url):
    headers = {
        'Cookie': f'xman_t={XMAN_T_COOKIE}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        res = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        final_url = res.url
        item_id = re.search(r'item/(\d+)\.html', final_url)
        if item_id:
            pid = item_id.group(1)
            # التعديل الجديد هنا لإضافة منصة الـ API والتوقيع
            return f"https://s.click.aliexpress.com/deep_link.htm?aff_short_key={AFF_SHORT_KEY}&dl_target_url=https://www.aliexpress.com/item/{pid}.html?&aff_platform=api-new&sk={AFF_SHORT_KEY}"
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    url_match = re.search(r'(https?://\S+aliexpress\S+)', user_msg)
    
    if url_match:
        original_url = url_match.group(1)
        wait_msg = await update.message.reply_text("⏳ جاري التحويل بالنظام المطور...")
        
        # محاولة التحويل السريع أولاً مع التوقيع الجديد
        item_id_quick = re.search(r'item/(\d+)\.html', original_url)
        
        if item_id_quick:
            pid = item_id_quick.group(1)
            final_link = f"https://s.click.aliexpress.com/deep_link.htm?aff_short_key={AFF_SHORT_KEY}&dl_target_url=https://www.aliexpress.com/item/{pid}.html?&aff_platform=api-new&sk={AFF_SHORT_KEY}"
            await wait_msg.edit_text(f"✅ تم التحويل بنجاح:\n\n{final_link}")
        else:
            final_link = await convert_via_cookie(original_url)
            if final_link:
                await wait_msg.edit_text(f"✅ تم التحويل بنظام الهوية:\n\n{final_link}")
            else:
                await wait_msg.edit_text("❌ فشل التحويل. الرابط غير مدعوم.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
