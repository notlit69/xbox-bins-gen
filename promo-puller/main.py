import requests
import time
import json

request_exceptions = (requests.exceptions.ProxyError,requests.exceptions.SSLError,requests.exceptions.Timeout)
if not json.load(open("config.json"))["proxy"]=="":
    proxies = {"https":json.load(open("config.json"))["proxy"]}
else:
    proxies=None

def remove_content(filename: str, delete_line: str) -> None:
        with open(filename, "r+") as io:
            content = io.readlines()
            io.seek(0)
            for line in content:
                if not (delete_line in line):
                    io.write(line)
            io.truncate()
def puller(ms_creds : str)-> None:
    try:
        getAuth = requests.post("http://127.0.0.1:1337/", json={"user": ms_creds.split("|")[0], "pass": ms_creds.split("|")[1]})
        headers = {"authorization":getAuth.text.replace('"','')}
    except:
        print("[-] Error sending request to pull promo [Make sure the promo server is running]","y")
        return 
    while True:
        try:
            getLink = requests.post("https://profile.gamepass.com/v2/offers/47D97C390AAE4D2CA336D2F7C13BA074",headers=headers,proxies=proxies)
            break
        except request_exceptions:
            continue
        except Exception as e:
            print(e,"r")
            return
    if getLink.status_code==500:
        print("[-] Microsoft internal server error!","c")
        remove_content("accs.txt",ms_creds)
        return
    if getLink.status_code==429:
        print("[!] You are being rate limited!")
        print("[!] Sleeping for 5 minutes...")
        time.sleep(300)
    try:
        link = getLink.json()["resource"]
    except:
        print(f"[!] Failed to fetch code! Response text : {getLink.text} status code : {getLink.status_code}")
        remove_content("accs.txt",ms_creds)
    print(link)
    open("promos.txt","a").write(link+"\n")

for l in open("accs.txt").read().splitlines():
    puller(l)

print("[+] Finished!")
