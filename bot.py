import sqlite3
import logging
import asyncio
from typing import Optional
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import qrcode
from aiogram.fsm.context import FSMContext
from io import BytesIO
from aiogram import types
from aiogram import F, Router, types
import aiohttp
def init_db():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()



products_db = {
    "155": "XYZ CHEATS APKMOD FF NONROOT",
    "153": "XYZ CHEATS PROXY APK SILENT FF NONROOT",
    "151": "ABCD PANEL FF NONROOT",
    "150": "DRIPCLIENT WIRE FF NONROOT ANDROID+IPHONE",
    "156": "RAPID CARROM POOL NONROOT ANDROID",
    "148": "SILENT CHEAT FF NONROOT PROXY",
    "149": "XRAG FF ROOT+NONROOT+IOS IPHONE+PC",
    "133": "AIM HACK FF",
    "138": "KOS 8 BALL POOL MOD+ROOT",
    "76": "KOS 8 BALL POOL VIRTUAL",
    "78": "SNAKE SOCCER STARS NONROOT ANDROID",
    "49": "BR MOD FF PC VERSION",
    "67": "BR MOD FF ROOT ANDROID",
}

# बोट सेटअप
API_TOKEN = '8765527795:AAFisjaHc8G0imEQ1FlpSxDS790E1FpiqFA'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router
async def send_payment_qr(call: types.CallbackQuery, amount: str):
 # यहाँ अपनी UPI ID डालें
 upi_id = "7318748360@fam"
 upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR"
 
 qr = qrcode.QRCode(version=1, box_size=10, border=4)
 qr.add_data(upi_url)
 qr.make(fit=True)
 img = qr.make_image(fill_color="black", back_color="white")
 
 buffer = BytesIO()
 img.save(buffer, format="PNG")
 buffer.seek(0)
 
 keyboard = InlineKeyboardMarkup(inline_keyboard=[
 [
 InlineKeyboardButton(text="Verify Payment", callback_data="verify_payment", style="success"),
 InlineKeyboardButton(text="Cancel Order", callback_data="cancel_order", style="danger")
 ]
 ])
 
 await call.message.answer_photo(photo=types.BufferedInputFile(buffer.getvalue(), filename="qr.png"), caption=caption, reply_markup=keyboard)
 await message.answer_photo(photo=types.BufferedInputFile(buffer.getvalue(), filename="qr.png"), caption=caption, reply_markup=keyboard)
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
            text="How To Use bot ",
            callback_data="how_to_bot",
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
    await message.answer(
        "<blockquote>🏪 SAHIL BHAI STORE 🔓</blockquote>\n"
        
        "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
        "┝  🛍️ Buy Now : All Key Purchase & Instant Delivery\n"
        "┝  📢 Check Update : Check Setup Video And Update Apk\n"
        "┝  🪙 Add Balance : Deposit Balance & Secure Auto-Add Payment System\n"
        "┝  🆔 My Profile + All History : Check Your Account Information + All History\n"
        "┝  👥 Refer And Earn : Share Refer Link & Earn Money\n"
        "┝  🎬 How To Use Bot : View Tutorial And Work This Bot\n"
        "┝  📨 Support : Bot Problem Fixed For Support Admin\n"
        "┝  🎁 Daily Gift : Free Spin and win random balance daily, Only one spin every 24 hours.",
        parse_mode="HTML",
        reply_markup=main_menu_kb(),
    )


    await callback_query.answer()
    await callback_query.message.edit_text(
        "यहाँ हमारे प्रोडक्ट्स की लिस्ट है:",
        reply_markup=your_products_kb()
    )
def update_kb():
    button = InlineKeyboardButton(text="Back", callback_data="menu_back")
    kb = InlineKeyboardMarkup(inline_keyboard=[[button]])
    kb.inline_keyboard[0][0].style = "danger"
    return kb

@dp.callback_query(F.data == "menu_check_update")
async def process_check_update(call: types.CallbackQuery):
    await call.answer()
    print("Check Update button pressed")
    update_text = (
        "<blockquote>📢 Follow our updates channel:</blockquote>\n"
        "🔗 <a href='https://t.me/Sahilbhaiallupdate'><b> Click Here For Setup & Updates</b></a>"
    )
    
    await call.message.edit_text(
        text=update_text,
        parse_mode="HTML",
        reply_markup=update_kb()
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
@dp.callback_query_handler(F.data == "menu_profile")
async def process_profile(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    user_id = callback_query.from_user.id
    
    # यहाँ आपको डेटाबेस से यूज़र की डिटेल्स फेच करनी होगी
    account_id = user_id
    account_tier = "RESELLER"
    current_funds = "0.27"
    active_referrals = "0"
    
    profile_text = (
        f"👤 YOUR PROFILE DASHBOARD 👤\n\n"
        f"🆔 Account ID: {account_id}\n"
        f"💎 Account Tier: {account_tier}\n"
        f"💰 Current Funds: ₹{current_funds}\n"
        f"👥 Active Referrals: {active_referrals} users\n\n"
        f"Select history filter panel below to view records."
    )
    
    # टेक्स्ट को HTML <pre> टैग्स में लपेटना
    formatted_text = f"<pre>{profile_text}</pre>"
    
    keyboard = [
        [
            InlineKeyboardButton("🔑 Key History", callback_data="key_history", style="success"),
            InlineKeyboardButton("💳 Deposit History", callback_data="deposit_history", style="success")
        ],
        [
            InlineKeyboardButton("⬅️ Back to Main Terminal", callback_data="main_menu", style="danger")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await callback_query.message.edit_text(
        text=formatted_text, 
        reply_markup=reply_markup,
        parse_mode="HTML"
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
from aiogram import F, Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()


def support_kb():
 button = InlineKeyboardButton(text="Back", callback_data="menu_back")
 kb = InlineKeyboardMarkup(inline_keyboard=[[button]])
 kb.inline_keyboard[0][0].style = "danger"
 return kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def add_balance_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[[]])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="₹100", callback_data="add_100", style="success"),
        InlineKeyboardButton(text="₹200", callback_data="add_200", style="success"),
    ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="₹500", callback_data="add_500", style="success"),
        InlineKeyboardButton(text="₹1000", callback_data="add_1000", style="success"),
    ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="TYPE CUSTOM AMOUNT", callback_data="custom_amount", style="success"),
    ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="Back to Menu", callback_data="menu_back", style="danger"),
    ])
    return kb

@router.callback_query(F.data == "menu_support")
async def menu_support(call: types.CallbackQuery):
 await call.message.edit_text(
 text="<blockquote>📨Contact admin support:</blockquote>\n\n📨@sahilxd78",
 parse_mode="HTML",
 reply_markup=support_kb(),
 )
 await call.answer()
@router.callback_query(F.data == "menu_back")
async def process_menu_back(call: types.CallbackQuery):
    await call.message.edit_text(
    f"<blockquote><b>🏪 SAHIL BHAI STORE 🔒</b>\n</blockquote>"
        
    f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
    f"┝🛍 Buy Now : All Key Purchase & Instant Delivery\n"
    f"┝📢 Check Update : Check Setup Video And Update Apk\n"
    f"┝🪙 Add Balance : Deposit Balance & Secure Auto-Add Payment System\n"
    f"┝🆔 My Profile + All History : Check Your Account Information + All History\n"
    f"┝👥 Refer And Earn : Share Refer Link & Earn Money\n"
    f"┝🎬 How To Use Bot : View Tutorial And Work This Bot\n"
    f"┝📨 Support : Bot Problem Fixed For Support Admin\n"
    f"┝🎁 Daily Gift : Free Spin and win random balance daily, Only one spin every 24 hours.",
    parse_mode="HTML",
    reply_markup=main_menu_kb(),
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
@router.callback_query(F.data == "menu_add_balance")
async def menu_add_balance(call: types.CallbackQuery):
    text = (
        "<blockquote>"
        "💰 <b>ADD FUNDS TO WALLET</b> "
        "</blockquote>\n\n"
        "Choose a quick amount to add or type/use a custom one below.\n\n"
        "<blockquote>"
        "🚀 <i>Predefined amounts are faster to process!</i>"
        "</blockquote>"
    )
    await call.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=add_balance_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "how_to_bot")
async def process_how_to_use(call: types.CallbackQuery):
    text = (
        "<blockquote>❗ How to use this bot:</blockquote>\n\n"
        "• Add balance via Sahil bhai Secure QR System or Binance Pay\n"
        "• Tap Buy Now and pick your desired product\n"
        "• Key is delivered instantly to this chat screen\n"
        "• Browse plans and checkout seamlessly"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text="🎬 VIEW TUTORIAL VIDEO ", url="https://t.me/sahil_bhai_69/6", style="success")],
 [InlineKeyboardButton(text="« Back", callback_data="menu_back", style="danger")]
])
    await call.message.edit_text(text=text, parse_mode="HTML", reply_markup=keyboard)
    await call.answer()


@router.message(F.text.startswith("/buy_"))
async def process_buy(message: types.Message):
    product_id = message.text.split("_")[1]

    api_url = "https://bantibhaiya.to/api/reseller_v1.php"
    payload = {
        "api_key": "c269687cb9bd332ca5f930bdb9a4d839",
        "action": "Buy",
        "product_id": product_id,
        "duration": "1",
        "android_id": "0b9b969bc2e7997b",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data=payload) as response:
            if response.status == 200:
                data = await response.json()
                key = data.get("key")
                await message.reply(f"आपकी प्रोडक्ट की डिलीवरी: {key}")
            else:
                await message.reply("प्रोडक्ट खरीदने में समस्या आई।")
# PAY UPI handler to generate QR
@router.callback_query(F.data == "pay_upi")
async def process_pay_upi(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    amount = user_data.get("amount")
    
    # Apni UPI ID yahan dein
    up_id = "7318748360@fam"
    upi_url = f"upi://pay?pa={up_id}&am={amount}&cu=INR"
    
    # QR Generation logic
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    caption = (
        "Scan & transfer exactly "
        f"<b>₹{amount}.00</b> via your UPI app terminal.\n"
        "Tap verify below after completing the core transaction transfer."
    )
    
    await call.message.answer_photo(
        photo=types.BufferedInputFile(buffer.getvalue(), filename="qr.png"),
        caption=caption,
        parse_mode="HTML",
        reply_markup=verify_kb(), # Yahan apka verify button keyboard hai
    )
    await call.answer()
@router.callback_query(F.data == "add_100")
async def process_add_100(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(amount="100")
    text = "<blockquote><b>SELECT GATEWAY MODE</b></blockquote>\n\nDeposit Amount: 💰 <b>₹100.00</b>\n\n<i>Cancel Request</i>"
    await call.message.edit_text(text=text, parse_mode="HTML", reply_markup=gateway_kb())
    await call.answer()

@router.callback_query(F.data == "add_200")
async def process_add_200(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(amount="200")
    text = "<blockquote><b>SELECT GATEWAY MODE</b></blockquote>\n\nDeposit Amount: 💰 <b>₹200.00</b>\n\n<i>Cancel Request</i>"
    await call.message.edit_text(text=text, parse_mode="HTML", reply_markup=gateway_kb())
    await call.answer()

@router.callback_query(F.data == "add_500")
async def process_add_500(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(amount="500")
    text = "<blockquote><b>SELECT GATEWAY MODE</b></blockquote>\n\nDeposit Amount: 💰 <b>₹500.00</b>\n\n<i>Cancel Request</i>"
    await call.message.edit_text(text=text, parse_mode="HTML", reply_markup=gateway_kb())
    await call.answer()

@router.callback_query(F.data == "add_1000")
async def process_add_1000(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(amount="1000")
    text = "<blockquote><b>SELECT GATEWAY MODE</b></blockquote>\n\nDeposit Amount: 💰 <b>₹1000.00</b>\n\n<i>Cancel Request</i>"
    await call.message.edit_text(text=text, parse_mode="HTML", reply_markup=gateway_kb())
    await call.answer()

from aiogram import types
from aiogram.filters import Command
import sqlite3

ADMIN_ID = 8395533259  # यहाँ अपनी Telegram ID डालें


@router.message(Command("add_product"))
async def add_product(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        await message.reply("Usage: /add_product <id> <name> <price>")
        return
    _, prod_id, name, price = args
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
            (prod_id, name, price),
        )
        conn.commit()
        await message.reply(f"Product {name} added successfully!")
    except sqlite3.IntegrityError:
        await message.reply("Product ID already exists.")
    finally:
        conn.close()
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@router.callback_query(F.data == "main_menu")
async def process_main_menu(call: types.CallbackQuery):

    # यहाँ आपका मेन मेन्यू कीबोर्ड कोड होना चाहिए
    await call.message.edit_text(
    text="""<blockquote>🏪  SAHIL BHAI STORE 🔓</blockquote>
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

┝ 🛍️ Buy Now : All Key Purchase & Instant Delivery
┝ ⏩ Check Update : Check Setup Video And Update Apk
┝ 🔂 Add Balance : Deposit Balance & Secure Auto-Add Payment System
┝ 🆔 My Profile + All History : Check Your Account Information + All History
┝ 👥 Refer And Earn : Share Refer Link & Earn Money
┝ 🔙 How To Use Bot : View Tutorial And Work This Bot
┝ 🚀 Upgrade To Reseller : Become a reseller and get discount keys at low prices
┝ 🎧 Support : Bot Problem Fixed For Support Admin
┝ 📅 Daily Gift : Free Spin and win random balance daily, Only one spin every 24 hours.""",
    parse_mode="HTML",
    reply_markup=main_menu_kb(),
)


@router.callback_query(F.data == "menu_shop")
async def process_menu_shop(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="DRIP CLIENT APK-MOD",
                    callback_data="drip_client",
                    style="success",
                )
            ],
            [
                InlineKeyboardButton(
                    text="PRIME HOOK APK-MOD",
                    callback_data="prime_hook",
                    style="success",
                )
            ],
            [
                InlineKeyboardButton(
                    text="« Back", callback_data="main_menu", style="danger"
                )
            ],
        ]
    )

    await call.message.edit_text(
        "<blockquote>🛍️ Choose a product from the list below:</blockquote>",
        reply_markup=keyboard,
        parse_mode="HTML",
    )



if __name__ == '__main__':
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))
    init_db()
