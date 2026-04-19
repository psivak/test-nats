import asyncio
import nats
import pytest
from nats.errors import TimeoutError

@pytest.fixture
async def nc():
    nc = await nats.connect("nats://localhost:4222")
    yield nc
    await nc.close()

@pytest.mark.asyncio
async def test_subject_wildcards(nc):
    # Test '*' wildcard
    sub = await nc.subscribe("time.*.east")
    await nc.publish("time.us.east", b"msg1")
    msg = await sub.next_msg(timeout=1)
    assert msg.data == b"msg1"
    
    # Test '>' wildcard
    sub_all = await nc.subscribe("time.us.>")
    await nc.publish("time.us.east.atlanta", b"msg2")
    msg = await sub_all.next_msg(timeout=1)
    assert msg.data == b"msg2"

@pytest.mark.asyncio
async def test_pub_sub(nc):
    msgs = []
    async def handler(msg):
        msgs.append(msg.data)

    await nc.subscribe("news", cb=handler)
    await nc.subscribe("news", cb=handler)
    
    await nc.publish("news", b"update")
    await asyncio.sleep(0.1)
    
    # One-to-many: both subscribers should receive the message
    assert len(msgs) == 2
    assert msgs == [b"update", b"update"]

@pytest.mark.asyncio
async def test_request_reply(nc):
    async def responder(msg):
        await nc.publish(msg.reply, b"pong")

    await nc.subscribe("ping", cb=responder)
    
    reply = await nc.request("ping", b"ping", timeout=1)
    assert reply.data == b"pong"

@pytest.mark.asyncio
async def test_queue_groups(nc):
    msgs = []
    async def handler(msg):
        msgs.append(msg.data)

    # Both subscribe to the same queue group 'workers'
    await nc.subscribe("tasks", queue="workers", cb=handler)
    await nc.subscribe("tasks", queue="workers", cb=handler)
    
    for i in range(10):
        await nc.publish("tasks", f"task-{i}".encode())
    
    await asyncio.sleep(0.1)
    
    # One-to-any: messages should be distributed, total should be 10
    assert len(msgs) == 10
    # Ideally they should be somewhat evenly distributed, but we just check total here
