# pydatanet, a lightweight easy-to-use yet intuitive networking library, built on top of plain-vanilla sockets.

PyDataNet does most of the tedious hard labour for you and removes the pain out of socket programming. It supports TCP and UDP (**UDP WIP**).

It features:
- Object serialization into bytes and de-serialization into the literal object through pickle so you don't have to worry about converting your objects into sendable bytes.
- An easy to understand client/server concept.
- Even a beginner can start learning it and get a small hang of how sockets work, hence, great if you don't want to directly dip your toes into sockets; but I would still recommend learning sockets as it can be crucial whilst debugging errors.

# Some boilerplate

**BASIC SERVER:**
```python
import pydatanet
from pydatanet.server import Server, ServerType

def onPacketSend(sender, data):
    print(f"{sender.getIp()} sent me this!: {data}")

myServer = Server('localhost', 5050, ServerType.TCP)
myServer.on_recv_bind(onPacketSend)
myServer.connect()
```
**BASIC CLIENT:**

```python
import pydatanet
from pydatanet.client import Client, ClientType # do not mistake for pydatanet.server.client!

def myFuncOnReceiveTCP(data_decoded):
    print(f"I got some data: {data_decoded}")

class myFancyClass():
    def __init__(self, doLikePizza: bool = False):
        self.doLikePizza = doLikePizza

c = Client(ClientType.TCP)
c.hook_tcp_recv(myFuncOnReceiveTCP)
c.connect("localhost", 5050)
c.send(
    {
        "foo": "bar",
        "math": 55,
        "myNumbers": [0, 1, 2, 3, 4, 5],
        "myClass": myFancyClass(True)
    }
)
```
and the best part, your data will reach the other side just in the same shape! Now, isn't that convenient?

# EXTRA FEATURES
- Incredibly foolproof; sockets created auto-close upon the program stopping so you don't shoot yourself in the foot. Even if THAT fails, it will auto-reuse the socket.
- You can supply the extra argument `autoPoll` to False and hook up `Client._connect` to your task managing system if you want to (if you want to control the frequency of heartbeats/polls).

# CLOSING NOTES
- Please report vulnerabilites, bugs, suggestions and performance issues in the issues tab. That would be greatly appreciated.
- This is **NOT** a full time project; this is just something I made because PyEnet was extremely imperformant and other libraries did not satisfy my needs. I will not dedicate my entire time to this.
- Check out TUO; a game I am working on, that was the drive to make this library. (https://discord.gg/2ZycjAA)
- I do not appreciate any illegal tomfoolery, better known as **felonies** to be committed using my library. I am not responsible for any damage conducted using this library.
- I swear I shall not add any protestware or malware. If you see someone adding such things, my account will have been likely hijacked. I do not like mixing politics into programming. (**cough cough**, @RIAEvangelist)
