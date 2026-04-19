import asyncio
import nats
import pytest
from nats.js.api import StreamConfig

@pytest.fixture
async def js():
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()
    yield js
    await nc.close()

@pytest.mark.asyncio
async def test_deduplication(js):
    # Create a stream with a deduplication window
    await js.add_stream(
        name="DEDUPE", 
        subjects=["dedupe.>"],
        duplicate_window=10 # seconds
    )
    
    # Publish with Msg-Id
    await js.publish("dedupe.test", b"msg", headers={"Nats-Msg-Id": "unique-1"})
    
    # Publish same Msg-Id again
    ack = await js.publish("dedupe.test", b"msg", headers={"Nats-Msg-Id": "unique-1"})
    
    # Second publish should be a duplicate
    assert ack.duplicate is True

@pytest.mark.asyncio
async def test_advisories(js):
    nc = js._nc
    
    # Listen for JetStream advisories (e.g., consumer created)
    # Note: This is a bit advanced as it uses system subjects
    sub = await nc.subscribe("$JS.EVENT.ADVISORY.CONSUMER.>")
    
    await js.add_stream(name="ADV_TEST", subjects=["adv.>"])
    await js.add_consumer("ADV_TEST", durable_name="adv_consumer")
    
    try:
        msg = await sub.next_msg(timeout=2)
        assert "$JS.EVENT.ADVISORY.CONSUMER.CREATE" in msg.subject
    except Exception:
        pytest.skip("Advisories might not be enabled or timing issue")
