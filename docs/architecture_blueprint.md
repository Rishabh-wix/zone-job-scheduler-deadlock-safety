# Smart City Zone Controller Architecture Blueprint

## Task 9 — Architecture Selection

### Selected Architecture: Client-Server Architecture

The Smart City system will use a Client-Server architecture.

Zone controllers in Zone-A, Zone-B, and Zone-C act as clients,
while the centralized cloud platform acts as the server.

The architecture can be represented as:

Zone-A Controller ─┐
                   │
Zone-B Controller ─┼──> Cloud Server ──> Smart City Dashboard
                   │
Zone-C Controller ─┘

### Why Client-Server Architecture?

1. Centralized management:
   The cloud server provides a central location for managing
   scheduling, safety checks, sensor data, and alerts.

2. Better security:
   Authentication, authorization, encryption, logging, and
   network security policies can be centrally controlled.

3. Scalability:
   Additional zone controllers can be connected without
   redesigning the complete system.

4. Central monitoring:
   The Smart City Dashboard can receive information from all
   three zones through the centralized server.

5. Easier maintenance:
   Scheduling and safety logic can be updated centrally instead
   of modifying every zone controller individually.


## Communication Plan

The system has two major communication flows.

### Flow A — Real-Time Public-Safety Alert

#### Communication Type

Synchronous communication over HTTPS.

#### Flow

Zone Controller
      |
      | HTTPS / TLS
      v
Cloud API Server
      |
      | HTTPS
      v
Smart City Dashboard

#### Why Synchronous?

A public-safety alert is time-sensitive. The zone controller needs
a request-response interaction so that the cloud service can
immediately receive the alert and return an acknowledgement.

HTTPS provides encrypted communication and protects the alert
while it travels across the network.

### Flow B — Full-Day Sensor Log

#### Communication Type

Asynchronous communication over HTTPS.

#### Flow

Zone Controller
      |
      v
Local Buffer / Queue
      |
      | Background Upload
      v
Cloud Storage

#### Why Asynchronous?

A full-day sensor log does not need to be transmitted to the cloud
immediately after every sensor event. The data can be buffered and
uploaded in batches during background processing.

This reduces unnecessary network traffic and avoids blocking the
zone controller while large log files are uploaded.

## Summary

| Flow | Communication | Protocol | Reason |
|------|---------------|----------|--------|
| Public-safety alert | Synchronous | HTTPS/TLS | Immediate request and acknowledgement |
| Full-day sensor log | Asynchronous | HTTPS/TLS | Batch/background transfer |
