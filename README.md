![Steam icon](http://i.imgur.com/9ca9yl7.png) steamBot
=====
![Warning icon](http://i.imgur.com/CvxgTJc.png) the code is currently very basic and badly intertwined, therefore the code is not optimal/quite usuable until this warning is removed.

steamBot is a **Python(3)** module, it offers the user to create automated steam market bots that create offers and bids themsleves depending on the current status of the market. No user participation is needed after the bot is coded correctly.

***
The module is still being coded and is not even near to ready, this is what is already done:
> - Fetching sessionID and country
> - Fetching an RSA key
> - Logging in
> - Placing a buy order

As said, not a lot has been done yet, this is what you can expect:

> - Fetching market data (per item)
> - Changing account details of the bot
> - Cancelling buy orders
> - Creating a bot with the module itself
> - Handling other unknown (login) errors (like Captcha)
> - Fetching the Steam Guard code from e-mail

***
### License and ToS
Not only does this repository have a license, but the steamBot might also not be in line with the Steam Terms of Service. The license is in the repository and you can check out the Steam Terms of Service [here][1].

### Requirements

Python 3 and the PyCrypto module to process the RSA key, and a logical mind. I am not sure if market bots are allowed, but logically thinking they aren't. So be cautious, as accounts **do** get banned.

### Usage

Since a recent update cookeis get stored. This means your bot doesn't have to log in over and over again. To create the cookies you must open credentials.json and fill in your credentials. Then run your bot and it will go through the login procedure. After this cookies *should* be stored in the data.pkl file. If not, either your credentials are incorrect or you have to fill in a captcha, which will be automatized later on.

After this you can delete your credentials.json if that makes you feel saver. However, remember that when you need to create a new set of cookies you must delete the data.pkl and have credentials.json existing. Explanations of the commands will be added to a wiki later.

[1]: http://store.steampowered.com/subscriber_agreement/
