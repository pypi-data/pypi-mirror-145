import pytest
from telliot_core.apps.core import TelliotCore
from web3.datastructures import AttributeDict

from telliot_feed_examples.feeds.uspce_feed import uspce_feed
from telliot_feed_examples.reporters.interval import IntervalReporter
from telliot_feed_examples.sources import uspce


@pytest.mark.skip("Asks for psswd")
@pytest.mark.asyncio
async def test_uspce_interval_reporter_submit_once(rinkeby_cfg):
    """test report of uspce manual price"""
    # Override Python built-in input method
    uspce.input = lambda: "123.456"

    async with TelliotCore(config=rinkeby_cfg) as core:

        account = core.get_account()
        tellorx = core.get_tellorx_contracts()
        r = IntervalReporter(
            endpoint=core.config.get_endpoint(),
            account=account,
            master=tellorx.master,
            oracle=tellorx.oracle,
            datafeed=uspce_feed,
            expected_profit="YOLO",
            transaction_type=0,
            gas_limit=400000,
            max_fee=None,
            priority_fee=None,
            legacy_gas_price=None,
            gas_price_speed="safeLow",
            chain_id=core.config.main.chain_id,
        )

        EXPECTED_ERRORS = {
            "Current addess disputed. Switch address to continue reporting.",
            "Current address is locked in dispute or for withdrawal.",
            "Current address is in reporter lock.",
            "Estimated profitability below threshold.",
            "Estimated gas price is above maximum gas price.",
            "Unable to retrieve updated datafeed value.",
        }

        ORACLE_ADDRESSES = {
            "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",  # mainnet
            "0x18431fd88adF138e8b979A7246eb58EA7126ea16",  # rinkeby
        }

        tx_receipt, status = await r.report_once()

        # Reporter submitted
        if tx_receipt is not None and status.ok:
            assert isinstance(tx_receipt, AttributeDict)
            assert tx_receipt.to in ORACLE_ADDRESSES
        # Reporter did not submit
        else:
            assert not tx_receipt
            assert not status.ok
            assert status.error in EXPECTED_ERRORS
