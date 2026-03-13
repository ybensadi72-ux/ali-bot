import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- [بيانات الهوية الاحترافية] ---
XMAN_T = "KoSqRkC+azCffzHCz/FfUwlZksMomuWFz7isGUjR6fwH42iM7bQIdbYFVGu48N8ZAq1ErTXraJcIKIQ1L/idOhWB2W1WIcUnawfEgcx6POpV81ReTj0Mwz3kK8Jp1yo2GdIHKyX0JwvvjBmYwDFRp/kW6drsvwo4ouJgjPNrLO3XQcGCvrs/czo76oQsJpiwbLypil2xa7p/taD2tQwlNclpPusRoFlfUSbY7L2StxjGpkC0sPshSN8B8ZQz99nR12esY52xdj9Z8v1/1YcQIrdCzGrMVyBRzsV926NVw3vo+3PiDdIdeDggZEIZsIObzag6L9d7n6M/Qb2HNFx7eMjNbEzAOJ3/SagLy1Q0Jy5A2QEYcVfxyKWAxl3wNQQjnkXSU3/MKYruiR476NI+HLYkoNYGdXkPAvmb8JZeHs28MhzU582KjfBite2Euh7aGiu3O3eSKN8SkbViOASlFHZWhuE6l+MmsPGEJ+e6QXO411/gv/fAGN7IGZhNclfOIUXF95lMpu1FjujtZ9ES6WyRCheo/S76RMOb+ybf6eJxbjk75NVHISN+h2bOqb14HJJeO39RWNaVDb2bC9I+NazTLH6g2utNxHxZODBssbS4HDB2IxjvGIjmjNGAHN4lrbtcUw1/wX+OAWXX/diWzDOl6rZQcaHGBaxQuVGEOJfCBMcenOQyUVbNSATo+HStuOs8K9vX78M="
XMAN_F = "N9ZQqKe0Jf/RW5bZNafyxOtEbJR6GmzkJH9eD6OE0QmSmbM1hE31apEPg/ODMIJzhSHjtq9sI5AzpmkmOMs5X1xuAy8oldOuu/Xwun593Nin+13PzwbOAyfHCM2I9OUkE0eoaAMwVNo8LALUJO4owZ7bBdJs47TdMdjJHbVy5ww0NLkZTA+aVmZysCPeHNncNf4sB4F5elOiEUlPyayGTg0Atjv6vPUDsaRcFK68oNTjb4aScmmGCl0fvfKdPUbGQ/5AYxovwU2+LZYeNJuHJxrAvuAiHb28th92u9MEaKIhBBlqqL2QsuCMiF1FqN9hviTmNzxmRR04670gYPQxDJ+oieqvihzOZPUNr8E6KIzntmIBn7LYnJ+NG5C5JAWym6/abchGanWU1Hn8TsUqgjLvxX093sAOnJlWaFIHfmKAoeleXb558A=="
SESSION_ID = "7DOE7EB1C0E7A45B2C14382A9E1E981C"

BOT_TOKEN = "6529390402:AAHxlLXqrWiMNRqi6E0RXwk1S9GsMqfSAgc"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_url = update.message.text
    if "aliexpress.com" in user_url:
        status_msg = await update.message.reply_text("🔎 يتم الآن استخراج الرابط الرسمي الموثق...")
        
        # تجهيز الكوكيز لمحاكاة المتصفح
        cookies = {
            'xman_t': XMAN_T,
            'xman_f': XMAN_F,
            'JSESSIONID': SESSION_ID,
            'language': 'en_US'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://portals.aliexpress.com/affi/portal/web/link_generator.htm',
            'Origin': 'https://portals.aliexpress.com'
        }

        try:
            # إرسال طلب التوليد الرسمي
            gen_api = "https://portals.aliexpress.com/affi/portal/web/link_generator.htm"
            data = {'memo': user_url, 'trackingId': 'default'}
            
            response = requests.post(gen_api, cookies=cookies, headers=headers, data=data, timeout=15)
            
            # محاولة العثور على رابط s.click الرسمي في رد الصفحة
            official_link = re.search(r'https://s.click.aliexpress.com/e/[a-zA-Z0-9]+', response.text)
            
            if official_link:
                await status_msg.edit_text(f"✅ تم التوليد بنجاح (رابط رسمي):\n\n{official_link.group(0)}")
            else:
                # إذا فشل السحب الرسمي، نستخدم البناء الذكي كخيار أمان
                item_id = re.search(r'item/(\d+)\.html', user_url)
                if item_id:
                    backup = f"https://s.click.aliexpress.com/deep_link.htm?aff_short_key=EuV7EW0&dl_target_url=https://www.aliexpress.com/item/{item_id.group(1)}.html?&aff_platform=api-new"
                    await status_msg.edit_text(f"⚠️ تعذر السحب الرسمي، إليك الرابط المطور:\n\n{backup}")
                else:
                    await status_msg.edit_text("❌ الرابط غير مدعوم، تأكد من نسخه بشكل صحيح.")
                    
        except Exception as e:
            await status_msg.edit_text(f"⚠️ خطأ أثناء المعالجة: {str(e)}")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت الاحترافي يعمل الآن...")
    app.run_polling()
