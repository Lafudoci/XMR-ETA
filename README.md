# XMR-ETA

This is a tool to predict the Estimated Time of Arrival of Monero (XMR) transaction.

After caculation, informatino will be uploaded to ThingSpeak database.

## Demo page:
https://xmr-tw.org/xmr-eta/

## Installation

* Create a thingspeak account
* Create a channel and get the write api key
* save the api key string as a "thingspeak_key.txt" in the same folder with xmr-eta.py
* pip install requests
* run the xmr-eta.py
* Check the output and thingspeak

## Thingspeak page
https://thingspeak.com/channels/321751

## Console output sample

 Height: 1412417

 Last block hash:
 491e172c7973bde9cee34dcb010106f53927591bcbf960b2b578a7420e3f7fa6

 Block size hard limit: 614.40 kB

 Predicted blockchain size per day: 210.94 mB

 Mempool txs: 9

 Valid Mempool txs size: 77.86 kB

 Med. valid tx: 12.85 kB (6 txs)

 Dynamic block size: 300.00 kB

 Avg. of last 30 blocks: 46.26 kB

 Block usage: 15.42 %

 Approx. tx speed per hour: 119 TPH

 Longest valid txs wait: 00:02:17 (fee: 0.0140, size: 13.35 kB)

 Predicted block txs: 6 valid txs (77k) ( 26% )

 Predicted block time: predict: 1, tph: 2, longest: 2

 Average wait time: 1 +- 0 blocks ( 0 hr: 2 min )
