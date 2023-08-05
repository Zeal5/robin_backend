from flashbots import flashbot
from web3_token import web3


flashbots_bundle_provider = flashbot(
    web3, "https://relay.flashbots.net"
)
