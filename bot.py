import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# بيانات الهوية الخاصة بك
XMAN_T = "KoSqRkC+azCffzHCz/FfUwlZksMomuWFz7isGUjR6fwH42iM7bQIdbYFVGu48N8ZAq1ErTXraJcIKIQ1L/idOhWB2W1WIcUnawfEgcx6POpV81ReTj0Mwz3kK8Jp1yo2GdIHKyX0JwvvjBmYwDFRp/kW6drsvwo4ouJgjPNrLO3XQcGCvrs/czo76oQsJpiwbLypil2xa7p/taD2tQwlNclpPusRoFlfUSbY7L2StxjGpkC0sPshSN8B8ZQz99nR12esY52xdj9Z8v1/1YcQIrdCzGrMVyBRzsV926NVw3vo+3PiDdIdeDggZEIZsIObzag6L9d7n6M/Qb2HNFx7eMjNbEzAOJ3/SagLy1Q0Jy5A2QEYcVfxyKWAxl3wNQQjnkXSU3/MKYruiR476NI+HLYkoNYGdXkPAvmb8JZeHs28MhzU582KjfBite2Euh7aGiu3O3eSKN8SkbViOASlFHZWhuE6l+MmsPGEJ+e6QXO411/gv/fAGN7IGZhNclfOIUXF95lMpu1FjujtZ9ES6WyRCheo/S76RMOb+ybf6eJxbjk75NVHISN+h2bOqb14HJJeO39RWNaVDb2bC9I+NazTLH6g2utNxHxZODBssbS4HDB2IxjvGIjmjNGAHN4lrbtcUw1/wX+OAWXX/diWzDOl6rZQcaHGBaxQuVGEOJfCBMcenOQyUVbNSATo+HStuOs8K9vX78M="
XMAN_F = "N9ZQqKe0Jf/RW5bZNafyxOtEbJR6GmzkJH9eD6OE0QmSmbM1hE31apEPg/ODMIJzhSHjtq9sI5AzpmkmOMs5X1xuAy8oldOuu/Xwun593Nin+13PzwbOAyfHCM2I9OUkE0eoaAMwVNo8LALUJO4owZ7bBdJs47TdMdjJHbVy5ww0NLkZTA+aVmZysCPeHNncNf4sB4F5elOiEUlPyayGTg0Atjv6vPUDsaRcFK68oNTjb4aScmmGCl0fvfKdPUbGQ/5AYxovwU2+LZYeNJuHJxrAvuAiHb28th92u9MEaKIhBBlqqL2QsuCMiF1FqN9hviTmNzxmRR04670gYPQxDJ+oieqvihzOZPUNr8E6KIzntmIBn7LYnJ+NG5C5JAWym6/abchGanWU1Hn8TsUqgjLvxX093sAOnJlWaFIHfmKAoeleXb558A=="
SESSION_ID = "7DOE7EB1C0E7A45B2C14382A9E1E981C"
AFF_SHORT_KEY = "EuV7EW0"
BOT_TOKEN = "6529390402:AAHxlLXqrWiMNRqi6E0RXwk1S9GsMqfSAgc"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_url = update.message.text
    if "aliexpress.com" in user_url:
        status_msg = await update.message.reply_text("🔄 جاري فك تشفير الرابط وتحويله...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': f'xman_t={XMAN_T}; xman_f={XMAN_F}; JSESSIONID={SESSION_ID}'
        }

        try:
            # الخطوة 1: فك الرابط المختصر لمعرفة الرابط الحقيقي للمنتج
            res = requests.get(user_url, headers=headers, allow_redirects=True, timeout=10)
            final_url = res.url
            
            # الخطوة 2: البحث عن رقم المنتج (Item ID)
            item_id_match = re.search(r'item/(\d+)\.html', final_url)
            
            if item_id_match:
                product_id = item_id_match.group(1)
                # الخطوة 3: بناء الرابط المطور الذي يفتح التطبيق مباشرة
                aff_link = f"https://s.click.aliexpress.com/deep_link.htm?aff_short_key={AFF_SHORT_KEY}&dl_target_url=https://www.aliexpress.com/item/{product_id}.html?&aff_platform=api-new&sk={AFF_SHORT_KEY}"
                
                await status_msg.edit_text(f"✅ تم التحويل بنجاح:\n\n{aff_link}")
            else:
                await status_msg.edit_text("❌ عذراً، لم أجد رقم منتج في هذا الرابط.")
                
        except Exception as e:
            await status_msg.edit_text(f"⚠️ خطأ: {str(e)}")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
