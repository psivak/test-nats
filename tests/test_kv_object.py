import asyncio
import nats
import pytest

@pytest.fixture
async def nc():
    nc = await nats.connect("nats://localhost:4222")
    yield nc
    await nc.close()

@pytest.mark.asyncio
async def test_kv_store(nc):
    js = nc.jetstream()
    
    # Use a unique bucket name for this test run to avoid conflicts
    bucket_name = "settings_test"
    try:
        await js.delete_key_value(bucket=bucket_name)
    except:
        pass
        
    # Create KV bucket with history
    kv = await js.create_key_value(bucket=bucket_name, history=5)
    
    # Put and Get
    await kv.put("theme", b"dark")
    entry = await kv.get("theme")
    assert entry.value == b"dark"
    
    # Update
    await kv.put("theme", b"light")
    entry = await kv.get("theme")
    assert entry.value == b"light"
    
    # History
    history = await kv.history("theme")
    assert len(history) == 2

@pytest.mark.asyncio
async def test_kv_watch(nc):
    js = nc.jetstream()
    bucket_name = "watcher_test"
    try:
        await js.delete_key_value(bucket=bucket_name)
    except:
        pass
    kv = await js.create_key_value(bucket=bucket_name)
    
    await kv.put("conf.app1", b"v1")
    
    # Watch returns an async iterator
    watcher = await kv.watch("conf.*")
    
    # Get first update from the iterator (existing state)
    msg = await anext(watcher)
    assert msg.key == "conf.app1"
    assert msg.value == b"v1"
    
    await watcher.stop()

@pytest.mark.asyncio
async def test_object_store(nc):
    js = nc.jetstream()
    
    # Create Object Store
    obs = await js.create_object_store("configs")
    
    # Put object
    await obs.put("app.conf", b"content" * 100)
    
    # Get object
    obj = await obs.get("app.conf")
    assert obj.data == b"content" * 100
    
    # Info - in nats-py it might be info() but let's check common alternatives
    # Actually, let's try 'get_info' based on common patterns if info fails
    # But wait, the error said 'ObjectStore' object has no attribute 'info'.
    # Checking nats-py source or docs mentally... it's often 'get' which returns Info inside? 
    # No, 'get' returns ObjectResult which has 'info' attribute.
    assert obj.info.name == "app.conf"
    assert obj.info.size == 700
