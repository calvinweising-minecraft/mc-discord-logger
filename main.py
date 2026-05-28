from ftplib import FTP
import time
import requests

# =========================
# FTP DATEN
# =========================

FTP_HOST = "DEIN_HOST"
FTP_USER = "DEIN_USER"
FTP_PASS = "DEIN_PASS"

# =========================
# DISCORD WEBHOOK
# =========================

WEBHOOK = "DEIN_WEBHOOK"

# =========================

LOG_PATH = "/logs/latest.log"

last_text = ""

print("Logger gestartet")

while True:
    try:
        ftp = FTP()
ftp.connect(FTP_HOST, 21, timeout=30)
ftp.login(FTP_USER, FTP_PASS)

ftp.set_pasv(True)

        lines = []

        ftp.retrlines(f"RETR {LOG_PATH}", lines.append)

        ftp.quit()

        text = "\n".join(lines)

        if text != last_text:

            new_part = text[len(last_text):]

            if new_part.strip():

                chunks = [new_part[i:i+1800] for i in range(0, len(new_part), 1800)]

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
