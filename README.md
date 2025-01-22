Use MQTT with a JSON payload a text source for OBS! 
Run this script outside of OBS, point the script to your MQTT broker and your OBS instance with websocket enabled
Create text sources with names that match your JSON keys in the MQTT topic. They will be updated every second.
This script was primarily written by ChatGPT with special massaging from myself to actually get it working.

I use this script to interface with the Sportzcast Scorelink 2 MQTT server software to pull my game clock and scores from the scoreboard controller directly into OBS
