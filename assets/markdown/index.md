Index

SYMBOLS

@abc.abstractmethod, The Repository in the Abstract

A

abstract base classes (ABCs)

ABC for the repository, The Repository in the Abstract

defining for notifications, Define the Abstract and Concrete
Implementations

switching to typing.Protocol, Option 3: The UoW Publishes
Events to the Message Bus

using duck typing and protocols instead of, The Repository in the
Abstract

using for ports, What Is a Port and What Is an Adapter, in Python?

abstract methods, The Repository in the Abstract

abstractions, A Brief Interlude: On Coupling and Abstractions-Wrap-
Up

abstracting state to aid testability, Abstracting State Aids
Testability-Abstracting State Aids Testability

AbstractRepository, service function depending on, A Typical
Service Function

AbstractUnitOfWork, Unit of Work and Its Context Manager

choosing right abstraction, Choosing the Right Abstraction(s)-
Implementing Our Chosen Abstractions

explicit dependencies are more abstract, Aren’t Explicit
Dependencies Totally Weird and Java-y?

implementing chosen abstraction, Implementing Our Chosen
Abstractions-Wrap-Up

edge-to-edge testing with fakes and dependency injection,
Testing Edge to Edge with Fakes and Dependency Injection-
Testing Edge to Edge with Fakes and Dependency Injection

not using mock.patch for testing, Why Not Just Patch It Out?

simplifying interface between business logic and I/O, Wrap-Up

using to reduce coupling, A Brief Interlude: On Coupling and
Abstractions

adapters

building adapter and doing dependency injection for it, Building
an Adapter “Properly”: A Worked Example-Wrap-Up

defining abstract and concrete implementations, Define the
Abstract and Concrete Implementations

defined, What Is a Port and What Is an Adapter, in Python?

Django views, API: Django Views Are Adapters

exercise for the reader, Figure Out How to Integration Test the
Real Thing

ports-and-adapters inspired patterns, Part I Recap

putting into folder, Putting Things in Folders to See Where It All
Belongs

Aggregate pattern, What Is an Aggregate?

aggregates

about, What Is an Aggregate?

acting as consistency boundaries, Discussion: Events, Commands,
and Error Handling

and consistency boundaries recap, Wrap-Up

changing multiple aggregates in a request, Wrap-Up

choosing an aggregrate, Choosing an Aggregate-Choosing an
Aggregate

exercise for the reader, What About Performance?

History aggregate recording orders and raising domain events,
Discussion: Events, Commands, and Error Handling

identifying aggregates and bounded contexts, Identifying
Aggregates and Bounded Contexts-An Event-Driven Approach to
Go to Microservices via Strangler Pattern

one aggregrate = one repository, One Aggregate = One
Repository

optimistic concurrency with version numbers, Optimistic
Concurrency with Version Numbers-Implementation Options for
Version Numbers

performance and, What About Performance?

Product aggregate, Aggregates and Consistency Boundaries

pros and cons or trade-offs, Wrap-Up

query on repository returning single aggregate, Implementation

raising events about, Discussion: Events, Commands, and Error
Handling

repository keeping track of aggregates passing through it, Option
3: The UoW Publishes Events to the Message Bus

testing for data integrity rules, Testing for Our Data Integrity
Rules-Pessimistic Concurrency Control Example: SELECT FOR
UPDATE

testing Product object to raise events, The Model Raises Events

UoW collecting events from and passing them to message bus,
Wrap-Up

allocate service

allocating against all batches with, Choosing an Aggregate

moving to be a method on Product aggregate, Choosing an
Aggregate

Allocated event, Our New Outgoing Event

AllocationRequired event, Refactoring Service Functions to Message
Handlers

passing to services.allocate, Imagining an Architecture Change:
Everything Will Be an Event Handler

Anemic Domain anti-pattern, The DIP in Action

APIs

adding API for adding a batch, Carrying the Improvement
Through to the E2E Tests

Django views as adapters, API: Django Views Are Adapters

end-to-end test of allocate API, A First End-to-End Test

modifying API to work with events, A Temporary Ugly Hack: The
Message Bus Has to Return Results

using repository directly in API endpoint, What Is the Trade-Off?

without Unit of Work pattern, talking directly to three layers, Unit
of Work Pattern

application services, Why Is Everything Called a Service?

architecture, summary diagram and table, Summary Diagram and
Table-Summary Diagram and Table

asynchronous messaging, temporal decoupling with, The Alternative:
Temporal Decoupling Using Asynchronous Messaging

atomic operations, Unit of Work Pattern

Unit of Work as abstraction over, Wrap-Up

using Unit of Work to group operations into atomic unit,
Examples: Using UoW to Group Multiple Operations into an
Atomic Unit-Example 2: Change Batch Quantity

B

Ball of Mud pattern, A Brief Interlude: On Coupling and Abstractions

distributed ball of mud and thinking in nouns, Distributed Ball of
Mud, and Thinking in Nouns-Distributed Ball of Mud, and
Thinking in Nouns

separating responsibilities, Separating Entangled Responsibilities

BatchCreated event, Refactoring Service Functions to Message
Handlers

services.add_batch as handler for, Imagining an Architecture
Change: Everything Will Be an Event Handler

batches

allocating against all batches using domain service, Choosing an
Aggregate

asking Product to allocate against, Choosing an Aggregate

batch quantities changed means deallocate and reallocate, A New
Requirement Leads Us to a New Architecture

collection of, Choosing an Aggregate

BatchQuantityChanged event

implementing, Our New Event

invoking handler change_batch_quantity, Imagining an
Architecture Change: Everything Will Be an Event Handler

Bernhardt, Gary, Implementing Our Chosen Abstractions

bootstrapping, Dependency Injection (and Bootstrapping)

bootstrapping script, capabilities of, A Bootstrap Script

changing notifications dependency in bootstrap script, Define the
Abstract and Concrete Implementations

dependency injection and bootstrap recap, Wrap-Up

dependency injection with, Aren’t Explicit Dependencies Totally
Weird and Java-y?

initializing dependency injection in tests, Initializing DI in Our
Tests

using in entrypoints, Using Bootstrap in Our Entrypoints

using to build message bus that talks to real notification class,
Figure Out How to Integration Test the Real Thing

bounded contexts, Choosing an Aggregate

identifying aggregates and, Identifying Aggregates and Bounded
Contexts-An Event-Driven Approach to Go to Microservices via
Strangler Pattern

product concept and, Choosing an Aggregate

business logic

abstractions simplifying interface with messy I/O, Wrap-Up

separating from state in code, Implementing Our Chosen
Abstractions

business logic layer, What Is a Domain Model?

business rules

invariants, concurrency, and locks, Invariants, Concurrency, and
Locks

invariants, constraints, and consistency, Invariants, Constraints,
and Consistency

C

Celery tool, The Message Bus Maps Events to Handlers

change_batch_quantity

handler tests for, Test-Driving a New Handler

implementation, handler delegating to model layer,
Implementation

choreography, Single Responsibility Principle

classes, dependency injection using, An Alternative Using Classes

classical mapping, Inverting the Dependency: ORM Depends on
Model

closures

dependency injection using, Preparing Handlers: Manual DI with
Closures and Partials

difference from partial functions, Preparing Handlers: Manual DI
with Closures and Partials

cohesion, high, between coupled elements, A Brief Interlude: On
Coupling and Abstractions

collaborators, The Unit of Work Collaborates with the Repository

collections, What Is an Aggregate?

Command Handler pattern, Wrap-Up

command-query responsibility segregation (CQRS), Command-Query
Responsibility Segregation (CQRS)-Wrap-Up

building read-only views into our data, Hold On to Your Lunch,
Folks

changing read model implementation to use Redis, Changing Our
Read Model Implementation Is Easy

denormalized copy of your data optimized for read operations,
Time to Completely Jump the Shark

domain model not optimized for read operations, Your Domain
Model Is Not Optimized for Read Operations

domain models for writing, Domain Models Are for Writing

full-blown CQRS versus simpler options, Wrap-Up

Post/Redirect/Get pattern and CQS, Post/Redirect/Get and CQS

read side and write side, Most Users Aren’t Going to Buy Your
Furniture

reads, Most Users Aren’t Going to Buy Your Furniture

consistency of, Most Users Aren’t Going to Buy Your
Furniture

rebuilding view model from scratch, Updating a Read Model
Table Using an Event Handler

SELECT N+1 and other performance problems, SELECT N+1
and Other Performance Considerations

simple view using existing repository, “Obvious” Alternative 1:
Using the Existing Repository

testing views, Testing CQRS Views

trade-offs for view model options, Wrap-Up

updating read model table using event handler, Time to
Completely Jump the Shark

view that uses the ORM, “Obvious” Alternative 2: Using the
ORM

commands, Commands and Command Handler-Wrap-Up

command flow to reserve stock, confirm reservation, dispatch
goods, and make customer VIP, Distributed Ball of Mud, and
Thinking in Nouns

command flow when warehouse knows stock is damaged,
Distributed Ball of Mud, and Thinking in Nouns

command flow with error, Error Handling in Distributed Systems

command handler logic in message bus, Message Bus Is Given
Handlers at Runtime

events versus, Commands and Events-Commands and Events

events, commands, and error handling, Discussion: Events,
Commands, and Error Handling-Discussion: Events, Commands,
and Error Handling

recovering from errors synchronously, Recovering from
Errors Synchronously

exception handling, Differences in Exception Handling

handlers for, Differences in Exception Handling

in our system now, Commands and Events

program output as list of commands, Choosing the Right
Abstraction(s)

splitting commands and events, trade-offs, Wrap-Up

commits

commit method, The Real Unit of Work Uses SQLAlchemy
Sessions

explicit tests for, Explicit Tests for Commit/Rollback Behavior

explicit versus implicit, Explicit Versus Implicit Commits

component diagram at end of Part One, Part I Recap

composition over inheritance in TrackingRepository wrapper class,
Option 3: The UoW Publishes Events to the Message Bus

composition root, Dependency Injection (and Bootstrapping), Aren’t
Explicit Dependencies Totally Weird and Java-y?

concurrency, Invariants, Concurrency, and Locks

aggregates and concurrency issues, Wrap-Up

allowing for greatest degree of, What Is an Aggregate?

enforcing rules using database transactions, Enforcing
Concurrency Rules by Using Database Transaction Isolation
Levels

integration test for, Testing for Our Data Integrity Rules

not provided by message bus implementation, The Message Bus
Maps Events to Handlers

optimistic concurrency with version numbers, Optimistic
Concurrency with Version Numbers-Implementation Options for
Version Numbers

pessimistic concurrency example, SELECT FOR UPDATE,
Pessimistic Concurrency Control Example: SELECT FOR
UPDATE

reproducing behavior with time.sleep function, Testing for Our
Data Integrity Rules

connascence, Error Handling in Distributed Systems

consistency, Invariants, Constraints, and Consistency

attainment of read consistency, Most Users Aren’t Going to Buy
Your Furniture

eventually consistent reads, Most Users Aren’t Going to Buy Your
Furniture

consistency boundaries, Aggregates and Consistency Boundaries, What
Is an Aggregate?

aggregates acting as, Discussion: Events, Commands, and Error
Handling

microservices as, The Alternative: Temporal Decoupling Using
Asynchronous Messaging

recap, Wrap-Up

constraints, Invariants, Constraints, and Consistency

context manager, Unit of Work Pattern

starting Unit of Work as, The Unit of Work Collaborates with the
Repository

Unit of Work and, Unit of Work and Its Context Manager-Fake
Unit of Work for Testing

control flow, using exceptions for, The Model Raises Events

coupling, A Brief Interlude: On Coupling and Abstractions

avoiding inappropriate coupling, Error Handling in Distributed
Systems

disadvantages of, A Brief Interlude: On Coupling and
Abstractions

domain logic coupled with I/O, Abstracting State Aids Testability

failure cascade as temporal coupling, Error Handling in
Distributed Systems

in tests that use mocks, Why Not Just Patch It Out?

reducing by abstracting away details, A Brief Interlude: On
Coupling and Abstractions

separating what you want to do from how to do it, Choosing the
Right Abstraction(s)

temporal decoupling using asynchronous messaging, The
Alternative: Temporal Decoupling Using Asynchronous

Messaging

trade-off between design feedback and, On Deciding What Kind
of Tests to Write

CQRS (see command-query responsibility segregation)

CQS (command-query separation), Post/Redirect/Get and CQS

CRUD wrapper around a database, Part I Recap

CSV over SMTP architecture, Why Not Just Run Everything in a
Spreadsheet?

CSVs, doing everything with, Swapping Out the Infrastructure: Do
Everything with CSVs-Implementing a Repository and Unit of Work
for CSVs

D

data access, applying dependency inversion principle to, Applying the
DIP to Data Access

data integrity

issues arising from splitting operation across two UoWs,
Implementing Our New Requirement

testing for, Testing for Our Data Integrity Rules-Pessimistic
Concurrency Control Example: SELECT FOR UPDATE

data storage, Repository pattern and, Repository Pattern

databases

SQLAlchemy adding session for Unit of Work, The Real Unit of
Work Uses SQLAlchemy Sessions

testing allocations persisted to database, The Straightforward
Implementation

testing transactions against real database, Explicit Tests for
Commit/Rollback Behavior

Unit of Work pattern managing state for, Unit of Work Pattern

dataclasses

events, Events Are Simple Dataclasses

use for message types, Recovering from Errors Synchronously

use for value objects, Dataclasses Are Great for Value Objects

deallocate service, building (exerise), A Typical Service Function

dependencies

abstract dependencies of service layer, The DIP in Action

testing, The DIP in Action

circular dependencies between event handlers, Wrap-Up

depending on abstractions, A Typical Service Function

edge-to-edge testing with dependency injection, Testing Edge to
Edge with Fakes and Dependency Injection-Testing Edge to Edge
with Fakes and Dependency Injection

keeping all domain dependencies in fixture functions, Mitigation:
Keep All Domain Dependencies in Fixture Functions

none in domain model, Applying the DIP to Data Access

real service layer dependencies at runtime, The DIP in Action

service layer dependency on abstract UoW, Using the UoW in the
Service Layer

UoW no longer dependent on message bus, The Message Bus
Now Collects Events from the UoW

dependency chains, A Bootstrap Script

dependency injection, Dependency Injection (and Bootstrapping)-An
Alternative Using Classes

by inspecting function signatures, A Bootstrap Script

explicit dependencies are better than implicit dependencies,
Aren’t Explicit Dependencies Totally Weird and Java-y?

implicit versus explicit dependencies, Implicit Versus Explicit
Dependencies

manual creation of partial functions inline, A Bootstrap Script

manual DI with closures or partial functions, Preparing Handlers:
Manual DI with Closures and Partials

recap of DI and bootstrap, Wrap-Up

using classes, An Alternative Using Classes

using DI framework, A Bootstrap Script

dependency inversion principle, Applying the DIP to Data Access,
Wrap-Up

declaring explicit dependency as example of, Aren’t Explicit
Dependencies Totally Weird and Java-y?

ORM depends on the data model, Inverting the Dependency:
ORM Depends on Model

dictionaries

dictionary of hashes to paths, Implementing Our Chosen
Abstractions

for filesystem operations, Choosing the Right Abstraction(s)

HANDLERS dicts for commands and events, Differences in
Exception Handling

directory structure, putting project into folders, Putting Things in
Folders to See Where It All Belongs

Distributed Ball of Mud anti-pattern

and thinking in nouns, Distributed Ball of Mud, and Thinking in
Nouns-Distributed Ball of Mud, and Thinking in Nouns

avoiding, The Alternative: Temporal Decoupling Using
Asynchronous Messaging

Django, Repository and Unit of Work Patterns with Django-Steps
Along the Way

applying patterns to Django app, What to Do If You Already Have
Django

steps along the way, Steps Along the Way

installing, Repository and Unit of Work Patterns with Django

ORM example, The “Normal” ORM Way: Model Depends on
ORM

Repository pattern with, Repository Pattern with Django-Custom
Methods on Django ORM Classes to Translate to/from Our
Domain Model

Unit of Work pattern with, Unit of Work Pattern with Django-Unit
of Work Pattern with Django

using, difficulty of, Why Was This All So Hard?

views are adapters, API: Django Views Are Adapters

Docker dev environment with real fake email server, Figure Out How
to Integration Test the Real Thing

domain driven design (DDD), Domain Modeling, What Is a Domain
Model?

(see also domain model; domain modeling)

Aggregate pattern, What Is an Aggregate?

bounded contexts, Choosing an Aggregate

choosing the right aggregate, references on, Wrap-Up

domain, defined, What Is a Domain Model?

Repository pattern and, What Is the Trade-Off?

Domain Events pattern, Events and the Message Bus

domain exceptions, Exceptions Can Express Domain Concepts Too

domain language, Exploring the Domain Language

domain layer

fully decoupling service layer from, Fully Decoupling the
Service-Layer Tests from the Domain-Adding a Missing Service

tests moving to service layer, Should Domain Layer Tests Move
to the Service Layer?

reasons for, Should Domain Layer Tests Move to the
Service Layer?

domain model, Reminder: Our Model-Introducing the Repository
Pattern

deciding whether to write tests against, On Deciding What Kind
of Tests to Write

Django custom ORM methods for conversion, Custom Methods
on Django ORM Classes to Translate to/from Our Domain Model

email sending code in, avoiding, And Let’s Not Make a Mess of
Our Model Either

events from, passing to message bus in service layer, Option 1:
The Service Layer Takes Events from the Model and Puts Them
on the Message Bus

folder for, Putting Things in Folders to See Where It All Belongs

getting benefits of rich model, The DIP in Action

invariants, constraints, and consistency, Invariants, Constraints,
and Consistency

maintaining small core of tests written against, Wrap-Up

new method on, change_batch_quantity, A New Method on the
Domain Model

not optimized for read operations, Your Domain Model Is Not
Optimized for Read Operations

persisting, Persisting Our Domain Model

raising events, The Model Raises Events

raising events and service layer passing them to message bus,
Wrap-Up

trade-offs as a diagram, Wrap-Up

translating to relational database

normal ORM way, model depends on ORM, The “Normal”
ORM Way: Model Depends on ORM

ORM depends on the model, Inverting the Dependency:
ORM Depends on Model

using spreadsheets instead of, Why Not Just Run Everything in a
Spreadsheet?

writing data, Domain Models Are for Writing

writing tests against, High and Low Gear

domain modeling, Domain Modeling-Exceptions Can Express Domain
Concepts Too

domain language, Exploring the Domain Language

functions for domain services, Not Everything Has to Be an
Object: A Domain Service Function-Exceptions Can Express
Domain Concepts Too

unit testing domain models, Unit Testing Domain Models-Value
Objects and Entities

dataclasses for value objects, Dataclasses Are Great for
Value Objects

value objects and entities, Value Objects and Entities

domain services, Not Everything Has to Be an Object: A Domain
Service Function, Why Is Everything Called a Service?

function for, Not Everything Has to Be an Object: A Domain
Service Function

driven adapters, Putting Things in Folders to See Where It All Belongs

duck typing, The Repository in the Abstract

for ports, What Is a Port and What Is an Adapter, in Python?

E

E2E tests (see end-to-end tests)

eager loading, SELECT N+1 and Other Performance Considerations

edge-to-edge testing, Implementing Our Chosen Abstractions-Testing
Edge to Edge with Fakes and Dependency Injection

Effective Aggregate Design (Vernon), Wrap-Up

email alerts, sending when out of stock, Avoiding Making a Mess-Or
the Service Layer!

end-to-end tests

aiming for one test per feature, Wrap-Up

decoupling of service layer from domain, carrying through to,
Carrying the Improvement Through to the E2E Tests

of allocate API, A First End-to-End Test

replacement with unit tests, Why Not Just Patch It Out?

__enter__ and __exit__ magic methods, Unit of Work and Its Context
Manager, The Real Unit of Work Uses SQLAlchemy Sessions

entities

defined, Value Objects and Entities

identity equality, Value Objects and Entities

value objects versus, Exceptions Can Express Domain Concepts
Too

entrypoints, Putting Things in Folders to See Where It All Belongs

__eq__magic method, Value Objects and Entities

equality operators, implementing on entities, Value Objects and
Entities

error handling

counting as a feature, Wrap-Up

events, commands, and, Discussion: Events, Commands, and
Error Handling-Discussion: Events, Commands, and Error
Handling

in distributed systems, Error Handling in Distributed Systems-
The Alternative: Temporal Decoupling Using Asynchronous
Messaging

errors, recovering from synchronously, Recovering from Errors
Synchronously

Evans, Eric, What Is an Aggregate?

event handlers

imagined architecture in which everything is an event handler,
Imagining an Architecture Change: Everything Will Be an Event
Handler

in message bus, Message Bus Is Given Handlers at Runtime

managing updates to read model, Changing Our Read Model
Implementation Is Easy

updating read model table using, Time to Completely Jump the
Shark

event storming, A New Requirement Leads Us to a New Architecture

event-driven architecture

going to microservices via Strangler pattern, An Event-Driven
Approach to Go to Microservices via Strangler Pattern-An
Event-Driven Approach to Go to Microservices via Strangler
Pattern

using events to integrate microservices, Event-Driven
Architecture: Using Events to Integrate Microservices-Wrap-Up

events

changing schema over time, Footguns

commands versus, Commands and Events-Differences in
Exception Handling

events, commands, and error handling, Discussion: Events,
Commands, and Error Handling-Discussion: Events, Commands,
and Error Handling

internal versus external, Internal Versus External Events

splitting command and events, trade-offs, Wrap-Up

events and the message bus, Events and the Message Bus-Wrap-Up

domain events and message bus recap, Wrap-Up

domain model raising events, The Model Raises Events

events as simple dataclasses, Events Are Simple Dataclasses

events flowing through the system, Events and the Message Bus

message bus mapping events to handlers, The Message Bus Maps
Events to Handlers

pros and cons or trade-offs, Wrap-Up

recording events, The Model Records Events

sending email alerts when out of stock, Avoiding Making a Mess-
Or the Service Layer!

avoiding messing up domain model, And Let’s Not Make a
Mess of Our Model Either

avoiding messing up web controllers, First, Let’s Avoid
Making a Mess of Our Web Controllers

out of place in the service layer, Or the Service Layer!

violating the single responsibility principle, Single
Responsibility Principle

service layer raising its own events, Option 2: The Service Layer
Raises Its Own Events

service layer with explicit message bus, Option 1: The Service
Layer Takes Events from the Model and Puts Them on the
Message Bus

transforming our app into message processor, Going to Town on
the Message Bus-Why Have We Achieved?

imagined architecture, everything will be an event handler,
Imagining an Architecture Change: Everything Will Be an
Event Handler

implementing the new requirement, Implementing Our New
Requirement-Test-Driving a New Handler

modifying API to work with events, A Temporary Ugly
Hack: The Message Bus Has to Return Results

new requirement and new architecture, A New Requirement
Leads Us to a New Architecture

refactoring service functions to message handlers,
Refactoring Service Functions to Message Handlers

temporary hack, message bus returning results, A Temporary
Ugly Hack: The Message Bus Has to Return Results

test driving new handler, Test-Driving a New Handler

tests writtern to in terms of events, Our Tests Are All
Written in Terms of Events Too

unit testing event handlers with fake message bus,
Optionally: Unit Testing Event Handlers in Isolation with a
Fake Message Bus

whole app as message bus, trade-offs, Why Have We
Achieved?

UoW publishes events to message bus, Option 3: The UoW
Publishes Events to the Message Bus

eventually consistent reads, Most Users Aren’t Going to Buy Your
Furniture

exception handling, differences for events and commands, Differences
in Exception Handling

exceptions

expressing domain concepts, Exceptions Can Express Domain
Concepts Too

using for control flow, The Model Raises Events

external events, The Message Bus Maps Events to Handlers, Event-
Driven Architecture: Using Events to Integrate Microservices-Wrap-
Up

extreme programming (XP), exhortation to listen to the code, On
Deciding What Kind of Tests to Write

F

faking

FakeNotifications for unit testing, Make a Fake Version for Your
Tests

FakeRepository, Introducing a Service Layer, and Using
FakeRepository to Unit Test It

adding fixture function on, Mitigation: Keep All Domain
Dependencies in Fixture Functions

new query type on, Implementation

using to unit test the service layer, Introducing a Service
Layer, and Using FakeRepository to Unit Test It

fakes versus mocks, Why Not Just Patch It Out?

FakeSession, using to unit test the service layer, Introducing a
Service Layer, and Using FakeRepository to Unit Test It

FakeUnitOfWork for service layer testing, Fake Unit of Work for
Testing

faking I/O in edge-to-edge test, Testing Edge to Edge with Fakes
and Dependency Injection

tweaking fakes in service layer to call super and implement
underscorey methods, Option 3: The UoW Publishes Events to the
Message Bus

filesystems

writing code to synchronize source and target directories,
Abstracting State Aids Testability-Abstracting State Aids
Testability

choosing right abstraction, Choosing the Right
Abstraction(s)-Implementing Our Chosen Abstractions

implementing chosen abstraction, Implementing Our Chosen
Abstractions-Wrap-Up

fixture functions, keeping all domain dependencies in, Mitigation:
Keep All Domain Dependencies in Fixture Functions

Flask framework, Some Pseudocode: What Are We Going to Need?

API endpoint, What Is the Trade-Off?

calling bootstrap in entrypoints, Using Bootstrap in Our
Entrypoints

endpoint for viewing allocations, Post/Redirect/Get and CQS

Flask API and service layer, Our First Use Case: Flask API and
Service Layer-The DIP in Action

app delegating to service layer, A Typical Service Function

connecting the app to real world, Connecting Our
Application to the Real World

different types of services, Why Is Everything Called a
Service?

end-to-end tests for happy and unhappy paths, A Typical
Service Function

error conditions requiring database checks, Error Conditions
That Require Database Checks

first API end-to-end test, A First End-to-End Test-A First
End-to-End Test

first cut of the app, The Straightforward Implementation-The
Straightforward Implementation

introducing service layer and fake repo to unit test it,
Introducing a Service Layer, and Using FakeRepository to
Unit Test It-A Typical Service Function

putting project into folders, Putting Things in Folders to See
Where It All Belongs

service layer benefits, Wrap-Up

service layer dependencies, The DIP in Action

service layer pros and cons, The DIP in Action

typical service layer function, A Typical Service Function

putting API endpoint in front of allocate domain service,
Connecting Our Application to the Real World

Fowler, Martin, Why Not Just Patch It Out?, Wrap-Up

Freeman, Steve, Why Not Just Patch It Out?

Functional Core, Imperative Shell (FCIS), Implementing Our Chosen
Abstractions

functions, Exceptions Can Express Domain Concepts Too

for domain services, Not Everything Has to Be an Object: A
Domain Service Function

service layer, A Typical Service Function

G

"Global Complexity, Local Simplicity" post, Wrap-Up

__gt__ magic method, Python’s Magic Methods Let Us Use Our
Models with Idiomatic Python

H

handlers

event and command handlers in message bus, Message Bus Is
Given Handlers at Runtime

new HANDLERS dicts for commands and events, Differences in
Exception Handling

__hash__ magic method, Value Objects and Entities

hashing a file, Abstracting State Aids Testability

dictionary of hashes to paths, Choosing the Right Abstraction(s)

hoisting I/O, Why Not Just Patch It Out?

I

I/O

disentangling details from program logic, Implementing Our
Chosen Abstractions

domain logic tightly coupled to, Abstracting State Aids
Testability

simplifying interface with business logic using abstractions,
Wrap-Up

idempotent message handling, Footguns

identity equality (entities), Value Objects and Entities

implicit versus explicit commits, Explicit Versus Implicit Commits

importing dependenies, Aren’t Explicit Dependencies Totally Weird
and Java-y?

inheritance, avoiding use of with wrapper class, Option 3: The UoW
Publishes Events to the Message Bus

integration tests

for concurrency behavior, Testing for Our Data Integrity Rules

test-driving Unit of Work with, Test-Driving a UoW with
Integration Tests

interfaces, Python and, What Is a Port and What Is an Adapter, in
Python?

invariants

invariants, concurrency, and locks, Invariants, Concurrency, and
Locks

invariants, constraints, and consistency, Invariants, Constraints,
and Consistency

protecting while allowing concurrency, What Is an Aggregate?

inward-facing adapters, Putting Things in Folders to See Where It All
Belongs

isolation levels (transaction), Enforcing Concurrency Rules by Using
Database Transaction Isolation Levels

J

Jung, Ed, Why Not Just Patch It Out?

K

katas, A Brief Interlude: On Coupling and Abstractions

L

layered architecture, Applying the DIP to Data Access

case study, layering an overgrown system, Separating Entangled
Responsibilities

locks on database tables, Invariants, Concurrency, and Locks

optimistic locking, Optimistic Concurrency with Version
Numbers, Optimistic Concurrency with Version Numbers

pessimistic locking, Optimistic Concurrency with Version
Numbers

London-school versus classic-style TDD, Why Not Just Patch It Out?

M

magic methods

allowing use of domain model with idiomatic Python, Python’s
Magic Methods Let Us Use Our Models with Idiomatic Python

__enter__ and __exit__, Unit of Work and Its Context Manager

__eq__, Value Objects and Entities

__hash__, Value Objects and Entities

MagicMock objects, Why Not Just Patch It Out?

mappers, Inverting the Dependency: ORM Depends on Model

message brokers, Using a Redis Pub/Sub Channel for Integration

message bus

abstract message bus and its real and fake versions, Optionally:
Unit Testing Event Handlers in Isolation with a Fake Message
Bus

before, message buse as optional add-on, Going to Town on the
Message Bus

Celery and, The Message Bus Maps Events to Handlers

class given handlers at runtime, Message Bus Is Given Handlers
at Runtime

dispatching events and commands differently, Differences in
Exception Handling

event and command handler logic staying the same, Message Bus
Is Given Handlers at Runtime

getting custom with overridden bootstrap defaults, Initializing DI
in Our Tests

handler publishing outgoing event, Our New Outgoing Event

handle_event method, Recovering from Errors Synchronously

handle_event with retries, Recovering from Errors Synchronously

mapping events to handlers, The Message Bus Maps Events to
Handlers

now collecting events from UoW, The Message Bus Now
Collects Events from the UoW

now the main entrypoint to service layer, Going to Town on the
Message Bus

pros and cons or trade-offs, Wrap-Up

recap, Wrap-Up

Redis pub/sub listener as thin adapter around, Redis Is Another
Thin Adapter Around Our Message Bus

returning results in temporary hack, A Temporary Ugly Hack: The
Message Bus Has to Return Results

service layer raising events and calling messagebus.handle,
Option 2: The Service Layer Raises Its Own Events

service layer with explicit message bus, Option 1: The Service
Layer Takes Events from the Model and Puts Them on the
Message Bus

Unit of Work publishing events to, Option 3: The UoW Publishes
Events to the Message Bus

unit testing event handlers with fake message bus, Optionally:
Unit Testing Event Handlers in Isolation with a Fake Message
Bus

whole app as, trade-offs, Why Have We Achieved?

wiring up new event handlers to, A New Method on the Domain
Model

Message Bus pattern, Events and the Message Bus

messaging

asynchronous, temporal decoupling with, The Alternative:
Temporal Decoupling Using Asynchronous Messaging

idempotent message handling, Footguns

reliable messaging is hard, Footguns

using Redis pub/sub channel for microservices integration, Using
a Redis Pub/Sub Channel for Integration

microservices

bounded contexts and, Choosing an Aggregate

event-based integration, Event-Driven Architecture: Using Events
to Integrate Microservices-Wrap-Up

distributed Ball of Mud and thinking in nouns, Distributed
Ball of Mud, and Thinking in Nouns-Distributed Ball of
Mud, and Thinking in Nouns

error handling in distributed systems, Error Handling in
Distributed Systems-The Alternative: Temporal Decoupling
Using Asynchronous Messaging

temporal decoupling using asynchronous messaging, The
Alternative: Temporal Decoupling Using Asynchronous
Messaging

testing with end-to-end test, Test-Driving It All Using an
End-to-End Test-Internal Versus External Events

trade-offs, Wrap-Up

using Redis pub/sub channel for ntegration, Using a Redis
Pub/Sub Channel for Integration

event-driven approach, using Strangler pattern, An Event-Driven
Approach to Go to Microservices via Strangler Pattern-An
Event-Driven Approach to Go to Microservices via Strangler
Pattern

minimum viable product, Persisting Our Domain Model

mock.patch method, Why Not Just Patch It Out?, Aren’t Explicit
Dependencies Totally Weird and Java-y?

mocking

avoiding use of mock.patch, Why Not Just Patch It Out?

don't mock what you don't own, Fake Unit of Work for Testing

mocks versus fakes, Why Not Just Patch It Out?

overmocked tests, pitfalls of, Why Not Just Patch It Out?

"Mocks Aren't Stubs" (Fowler), Why Not Just Patch It Out?

model (domain), What Is a Domain Model?

N

named tuples, Dataclasses Are Great for Value Objects

(see also dataclasses)

nouns, splitting system into, Distributed Ball of Mud, and Thinking in
Nouns-Distributed Ball of Mud, and Thinking in Nouns

O

object neighborhoods, The Unit of Work Collaborates with the
Repository

object-oriented composition, Why Not Just Patch It Out?

object-oriented design principles, Exceptions Can Express Domain
Concepts Too

object-relational mappers (ORMs), The “Normal” ORM Way: Model
Depends on ORM

associating right batches with Product objects, One Aggregate =
One Repository

Django ORM example, The “Normal” ORM Way: Model
Depends on ORM

Django, custom methods to translate to/from domain model,
Custom Methods on Django ORM Classes to Translate to/from
Our Domain Model

ORM depends on the data model, Inverting the Dependency:
ORM Depends on Model

testing the ORM, Inverting the Dependency: ORM Depends
on Model

orm.start_mappers function, A Bootstrap Script

Repository pattern and, What Is the Trade-Off?

SELECT N+1 performance problem, SELECT N+1 and Other
Performance Considerations

simple view using the ORM, “Obvious” Alternative 2: Using the
ORM

SQLAlchemy, model depends on ORM, The “Normal” ORM
Way: Model Depends on ORM

onion architecture, Applying the DIP to Data Access

optimistic concurrency with version numbers, Optimistic Concurrency
with Version Numbers-Implementation Options for Version Numbers

orchestration, Introducing a Service Layer, and Using FakeRepository
to Unit Test It

changing to choreography, Single Responsibility Principle

using application service, Why Is Everything Called a Service?

orchestration layer (see service layer)

Outbox pattern, Footguns

P

partial functions

dependency injection with, Preparing Handlers: Manual DI with
Closures and Partials

difference from closures, Preparing Handlers: Manual DI with
Closures and Partials

manually creating inline, A Bootstrap Script

patterns, deciding whether you need to use them, Part I Recap

PEP 544 protocols, The Repository in the Abstract

performance

consistency boundaries and, Aggregates and Consistency
Boundaries, Wrap-Up

impact of using aggregates, Choosing an Aggregate, What About
Performance?

persistence ignorance, The “Normal” ORM Way: Model Depends on
ORM

trade-offs, Wrap-Up

pessimistic concurrency, Optimistic Concurrency with Version
Numbers

example, SELECT FOR UPDATE, Pessimistic Concurrency
Control Example: SELECT FOR UPDATE

ports

defined, What Is a Port and What Is an Adapter, in Python?

ports-and-adapters inspired patterns, Part I Recap

putting in folder with adapters, Putting Things in Folders to See
Where It All Belongs

Post/Redirect/Get pattern, Post/Redirect/Get and CQS

command-query separation (CQS), Post/Redirect/Get and CQS

PostgreSQL

Anti-Patterns: Read-Modify-Write Cycles, Pessimistic
Concurrency Control Example: SELECT FOR UPDATE

documentation for transaction isolation levels, Enforcing
Concurrency Rules by Using Database Transaction Isolation

Levels

managing concurrency issues, Optimistic Concurrency with
Version Numbers

SERIALIZABLE transaction isolation level, Optimistic
Concurrency with Version Numbers

preparatory refactoring workflow, Imagining an Architecture Change:
Everything Will Be an Event Handler

primitives

moving from domain objects to, in service layer, Refactoring
Service Functions to Message Handlers

primitive obsession, Refactoring Service Functions to Message
Handlers

Product object, Aggregates and Consistency Boundaries

acting as consistency boundary, Discussion: Events, Commands,
and Error Handling

asking Product to allocate against its batches, Choosing an
Aggregate

code for, Choosing an Aggregate

service layer using, One Aggregate = One Repository

two transactions attempting concurrent update on, Optimistic
Concurrency with Version Numbers

version numbers implemented on, Implementation Options for
Version Numbers

ProductRepository object, One Aggregate = One Repository

projects

organizing into folders, Putting Things in Folders to See Where It
All Belongs

template project structure, A Template Project Structure-Wrap-
Up

protocols, abstract base classes, duck typing, and, The Repository in
the Abstract

publish-subscribe system

message bus as

handlers subscribed to receive events, The Message Bus
Maps Events to Handlers

publishing step, Option 1: The Service Layer Takes Events
from the Model and Puts Them on the Message Bus

using Redis pub/sub channel for microservices integration, Using
a Redis Pub/Sub Channel for Integration

PyCon talk on Mocking Pitfalls, Why Not Just Patch It Out?

pytest

@pytest.skip, What About Performance?

fixtures, Abstracting State Aids Testability

pytest-django plug-in, Repository Pattern with Django, Why Was
This All So Hard?

session argument, Inverting the Dependency: ORM Depends on
Model

Q

queries, Command-Query Responsibility Segregation (CQRS)

(see also command-query responsibility segregation)

questions from tech reviewers, Questions Our Tech Reviewers Asked
That We Couldn’t Work into Prose-Footguns

R

read-modify-write failure mode, Pessimistic Concurrency Control
Example: SELECT FOR UPDATE

reallocate service function, Example 1: Reallocate

reallocation

sequence diagram for flow, Implementing Our New Requirement

testing in isolation using fake message bus, Optionally: Unit
Testing Event Handlers in Isolation with a Fake Message Bus

Redis pub/sub channel, using for microservices integration, Using a
Redis Pub/Sub Channel for Integration

testing pub/sub model, Test-Driving It All Using an End-to-End
Test

publishing outgoing event, Our New Outgoing Event

Redis as thin adapter around message bus, Redis Is Another
Thin Adapter Around Our Message Bus

Redis, changing read model implementation to use, Changing Our Read
Model Implementation Is Easy

repositories

adding list method to existing repository object, Hold On to Your
Lunch, Folks

CSV-based repository, Implementing a Repository and Unit of
Work for CSVs

new query type on our repository, Implementation

one aggregrate = one repository, One Aggregate = One
Repository

repository keeping track of aggregates passing through it, Option
3: The UoW Publishes Events to the Message Bus

service layer function depending on abstract repository, A
Typical Service Function

simple view using existing repository, “Obvious” Alternative 1:
Using the Existing Repository

TrackerRepository wrapper class, Option 3: The UoW Publishes
Events to the Message Bus

Unit of Work collaborating with, The Unit of Work Collaborates
with the Repository

Repository pattern, Repository Pattern, Introducing the Repository
Pattern-Wrap-Up

and persistence ignorance, trade-offs, Wrap-Up

building fake repository for tests, Building a Fake Repository for
Tests Is Now Trivial!

ORMs and, What Is the Trade-Off?

recap of important points, Wrap-Up

simplest possible repository, The Repository in the Abstract

testing the repository with retrieving a complex object, What Is
the Trade-Off?

testing the repository with saving an object, What Is the Trade-
Off?

trade-offs, What Is the Trade-Off?

typical repository, What Is the Trade-Off?

using repository directly in API endpoint, What Is the Trade-Off?

with Django, Repository Pattern with Django-Custom Methods on
Django ORM Classes to Translate to/from Our Domain Model

resources, additional required reading, More Required Reading

responsibilities of code, Choosing the Right Abstraction(s)

separating responsibilities, Separating Entangled Responsibilities

case study, layering overgrown system, Separating Entangled
Responsibilities

retries

message bus handle_event with, Recovering from Errors
Synchronously

optimistic concurrency control and, Optimistic Concurrency with
Version Numbers

Tenacity library for, Recovering from Errors Synchronously

Rhodes, Brandon, Why Not Just Patch It Out?

rollbacks, Unit of Work and Its Context Manager

explicit tests for, Explicit Tests for Commit/Rollback Behavior

rollback method, The Real Unit of Work Uses SQLAlchemy
Sessions

S

seams, Wrap-Up

secondary adapters, Putting Things in Folders to See Where It All
Belongs

Seemann, Mark, blog post, Applying the DIP to Data Access

SELECT * FROM WHERE queries, Time to Completely Jump the
Shark

SELECT FOR UPDATE statement, Optimistic Concurrency with
Version Numbers

pessimistic concurrency control example with, Pessimistic
Concurrency Control Example: SELECT FOR UPDATE

SELECT N+1, SELECT N+1 and Other Performance Considerations

service functions

making them event handlers, Imagining an Architecture Change:
Everything Will Be an Event Handler

refactoring to message handlers, Refactoring Service Functions to
Message Handlers

service layer, Our First Use Case: Flask API and Service Layer-The
DIP in Action

benefits of, Wrap-Up

benefits to test-driven development, Wrap-Up

connecting our application to real world, Connecting Our
Application to the Real World

dependencies of, The DIP in Action

real dependencies at runtime, The DIP in Action

testing, The DIP in Action

difference between domain service and, Why Is Everything
Called a Service?

domain layer tests moving to, Should Domain Layer Tests Move
to the Service Layer?

reasons for, Should Domain Layer Tests Move to the
Service Layer?

end-to-end test of allocate API, testing happy and unhappy paths,
A Typical Service Function

error conditions requiring database checks in Flask app, Error
Conditions That Require Database Checks

first cut of Flask app, The Straightforward Implementation-The
Straightforward Implementation

Flask app delegating to, A Typical Service Function

from domain objects to primitives to events as interface,
Refactoring Service Functions to Message Handlers

fully decoupling from the domain, Fully Decoupling the Service-
Layer Tests from the Domain-Adding a Missing Service

introducing and using FakeRepository to unit test it, Introducing a
Service Layer, and Using FakeRepository to Unit Test It-Why Is
Everything Called a Service?

message bus as main entrypoint, Going to Town on the Message
Bus

pros and cons or trade-offs, The DIP in Action

putting project in folders, Putting Things in Folders to See Where
It All Belongs

raising events and passing them to message bus, Wrap-Up

raising its own events, Option 2: The Service Layer Raises Its
Own Events

sending email alerts when out of stock, avoiding, Or the Service
Layer!

taking events from model and putting them on message bus,
Option 1: The Service Layer Takes Events from the Model and
Puts Them on the Message Bus

totally free of event handling concerns, Option 3: The UoW
Publishes Events to the Message Bus

tweaking fakes in to call super and implement underscorey
methods, Option 3: The UoW Publishes Events to the Message
Bus

typical service function, A Typical Service Function

using Product objects, One Aggregate = One Repository

using Unit of Work in, Using the UoW in the Service Layer

using, test pyramid and, How Is Our Test Pyramid Looking?

writing bulk of tests against, Wrap-Up

writing tests against, High and Low Gear

service-layer services vs. domain services, Not Everything Has to Be
an Object: A Domain Service Function

services

application service and domain service, Why Is Everything
Called a Service?

service layer tests only using services, Adding a Missing Service

Session object, Wrap-Up

set, fake repository as wrapper around, Building a Fake Repository for
Tests Is Now Trivial!

simplifying abstractions, Choosing the Right Abstraction(s)

single responsibility principle (SRP), Single Responsibility Principle

Singleton pattern, messagebus.py implementing, Optionally: Unit
Testing Event Handlers in Isolation with a Fake Message Bus

situated software, A New Requirement Leads Us to a New
Architecture

Software Engineering Stack Exchange site, Why Not Just Patch It Out?

spreadsheets, using instead of domain model, Why Not Just Run
Everything in a Spreadsheet?

spy objects, Testing Edge to Edge with Fakes and Dependency
Injection

SQL

generating for domain model objects, The “Normal” ORM Way:
Model Depends on ORM

helpers for Unit of Work, Test-Driving a UoW with Integration
Tests

ORM and Repository pattern as abstractions in front of, What Is
the Trade-Off?

raw SQL in views, Hold On to Your Lunch, Folks

repository test for retrieving complex object, What Is the Trade-
Off?

repository test for saving an object, What Is the Trade-Off?

SQLAlchemy

database session for Unit of Work, The Real Unit of Work Uses
SQLAlchemy Sessions

not mocking, Fake Unit of Work for Testing

declarative syntax, model depends on ORM, The “Normal” ORM
Way: Model Depends on ORM

explicit ORM mapping with SQLAlchemy Table objects,
Inverting the Dependency: ORM Depends on Model

SELECT N+1 problem and, SELECT N+1 and Other
Performance Considerations

Session object, Wrap-Up

using directly in API endpoint, Inverting the Dependency: ORM
Depends on Model

using DSL to specify FOR UPDATE, Pessimistic Concurrency
Control Example: SELECT FOR UPDATE

stakeholders, convincing to try something new, Convincing Your
Stakeholders to Try Something New-Questions Our Tech Reviewers
Asked That We Couldn’t Work into Prose

state

abstracting to aid testability, Abstracting State Aids Testability-
Abstracting State Aids Testability

splitting off from logic in the program, Implementing Our Chosen
Abstractions

storage, Repository Pattern

(see also repositories; Repository pattern)

permanent, UoW providing entrypoint to, The Unit of Work
Collaborates with the Repository

Strangler pattern, going to microservices via, An Event-Driven
Approach to Go to Microservices via Strangler Pattern-An Event-
Driven Approach to Go to Microservices via Strangler Pattern

stubbing, mocks and stubs, Why Not Just Patch It Out?

super function, Option 3: The UoW Publishes Events to the Message
Bus

tweaking fakes in service layer to call, Option 3: The UoW
Publishes Events to the Message Bus

synchronous execution of event-handling code, Wrap-Up

T

temporal coupling, Error Handling in Distributed Systems

temporal decoupling using asynchronous messaging, The Alternative:
Temporal Decoupling Using Asynchronous Messaging

Tenacity library, Recovering from Errors Synchronously

test doubles

mocks versus fakes, Why Not Just Patch It Out?

mocks versus stubs, Why Not Just Patch It Out?

using lists to build, Testing Edge to Edge with Fakes and
Dependency Injection

"Test-Driven Development: That's Not What We Meant", Why Not Just
Patch It Out?

test-driven development (TDD), TDD in High Gear and Low Gear-
Wrap-Up

benefits of service layer to, Wrap-Up

classic versus London-school, Why Not Just Patch It Out?

deciding what kinds of tests to write, On Deciding What Kind of
Tests to Write

domain layer tests moving to service layer, Should Domain Layer
Tests Move to the Service Layer?

fully decoupling service layer from the domain, Fully Decoupling
the Service-Layer Tests from the Domain-Adding a Missing
Service

adding missing service, Adding a Missing Service

carrying improvement through to E2E tests, Carrying the
Improvement Through to the E2E Tests

keeping all domain dependencies in fixture functions,
Mitigation: Keep All Domain Dependencies in Fixture
Functions

high and low gear, High and Low Gear

test pyramid with service layer added, How Is Our Test Pyramid
Looking?

test pyramid, examining, TDD in High Gear and Low Gear

types of tests, rules of thumb for, Wrap-Up

unit tests operating at lower level, acting directly on model, TDD
in High Gear and Low Gear

testing

abstracting state to aid testability, Abstracting State Aids
Testability-Abstracting State Aids Testability

after implementing chosen abstraction, Implementing Our Chosen
Abstractions-Wrap-Up

avoiding use of mock.patch, Why Not Just Patch It Out?-
Wrap-Up

edge-to-edge testing with fakes and dependency injection,
Testing Edge to Edge with Fakes and Dependency Injection-
Testing Edge to Edge with Fakes and Dependency Injection

end-to-end test of pub/sub model, Test-Driving It All Using an
End-to-End Test

fake database session at service layer, Introducing a Service
Layer, and Using FakeRepository to Unit Test It

fake UoW for service layer testing, Fake Unit of Work for Testing

for data integrity rules, Testing for Our Data Integrity Rules-
Pessimistic Concurrency Control Example: SELECT FOR
UPDATE

integration test for CQRS view, Testing CQRS Views

integration test for overriding bootstrap defaults, Initializing DI in
Our Tests

integration tests for rollback behavior, Explicit Tests for
Commit/Rollback Behavior

tests folder tree, Tests

tests written in terms of events, Our Tests Are All Written in
Terms of Events Too

handler tests for change_batch_quantity, Test-Driving a New
Handler

unit testing event handlers with fake message bus,
Optionally: Unit Testing Event Handlers in Isolation with a
Fake Message Bus

Unit of Work with integration tests, Test-Driving a UoW with
Integration Tests

tidying up tests, Tidying Up the Integration Tests

unit test for bootstrap, Initializing DI in Our Tests

unit testing with fakes at service layer, Introducing a Service
Layer, and Using FakeRepository to Unit Test It

time.sleep function, Testing for Our Data Integrity Rules

reproducing concurrency behavior with, Testing for Our Data
Integrity Rules

transactions

concurrent, attempting update on Product, Optimistic Concurrency
with Version Numbers

simulating a slow transaction, Testing for Our Data Integrity
Rules

Unit of Work and, Wrap-Up

using to enforce concurrency rules, Enforcing Concurrency Rules
by Using Database Transaction Isolation Levels

type hints, Unit Testing Domain Models, Unit Testing Domain Models

U

underscorey methods

avoiding by implementing TrackingRepository wrapper class,
Option 3: The UoW Publishes Events to the Message Bus

tweaking fakes in service layer to implement, Option 3: The UoW
Publishes Events to the Message Bus

Unit of Work pattern, The Repository in the Abstract, Unit of Work
Pattern-Wrap-Up

and its context manager, Unit of Work and Its Context Manager

fake UoW for testing, Fake Unit of Work for Testing

real UoW using SQLAlchemy session, The Real Unit of
Work Uses SQLAlchemy Sessions

benefits of using, Wrap-Up

collaboration with repository, The Unit of Work Collaborates
with the Repository

explicit tests for commit/rollback behavior, Explicit Tests for
Commit/Rollback Behavior

explicit versus implicit commits, Explicit Versus Implicit
Commits

fake message bus implemented in UoW, Optionally: Unit Testing
Event Handlers in Isolation with a Fake Message Bus

getting rid of underscorey methods in UoW class, Option 3: The
UoW Publishes Events to the Message Bus

managing database state, Unit of Work Pattern

message bus now collecting events from UoW, The Message Bus
Now Collects Events from the UoW

modifying to connect domain events and message bus, Events and
the Message Bus

pros and cons or trade-offs, Wrap-Up

recap of important points, Wrap-Up

splitting operations across two UoWs, Implementing Our New
Requirement

test driving with integration tests, Test-Driving a UoW with
Integration Tests

tidying up integration tests, Tidying Up the Integration Tests

UoW and product repository, One Aggregate = One Repository

UoW collecting events from aggregates and passing them to
message bus, Wrap-Up

UoW for CSVs, Implementing a Repository and Unit of Work for
CSVs

UoW managing success or failure of aggregate update,
Discussion: Events, Commands, and Error Handling

UoW publishing events to message bus, Option 3: The UoW
Publishes Events to the Message Bus

using UoW in service layer, Using the UoW in the Service Layer

using UoW to group multiple operations into atomic unit,
Examples: Using UoW to Group Multiple Operations into an
Atomic Unit-Example 2: Change Batch Quantity

changing batch quantity example, Example 2: Change Batch
Quantity

reallocate function example, Example 1: Reallocate

with Django, Unit of Work Pattern with Django-Unit of Work
Pattern with Django

without, API talking directly to three layers, Unit of Work Pattern

unit testing, Introducing a Service Layer, and Using FakeRepository to
Unit Test It

(see also test-driven development; testing)

of domain models, Unit Testing Domain Models-Value Objects
and Entities

unit tests replacing end-to-end tests, Why Not Just Patch It Out?

unittest.mock function, Why Not Just Patch It Out?

UoW (see Unit of Work pattern)

use-case layer (see service layer)

V

validation, Validation-Validating Pragmatics

value objects

defined, Dataclasses Are Great for Value Objects

and entities, Value Objects and Entities

entities versus, Exceptions Can Express Domain Concepts Too

math with, Dataclasses Are Great for Value Objects

using dataclasses for, Dataclasses Are Great for Value Objects

Vens, Rob, Wrap-Up

Vernon, Vaughn, Wrap-Up

version numbers

implementation options for, Implementation Options for Version
Numbers

in the products table, implementing optimistic locking, Optimistic
Concurrency with Version Numbers

views

Django views as adapters, API: Django Views Are Adapters

keeping totally separate, denormalized datastore for view model,
Time to Completely Jump the Shark

read-only, Post/Redirect/Get and CQS

rebuilding view model from scratch, Updating a Read Model
Table Using an Event Handler

simple view that uses the ORM, “Obvious” Alternative 2: Using
the ORM

simple view that uses the repository, “Obvious” Alternative 1:
Using the Existing Repository

testing CQRS views, Testing CQRS Views

trade-offs for view model options, Wrap-Up

updating read model table using event handler, Time to
Completely Jump the Shark

W

web controllers, sending email alerts via, avoiding, Avoiding Making
a Mess

About the Authors

Harry Percival spent a few years being deeply unhappy as a
management consultant. Soon he rediscovered his true geek nature and
was lucky enough to fall in with a bunch of XP fanatics, working on

pioneering the sadly defunct Resolver One spreadsheet. He worked at
PythonAnywhere LLP, spreading the gospel of TDD worldwide at
talks, workshops, and conferences. He is now with MADE.com.

Bob Gregory is a UK-based software architect with MADE.com. He
has been building event-driven systems with domain-driven design for

more than a decade.

Colophon

The animal on the cover of Architecture Patterns with Python is a
Burmese python (Python bivitattus). As you might expect, the Burmese
python is native to Southeast Asia. Today it lives in jungles and

marshes in South Asia, Myanmar, China, and Indonesia; it’s also
invasive in Florida’s Everglades.

Burmese pythons are one of the world’s largest species of snakes.
These nocturnal, carnivorous constrictors can grow to 23 feet and 200
pounds. Females are larger than males. They can lay up to a hundred

eggs in one clutch. In the wild, Burmese pythons live an average of 20
to 25 years.

The markings on a Burmese python begin with an arrow-shaped spot of
light brown on top of the head and continue along the body in

rectangles that stand out against its otherwise tan scales. Before they
reach their full size, which takes two to three years, Burmese pythons

live in trees hunting small mammals and birds. They also swim for
long stretches of time—going up to 30 minutes without air.

Because of habitat destruction, the Burmese python has a conservation

status of Vulnerable. Many of the animals on O’Reilly’s covers are

endangered; all of them are important to the world.

The color illustration is by Jose Marzan, based on a black-and-white

engraving from Encyclopedie D’Histoire Naturelle. The cover fonts
are URW Typewriter and Guardian Sans. The text font is Adobe

Minion Pro; the heading font is Adobe Myriad Condensed; and the
code font is Dalton Maag’s Ubuntu Mono.

