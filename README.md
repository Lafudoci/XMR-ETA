# XMR-ETA

This tool predicts the Estimated Time of Arrival of Monero (XMR) transaction.

The scripts get mempool and block data from [moneroexplorer.org](https://moneroexplorer.org/). After caculation, informatino will be uploaded to ThingSpeak database for further usage.

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

 Height: 3101382

 Last block hash:
 b437202c12c100d345ea171d98658a2e58b76560c8f3a66bbda851fff987d542

 Block size hard limit: 705.51 kB

 Predicted blockchain size per day: 248.03 mB

 Mempool txs: 1095

 Valid Mempool txs size: 5198.83 kB

 Median valid tx: 1.50 kB (1095 txs)

 Median size of 100 blocks: 352.75 kB

 Median size of last 30 blocks: 353.85 kB

 Median size of last 10 blocks: 354.18 kB

 Median usage of last 10 blocks: 100.40 %

 Approx. tx per hour (30 blocks): 5531 TPH

 Longest valid txs wait: 00:11:57 (fee: 0.001062, size: 51.84 kB)

 Predicted block time: predict: 15, tph: 6, longest: 6

 Average wait time: 10 +- 4 blocks ( 0 hr: 20 min )
