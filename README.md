pulse-bot
=========

Pulse Bot is a free and open source application for tracking uptime and latency of your web application.

How does it work?
-----------------
1. Checkout the source:
<pre>git clone https://github.com/theak/pulse-bot.git</pre>
2. Register an AppEngine app:
** Visit http://cloud.google.com/console and click "Create Project"
** Note your Project ID-> you'll need this for the next step
3. Edit app.yaml in the project root
** Replace "Application: pulse-bot" with "Application: [your-project-id]"
4. (optional) Edit cron.yaml in the project root
** Specify the frequency at which you want the prober to update
** This is currently set to 5 minutes to stay within the AppEngine free app quota
5. Enjoy!
