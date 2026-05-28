from ftplib import FTP
import time
import requests

# =========================
# FTP DATEN
# =========================

FTP_HOST = "185.213.25.183"
FTP_USER = "gptfp464180618425463668"
FTP_PASS = "33p3q95r"

# =========================
# DISCORD WEBHOOK
# =========================

WEBHOOK = "https://discord.com/api/webhooks/1509533335750316174/zurVksPoPakkvwZ2ycBpwAFcwScjn2avULdvGTE6d6_3hKDw98CtU-GojRxRNe6KSzMr"

# =========================

LOG_PATH = "logs/latest.log"

last_text = ""

print("Logger gestartet")

while True:
    try:
        ftp = FTP()

        ftp.connect(FTP_HOST, 32031, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)

        ftp.set_pasv(True)

        lines = []

        ftp.retrlines(f"RETR {LOG_PATH}", lines.append)

        ftp.quit()

        text = "\n".join(lines)

        print(text)

        r = requests.post(
            WEBHOOK,
            json={"content": "TEST NACHRICHT"}
        )

        print(r.status_code)
        print(r.text)

        if text != last_text:

            new_part = text[len(last_text):]

            if new_part.strip():

                chunks = [
                    new_part[i:i+1800]
                    for i in range(0, len(new_part), 1800)
                ]

                for chunk in chunks:
                    requests.post(
                        WEBHOOK,
                        json={
                            "content": f"```{chunk}```"
                        }
                    )

            last_text = text

    except Exception as e:
        print("Fehler:", e)

    time.sleep(10)
