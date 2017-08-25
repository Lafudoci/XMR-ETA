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

Height: 1384313

 Last block hash:
 77981c8b4c354dbb445ad1daeae400a5946fdf5926d17b493f5a741494f2fbaa
 
 Block size limit: 690.36 kB

 Predicted blockchain size per day: 249.35 mB

 Mempool txs: 136

 Mempool txs size: 25931.96 kB

 Med. Small tx: 12.98 kB (25 txs)

 Med. big tx: 251.34 kB (111 txs)

 Half block block limit: 345.18 kB

 Avg. of last 30 blocks: 354.63 kB

 Block efficiency: 102.74 %

 Approx. tx speed per hour: 439 TPH

 longest small tx:  Longest wait: 02:00:45 (fee: 0.0060, size: 25.96 kB)

 Predicted block: 1 big_txs + 7 small_txs

 Average wait time: 3 +- 27 blocks ( 0 hr: 6 min )
