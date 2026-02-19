import concurrent.futures
import src.Twitch.TwitchPlays_Connection as TwitchPlays_Connection
from src.Twitch.TwitchPlays_KeyCodes import *
from PyQt5.QtCore import QThread

accentDict = {"À":"\u00C0","Á":"\u00C1",
             "È":"\u00C8","É":"\u00C9",
              "Ì":"\u00CC", "Í":"\u00CD",
              "Ò":"\u00D2","Ó":"\u00D3",
              "Ù":"\u00D9","Ú": "\u00DA","'":"\u2019" }

class TwitchNaturaController(QThread):
    def __init__(self,mainWindowSignal,config):
        super().__init__()
        self.mainWindow=mainWindowSignal
        self.TWITCH_CHANNEL = config.get("MAIN","channel")
        self.allowedMods = config.get("MAIN","mods").lower().replace(" ","").split(",")
        #print(self.allowedMods)
        self.MESSAGE_RATE = config.getfloat("MAIN","message_rate")#0.5
        self.MAX_QUEUE_LENGTH = config.getint("MAIN","queue_length")#= 10
        self.MAX_WORKERS = config.getint("MAIN","workers")#5 # Maximum number of threads you can
        self.TIMEOUT = config.getint("MAIN","timeout_timer")#5 # Maximum number of threads you can
        self.disconnect_probe = config.getboolean("MAIN","disconnect_probe")#5 # Maximum number of threads you can
            # Replace this with your Twitch username. Must be all lowercase.
        self.last_time = time.time()
        self.message_queue = []
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS)
        self.active_tasks = []
        self.t = TwitchPlays_Connection.Twitch()
        self.t.TIMEOUT=self.TIMEOUT
        self.t.disconnect_probe=self.disconnect_probe
        self.t.twitch_connect(self.TWITCH_CHANNEL)

    def handle_message(self,message):
        try:
            msg = message['message'].lower().replace(" ","")
            username = message['username'].lower()
            for acc in accentDict:
                msg=msg.replace(acc,accentDict[acc])
            print("Got this message from " + username + ": " + msg)
            if username in self.allowedMods:
                # if msg.startswith("!ko"):
                #     update= int(msg.replace("!ko","").replace("\U000e0000",""))
                #     self.mainWindow.emit(0,update)
                #EXTRA TRAINERS
                # if msg.startswith("!extra"):
                #     update= int(msg.replace("!extra","").replace("\U000e0000",""))
                #     self.mainWindow.emit(1,update)
                #skipped
                if msg.startswith("!skip"):
                    update= int(msg.replace("!skip","").replace("\U000e0000",""))
                    self.mainWindow.emit(0,update)
                #wild 
                if msg.startswith("!selv"):
                    update= int(msg.replace("!selv","").replace("\U000e0000",""))
                    self.mainWindow.emit(1,update)
                #lv
                if msg.startswith("!lv"):
                    update= int(msg.replace("!lv","").replace("\U000e0000",""))
                    self.mainWindow.emit(2,update)
        except Exception as e:
            print("Encountered exception: " + str(e))
    
    def run(self):
        print("Chat controller online")
        while True:
            self.active_tasks = [t for t in self.active_tasks if not t.done()]
            #Check for new messages
            new_messages = self.t.twitch_receive_messages()
            if new_messages:
                self.message_queue += new_messages; # New messages are added to the back of the queue
                self.message_queue = self.message_queue[-self.MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

            messages_to_handle = []
            if not self.message_queue:
                # No messages in the queue
                last_time = time.time()
            else:
                # Determine how many messages we should handle now
                r = 1 if self.MESSAGE_RATE == 0 else (time.time() - last_time) / self.MESSAGE_RATE
                n = int(r * len(self.message_queue))
                if n > 0:
                    # Pop the messages we want off the front of the queue
                    messages_to_handle = self.message_queue[0:n]
                    del self.message_queue[0:n]
                    last_time = time.time()

            if not messages_to_handle:
                continue
            else:
                for message in messages_to_handle:
                    if len(self.active_tasks) <= self.MAX_WORKERS:
                        self.active_tasks.append(self.thread_pool.submit(self.handle_message, message))
                    else:
                        print(f'WARNING: active tasks ({len(self.active_tasks)}) exceeds number of workers ({self.MAX_WORKERS}). ({len(self.message_queue)} messages in the queue)')
