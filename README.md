pulse-bot
=========

Pulse Bot is a free and open source application for tracking uptime and latency of your web application.

How does it work?
-----------------
1. Checkout the source:
<pre>git clone https://github.com/theak/pulse-bot.git</pre>
2. Register an AppEngine app:
  * Visit http://cloud.google.com/console and click "Create Project"
  * Note your Project ID-> you'll need this for the next step
3. Edit app.yaml in the project root
  * Replace "Application: pulse-bot" with "Application: [your-project-id]"
  * (optional) Edit cron.yaml with the frequency at which you want the prober to update- this is currently set to 5 minutes to stay within the AppEngine free app quota
5. Deploy!
  * Install the AppEngine SDK for Python: https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
  * Run: <pre>appcfg.py update .</pre>
    ** For more info, see: https://developers.google.com/appengine/docs/python/tools/uploadinganapp
