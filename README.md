# dwlogtomail
Direwolf APRS log to email
Project to take Direwolf APRS logs and send to email.

fulllog calculates distances to the source station, append distance and output to html formatted email.

dxrx is based on fullog, but additionally filters the result by distance and sends the filter results to email.
The idea behind dxrx is to have a form of alerting when there is a propagation "lift" on amateur VHF band.

Both files are best run as CRON jobs.  I set dxrx file to run every 5 minutes.  To prevent emails being sent every 5 minutes once triggered, the script writes
a timestamp to a text file as each email is sent.  The script reads that time and does not send another email if the time threshold has not been reached (I set
every 30 minutes).
