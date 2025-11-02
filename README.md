## PART A
### SERVICE DESIGN

#### Short Description 
In my opinion, this should be a separate system that subscribes to the necessary topics as a consumer group
in the message bus (for example, Kafka). To enable horizontal scaling,
it will be a microservice with shared state between different pods or process. For this purpose, we can use an in-memory
database such as Redis.

Users will send messages to the message bus with requests for match registration, and then wait for a response
from the system. Registered users will be added to a hash map in Redis, and if a delete or cancel request comes,
we will remove them.

To divide users into matches and teams, we will first register them into corresponding skill slots,
grouped by their skill rating (for example, each slot represents a 50-point range — 1–50, 51–100, 101–150, and so on).
To speed up the search, we can also use users from neighboring slots, although this approach can create conflicts
if the same player is already being used in another match. This is why atomic operations
(for example, using Lua scripts in Redis) should be used to “claim” players safely.

Every few seconds (for example, every 2 seconds), each slot will be checked to see if it is possible to generate
a match from the users currently waiting there. This allows horizontal scaling — we can assign process,
separate Celery workers or even separate pods to process different slots.

When a match is successfully created, the users who were matched are removed from the local state,
and a match.found event is published back to the message bus so that other services
(for example, the notifier or game server allocator) can process it.

#### Main Components

<b>Matchmaking API</b> – receives requests from the game client and publishes events to the message bus.

<b>Matchmaking Processor</b> – subscribes to the relevant Kafka topics, maintains matchmaking state in Redis, and performs the actual player grouping logic.

<b>Notifier Service</b> – listens to match.found events and notifies players through WebSocket.

<b>Game Server Allocator</b> – assigns an available game server once a match is formed and provides connection details to the players.

### Diagram
![Diagram](./diagram/service.jpg)

The diagram shows the interaction between the game client, the message bus, the matchmaking service,
and the in-memory database (Redis). The game client sends matchmaking requests to the message bus (matchmaking.request),
which are consumed by the matchmaking service. The service registers users in Redis, assigns them to skill-based slots,
and periodically checks these slots to form matches. When a match is successfully created, a matchmaking.found
event is published back to the bus so the client can join the assigned match. If a player cancels the search 
(matchmaking.user_cancel) or times out, the service removes them from Redis automatically.

