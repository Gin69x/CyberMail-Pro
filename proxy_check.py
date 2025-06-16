import requests

def is_proxy_working(proxy):
    try:
        response = requests.get("https://httpbin.org/ip", proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Read proxies from file
with open("proxies.txt", "r") as f:
    proxies = [line.strip() for line in f if line.strip()]

working_proxies = []
x=0

# Check each proxy
for proxy in proxies:
    x+=1
    print(f"{x}. Checking {proxy}...")
    if is_proxy_working(proxy):
        print(f"✅ Working: {proxy} \n")
        working_proxies.append(proxy)
    else:
        print(f"❌ Not working: {proxy} \n")

# Save only working proxies
with open("working_proxies.txt", "w") as f:
    for proxy in working_proxies:
        f.write(proxy + "\n")
