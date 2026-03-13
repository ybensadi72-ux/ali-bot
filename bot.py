import hashlib, time, requests, json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# CONFIG
API_KEY = "507938"
API_SECRET = "WNt3F9cDPR74HnOVFbAl0ueatQquibix"
BOT_TOKEN = "6529390402:AAHfTiJrKdMSH544cWB5Ck1Eez72aE5TPOE"

def get_link(url):
    endpoint = "https://eco.aliexpress.com/router/rest"
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
    params = {
        'app_key': API_KEY,
        'format': 'json',
        'method': 'aliexpress.affiliate.link.generate',
        'sign_method': 'md5',
        'timestamp': ts,
        'v': '2.0',
        'promotion_link_type': '0',
        'source_values': url
    }
    
    # SIGNATURE
    query = API_SECRET
    for k in sorted(params):
        query += k + str(params[k])
    query += API_SECRET
    params['sign'] = hashlib.md5(query.encode('utf-8')).hexdigest().upper()
    
    try:
        # Added realistic headers to bypass system blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        r = requests.post(endpoint, data=params, headers=headers, timeout=15)
        
        print(f"RAW: {r.text}") # Check this in terminal
        
        data = r.json()
        return data['aliexpress_affiliate_link_generate_response']['resp_result']['result']['promotion_links']['promotion_link'][0]['promotion_link']
    except Exception as e:
        print(f"LOG: {e}")
        return None

async def handle(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if "aliexpress.com" in u.message.text:
        res = get_link(u.message.text)
        if res:
            await u.message.reply_text(res)
        else:
            # If still fails, it's a network block
            await u.message.reply_text("CONNECTION REFUSED")

if __name__ == '__main__':
    print("RUNNING FINAL TEST...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
