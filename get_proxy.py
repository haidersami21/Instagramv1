import requests
import json

url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
output_file = "proxies.txt"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    data = response.json()

    proxies_list = []
    for proxy_info in data.get("data", []):
        if "protocols" in proxy_info and ("http" in proxy_info["protocols"] or "https" in proxy_info["protocols"]):
            proxies_list.append(f"{proxy_info['ip']}:{proxy_info['port']}")

    # Take up to 50 proxies, or all if less than 50
    proxies_to_save = proxies_list[:50]

    if proxies_to_save:
        with open(output_file, "w") as f:
            for proxy in proxies_to_save:
                f.write(proxy + "\n")
        print(f"Saved {len(proxies_to_save)} proxies to {output_file}")
    else:
        print("No suitable HTTP/HTTPS proxies found.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching proxy list: {e}")
except json.JSONDecodeError:
    print(f"Error decoding JSON from response: {response.text}")

