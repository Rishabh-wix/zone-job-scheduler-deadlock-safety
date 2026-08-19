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

# Task 10 — VPC and Network Security Design

## VPC Design

The Smart City cloud environment will use one VPC with separate
private subnets for the three zones.

### VPC CIDR

10.0.0.0/16

### Subnet Design

| Zone | Subnet | CIDR | Purpose |
|------|--------|------|---------|
| Zone-A | Private Subnet A | 10.0.1.0/24 | Zone-A controller resources |
| Zone-B | Private Subnet B | 10.0.2.0/24 | Zone-B controller resources |
| Zone-C | Private Subnet C | 10.0.3.0/24 | Zone-C controller resources |

## Why One VPC?

A single VPC provides centralized network management while the
three private subnets provide logical isolation between Zone-A,
Zone-B, and Zone-C.

This design makes it easier to apply common routing, security,
monitoring, and access-control policies.

The zones do not need separate VPCs because they are part of the
same Smart City cloud environment and need controlled access to
shared cloud services.

## Network-Level Security Control

The primary network-level security control will be Security Group
rules.

Security Groups will follow a least-privilege approach.

### Example Rules

1. Zone-A resources can communicate only with approved cloud API
   endpoints and required services.

2. Zone-B resources can communicate only with approved cloud API
   endpoints and required services.

3. Zone-C resources can communicate only with approved cloud API
   endpoints and required services.

4. Direct communication between Zone-A, Zone-B, and Zone-C
   controller resources will be denied unless explicitly required.

5. Only required inbound and outbound ports will be allowed.

6. Public access to the zone-controller resources will not be
   allowed directly.

## Network Flow

Zone-A Private Subnet ─┐
Zone-B Private Subnet ─┼──> Controlled Cloud Services
Zone-C Private Subnet ─┘

All traffic between zone resources and cloud services is controlled
using routing rules, Security Groups, and encrypted communication.

## Security Goal
The VPC design provides network isolation, controlled access to
cloud services, reduced attack surface, and centralized security
management while allowing all three zones to operate as part of
the same Smart City system.

# Task 11 — Security Objectives and Controls

The Smart City system must protect its infrastructure, users,
sensor data, and cloud services. The following six security
objectives are selected for the system.

## 1. Protect Sensitive Data

### Objective

Protect sensitive Smart City data from unauthorized access,
modification, or disclosure.

### Security Control

Encryption at rest using AWS Key Management Service (AWS KMS).

### Explanation

Sensitive sensor records, job information, logs, and other stored
data should be encrypted. Encryption keys should be managed
securely using AWS KMS with appropriate access permissions.

---

## 2. Strong Authentication

### Objective

Ensure that only authenticated users and devices can access
Smart City services.

### Security Control

Identity and Access Management (IAM) with strong authentication.

### Explanation

Users, administrators, and cloud services should use managed
identities. Strong authentication reduces the risk of unauthorized
account access.

---

## 3. Authorization and Least Privilege

### Objective

Ensure that authenticated users and services can access only the
resources required for their responsibilities.

### Security Control

Role-Based Access Control (RBAC) using IAM policies.

### Explanation

Permissions should be assigned according to job responsibilities.
For example, a zone operator should not receive administrative
permissions unless they are required. This follows the principle
of least privilege.

---

## 4. Protection Against Web and Network Attacks

### Objective

Protect public-facing cloud applications and APIs from common
malicious traffic and attacks.

### Security Control

AWS WAF and request-rate limiting.

### Explanation

AWS WAF can inspect incoming web requests and block malicious
traffic. Rate limiting can reduce abuse and help protect APIs from
excessive requests.

---

## 5. Secure Communication

### Objective

Protect information while it is transmitted between zone
controllers, cloud services, and the Smart City Dashboard.

### Security Control

HTTPS with TLS encryption.

### Explanation

All sensitive communication should use encrypted HTTPS/TLS
connections. This helps prevent attackers from reading or
modifying data while it is in transit.

---

## 6. High Availability

### Objective

Keep Smart City services available even when individual
infrastructure components fail.

### Security Control

Load balancing, Auto Scaling, and multi-AZ deployment.

### Explanation

Critical cloud services can be deployed across multiple
Availability Zones. Load balancing distributes traffic, while
Auto Scaling can add or remove resources according to demand.
This improves availability and resilience.

---

## Security Objectives Summary

| Security Objective | Control | Purpose |
|---------------------|---------|---------|
| Protect sensitive data | AWS KMS / encryption at rest | Protect stored data |
| Strong authentication | IAM / strong authentication | Verify identities |
| Authorization | RBAC / least privilege | Limit resource access |
| Attack protection | AWS WAF / rate limiting | Block malicious traffic |
| Secure communication | HTTPS / TLS | Protect data in transit |
| High availability | Load Balancer / Auto Scaling / Multi-AZ | Maintain service availability |


# Task 12 — IAM Roles and Data Protection

## IAM Role Design

The Smart City system will use role-based access control and
least-privilege permissions. Each role receives only the
permissions required for its responsibilities.

### Role 1 — Zone Operator

#### Responsibilities

The Zone Operator manages and monitors the assigned zone.

#### Permissions

- Read sensor and job status data for the assigned zone.
- Submit approved jobs to the scheduling system.
- View scheduling results for the assigned zone.
- View relevant operational logs.

#### Restrictions

The Zone Operator cannot modify IAM policies, create
administrative users, or access resources belonging to other
zones unless explicitly authorized.


### Role 2 — City Dashboard Administrator

#### Responsibilities

The City Dashboard Administrator manages the Smart City
dashboard and monitors city-wide operational information.

#### Permissions

- View data from all three zones.
- View public-safety alerts.
- Manage dashboard configurations.
- View system health and operational logs.

#### Restrictions

The Dashboard Administrator cannot modify core IAM security
policies unless the permission is explicitly required for the
administrator's responsibilities.


### Role 3 — Security Administrator

#### Responsibilities

The Security Administrator manages security-related configuration
and access policies.

#### Permissions

- Manage IAM roles and policies.
- Review authentication and authorization logs.
- Manage security configurations.
- Review security alerts and audit information.

#### Restrictions

The Security Administrator should not receive unnecessary
permissions to modify application data or scheduling results.

## Least-Privilege Principle

The three roles follow the principle of least privilege. A user
should receive only the permissions necessary to perform their
assigned responsibilities.

This reduces the impact of compromised accounts and limits
unauthorized access to Smart City resources.

---

# Data Protection

The Smart City system must protect data in three states:

1. Data at Rest
2. Data in Transit
3. Data in Use

## 1. Data at Rest

### Example

Zone-controller job information and sensor logs stored in cloud
storage.

### Protection

Use encryption at rest with AWS KMS-managed encryption keys.

### Explanation

Stored job information, sensor records, and logs should be
encrypted so that an attacker who gains access to the underlying
storage cannot directly read the protected data.

Access to encryption keys should be restricted through IAM
permissions.

---

## 2. Data in Transit

### Example

A public-safety alert being sent from a Zone Controller to the
Cloud API and then to the Smart City Dashboard.

### Protection

Use HTTPS with TLS encryption.

### Explanation

TLS protects the data while it travels between the Zone
Controller, Cloud API, and Dashboard. This helps prevent
eavesdropping and unauthorized modification during transmission.

---

## 3. Data in Use

### Example

The Banker's Algorithm processing resource-allocation data in
memory.

### Protection

Run sensitive processing inside an isolated application process
or container and restrict access to its memory and runtime
environment.

### Explanation

Data in use exists in memory while the application is processing
it. Access to the process should be restricted using operating
system permissions, container isolation, and least-privilege
service identities.

## Data Protection Summary

| Data State | Smart City Example | Protection |
|------------|--------------------|------------|
| Data at Rest | Stored jobs and sensor logs | Encryption at rest + AWS KMS |
| Data in Transit | Public-safety alert | HTTPS + TLS |
| Data in Use | Banker's Algorithm processing | Process/container isolation + least privilege |
