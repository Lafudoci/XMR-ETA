# XMR-ETA

This is a tool to predict the Estimated Time of Arrival of Monero (XMR) transaction.

After caculation, informatino will be uploaded to ThingSpeak database.

## Demo page:
https://xmr-tw.org/blockdata/

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

 Height: 1384139

Last block hash:
 571db1659ddbf970ba7ea99e9254022468273848862df2aac6ac38a913fbe1cb
 Block size limit: 682.79 kB

 Predicted blockchain size per day: 231.35 mB

 Mempool txs: 76

 Mempool txs size: 16733.18 kB

 Med. Small tx: 13.11 kB (10 txs)

 Med. big tx: 251.35 kB (67 txs)

 Half block block limit: 341.39 kB

 Avg. of last 30 blocks: 329.04 kB

 Block efficiency: 96.38 %

 Approx. tx speed per hour: 232 TPH

 Predicted block: 1 big_txs + 6 small_txs

 Average wait time: 2 blocks ( 0 hr: 4 min )

 Longest wait: 00:02:28 (fee: 0.0130, size: 13.24 kB)
