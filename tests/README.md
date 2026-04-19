# NATS Concept Tests

This test suite validates the core concepts and variations of NATS messaging.

## Concepts Tested

### Core NATS
- **Subject-Based Messaging**: Routing with dots, wildcards (`*`, `>`).
- **Pub/Sub**: One-to-many delivery.
- **Request/Reply**: Semantic request/response pattern.
- **Queue Groups**: Load balancing (one-to-any delivery).

### JetStream (Persistence)
- **Streams**: Message storage, retention policies (Limits, Interest, WorkQueue).
- **Consumers**:
  - **Pull Consumers**: Batch fetching.
  - **Push Consumers**: Server-initiated delivery.
  - **Durable vs Ephemeral**: State persistence.
  - **Deliver Policies**: All, New, Last, etc.
  - **Ack Policies**: Explicit, All, None.

### Advanced Features
- **Key/Value Store**: Key-based storage, history, watching.
- **Object Store**: Large file storage.
- **Deduplication**: Using `Nats-Msg-Id`.
