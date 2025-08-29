#!/usr/bin/env python3
# Direwolf APRS log parser to email
# written by Craig Snedden MM0NBW
# Edit where shown for own system

import os
import sys
import time
import math
import smtplib
import datetime
import pandas as pd
import numpy as np
from pytz import UTC
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------- Configuration ----------------------
# ---- Change these values for your own system -----

QTH_LAT = 56.000000
QTH_LON = -2.000000
DIST_THRESHOLD = 90  # miles
MAX_DISTANCE = 2000 # miles
REPORT_INTERVAL = 30  # minutes
RESEND_INTERVAL = 1800  # seconds

LOG_DIR = '/var/log/direwolf'
MAIL_LOG = '/home/pi/Documents/emaillog.txt'
DW_TEXT = '/home/pi/Documents/dwtext.txt'  #This is a dynamic file with the text that will be TX OTA by Direwolf

EMAIL_FROM = 'mail@mail.xxx'
EMAIL_PASSWORD = 'xxxxxxxxxx'  # consider using env vars or secrets manager
EMAIL_RECIPIENTS = ['recipient1@mail.xxx', 'recipient2@mail.xxx']

# ---------------------- Utility Functions ----------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def bearing(lat1, lon1, lat2, lon2):
    lat1, lat2 = map(np.radians, [lat1, lat2])
    dlon = np.radians(lon2 - lon1)
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1)*np.sin(lat2) - np.sin(lat1)*np.cos(lat2)*np.cos(dlon)
    brng = np.degrees(np.arctan2(x, y))
    return (brng + 360) % 360

def deg_to_cardinal(deg):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return dirs[int((deg + 11.25) % 360 / 22.5)]

def should_send_email():
    if not os.path.exists(MAIL_LOG):
        return True
    with open(MAIL_LOG, 'r') as f:
        last_line = f.readlines()[-1].strip()
    last_time = datetime.datetime.strptime(last_line, '%Y%m%d_%H:%M:%S')
    return (datetime.datetime.now() - last_time).total_seconds() > RESEND_INTERVAL

def log_email_timestamp():
    with open(MAIL_LOG, 'a') as f:
        f.write(datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S') + '\n')

def build_email(html_content):
    msg = MIMEMultipart()
    msg['Subject'] = "xxxx APRS DX report"
    msg['From'] = EMAIL_FROM
    msg.attach(MIMEText(html_content, 'html'))
    return msg

def send_email(msg):
    server = smtplib.SMTP_SSL('smtp.xxx.com', 465) # set for your system
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_RECIPIENTS, msg.as_string())
    server.quit()

# ---------------------- Main Logic ----------------------

def main():
    today = datetime.date.today().strftime('%Y-%m-%d')
    log_path = os.path.join(LOG_DIR, f"{today}.log")

    if not os.path.exists(log_path):
        sys.exit()

    if os.path.exists(DW_TEXT) and time.time() - os.path.getmtime(DW_TEXT) > 5400:
        os.remove(DW_TEXT)

    df = pd.read_csv(log_path, encoding="ISO-8859-1")
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce').fillna(QTH_LAT)
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce').fillna(QTH_LON)

    df['distance'] = haversine(QTH_LAT, QTH_LON, df['latitude'], df['longitude']).round(2)
    df['bearing'] = bearing(QTH_LAT, QTH_LON, df['latitude'], df['longitude']).round().astype(int)
    df['direction'] = df['bearing'].apply(deg_to_cardinal)

    now = datetime.datetime.now(UTC)
    df['isotime'] = pd.to_datetime(df['isotime'], errors='coerce')

    # If isotime is naive, localize to UTC; if aware, convert to UTC
    if df['isotime'].dt.tz is None:
        df['isotime'] = df['isotime'].dt.tz_localize(UTC)
    else:
        df['isotime'] = df['isotime'].dt.tz_convert(UTC)

    df['timenow'] = now
    df['diffmins'] = (df['timenow'] - df['isotime']).dt.total_seconds() / 60
    df['timefilt'] = df['diffmins'] < REPORT_INTERVAL

    
    filtered = df[
    (df['distance'] > DIST_THRESHOLD) &
    (df['distance'] < MAX_DISTANCE) &
    (df['timefilt'])
    ]
    report = filtered[["isotime", "source", "heard", "comment", "distance", "bearing", "direction"]]

    if report.empty or not should_send_email():
        sys.exit()

    log_email_timestamp()

    if not os.path.exists(DW_TEXT):
        with open(DW_TEXT, 'w') as f:
            f.write(':BLNXXX  :Possible 2 metre DX. xxx RX +100 miles')

    html = f"""
    <html>
        <body>
            <p>DX stations heard by XXXX since 00:00 today.<br>Distance > {DIST_THRESHOLD} miles</p>
            <p><a href="http://your-dashboard-URL">xxx Dashboard</a></p>
            <p>isotime is UTC</p>
            {report.to_html()}
            <p>dwrxdx report script by MM0NBW</p>
        </body>
    </html>
    """

    msg = build_email(html)
    send_email(msg)

if __name__ == "__main__":
    main()