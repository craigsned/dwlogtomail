# dwlogtomail
Direwolf APRS log to email
Project to take Direwolf APRS logs and send to email.

This is my first foray into any type of scripting.  There may be issues in the way this is coded and probably not the most efficient code.

Description of the files;

fulllog calculates distance and bearing to the source station, append distance and bearing as compass cardinal and outputs to html formatted email.  It is intended to run once a day to email the Direwolf log file in an easier to read format.

dxrx is based on fullog, but additionally filters the result by distance (I set greater than 90 miles) and time received (I set within the last 30 minutes) and sends the filtered results to email.  The idea behind dxrx is to have a form of alerting when there is a propagation "lift" on amateur VHF band.  As such, if the filter returns values dxrx also creates a text file, the content of which is transmitted by the radio as an APRS Bulletin (BLN) message.  This is picked up using a CBEACON in Direwolf.conf running every 15 minutes.  If the DW Text file does not exist, the CBEACON fails, but this causes no issues to Direwolf and can be safely ignored.  Once triggered by CBEACON the bulletin message stops after 90 minutes.  This is achieved by the script deleting the DW Text file.

Both files are best run automatically using CRON.  I set dxrx file to run every 10 minutes.  To prevent emails being sent every 10 minutes once triggered, the script writes a timestamp to a text file as each email is sent.  The script then reads the last time from the text file and does not send another email if the time threshold has not been reached (I set every 30 minutes).  The content of the DW Text file (set in the code) must conform to APRS message packet format - See APRS 101

Email is set up to run through a gmail account using an app password.  See - https://support.google.com/mail/answer/185833?hl=en-GB for further information on this.
email could easily be set up using other providers.


Pre-requisites.

Email account set up to send output.

Direwolf logging enabled (daily log, not rolling) - either command line or in direwolf.conf

A text file, containing at least single timestamp in the required format to prevent crash of dxrx on first run.  (I need to code adding a new line if the
text file is empty - currently I'm fixing this with a separate code that runs once a day at midnight to clear the file (to prevent creating a large file)
and writing a new timestamp).

Set QTH to be the same as the Direwolf.conf entry

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

Check the last time an email was sent (for dxrx script) - if less than (time) quit - this ensures emails are not continuously sent as the dxrx script runs in CRON.
The email log file must have an entry or this will cause the script to fail.  I set the entry for the log file using a separate script to clean up the file once
per day - remove all entries, then append current timestamp

Create the Direwolf CBEACON file (DW Text) and insert text.

Set the content for email from relevant fields in the Panda array

Log current time in the email log

Build email

Send email



Craig - MM0NBW
