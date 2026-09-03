import random
import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = '8717208912:AAHGgwn_7rURyL9C-D9PrJSsUlwdcizmfdE'

ITEMS = {
    'rusty_dagger': {'name': '🗡 خنجر زنگ‌زده', 'type': 'weapon', 'rarity': 'معمولی', 'atk': 4, 'def': 0, 'hp': 0, 'lvl_req': 1, 'price': 15, 'desc': 'خنجری کند که سال‌ها زیر خاک مدفون بوده.'},
    'cloth_vest': {'name': '🥼 جلیقه پارچه‌ای', 'type': 'armor', 'rarity': 'معمولی', 'atk': 0, 'def': 2, 'hp': 5, 'lvl_req': 1, 'price': 15, 'desc': 'لباسی ساده از جنس کتان.'},
    'leather_cap': {'name': '🧢 کلاه چرمی ساده', 'type': 'helmet', 'rarity': 'معمولی', 'atk': 0, 'def': 2, 'hp': 0, 'lvl_req': 1, 'price': 12, 'desc': 'دوخته شده از پوست گراز.'},
    'worn_boots': {'name': '🥾 کفش‌های مندرس', 'type': 'boots', 'rarity': 'معمولی', 'atk': -1, 'def': 2, 'hp': 0, 'lvl_req': 1, 'price': 10, 'desc': 'کفش‌هایی سنگین و وصله‌دار.'},

    'coral_trident': {'name': '🔱 سرنیزه مرجانی', 'type': 'weapon', 'rarity': 'کمیاب', 'atk': 14, 'def': 2, 'hp': 10, 'lvl_req': 3, 'price': 80, 'desc': 'تراشیده شده از مرجان‌های سخت اعماق اقیانوس.'},
    'spider_shield_armor': {'name': '🕷 زره تار عنکبوت سیاه', 'type': 'armor', 'rarity': 'کمیاب', 'atk': 2, 'def': 8, 'hp': 15, 'lvl_req': 5, 'price': 95, 'desc': 'ساخته شده از تار تنیده شده عنکبوت‌های غول‌پیکر باتلاق.'},
    'sand_blade': {'name': '🗡 شمشیر طوفان شن', 'type': 'weapon', 'rarity': 'خاص', 'atk': 22, 'def': 4, 'hp': 0, 'lvl_req': 8, 'price': 170, 'desc': 'تیغه‌ای بران که با ذرات شن برنده صیقل یافته است.'},
    'ice_crown': {'name': '👑 تاج یخبندان کهن', 'type': 'helmet', 'rarity': 'خاص', 'atk': 3, 'def': 12, 'hp': 20, 'lvl_req': 12, 'price': 220, 'desc': 'میراث پادشاهان یخ‌زده کوهستان‌های شمالی.'},
    'magma_plate': {'name': '🌋 زره مذاب ققنوس', 'type': 'armor', 'rarity': 'حماسی', 'atk': 10, 'def': 25, 'hp': 40, 'lvl_req': 18, 'price': 450, 'desc': 'پوشیده از پولک‌های سنگ‌شده‌ی جریان‌های آتشفشانی.'},
    'leviathan_axe': {'name': '🌊 تبر طوفان لِوایتان', 'type': 'weapon', 'rarity': 'افسانه‌ای', 'atk': 60, 'def': -5, 'hp': 30, 'lvl_req': 25, 'price': 850, 'desc': 'تبری که قدرت امواج خروشان دریا و طوفان را به دوش می‌کشد.'},

    'spirit_root_boots': {
        'name': '🌿 کفش‌های ریشه ارواح', 
        'type': 'boots', 
        'rarity': 'افسانه‌ای', 
        'atk': 5, 
        'def': 10, 
        'hp': 25, 
        'lvl_req': 5, 
        'price': 350, 
        'desc': 'بافته‌شده از ریشه‌های باستانی درخت مقدس که پوشنده را چابک می‌سازد.'
    },

    'mohabbat_e_zurvan': {
        'name': '✨ محبت زروان', 
        'type': 'weapon', 
        'rarity': 'اسطوره ای', 
        'atk': 999, 
        'def': 999, 
        'hp': 99999, 
        'lvl_req': 1, 
        'price': 999999, 
        'desc': 'شمشیری جاودانه آغشته به نور و مهر بیکران زروان، بخشاینده قدرت مطلق.'
    },
    
    'tof_e_abol': {'name': '🧪 تف ابول', 'type': 'helmet', 'rarity': 'افسانه ای', 'atk': 70, 'def': 25, 'hp': -8, 'lvl_req': 2, 'price': 143, 'desc': 'ناخواسته به سرو صورت طرف مقابل پرتاب میشه.'},									
    'health_potion': {'name': '🧪 معجون سلامتی', 'type': 'consumable', 'rarity': 'معمولی', 'heal': 50, 'price': 20, 'desc': 'زخم‌ها را التیام می‌بخشد.'},
    'wooden_chest': {'name': '📦 صندوق چوبی', 'type': 'chest', 'rarity': 'معمولی', 'price': 150, 'desc': 'صندوقی معمولی با لوت پایه.'},
    'iron_chest': {'name': '🧰 صندوق آهنی سنگین', 'type': 'chest', 'rarity': 'کمیاب', 'price': 400, 'desc': 'دارای تجهیزات باارزش‌تر.'},
    'golden_chest': {'name': '🌟 صندوق سلطنتی طلا', 'type': 'chest', 'rarity': 'خاص', 'price': 800, 'desc': 'دارای شانس آیتم‌های حماسی و افسانه‌ای.'}
}

CHEST_RATES = {
    'wooden_chest': {'gold': (15, 35), 'rates': {'معمولی': 70, 'کمیاب': 25, 'خاص': 5, 'حماسی': 0, 'افسانه‌ای': 0}},
    'iron_chest': {'gold': (50, 120), 'rates': {'معمولی': 30, 'کمیاب': 40, 'خاص': 25, 'حماسی': 5, 'افسانه‌ای': 0}},
    'golden_chest': {'gold': (150, 300), 'rates': {'معمولی': 0, 'کمیاب': 20, 'خاص': 40, 'حماسی': 30, 'افسانه‌ای': 10}}
}

GIFT_CODES = {
    'MMM45': {
        'reward': 'mohabbat_e_zurvan', 
        'type': 'item', 
        'desc': 'شمشیری جاودانه آغشته به نور و مهر بیکران زروان'
    },
    'KIR': {
        'reward': 100, 
        'type': 'gold', 
        'desc': 'پاداش ویژه ۱۰۰ سکه طلا'
    }
}

BIOMES = {
    'sea': {
        'name': '🌊 دریای طوفانی (ساحل صیادان)', 'min_lvl': 1,
        'enemies': [
            {'id': 'piranha', 'name': 'ماهی پیرانای خون‌خوار 🐟', 'hp': 30, 'atk': 8, 'xp': 40, 'gold': 20, 'tier': 'معمولی', 'loot': ['rusty_dagger', 'health_potion']},
            {'id': 'eel', 'name': 'مارماهی برقی ⚡', 'hp': 45, 'atk': 12, 'xp': 60, 'gold': 30, 'tier': 'معمولی', 'loot': ['coral_trident']}
        ],
        'boss': {'id': 'kraken_lord', 'name': '🐙 کراکن وحشت', 'hp': 250, 'atk': 35, 'xp': 400, 'gold': 300, 'tier': 'حماسی', 'loot': ['leviathan_axe']}
    },
    'forest': {
        'name': '🌲 جنگل زمزمه‌های تاریک', 'min_lvl': 5,
        'enemies': [
            {'id': 'wolf', 'name': 'گرگ خاکستری آلفا 🐺', 'hp': 55, 'atk': 15, 'xp': 80, 'gold': 40, 'tier': 'کمیاب', 'loot': ['leather_cap', 'health_potion']},
            {'id': 'treant', 'name': 'درخت کهن‌سال خشمگین 🌳', 'hp': 80, 'atk': 18, 'xp': 110, 'gold': 55, 'tier': 'کمیاب', 'loot': ['cloth_vest']}
        ],
        'boss': {'id': 'forest_guardian', 'name': '🌿 ارواح کهن درخت مقدس', 'hp': 350, 'atk': 40, 'xp': 550, 'gold': 450, 'tier': 'افسانه‌ای', 'loot': ['iron_chest', 'spirit_root_boots']}
    },
    'plains': {
        'name': '🌾 دشت‌های بادگیر طلایی', 'min_lvl': 10,
        'enemies': [
            {'id': 'bandit', 'name': 'راهزن فراری دشت 🗡', 'hp': 90, 'atk': 22, 'xp': 140, 'gold': 75, 'tier': 'کمیاب', 'loot': ['worn_boots']},
            {'id': 'knight_rogue', 'name': 'شوالیه طردشده 🛡', 'hp': 110, 'atk': 26, 'xp': 180, 'gold': 90, 'tier': 'خاص', 'loot': ['iron_chest']}
        ],
        'boss': {'id': 'warlord', 'name': '👑 فرمانده ارتش مزدوران', 'hp': 500, 'atk': 50, 'xp': 800, 'gold': 700, 'tier': 'افسانه‌ای', 'loot': ['golden_chest']}
    },
    'desert': {
        'name': '🏜 بیابان سوزان و سراب مرگ', 'min_lvl': 15,
        'enemies': [
            {'id': 'scorpion', 'name': 'عقرب غول‌پیکر زهرآگین 🦂', 'hp': 140, 'atk': 32, 'xp': 220, 'gold': 120, 'tier': 'خاص', 'loot': ['health_potion']},
            {'id': 'viper', 'name': 'مار صحرایی شاخ‌دار 🐍', 'hp': 160, 'atk': 36, 'xp': 260, 'gold': 140, 'tier': 'خاص', 'loot': ['sand_blade']}
        ],
        'boss': {'id': 'pharaoh', 'name': '⚱️ فرعون نفرین‌شده‌ی گم‌شده', 'hp': 700, 'atk': 65, 'xp': 1100, 'gold': 950, 'tier': 'افسانه‌ای', 'loot': ['golden_chest']}
    },
    'swamp': {
        'name': '🌿 باتلاق لجن‌زار تعفن', 'min_lvl': 19,
        'enemies': [
            {'id': 'bog_monster', 'name': 'هیولای لجن‌زار متحرک 🧟‍♂️', 'hp': 200, 'atk': 42, 'xp': 320, 'gold': 180, 'tier': 'حماسی', 'loot': ['spider_shield_armor']},
            {'id': 'giant_spider', 'name': 'عکبوتیه ملکه باتلاق 🕷', 'hp': 230, 'atk': 48, 'xp': 380, 'gold': 210, 'tier': 'حماسی', 'loot': ['health_potion']}
        ],
        'boss': {'id': 'swamp_witch', 'name': '🧙‍♀️ جادوگر پیر و خبیث باتلاق', 'hp': 900, 'atk': 75, 'xp': 1400, 'gold': 1200, 'tier': 'افسانه‌ای', 'loot': ['golden_chest']}
    },
    'snow_mountain': {
        'name': '❄️ کوهستان یخی و قله توفان', 'min_lvl': 23,
        'enemies': [
            {'id': 'yeti', 'name': 'یتی غول‌پیکر برفی 🦍', 'hp': 280, 'atk': 55, 'xp': 460, 'gold': 260, 'tier': 'حماسی', 'loot': ['ice_crown']},
            {'id': 'ice_golem', 'name': 'گولم بلورین یخ‌زده 🧊', 'hp': 320, 'atk': 60, 'xp': 520, 'gold': 300, 'tier': 'حماسی', 'loot': ['health_potion']}
        ],
        'boss': {'id': 'frost_dragon', 'name': '❄️ اژدهای کهن یخبندان شمالی', 'hp': 1200, 'atk': 90, 'xp': 1800, 'gold': 1600, 'tier': 'افسانه‌ای', 'loot': ['leviathan_axe']}
    },
    'volcano': {
        'name': '🌋 آتشفشان فعال و رود مذاب', 'min_lvl': 30,
        'enemies': [
            {'id': 'fire_elemental', 'name': 'عنصر آتش سوزان 🔥', 'hp': 380, 'atk': 70, 'xp': 650, 'gold': 380, 'tier': 'افسانه‌ای', 'loot': ['magma_plate']},
            {'id': 'lava_hound', 'name': 'سگ شکاری مذاب جهنم 🐕', 'hp': 420, 'atk': 78, 'xp': 720, 'gold': 420, 'tier': 'افسانه‌ای', 'loot': ['health_potion']}
        ],
        'boss': {'id': 'flame_lord', 'name': '🔥 پادشاه مطلق آتشفشان‌های سوزان', 'hp': 1600, 'atk': 110, 'xp': 2500, 'gold': 2200, 'tier': 'افسانه‌ای', 'loot': ['leviathan_axe']}
    }
}

players = {}
MAX_LEVEL = 50

def load_game():
    global players
    if os.path.exists("db.json"):
        with open("db.json", "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
                players = {int(k): v for k, v in raw.items()}
            except: pass

def save_game():
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)

load_game()

def get_player_stats(player):
    stats = {
        'atk': player.get('base_atk', 6), 
        'def': player.get('base_def', 3), 
        'max_hp': player.get('base_max_hp', 60), 
        'max_energy': player.get('base_max_energy', 100)
    }
    for slot in ['weapon', 'armor', 'helmet', 'boots']:
        item_id = player.get('equipped', {}).get(slot)
        if item_id and item_id in ITEMS:
            stats['atk'] += ITEMS[item_id].get('atk', 0)
            stats['def'] += ITEMS[item_id].get('def', 0)
            stats['max_hp'] += ITEMS[item_id].get('hp', 0)
            
    stats['atk'] = max(1, stats['atk']) 
    stats['def'] = max(0, stats['def'])
    stats['max_hp'] = max(10, stats['max_hp'])
    return stats

def add_item(player, item_id, qty=1):
    inv = player.setdefault('inventory', {})
    inv[item_id] = inv.get(item_id, 0) + qty

def roll_chest_item(chest_id):
    rates = CHEST_RATES[chest_id]['rates']
    rand = random.uniform(0, 100)
    cumulative = 0
    selected_rarity = 'معمولی'
    for rarity, chance in rates.items():
        cumulative += chance
        if rand <= cumulative:
            selected_rarity = rarity
            break
            
    pool = [i for i, d in ITEMS.items() if d['type'] not in ['consumable', 'chest'] and d['rarity'] == selected_rarity]
    if not pool: pool = ['health_potion']
    return random.choice(pool)

async def show_town(query_or_update, context, user_id, is_new=False, is_text_msg=False):
    # ساخت خودکار کاربر در صورت عدم وجود (جلوگیری از KeyError)
    if user_id not in players:
        user_obj = None
        if hasattr(query_or_update, 'from_user') and query_or_update.from_user:
            user_obj = query_or_update.from_user
        elif hasattr(query_or_update, 'message') and query_or_update.message and query_or_update.message.from_user:
            user_obj = query_or_update.message.from_user
            
        players[user_id] = {
            'name': user_obj.first_name if user_obj else "قهرمان",
            'lvl': 1,
            'xp': 0,
            'xp_needed': 100,
            'gold': 50,
            'inventory': {'health_potion': 2},
            'equipped': {},
            'base_max_hp': 60,
            'base_max_energy': 100,
            'base_atk': 6,
            'base_def': 3
        }
        save_game()

    player = players[user_id]
    if 'base_max_hp' not in player:
        player['base_max_hp'] = player.get('max_hp', 60)
        player['base_max_energy'] = player.get('max_energy', 100)
        
    stats = get_player_stats(player)
    player['hp'] = stats['max_hp']
    player['energy'] = stats['max_energy']
    player['defending'] = False
    save_game()
    
    text = f"🏘 **شهر پناهگاه مرکزی**\nدرود بر تو ای **{player.get('name', 'قهرمان')}**! (سطح {player.get('lvl', 1)})\nتمامی زخم‌هایت درمان شد."
    keyboard = [
        [InlineKeyboardButton("🗺 انتخاب مناطق و مپ‌ها", callback_data="map_menu")],
        [InlineKeyboardButton("📚 کتابخانه اطلاعات (Codex)", callback_data="codex_menu")],
        [InlineKeyboardButton("🎒 کوله‌پشتی", callback_data="inventory"), InlineKeyboardButton("🏪 بازار شهر", callback_data="shop_menu")],
        [InlineKeyboardButton("📊 شناسنامه قهرمان", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_new or is_text_msg:
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await query_or_update.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_stats(query, player):
    stats = get_player_stats(player)
    eq = player.get('equipped', {})
    wep = ITEMS[eq.get('weapon')]['name'] if eq.get('weapon') in ITEMS else "ندارد"
    arm = ITEMS[eq.get('armor')]['name'] if eq.get('armor') in ITEMS else "ندارد"
    helm = ITEMS[eq.get('helmet')]['name'] if eq.get('helmet') in ITEMS else "ندارد"
    boots = ITEMS[eq.get('boots')]['name'] if eq.get('boots') in ITEMS else "ندارد"
    
    text = f"📊 **شناسنامه قهرمان:**\n\n" \
           f"⭐ سطح: {player.get('lvl', 1)}/{MAX_LEVEL} (تجربه: {player.get('xp', 0)}/{player.get('xp_needed', 100)})\n" \
           f"❤️ جان: {player.get('hp')}/{stats['max_hp']} | ⚡ انرژی: {stats['max_energy']}\n" \
           f"⚔️ قدرت حمله کل: {stats['atk']} | 🛡 دفاع کل: {stats['def']}\n" \
           f"💰 سکه طلا: {player.get('gold', 0)}\n\n" \
           f"🎒 **تجهیزات:**\n• سلاح: {wep}\n• زره: {arm}\n• کلاه‌خود: {helm}\n• کفش: {boots}"
           
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 شهر", callback_data="town")]]), parse_mode='Markdown')

async def show_inventory(query, player, message=None):
    text = (message + "\n\n" if message else "") + "🎒 **موجودی کوله‌پشتی:**\nبرای استفاده/فروش روی آیتم ضربه بزنید:"
    keyboard = []
    has_items = False
    for item_id, qty in player.get('inventory', {}).items():
        if qty > 0 and item_id in ITEMS:
            has_items = True
            keyboard.append([InlineKeyboardButton(f"{ITEMS[item_id]['name']} (×{qty})", callback_data=f"inspect_{item_id}")])
            
    if not has_items: text += "\nکوله‌پشتی شما خالی است!"
    keyboard.append([InlineKeyboardButton("🔙 بازگشت به شهر", callback_data="town")])
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_item_inspect(query, player, item_id):
    if player.get('inventory', {}).get(item_id, 0) <= 0:
        await query.answer("آیتم را ندارید!", show_alert=True)
        return await show_inventory(query, player)
        
    item = ITEMS[item_id]
    sell_price = int(item['price'] / 2)
    is_equipped = item_id in player.get('equipped', {}).values()
    
    text = f"📦 **{item['name']}**\n" \
           f"🌟 کمیابی: `{item['rarity']}` | 📈 لول مورد نیاز: `{item.get('lvl_req', 1)}`\n" \
           f"ℹ️ {item['desc']}\n\n"
           
    if item['type'] not in ['consumable', 'chest']:
        text += f"📊 آمار آیتم:\n⚔️ حمله: {item.get('atk',0)} | 🛡 دفاع: {item.get('def',0)} | ❤️ جان افزوده: {item.get('hp',0)}\n\n"
        text += f"وضعیت: {'✅ مجهز شده' if is_equipped else '❌ داخل کوله'}"
    elif item['type'] == 'chest':
        text += "🎁 باز کردن این صندوق طلا و تجهیزات رندوم به همراه دارد."
        
    btn_txt = "✨ تجهیز کردن" if item['type'] not in ['consumable','chest'] else ("🧪 نوشیدن" if item['type'] == 'consumable' else "🎁 باز کردن صندوق")
    
    keyboard = [
        [InlineKeyboardButton(btn_txt, callback_data=f"use_{item_id}")],
        [InlineKeyboardButton(f"💰 فروش ({sell_price} طلا)", callback_data=f"sell_{item_id}")],
        [InlineKeyboardButton("🔙 کوله‌پشتی", callback_data="inventory")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_codex_menu(query):
    text = "📚 **کتابخانه و دایرةالمعارف سرزمین**\nاطلاعات کامل دشمنان، باس‌ها و آیتم‌ها را می‌توانید در اینجا بررسی کنید:"
    keyboard = [
        [InlineKeyboardButton("👹 لیست دشمنان و باس‌ها", callback_data="codex_enemies")],
        [InlineKeyboardButton("🛡 لیست تجهیزات و آیتم‌ها", callback_data="codex_items")],
        [InlineKeyboardButton("🔙 شهر", callback_data="town")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_codex_enemies(query):
    text = "👹 **دایرةالمعارف دشمنان و باس‌ها:**\n\n"
    for b_key, biome in BIOMES.items():
        text += f"📌 **{biome['name']}** (حداقل لول {biome['min_lvl']}):\n"
        for en in biome['enemies']:
            text += f"• {en['name']} | ❤️ جان: {en['hp']} | ⚔️ دمیج: {en['atk']} | 🌟 لوت: {', '.join([ITEMS[l]['name'] for l in en['loot'] if l in ITEMS])}\n"
        boss = biome['boss']
        text += f"👑 **باس:** {boss['name']} | ❤️ جان: {boss['hp']} | ⚔️ دمیج: {boss['atk']}\n\n"
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="codex_menu")]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_codex_items(query):
    text = "🛡 **دایرةالمعارف تجهیزات و آیتم‌ها:**\n\n"
    for i_id, item in ITEMS.items():
        if item['type'] not in ['consumable', 'chest']:
            text += f"• **{item['name']}** (`{item['rarity']}`)\n  لول نیاز: {item.get('lvl_req',1)} | ⚔️ حمله: {item.get('atk',0)} | 🛡 دفاع: {item.get('def',0)}\n"
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="codex_menu")]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_shop_menu(query):
    text = "🏪 **بازار بزرگ پادشاهی**\nبه کدام بخش می‌روید؟"
    keyboard = [
        [InlineKeyboardButton("🗡 خرید تجهیزات و معجون", callback_data="shop_gear")],
        [InlineKeyboardButton("🎁 خرید صندوق‌های شانس", callback_data="shop_chests")],
        [InlineKeyboardButton("🔙 شهر", callback_data="town")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def get_combat_keyboard(player):
    lvl = player.get('lvl', 1)
    cds = player.get('cooldowns', {})
    
    btn_atk = InlineKeyboardButton("⚔️ حمله (15)", callback_data="pve_atk")
    btn_def = InlineKeyboardButton("🛡 گارد (10)", callback_data="pve_defend")
    btn_heal = InlineKeyboardButton("🧪 معجون", callback_data="pve_heal")
    btn_flee = InlineKeyboardButton("🏃 فرار", callback_data="pve_flee")
    
    keyboard = [[btn_atk]]
    skills_row1 = []
    if lvl >= 3:
        txt = f"💥 کریتیکال ({cds.get('crit',0)})" if cds.get('crit',0)>0 else "💥 کریتیکال (30)"
        skills_row1.append(InlineKeyboardButton(txt, callback_data="pve_crit"))
    if lvl >= 10:
        txt = f"🩸 خونریزی ({cds.get('bleed',0)})" if cds.get('bleed',0)>0 else "🩸 خونریزی (25)"
        skills_row1.append(InlineKeyboardButton(txt, callback_data="pve_bleed"))
    if skills_row1: keyboard.append(skills_row1)
        
    skills_row2 = []
    if lvl >= 15:
        txt = f"💫 کوبنده ({cds.get('stun',0)})" if cds.get('stun',0)>0 else "💫 کوبنده (35)"
        skills_row2.append(InlineKeyboardButton(txt, callback_data="pve_stun"))
    if lvl >= 20:
        txt = f"🧛 مکیدن ({cds.get('lifesteal',0)})" if cds.get('lifesteal',0)>0 else "🧛 مکیدن خون (40)"
        skills_row2.append(InlineKeyboardButton(txt, callback_data="pve_lifesteal"))
    if skills_row2: keyboard.append(skills_row2)

    keyboard.append([btn_def, btn_heal])
    keyboard.append([btn_flee])
    return keyboard

async def start_combat(query, player, biome_key, is_boss=False):
    biome = BIOMES[biome_key]
    if player.get('lvl', 1) < biome['min_lvl']:
        return await query.answer(f"❌ برای ورود به این منطقه حداقل لول {biome['min_lvl']} نیاز است!", show_alert=True)
        
    enemy = biome['boss'].copy() if is_boss else random.choice(biome['enemies']).copy()
    enemy['is_boss'] = is_boss
    player['enemy'] = enemy
    player['enemy']['bleed'] = 0
    player['enemy']['stunned'] = False
    
    stats = get_player_stats(player)
    player['state'] = 'COMBAT_PVE'
    player['hp'] = stats['max_hp']
    player['energy'] = stats['max_energy']
    player['defending'] = False
    player['cooldowns'] = {'crit': 0, 'bleed': 0, 'stun': 0, 'lifesteal': 0}
    
    text = f"⚠️ نبرد با **{player['enemy']['name']}** در منطقه `{biome['name']}` آغاز شد!\n\n" \
           f"❤️ شما: {player['hp']}/{stats['max_hp']} | ⚡ انرژی: {player['energy']}/{stats['max_energy']}\n" \
           f"🖤 جان دشمن: {player['enemy']['hp']}"
           
    keyboard = await get_combat_keyboard(player)
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in players:
        return await update.message.reply_text("❌ ابتدا با دستور /start بازی را شروع کنید.")
        
    args = context.args
    if not args:
        return await update.message.reply_text("⚠️ لطفاً کد هدیه را وارد کنید.\nمثال: `/gift MMM45`", parse_mode='Markdown')
        
    code = args[0].strip().upper()
    player = players[user_id]
    
    if code not in GIFT_CODES:
        return await update.message.reply_text("❌ کد هدیه نامعتبر است یا وجود ندارد.")
        
    used_list = player.setdefault('used_codes', [])
    if code in used_list:
        return await update.message.reply_text("⚠️ شما قبلاً از این کد هدیه استفاده کرده‌اید!")
        
    gift = GIFT_CODES[code]
    used_list.append(code)
    
    if gift['type'] == 'item':
        item_id = gift['reward']
        add_item(player, item_id)
        item_name = ITEMS[item_id]['name'] if item_id in ITEMS else item_id
        await update.message.reply_text(f"🎉 تبریک! کد هدیه با موفقیت فعال شد.\n🎁 آیتم اسطوره‌ای دریافت شده: **{item_name}**", parse_mode='Markdown')
        
    elif gift['type'] == 'gold':
        gold_amount = gift['reward']
        player['gold'] = player.get('gold', 0) + gold_amount
        await update.message.reply_text(f"🎉 تبریک! کد هدیه با موفقیت فعال شد.\n💰 مقدار {gold_amount} سکه طلا به کیف پول شما اضافه شد!", parse_mode='Markdown')
        
    save_game()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    user_id = query.from_user.id
    
    # اگر کاربر در دیتابیس نبود، تابع show_town خودش او را می‌سازد پس نیازی به ریترن کردن ارور نیست
    if user_id not in players:
        await show_town(query, context, user_id)
        return
    
    player = players[user_id]
    data = query.data

    if data == "town":
        player['state'] = 'TOWN'
        await show_town(query, context, user_id)
        
    elif data == "stats": await show_stats(query, player)
    elif data == "inventory": await show_inventory(query, player)
    elif data == "shop_menu": await show_shop_menu(query)
    elif data == "codex_menu": await show_codex_menu(query)
    elif data == "codex_enemies": await show_codex_enemies(query)
    elif data == "codex_items": await show_codex_items(query)
        
    elif data == "shop_gear":
        text = f"🏪 طلای شما: {player.get('gold', 0)} 💰"
        keyboard = [
            [InlineKeyboardButton("🔱 سرنیزه مرجانی (80)", callback_data="buy_coral_trident"), InlineKeyboardButton("🕷 زره عنکبوت (95)", callback_data="buy_spider_shield_armor")],
            [InlineKeyboardButton("🗡 شمشیر شن (170)", callback_data="buy_sand_blade"), InlineKeyboardButton("👑 تاج یخی (220)", callback_data="buy_ice_crown")],
            [InlineKeyboardButton("🌋 زره مذاب (450)", callback_data="buy_magma_plate"), InlineKeyboardButton("🧪 معجون (20)", callback_data="buy_health_potion")],
            [InlineKeyboardButton("🔙 بازار", callback_data="shop_menu")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == "shop_chests":
        text = f"🎁 **مرکز صندوق‌های شانس** (طلای شما: {player.get('gold', 0)} 💰)"
        keyboard = [
            [InlineKeyboardButton("📦 صندوق چوبی (50)", callback_data="info_chest_wooden_chest")],
            [InlineKeyboardButton("🧰 صندوق آهنی (150)", callback_data="info_chest_iron_chest")],
            [InlineKeyboardButton("🌟 صندوق طلایی (400)", callback_data="info_chest_golden_chest")],
            [InlineKeyboardButton("🔙 بازار", callback_data="shop_menu")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data.startswith("info_chest_"):
        chest_id = data.replace("info_chest_", "")
        info = CHEST_RATES[chest_id]['rates']
        price = ITEMS[chest_id]['price']
        text = f"🎁 **{ITEMS[chest_id]['name']}**\n\n💰 قیمت: {price} طلا\n" \
               f"📊 **احتمال دراپ:** معمولی {info['معمولی']}% | کمیاب {info['کمیاب']}% | خاص {info['خاص']}% | حماسی {info['حماسی']}% | افسانه‌ای {info['افسانه‌ای']}%\n"
        keyboard = [[InlineKeyboardButton("💳 خرید صندوق", callback_data=f"buy_{chest_id}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="shop_chests")]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data.startswith("inspect_"): await show_item_inspect(query, player, data.replace("inspect_", ""))
    elif data.startswith("sell_"):
        item_id = data.replace("sell_", "")
        if player['inventory'].get(item_id, 0) > 0:
            player['inventory'][item_id] -= 1
            gain = int(ITEMS[item_id]['price'] / 2)
            player['gold'] = player.get('gold', 0) + gain
            await show_inventory(query, player, f"✅ فروخته شد. (+{gain} طلا)")

    elif data.startswith("use_"):
        item_id = data.replace("use_", "")
        item = ITEMS[item_id]
        if player['inventory'].get(item_id, 0) > 0:
            if item['type'] == 'chest':
                player['inventory'][item_id] -= 1
                drop_item = roll_chest_item(item_id)
                gold_amt = random.randint(*CHEST_RATES[item_id]['gold'])
                add_item(player, drop_item)
                player['gold'] = player.get('gold',0) + gold_amt
                msg = f"🎉 **صندوق باز شد!**\n🎁 {ITEMS[drop_item]['name']} ({ITEMS[drop_item]['rarity']})\n💰 {gold_amt} طلا"
                await show_inventory(query, player, msg)
                
            elif item['type'] == 'consumable':
                stats = get_player_stats(player)
                if player['hp'] < stats['max_hp']:
                    player['hp'] = min(stats['max_hp'], player['hp'] + item['heal'])
                    player['inventory'][item_id] -= 1
                    await show_item_inspect(query, player, item_id)
                else: await query.answer("جان کامل است!", show_alert=True)
                    
            elif item['type'] in ['weapon', 'armor', 'helmet', 'boots']:
                if player.get('lvl', 1) < item.get('lvl_req', 1):
                    return await query.answer(f"❌ نیاز به لول {item['lvl_req']} دارد!", show_alert=True)
                player.setdefault('equipped', {})[item['type']] = item_id
                stats = get_player_stats(player)
                player['hp'] = min(player['hp'], stats['max_hp'])
                await query.answer("✅ مجهز شد!", show_alert=True)
                await show_item_inspect(query, player, item_id)

    elif data.startswith("buy_"):
        item_id = data.replace("buy_", "")
        price = ITEMS[item_id]['price']
        if player.get('gold', 0) >= price:
            player['gold'] -= price
            add_item(player, item_id)
            await query.answer("✅ خریداری شد!", show_alert=True)
            if item_id in CHEST_RATES: await show_shop_menu(query)
            else: await show_inventory(query, player, "آیتم جدید اضافه شد.")
        else: await query.answer("❌ طلا کافی نیست!", show_alert=True)

    elif data == "map_menu":
        keyboard = []
        for b_key, b_val in BIOMES.items():
            keyboard.append([
                InlineKeyboardButton(f"⚔️ {b_val['name']} (لول {b_val['min_lvl']}+)", callback_data=f"explore_{b_key}"),
                InlineKeyboardButton(f"👑 باس", callback_data=f"boss_{b_key}")
            ])
        keyboard.append([InlineKeyboardButton("🔙 شهر", callback_data="town")])
        await query.edit_message_text(text="🗺 **نقشه مناطق ماجراجویی:**\nمنطقه مورد نظر خود را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data.startswith("explore_") or data.startswith("boss_"):
        is_boss = data.startswith("boss_")
        biome_key = data.replace("boss_", "").replace("explore_", "")
        await start_combat(query, player, biome_key, is_boss)

    elif player.get('state') == 'COMBAT_PVE':
        lvl = player.get('lvl', 1)
        enemy = player['enemy']
        stats = get_player_stats(player)
        p_atk, p_def = stats['atk'], stats['def']
        
        cds = player['cooldowns']
        for k in cds:
            if cds[k] > 0: cds[k] -= 1

        bleed_dmg = 0
        if enemy.get('bleed', 0) > 0:
            bleed_dmg = 12 if enemy.get('is_boss') else 7
            enemy['hp'] -= bleed_dmg
            enemy['bleed'] -= 1

        action_log, cost = "", 0

        if data == "pve_atk":
            cost = 15
            if player['energy'] < cost: return await query.answer("انرژی نداری!", show_alert=True)
            player['energy'] -= cost
            dmg = random.randint(int(p_atk*0.8), int(p_atk*1.2))
            enemy['hp'] -= dmg
            action_log = f"حمله: {dmg} آسیب."

        elif data == "pve_crit" and lvl >= 3:
            cost = 30
            if cds.get('crit', 0) > 0 or player['energy'] < cost: return await query.answer("مهارت آماده نیست!", show_alert=True)
            player['energy'] -= cost; cds['crit'] = 2
            dmg = int(p_atk * 1.9); enemy['hp'] -= dmg
            action_log = f"💥 کریتیکال! {dmg} آسیب."

        elif data == "pve_bleed" and lvl >= 7:
            cost = 25
            if cds.get('bleed', 0) > 0 or player['energy'] < cost: return await query.answer("مهارت آماده نیست!", show_alert=True)
            player['energy'] -= cost; cds['bleed'] = 2
            dmg = int(p_atk * 0.7); enemy['hp'] -= dmg; enemy['bleed'] = 2
            action_log = "🩸 خونریزی اعمال شد."

        elif data == "pve_stun" and lvl >= 10:
            cost = 35
            if cds.get('stun', 0) > 0 or player['energy'] < cost: return await query.answer("مهارت آماده نیست!", show_alert=True)
            player['energy'] -= cost; cds['stun'] = 2; enemy['stunned'] = True
            action_log = "💫 دشمن گیج شد."

        elif data == "pve_lifesteal" and lvl >= 15:
            cost = 40
            if cds.get('lifesteal', 0) > 0 or player['energy'] < cost: return await query.answer("مهارت آماده نیست!", show_alert=True)
            player['energy'] -= cost; cds['lifesteal'] = 2
            dmg = int(p_atk * 1.2); enemy['hp'] -= dmg
            heal_amt = int(dmg * 0.8)
            player['hp'] = min(stats['max_hp'], player['hp'] + heal_amt)
            action_log = f"🧛 مکیدن خون! {dmg} آسیب و {heal_amt} درمان."

        elif data == "pve_defend":
            cost = 10
            if player['energy'] < cost: return await query.answer("انرژی نداری!", show_alert=True)
            player['energy'] -= cost; player['defending'] = True
            action_log = "🛡 گارد فعال شد."

        elif data == "pve_heal":
            if player['inventory'].get('health_potion', 0) > 0:
                player['hp'] = min(stats['max_hp'], player['hp'] + 50)
                player['inventory']['health_potion'] -= 1
                action_log = "🧪 معجون مصرف شد."
            else: return await query.answer("معجون نداری!", show_alert=True)

        elif data == "pve_flee":
            player['state'] = 'TOWN'
            await query.answer("🏃 فرار کردی!", show_alert=True)
            return await show_town(query, context, user_id)

        if enemy['hp'] <= 0:
            player['state'] = 'TOWN'
            player['xp'] = player.get('xp', 0) + enemy['xp']
            player['gold'] = player.get('gold', 0) + enemy['gold']
            msg = f"🏆 **پیروزی!**\n✨ +{enemy['xp']} تجربه | 💰 +{enemy['gold']} طلا"
            
            if 'loot' in enemy and enemy['loot']:
                drop_item = random.choice(enemy['loot'])
                if drop_item in ITEMS:
                    add_item(player, drop_item)
                    msg += f"\n🎁 لوط ویژه دریافتی: **{ITEMS[drop_item]['name']}**"

            if player['xp'] >= player.get('xp_needed', 100) and player.get('lvl', 1) < MAX_LEVEL:
                player['lvl'] = player.get('lvl', 1) + 1
                player['xp'] = 0
                player['xp_needed'] = int(player.get('xp_needed', 100) * 1.3)
                msg += f"\n⭐ **سطح شما افزایش یافت! سطح جدید: {player['lvl']}**"
            
            save_game()
            return await query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت به شهر", callback_data="town")]]), parse_mode='Markdown')

        if enemy.get('stunned', False):
            enemy['stunned'] = False
            enemy_action_log = "💫 دشمن گیج است و نمی‌تواند حمله کند!"
        else:
            e_atk = enemy['atk']
            if player.get('defending', False):
                e_atk = max(1, int(e_atk - p_def * 1.5))
                player['defending'] = False
            else:
                e_atk = max(1, int(e_atk - p_def))
            
            player['hp'] -= e_atk
            enemy_action_log = f"ضربات دشمن: {e_atk} آسیب به شما."

        if player['hp'] <= 0:
            player['state'] = 'TOWN'
            save_game()
            return await query.edit_message_text(text="💀 **شکست خوردید!**\nجان شما به پایان رسید و با حالی نزار به شهر بازگشتید.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت به شهر", callback_data="town")]]), parse_mode='Markdown')

        text = f"⚔️ **میدان نبرد**\n{action_log}\n{enemy_action_log}\n\n" \
               f"❤️ شما: {player['hp']}/{stats['max_hp']} | ⚡ انرژی: {player['energy']}/{stats['max_energy']}\n" \
               f"🖤 جان دشمن ({enemy['name']}): {enemy['hp']}"
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(await get_combat_keyboard(player)), parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u, c: show_town(u, c, u.message.from_user.id, is_new=True, is_text_msg=True)))
    app.add_handler(CommandHandler("gift", redeem_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 ربات با موفقیت روشن شد و در حال اجراست...")
    app.run_polling()

if __name__ == '__main__':
    main()
