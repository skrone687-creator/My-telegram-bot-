import logging
import asyncio
from typing import Optional
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
# बोट सेटअप
API_TOKEN = '8955117111:AAGGqUdqe4AtpkAXlzfNQXb6UfC264EDT5g'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    # Row 1: Buy Now (Large)
    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text=" Buy Now",
            callback_data="menu_shop",
            style="danger"
        )
    ])

    # Row 2: Check Update & Add Balance
    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text=" Check Update",
            callback_data="menu_check_update",
            style="success"
        ),
        InlineKeyboardButton(
            text=" Add Balance",
            callback_data="menu_add_balance",
            style="primary"
        )
    ])

    # Row 3: My Profile + All History
    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text=" My Profile + All History",
            callback_data="menu_profile",
            style="success"
        )
    ])

    # Row 4: Refer And Earn & How To Use Bot
    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text=" Refer And Earn",
            callback_data="menu_refer",
            style="success"
        ),
        InlineKeyboardButton(
            text=" How To Use Bot",
            callback_data="menu_how_to",
            style="primary"
        )
    ])

    # Row 5: Support & Daily Gift
    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text=" Support",
            callback_data="menu_support",
            style="danger"
        ),
        InlineKeyboardButton(
            text=" Daily Gift",
            callback_data="menu_daily_gift",
            style="success"
        )
    ])

    return kb

# यहाँ आप अपने कमान्ड हैंडर्स जोड़ सकते हैं
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply(
        "🏪 SAHIL BHAI STORE 🔓\n\n🛍️ Buy Now : All Key Purchases &\ Instant Delivery\n🆙 Check Update : Check Setup Video And Update Apk\n💰 Add Balance : Deposit Balance &\ Secure Auto-Add Payment System\n🆔 My Profile + All History : Check Your Account Information + All History\n🔄 Refer And Earn : Share Refer Link &\ Earn Money\n❓ How To Use Bot : View Tutorial And Work This Bot\n🎧 Support : Bot Problem Fixed For Support Admin\n🎁 Daily Gift : Free Spin and win random balance daily. Only one spin every 24 hours.\n\n👇 Select an option from the menu below:",
        reply_markup=main_menu_kb()
    )

    await callback_query.answer()
    await callback_query.message.edit_text(
        "यहाँ हमारे प्रोडक्ट्स की लिस्ट है:",
        reply_markup=your_products_kb()
    )
@dp.callback_query(F.data == "menu_check_update")
async def process_check_update(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer()
        text = (
            "📢 **Follow our updates channel!** 📢\n\n"
            "🔗 [Click Here For Setup & Updates](https://t.me/sahilbhaiiallupdate)"
        )
        
        kb = InlineKeyboardMarkup(inline_keyboard=[])
        kb.add(
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data="menu_back",
                style="danger"
            )
        )
        
        await callback_query.message.edit_text(
            text=text,
            reply_markup=kb,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error processing update check: {e}")



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import qrcode
from io import BytesIO

# 1. Add Balance Menu Keyboard
def add_balance_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="₹100", callback_data="amt_100"),
        InlineKeyboardButton(text="₹200", callback_data="amt_200"),
        InlineKeyboardButton(text="₹500", callback_data="amt_500"),
        InlineKeyboardButton(text="₹1000", callback_data="amt_1000")
    )
    kb.add(InlineKeyboardButton(text="⌨️ TYPE CUSTOM AMOUNT", callback_data="amt_custom"))
    kb.add(InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="menu_back"))
    return kb

# 2. Handler for 'Add Balance' button
@dp.callback_query(F.data == "menu_add_balance")
async def process_add_balance(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "ADD FUNDS TO WALLET\n\nChoose a quick amount to add or type/use a custom one below:",
        reply_markup=add_balance_kb()
    )

# 3. Handler for amount selection (Generates QR)
@dp.callback_query(F.data.startswith('amt_'))
async def process_amount(callback_query: types.CallbackQuery):
    await callback_query.answer()
    amount = callback_query.data.split('_')[1]
    
    if amount == "custom":
        await callback_query.message.edit_text("Please enter the custom amount:")
        return

    # UPI QR Code Generation Logic
    upi_id = "7318748360@fam"
    payee_name = "Sahil"
    tx_ref = "TXN12345"
    
    upi_string = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR&tr={tx_ref}"
    
    img = qrcode.make(upi_string)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    await callback_query.message.answer_photo(
        photo=buf,
        caption=f"Scan & pay exactly ₹{amount} to add balance.",
        reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Verify Payment", callback_data="verify_pay"))
    )
# 1. Profile Dashboard Menu Keyboard
def profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="🔑 Key History", callback_data="key_history"),
        InlineKeyboardButton(text="💳 Deposit History", callback_data="deposit_history")
    )
    kb.add(InlineKeyboardButton(text="⬅️ Back to Main Terminal", callback_data="menu_back"))
    return kb

# 2. Handler for 'My Profile + All History' button
@dp.callback_query(F.data == "menu_profile")
async def process_profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    # यहाँ डेटाबेस से यूज़र की जानकारी निकालें
    user_id = callback_query.from_user.id
    account_id = user_id  # उदाहरण के लिए ID का उपयोग
    account_tier = "RESELLER" # उदाहरण के लिए टियर
    current_funds = "₹0.27" # उदाहरण के लिए बैलेंस
    active_referrals = 0 # उदाहरण के लिए रेफर्स
    
    profile_text = (
        f"👤 YOUR PROFILE DASHBOARD\n\n"
        f"🆔 Account ID: {account_id}\n"
        f"🌟 Account Tier: {account_tier}\n"
        f"💰 Current Funds: {current_funds}\n"
        f"👥 Active Referrals: {active_referrals} users\n\n"
        f"Select history filter panel below to view records."
    )
    
    await callback_query.message.edit_text(
        profile_text,
        reply_markup=profile_kb()
    )
@dp.callback_query(F.data == "menu_refer")
async def process_refer(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    referral_link = f"https://t.me/YOUR_BOT_USERNAME?start={callback_query.from_user.id}"
    
    await callback_query.message.edit_text(
        f"🔗 Refer And Earn!\n\n"
        f"अपने दोस्तों को आमंत्रित करें और पैसे कमाएँ।\n"
        f"आपका रेफरल लिंक: {referral_link}",
        reply_markup=main_menu_kb()
    )
@dp.callback_query(F.data == "menu_support")
async def process_support(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    # यहाँ अपना सपोर्ट यूजरनेम डालें
    support_username = "@SAHILXD78"
    await callback_query.message.edit_text(
        f"🎧 Support\n\n"
        f"अगर आपको कोई प्रॉब्लम है, तो आप हमें DM कर सकते हैं:\n"
        f"@{support_username}",
        reply_markup=main_menu_kb()
    )
import random

@dp.callback_query(F.data == "menu_daily_gift")
async def process_daily_gift(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    # ₹0 से ₹1 के बीच रैंडम अमाउंट
    gift_amount = round(random.uniform(0.0, 1.0), 2)
    
    await callback_query.message.edit_text(
        f"🎉 Daily Gift!\n\n"
        f"बधाई हो! आपको डेली गिफ्ट के रूप में\n"
        f"₹{gift_amount} मिले हैं।",
        reply_markup=main_menu_kb()
    )

  
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
