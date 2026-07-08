import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import requests
import asyncio
import json
from datetime import datetime, timedelta
import os
import re
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))

# ============ KONFIGURASI SERVER FIVEM ============
FIVEM_SERVERS = [
    {
        'id': 'cerita',
        'alias': ['cr', 'cerita'],
        'name': 'CR Roleplay 2.0',
        'ip': '49.128.187.106',
        'port': 30120,
        'connect': 'play.ceritaroleplayku.id',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/kr7k7d/577531329.png',
        'banner': 'https://ceritaroleplayku.id/cdn/banner.gif',
        'max_players': 1000
    },
    {
        'id': 'rumahkita',
        'alias': ['rk', 'rumahkita'],
        'name': 'Rumah Kita Roleplay',
        'ip': '49.128.187.86',
        'port': 30120,
        'connect': '49.128.187.86',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/bdx4lql/-362622762.png',
        'banner': 'https://i.imgur.com/YwwgqED.gif',
        'max_players': 828
    },
    {
        'id': 'kisahnusantara',
        'alias': ['kn', 'kisahnusantara'],
        'name': 'Kisah Nusantara Roleplay',
        'ip': '49.128.187.82',
        'port': 30120,
        'connect': '49.128.187.82:30120',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/gad5d7z/1411448061.png',
        'banner': 'https://raw.githubusercontent.com/ItsMeD4N/server-image/main/Banner.gif',
        'max_players': 500
    },
    {
        'id': 'moxie',
        'alias': ['mr', 'moxie'],
        'name': 'Moxie Roleplay',
        'ip': '49.128.187.74',
        'port': 30120,
        'connect': '49.128.187.74',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/qqa4y56/-2144017187.png',
        'banner': 'https://moxieroleplay.com/benner_atas.gif',
        'max_players': 888
    },
    {
        'id': 'bedaalam',
        'alias': ['ba', 'bedalam'],
        'name': 'Beda Alam Roleplay',
        'ip': '151.243.226.107',
        'port': 30120,
        'connect': 'cfx.re/join/amavek',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/amavek/-1359723291.png',
        'banner': 'https://r2.fivemanage.com/4OlIA4xGJFcA4SLA2hHkh/babanner.gif',
        'max_players': 888
    },
    {
        'id': 'satumimpi',
        'alias': ['sm', 'satumimpi'],
        'name': 'Satu Mimpi Roleplay',
        'ip': '49.128.187.46',
        'port': 30120,
        'connect': '49.128.187.82:30120',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/6gk4e4/142087119.png',
        'banner': 'https://i.ibb.co.com/gZnqLy52/banner.png',
        'max_players': 1000
    },
    {
        'id': 'garudaprime',
        'alias': ['gp', 'garudaprime'],
        'name': 'Garuda Prime Roleplay Indonesia',
        'ip': '49.128.187.58',
        'port': 30120,
        'connect': '49.128.187.82:30120',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/vgaqm5/299692501.png',
        'banner': 'https://r2.fivemanage.com/7G09CHGGrHzXExaewC5Z6/foto_loading_screen_dan_logo/GP_-_Banner_Screen.gif',
        'max_players': 1000
    },
    {
        'id': 'nusav',
        'alias': ['nv', 'nusav'],
        'name': 'Nusa V  Roleplay Indonesia',
        'ip': '49.128.187.110',
        'port': 30120,
        'connect': 'main.nusav.id',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/ele3bm/-171954672.png',
        'banner': 'https://r2.fivemanage.com/cyuKcqPPPVZbYFgiHZjyx/nusa_banner.gif',
        'max_players': 600
    },
    {
        'id': 'indopride',
        'alias': ['idp', 'indopride'],
        'name': 'Indopride Roleplay Indonesia',
        'ip': 'kota.indopride.id',
        'port': 30120,
        'connect': 'kota.indopride.id',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/bak4pl/-824144304.png',
        'banner': 'https://img-cdn.indopride.id/bannerlist.gif',
        'max_players': 2048
    },
    {
        'id': 'lastparadise',
        'alias': ['lp', 'lastparadise'],
        'name': 'Last Paradise Roleplay Indonesia',
        'ip': '104.234.180.112',
        'port': 30120,
        'connect': 'lastparadiserp.site',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/eql83a/-1133439874.png',
        'banner': 'https://r2.fivemanage.com/mc4Azw9KvdgtCqssLt1Fg/BANNER_GERBANG.png',
        'max_players': 888
    },
    {
        'id': 'kampoengrp',
        'alias': ['krp', 'kampoengrp'],
        'name': 'Kampoeng Roleplay Indonesia',
        'ip': 'play.kampoeng.vhicloud.com',
        'port': 30120,
        'connect': '49.128.187.82:30120',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/55kd96/540036569.png',
        'banner': 'https://kampoeng.my.id/imageingame/serverlist.png',
        'max_players': 888
    },
    {
        'id': 'solaris',
        'alias': ['sr', 'solaris'],
        'name': 'Solaris Roleplay Indonesia',
        'ip': '103.42.116.171',
        'port': 30120,
        'connect': 'cfx-solarisrp.cdn-fivem.my.id',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/da5dzj/-517661413.png',
        'banner': 'https://imgproxy.cfx.re/iRg9Ynl8TljuQiiDMCTpDbOepvxpQ5L__6WQRvOriJA/f:webp/q:70/aHR0cHM6Ly9tZWRpYS5kaXNjb3JkYXBwLm5ldC9hdHRhY2htZW50cy8xNDY5MDI2Mzg4MzgzMTA5NDA0LzE0NzkwOTM2MzgyMzQzNzQyNDgvYmFubmVyXzEucG5nP2V4PTY5YWFjOGNiJmlzPTY5YTk3NzRiJmhtPTc3OTllZWQ0NjliMTk1NmM2OGE5M2FkM2M0Y2M3MmRiNmQ1YThiMjljYjY2NWZhMGUxOWQ0MTliMWJlODRhNzUmPSZmb3JtYXQ9d2VicCZxdWFsaXR5PWxvc3NsZXNzJndpZHRoPTEzMzAmaGVpZ2h0PTE3OQ.webp',
        'max_players': 64
    },
    {
        'id': 'executive',
        'alias': ['exe', 'executive'],
        'name': 'Executive',
        'ip': '49.128.187.50',
        'port': 30120,
        'connect': 'cfx-solarisrp.cdn-fivem.my.id',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/roek67/1203606197.png',
        'banner': 'https://img.tutustk.dev/exe/exe_banner_detail.gif',
        'max_players': 1024
    },
    {
        'id': 'ime',
        'alias': ['ime'],
        'name': 'Ime Roleplay',
        'ip': 'main.imeroleplay.com',
        'port': 30120,
        'connect': 'main.imeroleplay.com',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/zrvmg4/-1132135871.png',
        'banner': 'https://r2.fivemanage.com/3OwGU5Pi8eHUKktx99jNa/imebanner.gif',
        'max_players': 2048
    },
    {
        'id': 'ceritakita',
        'alias': ['ckrp', 'ceritakita'],
        'name': 'Cerita Kita Roleplay',
        'ip': '49.128.187.42',
        'port': 30120,
        'connect': '49.128.187.42',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/zxmea5/932083279.png',
        'banner': 'https://r2.fivemanage.com/pMA0ekV3sPved8KVE0xBj/ServerProfile_Banner_CKRP_1.png',
        'max_players': 555
    },
    {
        'id': 'kisahbaru',
        'alias': ['ksb','kisbar'],
        'name': 'Kisah Baru Roleplay',
        'ip': '103.42.116.156',
        'port': 31968,
        'connect': '31.58.143.187',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/8emplj4/-137382032.png  ',
        'banner': 'https://ninky.starstrix.my.id/assets/strix/kisahbaru-banner.png',
        'max_players': 128
    },
    {
        'id': 'kotabaru',
        'alias': ['kb','kotbar'],
        'name': 'KotaBaru Roleplay',
        'ip': '51.79.201.132',
        'port': 10120,
        'connect': '31.58.143.187',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/mez5p7/1163679694.png',
        'banner': 'https://i.ibb.co.com/2P2Yc2n/banner-kb.gif',
        'max_players': 128
    },
    {
        'id': 'vmachi',
        'alias': ['vm','vmachi'],
        'name': 'VMachi Roleplay',
        'ip': '40.27.47.155',
        'port': 30120,
        'connect': '40.27.47.155',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/6my3348/-810602729.png',
        'banner': '',
        'max_players': 128
    },
    {
        'id': 'temanmain',
        'alias': ['tm','temanmain'],
        'name': 'Teman Main Roleplay',
        'ip': '204.10.193.53',
        'port': 30120,
        'connect': '204.10.193.53',
        'logo': 'https://frontend.cfx-services.net/api/servers/icon/rmavmzx/-2012019943.png',
        'banner': '',
        'max_players': 128
    },
]

# ============ PREMIUM SYSTEM ============
premium_data = {
    'active': False,
    'user_id': None,
    'level': None,  
    'server_id': None,  
    'start_date': None,
    'end_date': None,
    'days': 0,
    'activated_by': None
}

PREMIUM_FILE = 'premium_data.json'

def save_premium_data():
    with open(PREMIUM_FILE, 'w') as f:
        json.dump(premium_data, f, default=str)

def load_premium_data():
    global premium_data
    if os.path.exists(PREMIUM_FILE):
        try:
            with open(PREMIUM_FILE, 'r') as f:
                loaded = json.load(f)
                if loaded.get('start_date'):
                    loaded['start_date'] = datetime.fromisoformat(loaded['start_date'])
                if loaded.get('end_date'):
                    loaded['end_date'] = datetime.fromisoformat(loaded['end_date'])
                premium_data.update(loaded)
        except:
            pass

load_premium_data()

def is_premium():
    if not premium_data['active']:
        return False
    if premium_data['end_date'] and datetime.now() > premium_data['end_date']:
        premium_data['active'] = False
        save_premium_data()
        return False
    return True

def get_premium_level():
    if is_premium():
        return premium_data.get('level', 'gold')
    return None

def can_access_server(server_id):
    """Cek apakah user bisa akses server tertentu"""
    if not is_premium():
        return False
    
    level = premium_data.get('level', 'gold')
    
    if level == 'platinum':
        return True  
    
    if level == 'gold':
        return premium_data.get('server_id') == server_id  
    
    return False

def get_premium_server_name():
    if not is_premium():
        return None
    server_id = premium_data.get('server_id')
    if server_id:
        for server in FIVEM_SERVERS:
            if server['id'] == server_id:
                return server['name']
    return None

# ============ CUSTOM EMOJI ============
SIGNAL_HIJAU = '<:HIJAU:1524261565723967641>'
SIGNAL_KUNING = '<:KUNING:1524261567603146802>'
SIGNAL_ORANGE = '<:ORANGE:1524261569058312223>'
SIGNAL_RED = '<:RED:1524261571273167019>'

COLOR_HIJAU = 0x2ECC71
COLOR_KUNING = 0xF1C40F
COLOR_ORANGE = 0xE67E22
COLOR_MERAH = 0xE74C3C

ITEMS_PER_PAGE = 19

def get_signal(ping):
    if ping <= 50:
        return SIGNAL_HIJAU
    elif ping <= 100:
        return SIGNAL_KUNING
    elif ping <= 200:
        return SIGNAL_ORANGE
    else:
        return SIGNAL_RED

def get_ping_color(ping):
    if ping <= 50:
        return COLOR_HIJAU
    elif ping <= 100:
        return COLOR_KUNING
    elif ping <= 200:
        return COLOR_ORANGE
    else:
        return COLOR_MERAH

EMBED_COLOR = 0xFF0066

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ============ CACHE ============
cache = {}
CACHE_DURATION = 15
executor = ThreadPoolExecutor(max_workers=10)

# ============ FUNGSI AMBIL DATA ============
def fetch_server_data_sync(server_ip, server_port, server_id=None):
    # Fallback ke endpoint biasa (tanpa CFX API)
    try:
        players_url = f"http://{server_ip}:{server_port}/players.json"
        info_url = f"http://{server_ip}:{server_port}/info.json"
        
        players_data = []
        max_players = '?'
        online = False
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        
        # Ambil players
        for attempt in range(3):
            try:
                resp = requests.get(players_url, timeout=10, headers=headers)
                if resp.status_code == 200:
                    raw_data = resp.json()
                    for idx, player in enumerate(raw_data, 1):
                        name = player.get('name', 'Unknown')
                        name = name.replace('\x00', '').strip()
                        name = re.sub(r'[`|]', '', name)
                        if name:
                            players_data.append({
                                'no': idx,
                                'id': player.get('id', idx),
                                'name': name,
                                'ping': player.get('ping', 0)
                            })
                    
                    players_data.sort(key=lambda x: x['id'])
                    for idx, p in enumerate(players_data, 1):
                        p['no'] = idx
                    online = True
                    break
            except Exception as e:
                if attempt == 2:
                    print(f"Players error {server_ip}:{server_port} - {e}")
                continue
        
        # Ambil info
        for attempt in range(3):
            try:
                resp = requests.get(info_url, timeout=10, headers=headers)
                if resp.status_code == 200:
                    info = resp.json()
                    max_players = info.get('vars', {}).get('sv_maxClients', '?')
                    online = True
                    break
            except Exception as e:
                if attempt == 2:
                    print(f"Info error {server_ip}:{server_port} - {e}")
                continue
        
        return {
            'players': players_data,
            'max_players': max_players,
            'online': online
        }
        
    except Exception as e:
        print(f"Fetch error {server_ip}:{server_port} - {e}")
        return {
            'players': [],
            'max_players': '?',
            'online': False
        }

async def get_server_data_with_cache(server):
    cache_key = server['id']
    now = datetime.now().timestamp()
    
    if cache_key in cache:
        cached = cache[cache_key]
        if now - cached['timestamp'] < CACHE_DURATION:
            return cached['data']
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
        executor, 
        fetch_server_data_sync, 
        server['ip'], 
        server['port'],
        server['id']
    )
    
    cache[cache_key] = {
        'data': data,
        'timestamp': now
    }
    return data

# ============ FUNGSI PARSING ID ============
def parse_id_input(input_str):
    ids = set()
    parts = input_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            range_parts = part.split('-')
            try:
                start = int(range_parts[0])
                end = int(range_parts[1])
                for i in range(start, end + 1):
                    ids.add(i)
            except:
                pass
        else:
            try:
                ids.add(int(part))
            except:
                pass
    
    return sorted(ids)

# ============ FIND FIVEM SERVER ============
def find_fivem_server(identifier):
    identifier = identifier.lower().strip()
    for server in FIVEM_SERVERS:
        if server['id'] == identifier:
            return server
        for alias in server.get('alias', []):
            if alias == identifier:
                return server
    return None

# ============ FUNGSI MEMBUAT FIELD PLAYER ============
def create_player_fields(players, page, total_pages, total_players):
    if not players:
        return [{'name': 'Player List', 'value': '`Tidak ada pemain online`', 'inline': False}]
    
    fields = []
    current_field = ""
    field_num = 1
    start_num = 1
    
    for idx, player in enumerate(players, 1):
        no = str(player['no']).rjust(2)
        signal = get_signal(player['ping'])
        id_str = str(player['id']).rjust(3)
        name = player['name']
        ping = player['ping']
        if len(name) > 35:
            name = name[:32] + "..."
        
        line = f"`{no}` {signal} `{ping}ms` `{id_str}` **{name}**\n"
        
        if len(current_field) + len(line) > 1000 and current_field:
            end_num = idx - 1
            fields.append({
                'name': f"Player List ({start_num}-{end_num})",
                'value': current_field,
                'inline': False
            })
            current_field = line
            start_num = idx
            field_num += 1
        else:
            current_field += line
    
    if current_field:
        end_num = len(players)
        fields.append({
            'name': f"Player List ({start_num}-{end_num})",
            'value': current_field,
            'inline': False
        })
    
    return fields

# ============ PAGINATION VIEW ============
class PlayerPaginationView(View):
    def __init__(self, players, server, page=1, items_per_page=19):
        super().__init__(timeout=60)
        self.players = players
        self.server = server
        self.page = page
        self.items_per_page = items_per_page
        self.total_pages = (len(players) + items_per_page - 1) // items_per_page if players else 1
        
    def get_embed(self, page):
        start = (page - 1) * self.items_per_page
        end = min(start + self.items_per_page, len(self.players))
        page_players = self.players[start:end]
        total_players = len(self.players)
        
        try:
            max_players = int(self.server.get('max_players', 1000))
            occupancy = round((total_players / max_players) * 100) if max_players > 0 else 0
        except:
            occupancy = '?'
        
        embed = discord.Embed(
            title=f"💎 {self.server['name']}",
            color=EMBED_COLOR,
            timestamp=datetime.now()
        )
        
        connect_text = f"```\nconnect {self.server.get('connect', self.server['ip'])}\n```"
        
        embed.add_field(
            name="Status",
            value=f"Online: {total_players}/{self.server.get('max_players', '?')}\nOccupancy: {occupancy}%\n{connect_text}",
            inline=False
        )
        
        fields = create_player_fields(page_players, page, self.total_pages, total_players)
        for field in fields:
            embed.add_field(**field)
        
        if self.server.get('logo'):
            embed.set_thumbnail(url=self.server['logo'])
        
        if self.server.get('banner'):
            embed.set_image(url=self.server['banner'])
        
        embed.set_footer(text=f"Gunakan tombol navigasi • {total_players} total pemain")
        
        return embed
    
    @discord.ui.button(label='◀ Sebelumnya', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
            await self.update_message(interaction)
    
    @discord.ui.button(label='Halaman', style=discord.ButtonStyle.secondary, disabled=True)
    async def page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
    
    @discord.ui.button(label='Selanjutnya ▶', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.total_pages:
            self.page += 1
            await self.update_message(interaction)
    
    async def update_message(self, interaction):
        embed = self.get_embed(self.page)
        self.page_button.label = f'{self.page}/{self.total_pages}'
        await interaction.response.edit_message(embed=embed, view=self)

# ============ PERINTAH BOT ============
@bot.event
async def on_ready():
    print(f'Bot {bot.user} sudah aktif!')
    print(f'Memantau {len(FIVEM_SERVERS)} server FiveM')
    
    # Test koneksi ke server
    print('🔄 Testing koneksi ke server...')
    for server in FIVEM_SERVERS:
        try:
            data = await get_server_data_with_cache(server)
            if data and data['online']:
                print(f'✅ {server["name"]} - Online ({len(data["players"])} pemain)')
            else:
                print(f'❌ {server["name"]} - Offline')
        except Exception as e:
            print(f'❌ {server["name"]} - Error: {e}')
    
    if is_premium():
        level = premium_data.get('level', 'gold').upper()
        server_name = get_premium_server_name() or 'Semua Server'
        print(f'💎 Premium {level} aktif untuk User ID: {premium_data["user_id"]}')
        print(f'   Server: {server_name}')
        print(f'   Sisa: {(premium_data["end_date"] - datetime.now()).days} hari')
    else:
        print('❌ Tidak ada premium aktif')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="ServerSeeker"
        ),
        status=discord.Status.online
    )

# ============ !SERVER ============
@bot.command(name='server')
async def server_list(ctx):
    embed = discord.Embed(
        title='📋 Server Directory',
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    
    sorted_servers = sorted(FIVEM_SERVERS, key=lambda x: x['name'].lower())
    
    for server in sorted_servers:
        alias_list = ', '.join(server.get('alias', []))
        embed.add_field(
            name=f"🖥️ {server['name']}",
            value=f"**Query:** `{alias_list}`",
            inline=False
        )
    
    embed.set_footer(text='Gunakan !player <query> untuk melihat pemain')
    await ctx.send(embed=embed)

# ============ !SERVERSTATUS ============
@bot.command(name='serverstatus')
async def server_status(ctx):
    if not is_premium():
        embed = discord.Embed(
            title="🔒 Akses Terkunci",
            description="Fitur ini hanya untuk pengguna premium.",
            color=0xE74C3C
        )
        embed.add_field(
            name="💎 Cara Aktivasi",
            value="Gunakan `!premiumlist` untuk melihat panduan aktivasi premium",
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title='📡 Status Server',
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    
    online = 0
    total_players = 0
    status_list = []
    
    for server in FIVEM_SERVERS:
        # Cek akses untuk Gold
        if not can_access_server(server['id']):
            continue
        
        data = await get_server_data_with_cache(server)
        
        if not data['online']:
            status_list.append(f"❌ **{server['name']}**\n└ Status: `Offline`")
        else:
            online += 1
            player_count = len(data['players'])
            total_players += player_count
            max_players = data.get('max_players', '?')
            
            try:
                max_int = int(max_players)
                percent = round((player_count / max_int) * 100)
                status_list.append(
                    f"▶️ **{server['name']}**\n"
                    f"`{player_count}/{max_players}` pemain  `{percent}%`"
                )
            except:
                status_list.append(
                    f"▶️ **{server['name']}**\n"
                    f"`{player_count}/{max_players}` pemain"
                )
    
    if not status_list:
        embed.add_field(
            name="",
            value="Tidak ada server yang dapat diakses.\nGold: hanya 1 server pilihan\nPlatinum: semua server",
            inline=False
        )
    else:
        embed.add_field(
            name="",
            value="\n\n".join(status_list) if status_list else "Tidak ada data",
            inline=False
        )
    
    level = premium_data.get('level', 'gold').upper()
    embed.set_footer(text=f"💎 {level} Active • {online}/{len(FIVEM_SERVERS)} online | Total: {total_players} pemain")
    await ctx.send(embed=embed)

# ============ !PLAYER ============
@bot.command(name='player')
async def player_command(ctx, server_id: str, *, query: str = None):
    async with ctx.typing():
        if not is_premium():
            embed = discord.Embed(
                title="🔒 Akses Terkunci",
                description="Fitur ini hanya untuk pengguna premium.",
                color=0xE74C3C
            )
            embed.add_field(
                name="💎 Cara Aktivasi",
                value="Gunakan `!premiumlist` untuk melihat panduan aktivasi premium",
                inline=False
            )
            await ctx.send(embed=embed)
            return
        
        target_server = find_fivem_server(server_id)
        
        if not target_server:
            embed = discord.Embed(
                title="Server tidak ditemukan",
                description=f"Server `{server_id}` tidak ditemukan.\nGunakan `!server` untuk melihat daftar.",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return
        
        # Cek akses untuk Gold
        if not can_access_server(target_server['id']):
            level = premium_data.get('level', 'gold').upper()
            embed = discord.Embed(
                title="🔒 Server Tidak Tersedia",
                description=f"Premium **{level}** hanya bisa mengakses server terpilih.",
                color=0xE74C3C
            )
            if level == 'GOLD':
                premium_server = get_premium_server_name() or 'Tidak ada'
                embed.add_field(
                    name="📌 Server Premium Anda",
                    value=f"**{premium_server}**\n\n💡 Upgrade ke Platinum untuk akses semua server!",
                    inline=False
                )
            await ctx.send(embed=embed)
            return
        
        data = await get_server_data_with_cache(target_server)
        
        if not data['online']:
            embed = discord.Embed(
                title=f"💎 {target_server['name']} - Offline",
                description="Server tidak dapat diakses atau sedang offline.",
                color=0xE74C3C
            )
            if target_server.get('logo'):
                embed.set_thumbnail(url=target_server['logo'])
            await ctx.send(embed=embed)
            return
        
        players = data['players']
        max_players = data['max_players']
        total_players = len(players)
        
        if query is None:
            if total_players == 0:
                embed = discord.Embed(
                    title=f"💎 {target_server['name']}",
                    color=EMBED_COLOR,
                    timestamp=datetime.now()
                )
                connect_text = f"```\nconnect {target_server.get('connect', target_server['ip'])}\n```"
                embed.add_field(
                    name="Status",
                    value=f"Online: 0/{max_players}\nOccupancy: 0%\n{connect_text}",
                    inline=False
                )
                embed.add_field(
                    name="Player List",
                    value="`Tidak ada pemain online`",
                    inline=False
                )
                if target_server.get('logo'):
                    embed.set_thumbnail(url=target_server['logo'])
                if target_server.get('banner'):
                    embed.set_image(url=target_server['banner'])
                await ctx.send(embed=embed)
                return
            
            view = PlayerPaginationView(players, target_server, page=1, items_per_page=ITEMS_PER_PAGE)
            embed = view.get_embed(1)
            view.page_button.label = f'1/{view.total_pages}'
            await ctx.send(embed=embed, view=view)
            return
        
        # ============ CEK APAKAH QUERY ID ============
        try:
            if re.match(r'^[\d,\-\s]+$', query):
                search_ids = parse_id_input(query)
                
                if search_ids:
                    found = []
                    not_found = []
                    
                    for search_id in search_ids:
                        player = next((p for p in players if p['id'] == search_id), None)
                        if player:
                            found.append(player)
                        else:
                            not_found.append(search_id)
                    
                    avg_ping = round(sum(p['ping'] for p in players) / len(players)) if players else 0
                    
                    embed = discord.Embed(
                        title=f"💎 {target_server['name']}",
                        color=get_ping_color(avg_ping) if found else 0xE74C3C,
                        timestamp=datetime.now()
                    )
                    
                    connect_text = f"```\nconnect {target_server.get('connect', target_server['ip'])}\n```"
                    
                    status_text = f"Online: {total_players}/{max_players}\n"
                    status_text += f"Cari ID: {query}\n"
                    status_text += f"Ditemukan: {len(found)} dari {len(search_ids)}\n"
                    status_text += connect_text
                    
                    if not_found:
                        status_text += f"\nID Tidak Ditemukan: {', '.join(map(str, not_found))}"
                    
                    embed.add_field(
                        name="Status",
                        value=status_text,
                        inline=False
                    )
                    
                    if found:
                        lines = []
                        for p in found[:30]:
                            no = str(p['no']).rjust(2)
                            signal = get_signal(p['ping'])
                            id_str = str(p['id']).rjust(3)
                            ping = p['ping']
                            lines.append(f"`{no}` {signal} `{ping}ms` `{id_str}` **{p['name']}**")
                        embed.add_field(
                            name=f"Player Ditemukan ({len(found)})",
                            value="\n".join(lines) if lines else "`Tidak ada`",
                            inline=False
                        )
                    else:
                        embed.add_field(
                            name="Player Ditemukan",
                            value="`Tidak ada pemain ditemukan`",
                            inline=False
                        )
                    
                    if target_server.get('logo'):
                        embed.set_thumbnail(url=target_server['logo'])
                    
                    if target_server.get('banner'):
                        embed.set_image(url=target_server['banner'])
                    
                    embed.set_footer(
                        text=f"Requested by {ctx.author.name} • {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                        icon_url=ctx.author.display_avatar.url
                    )
                    
                    await ctx.send(embed=embed)
                    return
        except:
            pass
        
        # ============ QUERY NAMA ============
        matches = [p for p in players if query.lower() in p['name'].lower()]
        
        if not matches:
            embed = discord.Embed(
                title=f"💎 {target_server['name']} ",
                description=f"Query: {query}\nOnline: {total_players} pemain\nHasil: 0 ditemukan",
                color=0xE74C3C,
                timestamp=datetime.now()
            )
            
            if target_server.get('logo'):
                embed.set_thumbnail(url=target_server['logo'])
            
            embed.set_footer(
                text=f"Requested by {ctx.author.name} • {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                icon_url=ctx.author.display_avatar.url
            )
            
            await ctx.send(embed=embed)
            return
        
        avg_ping = round(sum(p['ping'] for p in matches) / len(matches)) if matches else 0
        
        embed = discord.Embed(
            title=f"💎 {target_server['name']}",
            color=get_ping_color(avg_ping),
            timestamp=datetime.now()
        )
        
        connect_text = f"```\nconnect {target_server.get('connect', target_server['ip'])}\n```"
        
        embed.add_field(
            name="Status",
            value=f"Query: {query}\nOnline: {total_players} pemain\nHasil: {len(matches)} ditemukan\n{connect_text}",
            inline=False
        )
        
        lines = []
        for p in matches[:30]:
            no = str(p['no']).rjust(2)
            signal = get_signal(p['ping'])
            id_str = str(p['id']).rjust(3)
            ping = p['ping']
            lines.append(f"`{no}` {signal} `{ping}ms` `{id_str}` **{p['name']}**")

        embed.add_field(
            name=f"Player Ditemukan ({len(matches)})",
            value="\n".join(lines) if lines else "`Tidak ada`",
            inline=False
        )
        
        if target_server.get('logo'):
            embed.set_thumbnail(url=target_server['logo'])
        
        if target_server.get('banner'):
            embed.set_image(url=target_server['banner'])
        
        embed.set_footer(
            text=f"Requested by {ctx.author.name} • {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            icon_url=ctx.author.display_avatar.url
        )
        
        await ctx.send(embed=embed)

# ============ PERINTAH PREMIUM ============
@bot.command(name='premium')
@commands.is_owner()
async def premium_activate(ctx, level: str = None, days: int = None, server_id: str = None):
    """
    !premium <gold/platinum> <hari> <server_id> - Aktivasi premium
    Contoh: !premium gold 30 cerita
            !premium platinum 30 all
    """
    if level is None or days is None:
        embed = discord.Embed(
            title="Premium Activation",
            description="Gunakan: `!premium <level> <hari> <server_id>`\n\n**Level:**\n• `gold` - 1 server FiveM (Rp 25.000/bulan)\n• `platinum` - Semua server (Rp 100.000/bulan)\n\n**Contoh:**\n• `!premium gold 30 cerita`\n• `!premium platinum 30 all`\n\n**Server ID:**\nGunakan `!server` untuk melihat daftar server",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
        return
    
    if level.lower() not in ['gold', 'platinum']:
        await ctx.send("❌ Level harus `gold` atau `platinum`!")
        return
    
    if days <= 0:
        await ctx.send("❌ Hari harus lebih dari 0!")
        return
    
    # Untuk Gold, wajib pilih server
    if level.lower() == 'gold':
        if server_id is None or server_id.lower() == 'all':
            await ctx.send("❌ Gold memerlukan server_id tertentu!\nContoh: `!premium gold 30 cerita`")
            return
        
        target_server = find_fivem_server(server_id)
        if not target_server:
            await ctx.send(f"❌ Server `{server_id}` tidak ditemukan!\nGunakan `!server` untuk melihat daftar.")
            return
        server_id = target_server['id']
    else:
        server_id = 'all'
    
    premium_data['active'] = True
    premium_data['user_id'] = str(ctx.author.id)
    premium_data['level'] = level.lower()
    premium_data['server_id'] = server_id
    premium_data['start_date'] = datetime.now()
    premium_data['end_date'] = datetime.now() + timedelta(days=days)
    premium_data['days'] = days
    premium_data['activated_by'] = str(ctx.author.id)
    
    save_premium_data()
    
    # Format durasi
    if days == 1:
        durasi = "1 hari"
    elif days < 30:
        durasi = f"{days} hari"
    elif days == 30:
        durasi = "1 bulan"
    elif days < 365:
        bulan = days // 30
        sisa_hari = days % 30
        if sisa_hari == 0:
            durasi = f"{bulan} bulan"
        else:
            durasi = f"{bulan} bulan {sisa_hari} hari"
    elif days == 365:
        durasi = "1 tahun"
    else:
        tahun = days // 365
        sisa_hari = days % 365
        if sisa_hari == 0:
            durasi = f"{tahun} tahun"
        else:
            durasi = f"{tahun} tahun {sisa_hari} hari"
    
    server_display = 'Semua Server' if server_id == 'all' else target_server['name']
    
    embed = discord.Embed(
        title="✅ Premium Activated!",
        description=f"**Level:** {level.upper()}\n**Server:** {server_display}\n**Durasi:** {durasi} ({days} hari)\n**Aktif Sampai:** {premium_data['end_date'].strftime('%d/%m/%Y %H:%M')}",
        color=0xFF0066
    )
    embed.set_footer(text=f"Diaktivasi oleh {ctx.author.name}")
    await ctx.send(embed=embed)

# ============ !PREMIUMLIST ============
@bot.command(name='premiumlist')
async def premium_list(ctx):
    embed = discord.Embed(
        title="💎 Premium Plans",
        description="Aktivasi premium untuk mengakses bot!",
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="⭐ Gold — Rp 25.000 / bulan",
        value=(
            "✅ Akses **1 server FiveM** pilihan\n"
            "✅ Semua fitur player tracker\n"
            "✅ Cepat, tanpa delay\n"
            "✅ Bisa ganti server 1x per bulan\n\n"
            "**Cocok untuk:** Memantau 1 server favorit"
        ),
        inline=False
    )
    
    embed.add_field(
        name="👑 Platinum — Rp 100.000 / bulan",
        value=(
            "✅ Akses **SEMUA server** yang terdaftar\n"
            "✅ Semua fitur player tracker\n"
            "✅ Cepat, tanpa delay\n"
            "✅ Bisa ganti server kapan saja\n\n"
            "**Cocok untuk:** Owner komunitas, partner, multi-server"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🆓 FREE",
        value=(
            "✅ `!server` - Lihat daftar server\n"
            "✅ `!commands` - Lihat semua perintah\n"
            "✅ `!premiumlist` - Info harga & aktivasi\n"
            "❌ `!player` - Tidak bisa (terkunci)\n"
            "❌ `!serverstatus` - Tidak bisa (terkunci)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📌 Cara Aktivasi",
        value=(
            "1. Transfer ke rekening berikut:\n"
            "   • Bank BCA: `123-456-7890`\n"
            "   • E-Wallet: `0812-3456-7890`\n"
            "2. Kirim bukti transfer ke owner\n"
            "3. Owner akan aktivasi premium"
        ),
        inline=False
    )
    
    # Tampilkan status premium user saat ini
    if is_premium():
        level = premium_data.get('level', 'gold').upper()
        server_display = get_premium_server_name() or 'Semua Server' if premium_data.get('server_id') == 'all' else 'Semua Server'
        embed.add_field(
            name="💎 Status Premium Anda",
            value=f"**Level:** {level}\n**Server:** {server_display}\n**Aktif sampai:** {premium_data['end_date'].strftime('%d/%m/%Y %H:%M')}",
            inline=False
        )
    
    embed.set_footer(text="Hubungi owner untuk aktivasi premium")
    await ctx.send(embed=embed)

# ============ KONFIGURASI CHANNEL ============
# Daftar channel ID yang diizinkan untuk menggunakan bot
# Kosongkan [] untuk mengizinkan semua channel
ALLOWED_CHANNELS = []  # Contoh: [123456789012345678, 987654321098765432]

# File untuk menyimpan channel yang diizinkan
CHANNEL_FILE = 'allowed_channels.json'

def load_allowed_channels():
    global ALLOWED_CHANNELS
    if os.path.exists(CHANNEL_FILE):
        try:
            with open(CHANNEL_FILE, 'r') as f:
                ALLOWED_CHANNELS = json.load(f)
                print(f'✅ Channel whitelist dimuat: {len(ALLOWED_CHANNELS)} channel')
        except:
            ALLOWED_CHANNELS = []
    else:
        ALLOWED_CHANNELS = []
        save_allowed_channels()

def save_allowed_channels():
    global ALLOWED_CHANNELS
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(ALLOWED_CHANNELS, f, indent=4)

load_allowed_channels()

def is_channel_allowed(channel_id):
    """Cek apakah channel diizinkan"""
    if not ALLOWED_CHANNELS:
        return True  # Jika kosong, semua channel diizinkan
    return channel_id in ALLOWED_CHANNELS

# ============ CHECK CHANNEL ============
@bot.event
async def on_message(message):
    # Skip pesan dari bot
    if message.author.bot:
        return
    
    # Skip jika bukan command
    if not message.content.startswith('!'):
        return
    
    # Cek apakah channel diizinkan
    if not is_channel_allowed(message.channel.id):
        # Buat daftar channel yang diizinkan
        if ALLOWED_CHANNELS:
            channel_mentions = []
            for channel_id in ALLOWED_CHANNELS:
                ch = bot.get_channel(channel_id)
                if ch:
                    channel_mentions.append(ch.mention)
            
            if channel_mentions:
                allowed_text = ", ".join(channel_mentions)
            else:
                allowed_text = "Tidak ada channel yang diizinkan"
        else:
            allowed_text = "Semua channel diizinkan"
        
        embed = discord.Embed(
            title="🔒 Channel Tidak Diizinkan",
            description=f"Bot ini hanya dapat digunakan di channel: **{allowed_text}**",
            color=0xE74C3C
        )
        await message.channel.send(embed=embed, delete_after=10)
        return
    
    # Proses command
    await bot.process_commands(message)

# ============ !SETCHANNEL ============
@bot.command(name='setchannel')
@commands.is_owner()
async def set_channel(ctx, action: str = None, channel: discord.TextChannel = None):
    global ALLOWED_CHANNELS
    
    embed = discord.Embed(
        title="🔧 Channel Settings",
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    
    if action is None:
        embed.description = (
            "**Gunakan:**\n"
            "`!setchannel add #channel` - Tambah channel\n"
            "`!setchannel remove #channel` - Hapus channel\n"
            "`!setchannel list` - Lihat daftar channel\n"
            "`!setchannel clear` - Izinkan semua channel"
        )
        await ctx.send(embed=embed)
        return
    
    # ===== LIST =====
    if action.lower() == 'list':
        if not ALLOWED_CHANNELS:
            embed.description = "✅ **Semua channel diizinkan** (tidak ada pembatasan)"
            embed.color = 0x2ECC71
        else:
            channel_list = []
            for channel_id in ALLOWED_CHANNELS:
                ch = bot.get_channel(channel_id)
                if ch:
                    channel_list.append(f"• {ch.mention} (`{channel_id}`)")
                else:
                    channel_list.append(f"• Channel tidak ditemukan (`{channel_id}`)")
            
            embed.description = f"**Daftar Channel yang Diizinkan ({len(channel_list)})**\n\n" + "\n".join(channel_list)
            embed.color = 0x3498DB
        
        await ctx.send(embed=embed)
        return
    
    # ===== CLEAR =====
    if action.lower() == 'clear':
        ALLOWED_CHANNELS = []
        save_allowed_channels()
        embed.description = "✅ **Semua channel diizinkan** (pembatasan dihapus)"
        embed.color = 0x2ECC71
        await ctx.send(embed=embed)
        return
    
    # ===== ADD / REMOVE =====
    if channel is None:
        embed.description = f"❌ Harap mention channel!\nContoh: `!setchannel {action} #channel`"
        embed.color = 0xE74C3C
        await ctx.send(embed=embed)
        return
    
    # ADD
    if action.lower() == 'add':
        if channel.id in ALLOWED_CHANNELS:
            embed.description = f"⚠️ Channel {channel.mention} sudah ada di daftar!"
            embed.color = 0xF1C40F
        else:
            ALLOWED_CHANNELS.append(channel.id)
            save_allowed_channels()
            embed.description = f"✅ Channel {channel.mention} ditambahkan ke daftar izin!"
            embed.color = 0x2ECC71
        await ctx.send(embed=embed)
        return
    
    # REMOVE
    if action.lower() == 'remove':
        if channel.id not in ALLOWED_CHANNELS:
            embed.description = f"⚠️ Channel {channel.mention} tidak ada di daftar!"
            embed.color = 0xF1C40F
        else:
            ALLOWED_CHANNELS.remove(channel.id)
            save_allowed_channels()
            embed.description = f"✅ Channel {channel.mention} dihapus dari daftar izin!"
            embed.color = 0x2ECC71
        await ctx.send(embed=embed)
        return
    
    # Invalid action
    embed.description = f"❌ Aksi `{action}` tidak dikenal!\nGunakan: `add`, `remove`, `list`, `clear`"
    embed.color = 0xE74C3C
    await ctx.send(embed=embed)

# ============ !PREMIUMSTATUS ============
@bot.command(name='premiumstatus')
async def premium_status(ctx):
    if not is_premium():
        embed = discord.Embed(
            title="Premium Status",
            description="❌ Tidak ada premium yang aktif",
            color=0xE74C3C
        )
        embed.add_field(
            name="💎 Info",
            value="Gunakan `!premiumlist` untuk melihat panduan aktivasi",
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    end_date = premium_data['end_date']
    now = datetime.now()
    remaining = end_date - now
    
    days_left = remaining.days
    hours_left = remaining.seconds // 3600
    minutes_left = (remaining.seconds % 3600) // 60
    
    level = premium_data.get('level', 'gold').upper()
    server_display = get_premium_server_name() or 'Semua Server' if premium_data.get('server_id') == 'all' else 'Semua Server'
    
    embed = discord.Embed(
        title=f"💎 Premium Status ({level})",
        color=0xFF0066
    )
    
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Server", value=server_display, inline=True)
    embed.add_field(name="Durasi", value=f"{premium_data['days']} hari", inline=True)
    embed.add_field(name="Aktif Sampai", value=end_date.strftime('%d/%m/%Y %H:%M'), inline=False)
    embed.add_field(name="Sisa Waktu", value=f"{days_left} hari {hours_left} jam {minutes_left} menit", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='premiumdata')
async def premium_data_cmd(ctx):
    if not is_premium():
        await ctx.send("❌ Tidak ada premium yang aktif")
        return
    
    embed = discord.Embed(
        title="💎 Premium Data",
        color=0x9B59B6,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="User ID",
        value=f"`{premium_data['user_id']}`",
        inline=False
    )
    
    embed.add_field(
        name="Level",
        value=premium_data.get('level', 'gold').upper(),
        inline=False
    )
    
    server_display = get_premium_server_name() or 'Semua Server' if premium_data.get('server_id') == 'all' else 'Semua Server'
    embed.add_field(
        name="Server",
        value=server_display,
        inline=False
    )
    
    embed.add_field(
        name="Durasi",
        value=f"{premium_data['days']} hari",
        inline=False
    )
    
    embed.add_field(
        name="Aktif Sampai",
        value=premium_data['end_date'].strftime('%d/%m/%Y %H:%M'),
        inline=False
    )
    
    embed.add_field(
        name="Diaktivasi oleh",
        value=f"<@{premium_data['activated_by']}>",
        inline=False
    )
    
    await ctx.send(embed=embed)

# ============ !PREMIUMDEACTIVATE ============
@bot.command(name='premiumdeactivate')
@commands.is_owner()
async def premium_deactivate(ctx):
    if not is_premium():
        embed = discord.Embed(
            title="❌ Tidak Ada Premium Aktif",
            description="Tidak ada premium yang sedang aktif untuk dinonaktifkan.",
            color=0xE74C3C
        )
        await ctx.send(embed=embed)
        return
    
    old_user_id = premium_data['user_id']
    old_level = premium_data.get('level', 'gold').upper()
    old_days = premium_data['days']
    old_end_date = premium_data['end_date'].strftime('%d/%m/%Y %H:%M') if premium_data['end_date'] else 'Tidak diketahui'
    
    premium_data['active'] = False
    premium_data['user_id'] = None
    premium_data['level'] = None
    premium_data['server_id'] = None
    premium_data['start_date'] = None
    premium_data['end_date'] = None
    premium_data['days'] = 0
    premium_data['activated_by'] = None
    
    save_premium_data()
    
    embed = discord.Embed(
        title="✅ Premium Deactivated!",
        description=f"Premium **{old_level}** untuk User ID `{old_user_id}` telah dinonaktifkan.",
        color=0xE74C3C
    )
    embed.add_field(
        name="📊 Detail Sebelumnya",
        value=f"**Level:** {old_level}\n**Durasi:** {old_days} hari\n**Aktif Sampai:** {old_end_date}",
        inline=False
    )
    embed.set_footer(text=f"Dinonaktifkan oleh {ctx.author.name}")
    
    await ctx.send(embed=embed)

# ============ !COMMANDS ============
@bot.command(name='commands')
async def commands_list(ctx):
    embed = discord.Embed(
        title="Command List",
        description="Berikut adalah daftar perintah yang tersedia",
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    
    public_commands = (
        "`!commands` - Lihat commands ini\n"
        "`!premiumlist` - Info harga & aktivasi\n"
        "`!server` - Lihat daftar server"
    )
    embed.add_field(
        name="Public Commands",
        value=public_commands,
        inline=False
    )
    
    if is_premium():
        premium_commands = (
            "`!player <query>` - Lihat pemain di server\n"
            "`!player <query> <id>` - Cari pemain by ID\n"
            "`!player <query> <nama>` - Cari pemain by nama\n"
            "`!serverstatus` - Status semua server\n"
            "`!premiumstatus` - Status premium\n"
            "`!premiumdata` - Data premium"
        )
        level = premium_data.get('level', 'gold').upper()
        embed.add_field(
            name=f"Premium Commands",
            value=premium_commands,
            inline=False
        )
    else:
        embed.add_field(
            name="🔒 Premium Commands (Terkunci)",
            value="Aktivasi premium untuk mengakses commands ini\nGunakan `!premiumlist` untuk info",
            inline=False
        )
    
    if ctx.author.id == OWNER_ID:
        embed.add_field(
            name="Owner",
            value="`!premium <level> <hari> <server_id>` - Aktivasi premium\n`!premiumdeactivate` - Nonaktifkan premium\n`!setchannel add/remove/list/clear` - Atur channel bot",
            inline=False
        )
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

# ============ ERROR HANDLER ============
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("❌ Perintah ini hanya untuk owner bot!")
    else:
        print(f"Error: {error}")

# ============ TASK OTOMATIS ============
@tasks.loop(minutes=5)
async def update_status():
    total_players = 0
    online_servers = 0
    
    if is_premium():
        level = premium_data.get('level', 'gold').upper()
        for server in FIVEM_SERVERS:
            if can_access_server(server['id']):
                data = await get_server_data_with_cache(server)
                if data and data['online']:
                    online_servers += 1
                    total_players += len(data['players'])
        
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"💎 {level} • {total_players} pemain di {online_servers} server"
            )
        )
    else:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="ServerSeeker"
            ),
            status=discord.Status.online
        )

@update_status.before_loop
async def before_update_status():
    await bot.wait_until_ready()

# ============ JALANKAN BOT ============
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: Token bot tidak ditemukan!")
    else:
        print("Menjalankan FiveM Tracker Bot...")
        print(f"Cache: {CACHE_DURATION} detik")
        print(f"Items per page: {ITEMS_PER_PAGE}")
        print("💎 PREMIUM: !premium <gold/platinum> <hari> <server_id>")
        bot.run(BOT_TOKEN)
