# Woopy
Woopy is a minimal Python API for trading on WooTrade. It is a Python interface for the [WooTrade API](https://kronosresearch.github.io/wootrade-documents)
. Woopy is an alternative to [python-wootrade](https://github.com/wanth1997/python-wootrade), which is computationally intensive and appears unstable at Windows platforms. This has been the mean reason for the development of Woopy. 

One of the reasons for the instability of python-wootrade is the unnecessary code complexity, which makes is hard to debug. It seems that python-wootrade is a stripped down version of [python-binance](https://github.com/sammchardy/python-binance). The source code of python-binance is equally complicated.

Woopy avoids all unnecessary complications, which leaves a simple module that is easy to maintain. Woopy has only two dependencies, namely `requests` and `websockets`.

# Prerequisites

1. First of all, you need an account at WooTrade. 
2. Next, you need to register your application by creating an **API Key and Secret**, which can be found at Account > Subaccounts and API. 
3. Then, you fetch your **Application ID**, wich can be found at Account > Subaccounts and API. 
4. It is preferrable to store the Application ID, API Key and API Secret as environment variables, rather than storing them as plaintext in your source code.

# Installation

1. Optionally create (`python -m venv venv`) and activate (`venv\Scripts\activate`) a virtual environment.
2. Run

```
pip install woopy
```

Test your installation by running the following script:

``` 
import woopy
import os

woo_key = os.getenv("WOO_API_KEY", "my-woo-key")
woo_secret = os.getenv("WOO_API_SECRET", "my-woo-secret")
woo_app_id = os.getenv("WOO_APPLICATION_ID", "my-app-id")

symbol = 'SPOT_BTC_USDT'

topics = {
    f'wss://wss.woo.org/ws/stream/{woo_app_id}': [f'{symbol}@trade'],
    f'wss://wss.woo.org/v2/ws/private/stream/{woo_app_id}': ['positioninfo']
}

for msg in woopy.receive(topics, woo_key, woo_secret):
    print(msg)
```

You should see a stream of messages containing trade information and private information on your position.

# Concepts

There are two ways to communicate with WooTrade, namely via HTTP requests and via websockets. 

## HTTP

The HTTP requests are rather straightforward and can be called via `get()`, `post()`, and `delete()`. The required arguments can be found in the [WooTrade API reference](https://kronosresearch.github.io/wootrade-documents).

## Websockets

The websockets interface is implemented as an iterable `receive()`, which requires a dictionary of topics as one of its arguments. The keys of this dictionary are public and private endpoints of WooTrade. The values of this dictionary are their respective topics, as specified by the [WooTrade API reference](https://kronosresearch.github.io/wootrade-documents).

The `receive()` iterator handles all connection errors and **automatically reconnects** to the disconnected websocket. Such disconnects can be caused by an interrupted internet connection, or just when WooTrade decides that the session was long enough.

For simplicity, Woopy assumes **static topics**, i.e., all topics are known from the start.


Happy trading!
