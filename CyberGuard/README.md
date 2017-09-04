
# CyberGuard
​
Basic chatBOT for discord.
### Prerequisites
* python3
​
  Modules:
  * discord
  * asyncio
  * random
  * pickle
  * os
### Installing
Install python for your OS from [Python web page](https://www.python.org/downloads/)

Install modules (some of these will be propably installed with python)
```
pip install discord
pip install asyncio
pip install random
pip install pickle
pip install os
```
## How to run discord bot
1. Sign up to [Discord](https://discordapp.com/)
2. Go to [Discord for developers](https://discordapp.com/developers/) and create new app or click [HERE](https://discordapp.com/developers/applications/me#top)
  Click to ( + ) button and type name for your bot (you can change Icon as well) and click Create App. 
  
  On the next screen click to Crate a Bot User and confirm
  Reveal your bot token by clicking link next to it and save it (this will be your token in aplication)
  Copy your bot ClientID and visit this page (replace ##### with your bot clientID and authorize your bo
  ```
  https://discordapp.com/oauth2/authorize?client_id=#####&scope=bot&permissions=0
  ```
  Save your bot settings by clicking Save Changes button on the bottom of the page
 
 3. Edit discordBOT.py file in your favorite text editor and paste your token (line 14)
   You can change your botname and command prefix as well (line 20 and 21). Edit your contact info on line 53

4. run your bot by typing
   ```
   python discordBOT.py
   ```
 5. type something in discord chat with your owner account, in terminal windows you will see your clientID
   stop discordBOT by pressing CTRL+C, copy your clientID from terminal window and paste it to your discordBOT.py (line 17) - that grants you priviledges to use admin commands
   
 6. repeat step 4 and run your bot again
 
 that's it :)
 
 ## Possible commands
 You can use these commands to control your bot (this example is for ! as command prefix):
 
   User commands:
   * ``` !contact ``` Bot sends your contact information you providein step 3 to the chat
   * ``` !coin ``` Bot toss coin and send result (HEADS or TAILS) to the chat
   
   Admin commands:
   * ``` !allowurl @user ``` Allow user to type URLs in chat
   * ``` !dennyurl @user ``` Denny user to type URLs in chat (default for all)
