import asyncio
import nats
import pytest
from nats.js.api import StreamConfig, RetentionPolicy, StorageType, ConsumerConfig, DeliverPolicy, AckPolicy

@pytest.fixture
async def js():
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()
    yield js
    await nc.close()

@pytest.mark.asyncio
async def test_stream_creation_and_pub(js):
    # Create a stream
    try:
        await js.delete_stream("EVENTS")
    except:
        pass
    await js.add_stream(name="EVENTS", subjects=["events.>"])
    
    # Publish to stream
    ack = await js.publish("events.page_load", b"payload")
    assert ack.stream == "EVENTS"
    assert ack.seq == 1

@pytest.mark.asyncio
async def test_pull_consumer(js):
    try:
        await js.delete_stream("PULL_TEST")
    except:
        pass
    await js.add_stream(name="PULL_TEST", subjects=["pull.>"])
    await js.publish("pull.1", b"msg1")
    await js.publish("pull.2", b"msg2")
    
    # Create pull consumer
    psub = await js.pull_subscribe("pull.>", "mon_pull")
    
    # Fetch messages
    msgs = await psub.fetch(2)
    assert len(msgs) == 2
    for msg in msgs:
        await msg.ack()

@pytest.mark.asyncio
async def test_push_consumer(js):
    try:
        await js.delete_stream("PUSH_TEST")
    except:
        pass
    await js.add_stream(name="PUSH_TEST", subjects=["push.>"])
    await js.publish("push.1", b"msg1")
    
    # Create push consumer
    sub = await js.subscribe("push.>", durable="mon_push")
    msg = await sub.next_msg(timeout=1)
    assert msg.data == b"msg1"
    await msg.ack()

@pytest.mark.asyncio
async def test_retention_workqueue(js):
    # WorkQueue: message is deleted after first ack
    try:
        await js.delete_stream("WQ")
    except:
        pass
    await js.add_stream(
        name="WQ", 
        subjects=["wq.>"], 
        retention=RetentionPolicy.WORK_QUEUE
    )
    
    await js.publish("wq.1", b"task")
    
    sub = await js.pull_subscribe("wq.>", "wq_consumer")
    msgs = await sub.fetch(1)
    await msgs[0].ack()
    
    # Wait for server to update stats
    await asyncio.sleep(0.5)
    
    # After ack, stream should be empty
    si = await js.stream_info("WQ")
    assert si.state.messages == 0

@pytest.mark.asyncio
async def test_deliver_policy_new(js):
    try:
        await js.delete_stream("DP_TEST")
    except:
        pass
    await js.add_stream(name="DP_TEST", subjects=["dp.>"])
    await js.publish("dp.old", b"old")
    
    # DeliverPolicy.NEW should ignore existing messages
    sub = await js.subscribe("dp.>", deliver_policy=DeliverPolicy.NEW)
    
    await js.publish("dp.new", b"new")
    msg = await sub.next_msg(timeout=1)
    assert msg.data == b"new"
