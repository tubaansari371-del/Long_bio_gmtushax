from flask import Flask, request, jsonify, render_template
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
import requests
import re
import urllib.parse

app = Flask(__name__)

@@ -17,34 +18,35 @@
except ImportError:
    print("⚠ config.py not found, using defaults")
    SITE_CONFIG = {
        "site_name": "GM TUSHARX",
        "site_name": "GM TUSHAR BIO TOOL",
        "site_logo_emoji": "⚡",
        "freefire_version": "OB53",
        "youtube_link": "https://youtube.com/@gm_tushar_14?si=rpUZvKCm91LSWyxR",
        "instagram_link": "https://www.instagram.com/_gmtusharx_?igsh=MXJuZ2M1NzdlbmVmcA==",
        "popup_title": "⚡ JOIN THE COMMUNITY ⚡",
        "popup_message": "Subscribe to YouTube & Follow on Instagram to unlock the Bio Injector!",
        "bio_char_limit": 300,
        "youtube_link": "https://youtube.com",
        "instagram_link": "https://instagram.com",
        "telegram_link": "https://t.me/yourchannel",
        "popup_title": "JOIN COMMUNITY",
        "popup_message": "Follow us!",
        "bio_char_limit": 280,
        "default_region": "IND",
        "footer_text": "FREE FIRE • Long Bio Injector"
        "footer_text": "FF BIO TOOL",
        "howto_youtube_link": "https://youtu.be/your-tutorial",
        "howto_button_text": "📺 Watch Tutorial",
        "create_own_site_link": "https://youtu.be/create-site-tutorial",
        "templates": [],
        "regions": [],
        "v_badges": [],
        "colors": [],
        "gradients": []
    }

app.config['SITE_CONFIG'] = SITE_CONFIG

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Protobuf setup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Protobuf setup (same as before)
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage\"\x0e\n\x0c\x45mptyMessageb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data1_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_DATA']._serialized_start = 15
    _globals['_DATA']._serialized_end = 202
    _globals['_EMPTYMESSAGE']._serialized_start = 204
    _globals['_EMPTYMESSAGE']._serialized_end = 218

Data = _sym_db.GetSymbol('Data')
EmptyMessage = _sym_db.GetSymbol('EmptyMessage')
@@ -53,9 +55,6 @@
key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])




def get_region_url(region):
    region_urls = {
        "IND": "https://client.ind.freefiremobile.com",
@@ -66,12 +65,10 @@
        "ME": "https://clientbp.common.ggbluefox.com",
        "TH": "https://clientbp.common.ggbluefox.com"
    }
    return region_urls.get(region, "https://clientbp.ggblueshark.com")
    return region_urls.get(region.upper(), "https://clientbp.ggblueshark.com")

def get_account_from_eat(eat_token):
    """Get JWT and account info from EAT token (API hidden from user)"""
    try:
        # Clean token from URL if needed
        if '?eat=' in eat_token:
            parsed = urllib.parse.urlparse(eat_token)
            params = urllib.parse.parse_qs(parsed.query)
@@ -81,6 +78,7 @@
            if match:
                eat_token = match.group(1)

        EAT_API_URL = "https://eat-api.thory.buzz/api"
        response = requests.get(f"{EAT_API_URL}?eatjwt={eat_token}", timeout=15)

        if response.status_code != 200:
@@ -102,15 +100,10 @@

        return jwt_token, account_info, None

    except requests.exceptions.Timeout:
        return None, None, "Request timeout - please try again"
    except requests.exceptions.ConnectionError:
        return None, None, "Connection error - check your network"
    except Exception as e:
        return None, None, str(e)

def update_bio_with_jwt(jwt_token, bio_text, region):
    """Update bio using JWT token"""
    try:
        base_url = get_region_url(region)
        url_bio = f"{base_url}/UpdateSocialBasicInfo"
@@ -157,18 +150,14 @@
    except Exception as e:
        raise Exception(str(e))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Routes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
@app.route('/page')
def index():
    return render_template('index.html', config=SITE_CONFIG)

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    """Step 1: Verify EAT token and return account info"""
    try:
        data = request.get_json()
        eat_token = data.get('eat_token')
@@ -185,19 +174,17 @@
            "success": True,
            "account": {
                "uid": account_info.get('uid'),
                "region": account_info.get('region')
                "region": account_info.get('region'),
                "nickname": account_info.get('nickname')
            },
            "jwt_token": jwt_token
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
EAT_API_URL = "https://eat-api.thory.buzz/api"

@app.route('/api/update-bio', methods=['POST'])
def update_bio():
    """Step 2: Update bio using verified JWT"""
    try:
        data = request.get_json()
        jwt_token = data.get('jwt_token')