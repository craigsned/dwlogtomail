# dwlogtomail
Direwolf APRS log to email
Project to take Direwolf APRS logs and send to email.

Two slightly different files were created.  One to read the log file, calculate distances to the source station, append distance and output to email.

The second file does the above, but filters the result by distance and sends the filter results to email.

Both files are best run as CRON jobs.  I set the second file to run every 5 minutes.  To prevent emails being sent every 5 minutes once triggered, the script writes
a timestamp to a text file as each email is sent.  The script reads that time and does not send another email if the time threshold has not been reached (I set
every 30 minutes).
