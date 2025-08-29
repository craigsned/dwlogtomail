# dwlogtomail
Direwolf APRS log to email
Project to take Direwolf APRS logs and send to email.

This is my first foray into any type of scripting.  There may be issues in the way this is coded and probably not the most efficient code.

Description of the files;

fulllog calculates distance and bearing to the source station, append distance and bearing as compass cardinal and outputs to html formatted email.  It is intended to run once a day to email the Direwolf log file in an easier to read format.

📡 APRS DX Alert Script — Summary
This Python script monitors your Direwolf APRS log file for long-distance packet receptions and automatically sends an email alert when stations are heard beyond a specified range.
🧭 Core Functionality:
- Reads the daily Direwolf log file from /var/log/direwolf/YYYY-MM-DD.log
- Extracts latitude and longitude from each packet (or substitutes your RX QTH if missing)
- Calculates distance and bearing from your RX station using geodesic math
- Filters for stations heard within the last 30 minutes and more than 90 miles away
- Determines compass direction (e.g., NE, SSW) from your QTH to the remote station
- Formats the filtered data into an HTML table for email presentation
- Throttles email alerts to avoid sending more than one every 30 minutes
- Writes a short DX message to a local file (dwtext.txt) if a new alert is triggered
- Sends an email via SMTP to your configured recipients
  
🛡 Reliability Features:
- Automatically deletes stale dwtext.txt files older than 90 minutes
- Skips processing if the log file doesn’t exist
- Skips sending if no qualifying DX entries are found
- Uses timezone-aware datetime handling to avoid timestamp errors
  
📤 Email Output:
- Subject: xxx APRS DX report
- Includes a link to your dashboard if you have one.
- Lists all stations heard today that exceed the distance threshold
- Notes that timestamps are in UTC


Email is set up to run through a gmail account using an app password.  See - https://support.google.com/mail/answer/185833?hl=en-GB for further information on this.  Email could easily be set up using other providers.


Pre-requisites.

Email account set up to send output.

Direwolf logging enabled (daily log, not rolling) - either command line or in direwolf.conf

Set your own parameters in the script for QTH, email addresses etc.  QTH must be the same as the Direwolf.conf entry to ensure accuracy.

------
Logic Flow

Set date and time - required to find today's log file

Set APRS receiver location - QTH

Set distance filter (for dxrx script)

Set time period to filter log - last 'n' minutes - helps prevent email sending continuously after being triggered if no new stations heard over 'n' distance.
(for dxrx script)

Set path to Direwolf log file

Set path to mail log file (for dxrx script)

Set path to Direwolf CBEACON text file (for dxrx script)

If Direwolf log file does not exist - exit

Read the Direwolf log file into a Pandas array

Check if the Direwolf CBEACON text file exists and if it is older than 'n' minutes delete it - prevent CBEACON from sending continuously once triggered.

Deal with instances where latitude is greater than 90 or less than -90 (otherwise this throws an error)

Deal with log entries with no location data by inserting receiver location (QTH) into lat and log fields in the Pandas array

Calculate the distance from receiver station (QTH) to source station and insert into new column in Pandas array

Filter the Pandas array according to distance filter (for dxrx script)

If filter results return no rows (i.e. nothing to report) exit

If filter has content;

Check the last time an email was sent (for dxalert script) - if less than (time) quit - this ensures emails are not continuously sent as the dxalert script runs in CRON.
The email log file must have an entry or this will cause the script to fail.  I set the entry for the log file using a separate script to clean up the file once
per day - remove all entries, then append current timestamp

Create the Direwolf CBEACON file (DW Text) and insert text.

Set the content for email from relevant fields in the Panda array

Log current time in the email log

Build email

Send email



Craig - MM0NBW
