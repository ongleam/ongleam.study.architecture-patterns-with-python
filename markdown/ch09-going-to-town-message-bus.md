# Chapter 9. Going to Town on the Message Bus

Chapter 9. Going to Town on
the Message Bus

In this chapter, we’ll start to make events more fundamental to the
internal structure of our application. We’ll move from the current state
in Figure 9-1, where events are an optional side effect…

Figure 9-1. Before: the message bus is an optional add-on

…to the situation in Figure 9-2, where everything goes via the message
bus, and our app has been transformed fundamentally into a message
processor.

Figure 9-2. The message bus is now the main entrypoint to the service layer

The code for this chapter is in the chapter_09_all_messagebus branch on GitHub:

TIP

git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_09_all_messagebus
# or to code along, checkout the previous chapter:
git checkout chapter_08_events_and_message_bus

A New Requirement Leads Us to a New
Architecture

Rich Hickey talks about situated software, meaning software that runs
for extended periods of time, managing a real-world process.
Examples include warehouse-management systems, logistics
schedulers, and payroll systems.

This software is tricky to write because unexpected things happen all
the time in the real world of physical objects and unreliable humans.
For example:

During a stock-take, we discover that three SPRINGY-
MATTRESSes have been water damaged by a leaky roof.

A consignment of RELIABLE-FORKs is missing the required
documentation and is held in customs for several weeks.
Three RELIABLE-FORKs subsequently fail safety testing and
are destroyed.

A global shortage of sequins means we’re unable to
manufacture our next batch of SPARKLY-BOOKCASE.

In these types of situations, we learn about the need to change batch
quantities when they’re already in the system. Perhaps someone made
a mistake on the number in the manifest, or perhaps some sofas fell off
a truck. Following a conversation with the business,  we model the
situation as in Figure 9-3.

1

Figure 9-3. Batch quantity changed means deallocate and reallocate

An event we’ll call BatchQuantityChanged should lead us to change
the quantity on the batch, yes, but also to apply a business rule: if the
new quantity drops to less than the total already allocated, we need to
deallocate those orders from that batch. Then each one will require a
new allocation, which we can capture as an event called
AllocationRequired.

Perhaps you’re already anticipating that our internal message bus and
events can help implement this requirement. We could define a service
called change_batch_quantity that knows how to adjust batch
quantities and also how to deallocate any excess order lines, and then
each deallocation can emit an AllocationRequired event that can be
forwarded to the existing allocate service, in separate transactions.

Once again, our message bus helps us to enforce the single

responsibility principle, and it allows us to make choices about
transactions and data integrity.

Imagining an Architecture Change: Everything
Will Be an Event Handler

But before we jump in, think about where we’re headed. There are two
kinds of flows through our system:

API calls that are handled by a service-layer function

Internal events (which might be raised as a side effect of a
service-layer function) and their handlers (which in turn call
service-layer functions)

Wouldn’t it be easier if everything was an event handler? If we rethink

our API calls as capturing events, the service-layer functions can be
event handlers too, and we no longer need to make a distinction

between internal and external event handlers:

services.allocate() could be the handler for an
AllocationRequired event and could emit Allocated
events as its output.

services.add_batch() could be the handler for a
BatchCreated event.

2

Our new requirement will fit the same pattern:

An event called BatchQuantityChanged can invoke a
handler called change_batch_quantity().

And the new AllocationRequired events that it may raise
can be passed on to services.allocate() too, so there is
no conceptual difference between a brand-new allocation
coming from the API and a reallocation that’s internally
triggered by a deallocation.

All sound like a bit much? Let’s work toward it all gradually. We’ll

follow the Preparatory Refactoring workflow, aka “Make the change
easy; then make the easy change”:

1. We refactor our service layer into event handlers. We can get
used to the idea of events being the way we describe inputs to
the system. In particular, the existing services.allocate()
function will become the handler for an event called
AllocationRequired.

2. We build an end-to-end test that puts

BatchQuantityChanged events into the system and looks for
Allocated events coming out.

3. Our implementation will conceptually be very simple: a new

handler for BatchQuantityChanged events, whose
implementation will emit AllocationRequired events,
which in turn will be handled by the exact same handler for
allocations that the API uses.

Along the way, we’ll make a small tweak to the message bus and UoW,

moving the responsibility for putting new events on the message bus

into the message bus itself.

Refactoring Service Functions to
Message Handlers

We start by defining the two events that capture our current API inputs
—AllocationRequired and BatchCreated:

BatchCreated and AllocationRequired events
(src/allocation/domain/events.py)

@dataclass
class BatchCreated(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

...

@dataclass
class AllocationRequired(Event):
    orderid: str
    sku: str
    qty: int

Then we rename services.py to handlers.py; we add the existing
message handler for send_out_of_stock_notification; and most
importantly, we change all the handlers so that they have the same

inputs, an event and a UoW:

Handlers and services are the same thing
(src/allocation/service_layer/handlers.py)

def add_batch(
        event: events.BatchCreated, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku=event.sku)
        ...

def allocate(
        event: events.AllocationRequired, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    ...

def send_out_of_stock_notification(
        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
):
    email.send(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )

The change might be clearer as a diff:

Changing from services to handlers

(src/allocation/service_layer/handlers.py)

 def add_batch(
-        ref: str, sku: str, qty: int, eta: Optional[date],
-        uow: unit_of_work.AbstractUnitOfWork
+        event: events.BatchCreated, uow: unit_of_work.AbstractUnitOfWork
 ):
     with uow:
-        product = uow.products.get(sku=sku)
+        product = uow.products.get(sku=event.sku)
     ...

 def allocate(
-        orderid: str, sku: str, qty: int,
-        uow: unit_of_work.AbstractUnitOfWork
+        event: events.AllocationRequired, uow: unit_of_work.AbstractUnitOfWork
 ) -> str:
-    line = OrderLine(orderid, sku, qty)
+    line = OrderLine(event.orderid, event.sku, event.qty)
     ...

+

+def send_out_of_stock_notification(
+        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
+):
+    email.send(
     ...

Along the way, we’ve made our service-layer’s API more structured

and more consistent. It was a scattering of primitives, and now it uses
well-defined objects (see the following sidebar).

FROM  DOM AIN OBJECT S, VIA PRIM IT IVE OBSESSION, T O
EVENT S AS AN INT ERFACE

Som e of you m ay rem em ber “Fully Decoupling the Service-Layer Tes ts  from  the Dom ain”, in
which we changed our s ervice-layer API from  being in term s  of dom ain objects  to prim itives . And
now we’re m oving back, but to different objects ? What gives ?

In OO circles , people talk about prim itive ob session as  an anti-pattern: avoid prim itives  in public
APIs , and ins tead wrap them  with cus tom  value clas s es , they would s ay. In the Python world, a lot
of people would be quite s keptical of that as  a rule of thum b. When m indles s ly applied, it’s
certainly a recipe for unneces s ary com plexity. So that’s  not what we’re doing per s e.

The m ove from  dom ain objects  to prim itives  bought us  a nice bit of decoupling: our client code
was  no longer coupled directly to the dom ain, s o the s ervice layer could pres ent an API that s tays
the s am e even if we decide to m ake changes  to our m odel, and vice vers a.

So have we gone backward? Well, our core dom ain m odel objects  are s till free to vary, but
ins tead we’ve coupled the external world to our event clas s es . They’re part of the dom ain too, but
the hope is  that they vary les s  often, s o they’re a s ens ible artifact to couple on.

And what have we bought ours elves ? Now, when invoking a us e cas e in our application, we no
longer need to rem em ber a particular com bination of prim itives , but jus t a s ingle event clas s  that
repres ents  the input to our application. That’s  conceptually quite nice. On top of that, as  you’ll s ee
in Appendix E, thos e event clas s es  can be a nice place to do s om e input validation.

The Message Bus Now Collects Events from the
UoW

Our event handlers now need a UoW. In addition, as our message bus

becomes more central to our application, it makes sense to put it

explicitly in charge of collecting and processing new events. There

was a bit of a circular dependency between the UoW and message bus
until now, so this will make it one-way:

Handle takes a UoW and manages a queue

(src/allocation/service_layer/messagebus.py)

def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())

The message bus now gets passed the UoW each time it starts up.

When we begin handling our first event, we start a queue.

We pop events from the front of the queue and invoke their
handlers (the HANDLERS dict hasn’t changed; it still maps event
types to handler functions).

The message bus passes the UoW down to each handler.

After each handler finishes, we collect any new events that have
been generated and add them to the queue.

In unit_of_work.py, publish_events() becomes a less active
method, collect_new_events():

UoW no longer puts events directly on the bus

(src/allocation/service_layer/unit_of_work.py)

-from . import messagebus
-

 class AbstractUnitOfWork(abc.ABC):
@@ -23,13 +21,11 @@ class AbstractUnitOfWork(abc.ABC):

     def commit(self):
         self._commit()
-        self.publish_events()

-    def publish_events(self):
+    def collect_new_events(self):
         for product in self.products.seen:
             while product.events:
-                event = product.events.pop(0)
-                messagebus.handle(event)
+                yield product.events.pop(0)

The unit_of_work module now no longer depends on
messagebus.

We no longer publish_events automatically on commit. The
message bus is keeping track of the event queue instead.

And the UoW no longer actively puts events on the message bus; it
just makes them available.

Our Tests Are All Written in Terms of Events Too

Our tests now operate by creating events and putting them on the
message bus, rather than invoking service-layer functions directly:

Handler tests use events (tests/unit/test_handlers.py)

class TestAddBatch:

     def test_for_new_product(self):
         uow = FakeUnitOfWork()
-        services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
+        messagebus.handle(
+            events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow
+        )
         assert uow.products.get("CRUNCHY-ARMCHAIR") is not None

         assert uow.committed

...

 class TestAllocate:

     def test_returns_allocation(self):
         uow = FakeUnitOfWork()
-        services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
-        result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
+        messagebus.handle(
+            events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow
+        )
+        result = messagebus.handle(
+            events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow
+        )
         assert result == "batch1"

A Temporary Ugly Hack: The Message Bus Has to
Return Results

Our API and our service layer currently want to know the allocated
batch reference when they invoke our allocate() handler. This
means we need to put in a temporary hack on our message bus to let it
return events:

Message bus returns results
(src/allocation/service_layer/messagebus.py)

 def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
+    results = []
     queue = [event]
     while queue:
         event = queue.pop(0)
         for handler in HANDLERS[type(event)]:
-            handler(event, uow=uow)
+            results.append(handler(event, uow=uow))
             queue.extend(uow.collect_new_events())
+    return results

It’s because we’re mixing the read and write responsibilities in our
system. We’ll come back to fix this wart in Chapter 12.

Modifying Our API to Work with Events

Flask changing to message bus as a diff
(src/allocation/entrypoints/flask_app.py)

 @app.route("/allocate", methods=['POST'])
 def allocate_endpoint():
     try:
-        batchref = services.allocate(
-            request.json['orderid'],
-            request.json['sku'],
-            request.json['qty'],
-            unit_of_work.SqlAlchemyUnitOfWork(),
+        event = events.AllocationRequired(
+            request.json['orderid'], request.json['sku'], request.json['qty'],
         )
+        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())

+        batchref = results.pop(0)
     except InvalidSku as e:

Instead of calling the service layer with a bunch of primitives
extracted from the request JSON…

We instantiate an event.

Then we pass it to the message bus.

And we should be back to a fully functional application, but one that’s
now fully event-driven:

What used to be service-layer functions are now event
handlers.

That makes them the same as the functions we invoke for
handling internal events raised by our domain model.

We use events as our data structure for capturing inputs to the
system, as well as for handing off of internal work packages.

The entire app is now best described as a message processor,
or an event processor if you prefer. We’ll talk about the
distinction in the next chapter.

Implementing Our New Requirement

We’re done with our refactoring phase. Let’s see if we really have
“made the change easy.” Let’s implement our new requirement, shown

in Figure 9-4: we’ll receive as our inputs some new
BatchQuantityChanged events and pass them to a handler, which in
turn might emit some AllocationRequired events, and those in turn
will go back to our existing handler for reallocation.

Figure 9-4. Sequence diagram for reallocation flow

WARNING

When you split things out like this across two units of work, you now have two
database transactions, so you are opening yourself up to integrity issues:
something could happen that means the first transaction completes but the second
one does not. You’ll need to think about whether this is acceptable, and whether
you need to notice when it happens and do something about it. See “Footguns” for
more discussion.

Our New Event

The event that tells us a batch quantity has changed is simple; it just
needs a batch reference and a new quantity:

New event (src/allocation/domain/events.py)

@dataclass
class BatchQuantityChanged(Event):
    ref: str
    qty: int

Test-Driving a New Handler

Following the lessons learned in Chapter 4, we can operate in “high
gear” and write our unit tests at the highest possible level of
abstraction, in terms of events. Here’s what they might look like:

Handler tests for change_batch_quantity
(tests/unit/test_handlers.py)

class TestChangeBatchQuantity:

    def test_changes_available_quantity(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            events.BatchCreated("batch1", "ADORABLE-SETTEE", 100, None), uow
        )
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100

        messagebus.handle(events.BatchQuantityChanged("batch1", 50), uow)

        assert batch.available_quantity == 50

    def test_reallocates_if_necessary(self):
        uow = FakeUnitOfWork()
        event_history = [
            events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
            events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50,
date.today()),
            events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
            events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
        ]
        for e in event_history:
            messagebus.handle(e, uow)
        [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
        assert batch1.available_quantity == 10
        assert batch2.available_quantity == 50

        messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

        # order1 or order2 will be deallocated, so we'll have 25 - 20
        assert batch1.available_quantity == 5
        # and 20 will be reallocated to the next batch
        assert batch2.available_quantity == 30

The simple case would be trivially easy to implement; we just
modify a quantity.

But if we try to change the quantity to less than has been allocated,
we’ll need to deallocate at least one order, and we expect to
reallocate it to a new batch.

Implementation

Our new handler is very simple:

Handler delegates to model layer

(src/allocation/service_layer/handlers.py)

def change_batch_quantity(
        event: events.BatchQuantityChanged, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit()

We realize we’ll need a new query type on our repository:

A new query type on our repository
(src/allocation/adapters/repository.py)

class AbstractRepository(abc.ABC):
    ...

    def get(self, sku) -> model.Product:
        ...

    def get_by_batchref(self, batchref) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod

    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> model.Product:
        raise NotImplementedError
    ...

class SqlAlchemyRepository(AbstractRepository):
    ...

    def _get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()

    def _get_by_batchref(self, batchref):
        return self.session.query(model.Product).join(model.Batch).filter(
            orm.batches.c.reference == batchref,
        ).first()

And on our FakeRepository too:

Updating the fake repo too (tests/unit/test_handlers.py)

class FakeRepository(repository.AbstractRepository):
    ...

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next((
            p for p in self._products for b in p.batches
            if b.reference == batchref
        ), None)

NOTE

We’re adding a query to our repository to make this use case easier to implement.
So long as our query is returning a single aggregate, we’re not bending any rules.
If you find yourself writing complex queries on your repositories, you might want
to consider a different design. Methods like get_most_popular_products or
find_products_by_order_id in particular would definitely trigger our spidey
sense. Chapter 11 and the epilogue have some tips on managing complex queries.

A New Method on the Domain Model

We add the new method to the model, which does the quantity change
and deallocation(s) inline and publishes a new event. We also modify

the existing allocate function to publish an event:

Our model evolves to capture the new requirement
(src/allocation/domain/model.py)

class Product:
    ...

    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in self.batches if b.reference == ref)
        batch._purchased_quantity = qty
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            self.events.append(
                events.AllocationRequired(line.orderid, line.sku, line.qty)
            )
...

class Batch:
    ...

    def deallocate_one(self) -> OrderLine:
        return self._allocations.pop()

We wire up our new handler:

The message bus grows
(src/allocation/service_layer/messagebus.py)

HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.BatchQuantityChanged: [handlers.change_batch_quantity],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],

}  # type: Dict[Type[events.Event], List[Callable]]

And our new requirement is fully implemented.

Optionally: Unit Testing Event Handlers in
Isolation with a Fake Message Bus

Our main test for the reallocation workflow is edge-to-edge (see the
example code in “Test-Driving a New Handler”). It uses the real
message bus, and it tests the whole flow, where the
BatchQuantityChanged event handler triggers deallocation, and
emits new AllocationRequired events, which in turn are handled by
their own handlers. One test covers a chain of multiple events and
handlers.

Depending on the complexity of your chain of events, you may decide
that you want to test some handlers in isolation from one another. You
can do this using a “fake” message bus.

In our case, we actually intervene by modifying the
publish_events() method on FakeUnitOfWork and decoupling it
from the real message bus, instead making it record what events it

sees:

Fake message bus implemented in UoW (tests/unit/test_handlers.py)

class FakeUnitOfWorkWithFakeMessageBus(FakeUnitOfWork):

    def __init__(self):
        super().__init__()
        self.events_published = []  # type: List[events.Event]

    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                self.events_published.append(product.events.pop(0))

Now when we invoke messagebus.handle() using the
FakeUnitOfWorkWithFakeMessageBus, it runs only the handler for
that event. So we can write a more isolated unit test: instead of
checking all the side effects, we just check that
BatchQuantityChanged leads to AllocationRequired if the
quantity drops below the total already allocated:

Testing reallocation in isolation (tests/unit/test_handlers.py)

def test_reallocates_if_necessary_isolated():
    uow = FakeUnitOfWorkWithFakeMessageBus()

    # test setup as before
    event_history = [
        events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
        events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
        events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),

        events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
    ]
    for e in event_history:
        messagebus.handle(e, uow)
    [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
    assert batch1.available_quantity == 10
    assert batch2.available_quantity == 50

    messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

    # assert on new events emitted rather than downstream side-effects
    [reallocation_event] = uow.events_published
    assert isinstance(reallocation_event, events.AllocationRequired)
    assert reallocation_event.orderid in {'order1', 'order2'}
    assert reallocation_event.sku == 'INDIFFERENT-TABLE'

Whether you want to do this or not depends on the complexity of your
chain of events. We say, start out with edge-to-edge testing, and resort
to this only if necessary.

EXERCISE FOR T HE READER

A great way to force yours elf to really unders tand s om e code is  to refactor it. In the dis cus s ion of
tes ting handlers  in is olation, we us ed s om ething called FakeUnitOfWorkWithFakeMessageBus,
which is  unneces s arily com plicated and violates  the SRP.

If we change the m es s age bus  to being a clas s ,  then building a FakeMessageBus is  m ore
s traightforward:

3

An ab stract m essage b us and its real and fak e versions

class AbstractMessageBus:
    HANDLERS: Dict[Type[events.Event], List[Callable]]

    def handle(self, event: events.Event):
        for handler in self.HANDLERS[type(event)]:
            handler(event)

class MessageBus(AbstractMessageBus):
    HANDLERS = {
        events.OutOfStock: [send_out_of_stock_notification],

    }

class FakeMessageBus(messagebus.AbstractMessageBus):
    def __init__(self):
        self.events_published = []  # type: List[events.Event]
        self.handlers = {
            events.OutOfStock: [lambda e: self.events_published.append(e)]
        }

So jum p into the code on GitHub and s ee if you can get a clas s -bas ed vers ion working, and then
write a vers ion of test_reallocates_if_necessary_isolated() from  earlier.

We us e a clas s -bas ed m es s age bus  in Chapter 13, if you need m ore ins piration.

Wrap-Up

Let’s look back at what we’ve achieved, and think about why we did
it.

What Have We Achieved?

Events are simple dataclasses that define the data structures for inputs
and internal messages within our system. This is quite powerful from a
DDD standpoint, since events often translate really well into business
language (look up event storming if you haven’t already).

Handlers are the way we react to events. They can call down to our
model or call out to external services. We can define multiple handlers
for a single event if we want to. Handlers can also raise other events.
This allows us to be very granular about what a handler does and
really stick to the SRP.

Why Have We Achieved?

Our ongoing objective with these architectural patterns is to try to have
the complexity of our application grow more slowly than its size.
When we go all in on the message bus, as always we pay a price in
terms of architectural complexity (see Table 9-1), but we buy

ourselves a pattern that can handle almost arbitrarily complex
requirements without needing any further conceptual or architectural
change to the way we do things.

Here we’ve added quite a complicated use case (change quantity,
deallocate, start new transaction, reallocate, publish external
notification), but architecturally, there’s been no cost in terms of

complexity. We’ve added new events, new handlers, and a new
external adapter (for email), all of which are existing categories of
things in our architecture that we understand and know how to reason
about, and that are easy to explain to newcomers. Our moving parts

each have one job, they’re connected to each other in well-defined
ways, and there are no unexpected side effects.

Table 9-1. Whole app is a message bus: the trade-offs

Pros

Cons

A message bus is still a slightly unpredictable way of
doing things from
a web point of view. You don’t know in advance
when things are going to end.

There will be duplication of fields and structure
between model objects and events, which will have a
maintenance cost. Adding a field to one usually
means adding a field to at least
one of the others.

Handlers
and
services
are the
same thing,
so that’s
simpler.

We have a
nice data
structure
for inputs
to the
system.

Now, you may be wondering, where are those
BatchQuantityChanged events going to come from? The answer is
revealed in a couple chapters’ time. But first, let’s talk about events
versus commands.

1  Event-based modeling is so popular that a practice called event storming has been
developed for facilitating event-based requirements gathering and domain model

elaboration.

2  If you’ve done a bit of reading about event-driven architectures, you may be thinking,
“Some of these events sound more like commands!” Bear with us! We’re trying to
introduce one concept at a time. In the next chapter, we’ll introduce the distinction
between commands and events.

3  The “simple” implementation in this chapter essentially uses the messagebus.py module

itself to implement the Singleton Pattern.
