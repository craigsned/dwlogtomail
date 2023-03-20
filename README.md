# dwlogtomail
Direwolf APRS log to email
Project to take Direwolf APRS logs and send to email.

This is my first foray into any type of scripting.  There may be issues in the way this is coded and probably not the most efficient code.

Descrition of the files;

fulllog calculates distances to the source station, append distance and output to html formatted email.

dxrx is based on fullog, but additionally filters the result by distance and sends the filter results to email.
The idea behind dxrx is to have a form of alerting when there is a propagation "lift" on amateur VHF band.

Both files are best run as CRON jobs.  I set dxrx file to run every 5 minutes.  To prevent emails being sent every 5 minutes once triggered, the script writes
a timestamp to a text file as each email is sent.  The script reads that time and does not send another email if the time threshold has not been reached (I set
every 30 minutes).

Email is set up to run through a gmail account using an app password.  See - https://support.google.com/mail/answer/185833?hl=en-GB for further information on this.
email could easily be set up using other providers.

Pre-requisites
email account set up to send output
path to Direwolf log file is known
a text file is created, containing at least single timestamp in the required format to prevent crash of dxrx on first run.  (I need to code adding a new line if the text file is empty - currently I'm fixing this with a separate code that runs once a day at midnight to clear the file (to prevent creating a large file) and writing a new timestamp)

Craig - MM0NBW
