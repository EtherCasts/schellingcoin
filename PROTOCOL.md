From http://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed/

This mechanism is how SchellingCoin works. The basic protocol is as follows:

1. During an even-numbered block, all users can submit a hash of the ETH/USD price together with their Ethereum address
2. During the block after, users can submit the value whose hash they provided in the previous block.
3. Define the “correctly submitted values” as all values N where H(N+ADDR) was submitted in the first block and N was submitted in the second block, both messages were signed/sent by the account with address ADDR and ADDR is one of the allowed participants in the system.
4. Sort the correctly submitted values (if many values are the same, have a secondary sort by H(N+PREVHASH+ADDR) where PREVHASH is the hash of the last block)
5. Every user who submitted a correctly submitted value between the 25th and 75th percentile gains a reward of N tokens (which we’ll call “schells”)

The protocol does not include a specific mechanism for preventing sybil attacks; it is assumed that proof of work, proof of stake or some other similar solution will be used.
