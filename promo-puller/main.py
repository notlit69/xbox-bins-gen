import requests
import time
import threading
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
def puller(creds)-> None:
    try:
        getAuth = requests.post("http://127.0.0.1:1338", json={"user": creds.split("|")[0], "pass": creds.split("|")[1]})
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
        threading.Lock().acquire()
        print("[-] Microsoft internal server error!","c")
        # remove_content("emails.txt",ms_creds)
        threading.Lock().release()
        return
    if getLink.status_code==429:
        threading.Lock().acquire()
        print("[!] You are being rate limited!")
        print("[!] Sleeping for 5 minutes...")
        threading.Lock().release()
        time.sleep(300)
    try:
        link = getLink.json()["resource"]
    except:
        threading.Lock().acquire()
        print(f"[!] Failed to fetch code! Response text : {getLink.text} status code : {getLink.status_code}")
        remove_content("emails.txt",creds)
        threading.Lock().release()
        return
    threading.Lock().acquire()
    print(link)
    remove_content("emails.txt",creds)
    open("promos.txt","a").write(link+"\n")
    threading.Lock().release()
accs = open("accs.txt").read().splitlines()
threads = int(input("[?] Enter amount of threads -> "))

while len(accs) > 0:
    thread_lists = []
    for b in range(threads):
        acc = accs[0]
        start_thread = threading.Thread(target=puller,args=(acc,))
        thread_lists.append(start_thread)
        start_thread.start()
        accs.pop(0)
    for threads_ in thread_lists:
        threads_.join()

print("[-] Out of materials!")
