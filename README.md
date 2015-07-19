![Steam icon](http://i.imgur.com/9ca9yl7.png) steamBot
=====

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

### Requirements.

Python 3 and the PyCrypto module to process the RSA key, and a logical mind. I am not sure if market bots are allowed, but logically thinking they aren't. So be cautious, as accounts **do** get banned.

[1]: http://store.steampowered.com/subscriber_agreement/
