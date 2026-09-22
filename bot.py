import sqlite3
import logging
import datetime
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
    "62": "DRIPCLIENT FF NONROOT",
    "54": "PATO TEAM FF ALL",
    "48": "PRIME HOOK FF NONROOT",
    "150": "DRIPCLIENT ",
    "156": "RAPID CARR ",
    "148": "SILENT CHE ",
    "149": "XRAG FF ROO",
    "133": "AIM HACK FF",
    "138": "KOS 8 BALL ",
    "76": "KOS 8 B",
    "78": "SNAKE SOCCE",
    "49": "BR M",
    "67": "BR MOD ",
}
plans_db = {
    "62": [{"plan_name": "1 HOURS", "price": 15.00}, {"plan_name": "3 HOURS", "price": 30.00}],
    "54": [{"plan_name": "1 DAYS", "price": 70.00}, {"plan_name": "3 DAYS", "price": 150.00}],
    "48": [{"plan_name": "1 HOURS", "price": 20.00}, {"plan_name": "12 HOURS", "price": 110.00}],
    "150": [{"plan_name": "7 DAYS", "price": 200.00}, {"plan_name": "30 DAYS", "price": 500.00}],
    "156": [{"plan_name": "1 HOURS", "price": 10.00}, {"plan_name": "6 HOURS", "price": 40.00}],
    "148": [{"plan_name": "3 DAYS", "price": 180.00}, {"plan_name": "7 DAYS", "price": 300.00}],
    "149": [{"plan_name": "12 HOURS", "price": 90.00}, {"plan_name": "1 DAYS", "price": 150.00}],
    "133": [{"plan_name": "1 HOURS", "price": 25.00}, {"plan_name": "6 HOURS", "price": 75.00}],
    "138": [{"plan_name": "1 DAYS", "price": 50.00}, {"plan_name": "7 DAYS", "price": 250.00}],
    "76": [{"plan_name": "12 HOURS", "price": 60.00}, {"plan_name": "3 DAYS", "price": 200.00}],
    "78": [{"plan_name": "1 HOURS", "price": 5.00}, {"plan_name": "1 DAYS", "price": 30.00}],
    "49": [{"plan_name": "6 HOURS", "price": 50.00}, {"plan_name": "7 DAYS", "price": 280.00}],
    "67": [{"plan_name": "1 DAYS", "price": 80.00}, {"plan_name": "30 DAYS", "price": 600.00}],
}

# बोट सेटअप
API_TOKEN = '8899833892:AAGoffSxzSv9tbMnye5cHl8RaweKFg-i1Dw'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
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
     "<blockquote><b>🏪 SAHIL BHAI STORE 🔓</b></blockquote>\n\n"
     "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
     "┝🛍️ Buy Now : All Key Purchase & Instant Delivery\n"
     "┝📢 Check Update : Check Setup Video And Update Apk\n"
     "┝🪙 Add Balance : Deposit Balance & Secure Auto-Add Payment System\n"
     "┝🆔 My Profile + All History : Check Your Account Information + All History\n"
     "┝👥 Refer And Earn : Share Refer Link & Earn Money\n"
     "┝🎬  How To Use Bot : View Tutorial And Work This Bot\n"
     "┝📨 Support : Bot Problem Fixed For Support Admin\n"
     "┝🎁 Daily Gift : Free Spin and win random balance daily, Only one spin every 24 hours.\n\n"
     "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
     "<blockquote>💰 Your Balance:🪙₹0.00</blockquote>\n\n"  
     "<i>👇 Select an option from the menu below:</i>",
     parse_mode="HTML",
     reply_markup=main_menu_kb(),
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
@dp.callback_query(F.data.startswith("amount_"))
async def process_amount(callback_query: types.CallbackQuery):
    amount = callback_query.data.split("_")[1]
    print(callback_query.data)
    text = (
        f"<blockquote><b>💸SELECT GATEWAY MODE</b></blockquote>\n\n"
        f" Deposit Amount: 🪙₹{amount}.00"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="PAY UPI", callback_data=f"pay_upi_{amount}", style="success")],
        [InlineKeyboardButton(text="Cancel Request", callback_data="main_menu", style="danger")]
    ])
    await callback_query.message.edit_text(text=text, parse_mode="HTML", reply_markup=keyboard)


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
    
    user_id = callback_query.from_user.id
    
    account_id = user_id
    account_tier = "RESELLER"
    current_funds = "$0.27"
    active_referrals = "0"
    
    profile_text = (
    "<blockquote>👤 YOUR PROFILE DASHBOARD 👤</blockquote>\n\n"
    f"<blockquote>🆔 Account ID: <code>{account_id}</code></blockquote>\n"
    "<blockquote>💎 Account Tier: USER</blockquote>\n"
    f"<blockquote>💰 Current Funds: {current_funds}</blockquote>\n"
    f"<blockquote>👥 Active Referrals: {active_referrals} users</blockquote>\n\n"
    "Select history filter panel below to view records."
)

    keyboard = [
        [
            types.InlineKeyboardButton(text=" Key History", callback_data="key_history", style="success"),
            types.InlineKeyboardButton(text=" Deposit History", callback_data="deposit_history", style="success"),
        ],
        [
            types.InlineKeyboardButton(text=" Back to Main Terminal", callback_data="menu_back", style="danger"),
        ]
    ]
    
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback_query.message.edit_text(
        text=profile_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
router = Router()    

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@router.callback_query(F.data == "menu_refer")
async def refer_and_earn(call: types.CallbackQuery):
    user_id = call.from_user.id
    bot_username = "sahil_bhai_store_kbot"
    referral_link = f"https://t.me/{bot_username}?start=ref{user_id}"

    message_text = (
    f"<blockquote>🔗 Share your referral link</blockquote>\n\n"    
    f"<code>{referral_link}</code>\n\n"
    f"┝  You earn 1% Commission whenever your referred friends purchase any plan!\n"
    f"┝  Total referrals: 0"
)

    keyboard = InlineKeyboardMarkup(
 inline_keyboard=[
 [
 InlineKeyboardButton(
 text="Back", callback_data="menu_back", style="danger"
 )
 ]
 ]
)

    await call.message.edit_text(
    text=message_text, reply_markup=keyboard, parse_mode="HTML"
)

def support_kb():
 button = InlineKeyboardButton(text="Back", callback_data="menu_back")
 kb = InlineKeyboardMarkup(inline_keyboard=[[button]])
 kb.inline_keyboard[0][0].style = "danger"
 return kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def add_balance_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[[]])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="₹100", callback_data="amount_100", style="success"),
        InlineKeyboardButton(text="₹200", callback_data="amount_200", style="success"),
    ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="₹500", callback_data="amount_500", style="success"),
        InlineKeyboardButton(text="₹1000", callback_data="amount_1000", style="success"),
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
 text="<blockquote>📨Contact admin support:</blockquote>\n📨@sahilxd78",
 parse_mode="HTML",
 reply_markup=support_kb(),
 )
 await call.answer()
@router.callback_query(F.data == "menu_back")
async def process_menu_back(call: types.CallbackQuery):
    await call.message.edit_text(
    "<blockquote><b>🏪 SAHIL BHAI STORE 🔓</b></blockquote>\n\n"
    "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
    "┝🛍️ Buy Now : All Key Purchase & Instant Delivery\n"
    "┝📢 Check Update : Check Setup Video And Update Apk\n"
    "┝🪙 Add Balance : Deposit Balance & Secure Auto-Add Payment System\n"
    "┝🆔 My Profile + All History : Check Your Account Information + All History\n"
    "┝👥 Refer And Earn : Share Refer Link & Earn Money\n"
    "┝🎬  How To Use Bot : View Tutorial And Work This Bot\n"
    "┝📨 Support : Bot Problem Fixed For Support Admin\n"
    "┝🎁 Daily Gift : Free Spin and win random balance daily, Only one spin every 24 hours.\n\n"
    "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
    "<blockquote>💰 Your  Balance:🪙₹0.00</blockquote>\n\n"  
    "<i>👇 Select an option from the menu below:</i>",
    parse_mode="HTML",
    reply_markup=main_menu_kb(),
 )

import random

@router.callback_query(F.data == "menu_daily_gift")
async def process_daily_gift(call: types.CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    now = datetime.datetime.now()

    if user_id in user_last_spin:
        last_spin = user_last_spin[user_id]
        time_diff = now - last_spin
        if time_diff < datetime.timedelta(hours=24):
            remaining = datetime.timedelta(hours=24) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Back to Menu",
                            callback_data="back_to_menu",
                            style="danger",
                        )
                    ]
                ]
            )
            await call.message.edit_text(
                f"⏳ Please wait {hours} hours and {minutes} minutes before your next spin.",
                reply_markup=keyboard,
            )
            return

    text = (
        "<blockquote><b>🎁 Daily Lucky Spin Wheel </b></blockquote>\n\n"
        "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
        "Spin the wheel once every 24 hours and win free balance credited instantly to your wallet!\n\n"
        "┝ 🪙 Winning Range: ₹0.00 to ₹1.00\n"
        "┝ ⏳ Spin Limit: 1 spin per 24 hours\n\n"
        "👇 Click the button below to try your luck:"
    )

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Spin Now!",
                    callback_data="spin_now",
                    style="success",
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Back to Menu",
                    callback_data="back_to_menu",
                    style="danger",
                )
            ],
        ]
    )
    await call.message.edit_text(
        text=text, reply_markup=keyboard, parse_mode="HTML"
    )


@dp.callback_query(F.data == "spin_now")
async def process_spin(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_last_spin[user_id] = datetime.datetime.now()
    gift_amount = round(random.uniform(0.0, 1.0), 2)

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Back to Menu",
                    callback_data="back_to_menu",
                    style="danger",
                )
            ]
        ]
    )

    await call.message.edit_text(
        f"🎉 Congratulations! You won ₹{gift_amount}!", reply_markup=keyboard
    )


@dp.callback_query(F.data == "back_to_menu")
async def process_back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        "Select an option from the menu below:", reply_markup=main_menu_kb()
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
        "• Add balance via  UIP QR System or Binance Pay\n"
        "• Tap Buy Now and pick your desired product\n"
        "• Key is delivered instantly to this chat screen\n"
        "• Browse plans and checkout seamlessly"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text="🎬 VIEW TUTORIAL VIDEO ", url="https://t.me/sahil_bhai_69/6", style="success")],
 [InlineKeyboardButton(text=" Back", callback_data="menu_back", style="danger")]
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
    "<blockquote><b>🏪 SAHIL BHAI STORE 🔓</b></blockquote>\n\n"
     "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
     "┝🛍️ Buy Now : All Key Purchase & Instant Delivery\n"
     "┝📢 Check Update : Check Setup Video And Update Apk\n"
     "┝🪙 Add Balance : Deposit Balance & Secure Auto-Add Payment System\n"
     "┝🆔 My Profile + All History : Check Your Account Information + All History\n"
     "┝👥 Refer And Earn : Share Refer Link & Earn Money\n"
     "┝🎬  How To Use Bot : View Tutorial And Work This Bot\n"
     "┝📨 Support : Bot Problem Fixed For Support Admin\n"
     "┝🎁 Daily Gift : Free Spin and win random balance daily, Only one spin every 24 hours.\n\n"
     "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
     "<blockquote>💰 Your Balance:🪙₹0.00</blockquote>\n\n"  
     "<i>👇 Select an option from the menu below:</i>",
     parse_mode="HTML",
     reply_markup=main_menu_kb(),
 )

@router.callback_query(F.data == "menu_shop")
async def process_menu_shop(call: types.CallbackQuery):
    keyboard_buttons = []

    for id, name in products_db.items():
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=name,
                    callback_data=f"buy_product_{id}",
                    style="success",
                )
            ]
        )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text="Back", callback_data="main_menu", style="danger"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await call.message.edit_text(
        "<blockquote>〰️ PRODUCT STORE — SHOP 〰️</blockquote>\n\n<blockquote>🛍️  Choose a product from the list below:</blockquote>",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
def get_plans_for_product(product_id):
    return plans_db.get(product_id, [])

@router.callback_query(lambda c: c.data.startswith("buy_product_"))
async def process_buy_product(call: types.CallbackQuery):
    product_id = call.data.split("_")[2]
    plans = get_plans_for_product(product_id)

    keyboard_buttons = []
    for plan in plans:
        keyboard_buttons.append([
            types.InlineKeyboardButton(
                text=f"{plan['plan_name']} - ₹{plan['price']}",
                callback_data=f"select_plan_{plan['plan_name']}"
            )
        ])

    keyboard_buttons.append([
        types.InlineKeyboardButton(text="Back", callback_data="menu_shop")
    ])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await call.message.edit_text(
        "<b>Choose your access plan:</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await call.answer()


if __name__ == '__main__':
    init_db()
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))
    
