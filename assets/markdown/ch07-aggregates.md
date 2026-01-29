# Chapter 7. Aggregates and Consistency Boundaries

Chapter 7. Aggregates and
Consistency Boundaries

In this chapter, we’d like to revisit our domain model to talk about
invariants and constraints, and see how our domain objects can
maintain their own internal consistency, both conceptually and in

persistent storage. We’ll discuss the concept of a consistency

boundary and show how making it explicit can help us to build high-
performance software without compromising maintainability.

Figure 7-1 shows a preview of where we’re headed: we’ll introduce a
new model object called Product to wrap multiple batches, and we’ll
make the old allocate() domain service available as a method on
Product instead.

Figure 7-1. Adding the Product aggregate

Why? Let’s find out.

The code for this chapter is in the appendix_csvs branch on GitHub:

TIP

git clone https://github.com/cosmicpython/code.git
cd code
git checkout appendix_csvs
# or to code along, checkout the previous chapter:
git checkout chapter_06_uow

Why Not Just Run Everything in a
Spreadsheet?

What’s the point of a domain model, anyway? What’s the fundamental

problem we’re trying to address?

Couldn’t we just run everything in a spreadsheet? Many of our users

would be delighted by that. Business users like spreadsheets because
they’re simple, familiar, and yet enormously powerful.

In fact, an enormous number of business processes do operate by
manually sending spreadsheets back and forth over email. This “CSV
over SMTP” architecture has low initial complexity but tends not to
scale very well because it’s difficult to apply logic and maintain
consistency.

Who is allowed to view this particular field? Who’s allowed to update
it? What happens when we try to order –350 chairs, or 10,000,000
tables? Can an employee have a negative salary?

These are the constraints of a system. Much of the domain logic we
write exists to enforce these constraints in order to maintain the
invariants of the system. The invariants are the things that have to be
true whenever we finish an operation.

Invariants, Constraints, and Consistency

The two words are somewhat interchangeable, but a constraint is a
rule that restricts the possible states our model can get into, while an
invariant is defined a little more precisely as a condition that is
always true.

If we were writing a hotel-booking system, we might have the
constraint that double bookings are not allowed. This supports the
invariant that a room cannot have more than one booking for the same
night.

Of course, sometimes we might need to temporarily bend the rules.
Perhaps we need to shuffle the rooms around because of a VIP
booking. While we’re moving bookings around in memory, we might
be double booked, but our domain model should ensure that, when

we’re finished, we end up in a final consistent state, where the
invariants are met. If we can’t find a way to accommodate all our
guests, we should raise an error and refuse to complete the operation.

Let’s look at a couple of concrete examples from our business
requirements; we’ll start with this one:

An order line can be allocated to only one batch at a time.
—The business

This is a business rule that imposes an invariant. The invariant is that
an order line is allocated to either zero or one batch, but never more
than one. We need to make sure that our code never accidentally calls
Batch.allocate() on two different batches for the same line, and
currently, there’s nothing there to explicitly stop us from doing that.

Invariants, Concurrency, and Locks

Let’s look at another one of our business rules:

We can’t allocate to a batch if the available quantity is less than
the quantity of the order line.

—The business

Here the constraint is that we can’t allocate more stock than is
available to a batch, so we never oversell stock by allocating two
customers to the same physical cushion, for example. Every time we
update the state of the system, our code needs to ensure that we don’t
break the invariant, which is that the available quantity must be greater
than or equal to zero.

In a single-threaded, single-user application, it’s relatively easy for us
to maintain this invariant. We can just allocate stock one line at a time,
and raise an error if there’s no stock available.

This gets much harder when we introduce the idea of concurrency.
Suddenly we might be allocating stock for multiple order lines

simultaneously. We might even be allocating order lines at the same
time as processing changes to the batches themselves.

We usually solve this problem by applying locks to our database
tables. This prevents two operations from happening simultaneously on
the same row or same table.

As we start to think about scaling up our app, we realize that our
model of allocating lines against all available batches may not scale. If
we process tens of thousands of orders per hour, and hundreds of
thousands of order lines, we can’t hold a lock over the whole batches
table for every single one—we’ll get deadlocks or performance
problems at the very least.

What Is an Aggregate?

OK, so if we can’t lock the whole database every time we want to
allocate an order line, what should we do instead? We want to protect
the invariants of our system but allow for the greatest degree of
concurrency. Maintaining our invariants inevitably means preventing
concurrent writes; if multiple users can allocate DEADLY-SPOON at the
same time, we run the risk of overallocating.

On the other hand, there’s no reason we can’t allocate DEADLY-SPOON
at the same time as FLIMSY-DESK. It’s safe to allocate two products at
the same time because there’s no invariant that covers them both. We
don’t need them to be consistent with each other.

The Aggregate pattern is a design pattern from the DDD community

that helps us to resolve this tension. An aggregate is just a domain
object that contains other domain objects and lets us treat the whole
collection as a single unit.

The only way to modify the objects inside the aggregate is to load the
whole thing, and to call methods on the aggregate itself.

As a model gets more complex and grows more entity and value
objects, referencing each other in a tangled graph, it can be hard to

keep track of who can modify what. Especially when we have
collections in the model as we do (our batches are a collection), it’s a

good idea to nominate some entities to be the single entrypoint for
modifying their related objects. It makes the system conceptually

simpler and easy to reason about if you nominate some objects to be in

charge of consistency for the others.

For example, if we’re building a shopping site, the Cart might make a

good aggregate: it’s a collection of items that we can treat as a single

unit. Importantly, we want to load the entire basket as a single blob
from our data store. We don’t want two requests to modify the basket

at the same time, or we run the risk of weird concurrency errors.
Instead, we want each change to the basket to run in a single database

transaction.

We don’t want to modify multiple baskets in a transaction, because
there’s no use case for changing the baskets of several customers at the

same time. Each basket is a single consistency boundary responsible
for maintaining its own invariants.

An AGGREGATE is a cluster of associated objects that we treat as
a unit for the purpose of data changes.

—Eric Evans, Domain-Driven Design blue book

Per Evans, our aggregate has a root entity (the Cart) that encapsulates

access to items. Each item has its own identity, but other parts of the
system will always refer to the Cart only as an indivisible whole.

TIP

Just as we sometimes use _leading_underscores to mark methods or
functions as “private,” you can think of aggregates as being the “public” classes
of our model, and the rest of the entities and value objects as “private.”

Choosing an Aggregate

What aggregate should we use for our system? The choice is somewhat
arbitrary, but it’s important. The aggregate will be the boundary where

we make sure every operation ends in a consistent state. This helps us
to reason about our software and prevent weird race issues. We want

to draw a boundary around a small number of objects—the smaller, the
better, for performance—that have to be consistent with one another,

and we need to give this boundary a good name.

The object we’re manipulating under the covers is Batch. What do we
call a collection of batches? How should we divide all the batches in

the system into discrete islands of consistency?

We could use Shipment as our boundary. Each shipment contains
several batches, and they all travel to our warehouse at the same time.

Or perhaps we could use Warehouse as our boundary: each warehouse
contains many batches, and counting all the stock at the same time
could make sense.

Neither of these concepts really satisfies us, though. We should be able
to allocate DEADLY-SPOONs and FLIMSY-DESKs at the same time, even
if they’re in the same warehouse or the same shipment. These concepts

have the wrong granularity.

When we allocate an order line, we’re interested only in batches that
have the same SKU as the order line. Some sort of concept like
GlobalSkuStock could work: a collection of all the batches for a
given SKU.

It’s an unwieldy name, though, so after some bikeshedding via
SkuStock, Stock, ProductStock, and so on, we decided to simply
call it Product—after all, that was the first concept we came across in
our exploration of the domain language back in Chapter 1.

So the plan is this: when we want to allocate an order line, instead of
Figure 7-2, where we look up all the Batch objects in the world and
pass them to the allocate() domain service…

Figure 7-2. Before: allocate against all batches using the domain service

…we’ll move to the world of Figure 7-3, in which there is a new
Product object for the particular SKU of our order line, and it will be
in charge of all the batches for that SKU, and we can call a
.allocate() method on that instead.

Figure 7-3. After: ask Product to allocate against its batches

Let’s see how that looks in code form:

Our chosen aggregate, Product (src/allocation/domain/model.py)

class Product:

    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            raise OutOfStock(f'Out of stock for sku {line.sku}')

Product’s main identifier is the sku.

Our Product class holds a reference to a collection of batches
for that SKU.

Finally, we can move the allocate() domain service to be a
method on the Product aggregate.

NOTE

This Product might not look like what you’d expect a Product model to look like.
No price, no description, no dimensions. Our allocation service doesn’t care about
any of those things. This is the power of bounded contexts; the concept of a
product in one app can be very different from another. See the following sidebar
for more discussion.

AGGREGAT ES, BOUNDED CONT EXT S, AND M ICROSERVICES

One of the m os t im portant contributions  from  Evans  and the DDD com m unity is  the concept of
b ounded contexts.

In es s ence, this  was  a reaction agains t attem pts  to capture entire bus ines s es  into a s ingle
m odel. The word custom er m eans  different things  to people in s ales , cus tom er s ervice, logis tics ,
s upport, and s o on. Attributes  needed in one context are irrelevant in another; m ore pernicious ly,
concepts  with the s am e nam e can have entirely different m eanings  in different contexts . Rather
than trying to build a s ingle m odel (or clas s , or databas e) to capture all the us e cas es , it’s  better
to have s everal m odels , draw boundaries  around each context, and handle the trans lation
between different contexts  explicitly.

This  concept trans lates  very well to the world of m icros ervices , where each m icros ervice is  free
to have its  own concept of “cus tom er” and its  own rules  for trans lating that to and from  other
m icros ervices  it integrates  with.

In our exam ple, the allocation s ervice has  Product(sku, batches), whereas  the ecom m erce will
have Product(sku, description, price, image_url, dimensions, etc...). As  a rule of thum b,
your dom ain m odels  s hould include only the data that they need for perform ing calculations .

Whether or not you have a m icros ervices  architecture, a key cons ideration in choos ing your
aggregates  is  als o choos ing the bounded context that they will operate in. By res tricting the
context, you can keep your num ber of aggregates  low and their s ize m anageable.

Once again, we find ours elves  forced to s ay that we can’t give this  is s ue the treatm ent it des erves
here, and we can only encourage you to read up on it els ewhere. The Fowler link at the s tart of
this  s idebar is  a good s tarting point, and either (or indeed, any) DDD book will have a chapter or
m ore on bounded contexts .

One Aggregate = One Repository

Once you define certain entities to be aggregates, we need to apply the

rule that they are the only entities that are publicly accessible to the
outside world. In other words, the only repositories we are allowed
should be repositories that return aggregates.

NOTE

The rule that repositories should only return aggregates is the main place where
we enforce the convention that aggregates are the only way into our domain
model. Be wary of breaking it!

In our case, we’ll switch from BatchRepository to
ProductRepository:

Our new UoW and repository (unit_of_work.py and repository.py)

class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractProductRepository

...

class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product):
        ...

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        ...

The ORM layer will need some tweaks so that the right batches
automatically get loaded and associated with Product objects. The
nice thing is, the Repository pattern means we don’t have to worry
about that yet. We can just use our FakeRepository and then feed
through the new model into our service layer to see how it looks with
Product as its main entrypoint:

Service layer (src/allocation/service_layer/services.py)

def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()

def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit()
    return batchref

What About Performance?

We’ve mentioned a few times that we’re modeling with aggregates
because we want to have high-performance software, but here we are
loading all the batches when we only need one. You might expect that
to be inefficient, but there are a few reasons why we’re comfortable

here.

First, we’re purposefully modeling our data so that we can make a
single query to the database to read, and a single update to persist our

changes. This tends to perform much better than systems that issue lots
of ad hoc queries. In systems that don’t model this way, we often find
that transactions slowly get longer and more complex as the software

evolves.

Second, our data structures are minimal and comprise a few strings
and integers per row. We can easily load tens or even hundreds of

batches in a few milliseconds.

Third, we expect to have only 20 or so batches of each product at a
time. Once a batch is used up, we can discount it from our

calculations. This means that the amount of data we’re fetching
shouldn’t get out of control over time.

If we did expect to have thousands of active batches for a product,

we’d have a couple of options. For one, we could use lazy-loading for
the batches in a product. From the perspective of our code, nothing
would change, but in the background, SQLAlchemy would page
through data for us. This would lead to more requests, each fetching a

smaller number of rows. Because we need to find only a single batch
with enough capacity for our order, this might work pretty well.

EXERCISE FOR T HE READER

You’ve jus t s een the m ain top layers  of the code, s o this  s houldn’t be too hard, but we’d like you
to im plem ent the Product aggregate s tarting from  Batch, jus t as  we did.

Of cours e, you could cheat and copy/pas te from  the previous  lis tings , but even if you do that, you’ll
s till have to s olve a few challenges  on your own, like adding the m odel to the ORM and m aking
s ure all the m oving parts  can talk to each other, which we hope will be ins tructive.

You’ll find the code on GitHub. We’ve put in a “cheating” im plem entation in the delegates  to the
exis ting allocate() function, s o you s hould be able to evolve that toward the real thing.

We’ve m arked a couple of tes ts  with @pytest.skip(). After you’ve read the res t of this  chapter,
com e back to thes e tes ts  to have a go at im plem enting vers ion num bers . Bonus  points  if you can
get SQLAlchem y to do them  for you by m agic!

If all else failed, we’d just look for a different aggregate. Maybe we
could split up batches by region or by warehouse. Maybe we could

redesign our data access strategy around the shipment concept. The
Aggregate pattern is designed to help manage some technical
constraints around consistency and performance. There isn’t one
correct aggregate, and we should feel comfortable changing our minds

if we find our boundaries are causing performance woes.

Optimistic Concurrency with Version
Numbers

We have our new aggregate, so we’ve solved the conceptual problem

of choosing an object to be in charge of consistency boundaries. Let’s
now spend a little time talking about how to enforce data integrity at
the database level.

NOTE

This section has a lot of implementation details; for example, some of it is
Postgres-specific. But more generally, we’re showing one way of managing
concurrency issues, but it is just one approach. Real requirements in this area vary
a lot from project to project. You shouldn’t expect to be able to copy and paste
code from here into production.

We don’t want to hold a lock over the entire batches table, but how
will we implement holding a lock over just the rows for a particular
SKU?

One answer is to have a single attribute on the Product model that
acts as a marker for the whole state change being complete and to use

it as the single resource that concurrent workers can fight over. If two
transactions read the state of the world for batches at the same time,
and both want to update the allocations tables, we force both to also
try to update the version_number in the products table, in such a
way that only one of them can win and the world stays consistent.

Figure 7-4 illustrates two concurrent transactions doing their read
operations at the same time, so they see a Product with, for example,
version=3. They both call Product.allocate() in order to modify a
state. But we set up our database integrity rules such that only one of
them is allowed to commit the new Product with version=4, and the
other update is rejected.

TIP

Version numbers are just one way to implement optimistic locking. You could
achieve the same thing by setting the Postgres transaction isolation level to
SERIALIZABLE, but that often comes at a severe performance cost. Version
numbers also make implicit concepts explicit.

Figure 7-4. Sequence diagram: two transactions attempting a concurrent update on
Product

OPT IM IST IC CONCURRENCY CONT ROL AND RET RIES

What we’ve im plem ented here is  called optim istic concurrency control becaus e our default
as s um ption is  that everything will be fine when two us ers  want to m ake changes  to the
databas e. We think it’s  unlikely that they will conflict with each other, s o we let them  go ahead and
jus t m ake s ure we have a way to notice if there is  a problem .

Pessim istic concurrency control works  under the as s um ption that two us ers  are going to caus e
conflicts , and we want to prevent conflicts  in all cas es , s o we lock everything jus t to be s afe. In
our exam ple, that would m ean locking the whole batches table, or us ing SELECT FOR UPDATE—
we’re pretending that we’ve ruled thos e out for perform ance reas ons , but in real life you’d want to
do s om e evaluations  and m eas urem ents  of your own.

With pes s im is tic locking, you don’t need to think about handling failures  becaus e the databas e
will prevent them  for you (although you do need to think about deadlocks ). With optim is tic locking,
you need to explicitly handle the pos s ibility of failures  in the (hopefully unlikely) cas e of a clas h.

The us ual way to handle a failure is  to retry the failed operation from  the beginning. Im agine we
have two cus tom ers , Harry and Bob, and each s ubm its  an order for SHINY-TABLE. Both threads
load the product at vers ion 1 and allocate s tock. The databas e prevents  the concurrent update,
and Bob’s  order fails  with an error. When we retry the operation, Bob’s  order loads  the product at
vers ion 2 and tries  to allocate again. If there is  enough s tock left, all is  well; otherwis e, he’ll
receive OutOfStock. Mos t operations  can be retried this  way in the cas e of a concurrency problem .

Read m ore on retries  in “Recovering from  Errors  Synchronous ly” and “Footguns ”.

Implementation Options for Version Numbers

There are essentially three options for implementing version numbers:

1. version_number lives in the domain; we add it to the
Product constructor, and Product.allocate() is
responsible for incrementing it.

2. The service layer could do it! The version number isn’t

strictly a domain concern, so instead our service layer could
assume that the current version number is attached to Product
by the repository, and the service layer will increment it
before it does the commit().

3. Since it’s arguably an infrastructure concern, the UoW and

repository could do it by magic. The repository has access to
version numbers for any products it retrieves, and when the
UoW does a commit, it can increment the version number for
any products it knows about, assuming them to have changed.

Option 3 isn’t ideal, because there’s no real way of doing it without

having to assume that all products have changed, so we’ll be
incrementing version numbers when we don’t have to.

1

Option 2 involves mixing the responsibility for mutating state between

the service layer and the domain layer, so it’s a little messy as well.

So in the end, even though version numbers don’t have to be a domain
concern, you might decide the cleanest trade-off is to put them in the

domain:

Our chosen aggregate, Product (src/allocation/domain/model.py)

class Product:

    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):

        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            batch.allocate(line)
            self.version_number += 1
            return batch.reference

        except StopIteration:
            raise OutOfStock(f'Out of stock for sku {line.sku}')

There it is!

TIP

If you’re scratching your head at this version number business, it might help to
remember that the number isn’t important. What’s important is that the Product
database row is modified whenever we make a change to the Product aggregate.
The version number is a simple, human-comprehensible way to model a thing that
changes on every write, but it could equally be a random UUID every time.

Testing for Our Data Integrity Rules

Now to make sure we can get the behavior we want: if we have two
concurrent attempts to do allocation against the same Product, one of
them should fail, because they can’t both update the version number.

First, let’s simulate a “slow” transaction using a function that does
allocation and then does an explicit sleep:

2

time.sleep can reproduce concurrency behavior
(tests/integration/test_uow.py)

def try_to_allocate(orderid, sku, exceptions):
    line = model.OrderLine(orderid, sku, 10)
    try:
        with unit_of_work.SqlAlchemyUnitOfWork() as uow:
            product = uow.products.get(sku=sku)
            product.allocate(line)
            time.sleep(0.2)

            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)

Then we have our test invoke this slow allocation twice, concurrently,
using threads:

An integration test for concurrency behavior

(tests/integration/test_uow.py)

def
test_concurrent_updates_to_version_are_not_allowed(postgres_session_factory):
    sku, batch = random_sku(), random_batchref()
    session = postgres_session_factory()
    insert_batch(session, batch, sku, 100, eta=None, product_version=1)
    session.commit()

    order1, order2 = random_orderid(1), random_orderid(2)
    exceptions = []  # type: List[Exception]
    try_to_allocate_order1 = lambda: try_to_allocate(order1, sku, exceptions)
    try_to_allocate_order2 = lambda: try_to_allocate(order2, sku, exceptions)
    thread1 = threading.Thread(target=try_to_allocate_order1)
    thread2 = threading.Thread(target=try_to_allocate_order2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    [[version]] = session.execute(
        "SELECT version_number FROM products WHERE sku=:sku",
        dict(sku=sku),
    )
    assert version == 2
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in
str(exception)

    orders = list(session.execute(
        "SELECT orderid FROM allocations"
        " JOIN batches ON allocations.batch_id = batches.id"
        " JOIN order_lines ON allocations.orderline_id = order_lines.id"
        " WHERE order_lines.sku=:sku",
        dict(sku=sku),
    ))
    assert len(orders) == 1
    with unit_of_work.SqlAlchemyUnitOfWork() as uow:
        uow.session.execute('select 1')

We start two threads that will reliably produce the concurrency
behavior we want: read1, read2, write1, write2.

We assert that the version number has been incremented only once.

We can also check on the specific exception if we like.

And we double-check that only one allocation has gotten through.

Enforcing Concurrency Rules by Using Database
Transaction Isolation Levels

To get the test to pass as it is, we can set the transaction isolation level

on our session:

Set isolation level for session
(src/allocation/service_layer/unit_of_work.py)

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
    config.get_postgres_uri(),
    isolation_level="REPEATABLE READ",
))

TIP

Transaction isolation levels are tricky stuff, so it’s worth spending time
understanding the Postgres documentation.

3

Pessimistic Concurrency Control Example:
SELECT FOR UPDATE

There are multiple ways to approach this, but we’ll show one. SELECT
FOR UPDATE produces different behavior; two concurrent transactions
will not be allowed to do a read on the same rows at the same time:

SELECT FOR UPDATE is a way of picking a row or rows to use as a
lock (although those rows don’t have to be the ones you update). If two
transactions both try to SELECT FOR UPDATE a row at the same time,
one will win, and the other will wait until the lock is released. So this
is an example of pessimistic concurrency control.

Here’s how you can use the SQLAlchemy DSL to specify FOR UPDATE
at query time:

SQLAlchemy with_for_update
(src/allocation/adapters/repository.py)

    def get(self, sku):
        return self.session.query(model.Product) \
                           .filter_by(sku=sku) \
                           .with_for_update() \
                           .first()

This will have the effect of changing the concurrency pattern from

read1, read2, write1, write2(fail)

to

read1, write1, read2, write2(succeed)

Some people refer to this as the “read-modify-write” failure mode.
Read “PostgreSQL Anti-Patterns: Read-Modify-Write Cycles” for a
good overview.

We don’t really have time to discuss all the trade-offs between
REPEATABLE READ and SELECT FOR UPDATE, or optimistic versus
pessimistic locking in general. But if you have a test like the one
we’ve shown, you can specify the behavior you want and see how it
changes. You can also use the test as a basis for performing some
performance experiments.

Wrap-Up

Specific choices around concurrency control vary a lot based on

business circumstances and storage technology choices, but we’d like
to bring this chapter back to the conceptual idea of an aggregate: we
explicitly model an object as being the main entrypoint to some subset
of our model, and as being in charge of enforcing the invariants and
business rules that apply across all of those objects.

Choosing the right aggregate is key, and it’s a decision you may revisit
over time. You can read more about it in multiple DDD books. We also

recommend these three online papers on effective aggregate design by
Vaughn Vernon (the “red book” author).

Table 7-1 has some thoughts on the trade-offs of implementing the
Aggregate pattern.

Table 7-1. Aggregates: the trade-offs

Pros

Cons

Python might not have “official”
public and private methods, but
we do have
the underscores convention,
because it’s often useful to try
to indicate what’s for
“internal” use and what’s for
“outside code” to use. Choosing
aggregates is
just the next level up: it lets you
decide which of your domain
model classes
are the public ones, and which
aren’t.

Yet another new concept for
new developers to take on.
Explaining entities versus
value objects was already a
mental load; now there’s a third
type of domain
model object?

Sticking rigidly to the rule that
we modify only one aggregate
at a time is a
big mental shift.

Modeling our operations around
explicit consistency boundaries
helps us avoid
performance problems with our
ORM.

Dealing with eventual
consistency between
aggregates can be complex.

Putting the aggregate in sole
charge of state changes to its
subsidiary models
makes the system easier to
reason about, and makes it
easier to control invariants.

AGGREGAT ES AND CONSIST ENCY BOUNDARIES RECAP

Aggregates are your entrypoints into the domain model

By res tricting the num ber of ways  that things  can be changed, we m ake the s ys tem  eas ier to
reas on about.

Aggregates are in charge of a consistency boundary

An aggregate’s  job is  to be able to m anage our bus ines s  rules  about invariants  as  they apply
to a group of related objects . It’s  the aggregate’s  job to check that the objects  within its  rem it
are cons is tent with each other and with our rules , and to reject changes  that would break the
rules .

Aggregates and concurrency issues go together

When thinking about im plem enting thes e cons is tency checks , we end up thinking about
trans actions  and locks . Choos ing the right aggregate is  about perform ance as  well as
conceptual organization of your dom ain.

Part I Recap

Do you remember Figure 7-5, the diagram we showed at the beginning
of Part I to preview where we were heading?

Figure 7-5. A component diagram for our app at the end of Part I

So that’s where we are at the end of Part I. What have we achieved?
We’ve seen how to build a domain model that’s exercised by a set of
high-level unit tests. Our tests are living documentation: they describe
the behavior of our system—the rules upon which we agreed with our
business stakeholders—in nice readable code. When our business
requirements change, we have confidence that our tests will help us to
prove the new functionality, and when new developers join the project,
they can read our tests to understand how things work.

We’ve decoupled the infrastructural parts of our system, like the
database and API handlers, so that we can plug them into the outside of
our application. This helps us to keep our codebase well organized
and stops us from building a big ball of mud.

By applying the dependency inversion principle, and by using ports-
and-adapters-inspired patterns like Repository and Unit of Work,

we’ve made it possible to do TDD in both high gear and low gear and
to maintain a healthy test pyramid. We can test our system edge to
edge, and the need for integration and end-to-end tests is kept to a
minimum.

Lastly, we’ve talked about the idea of consistency boundaries. We
don’t want to lock our entire system whenever we make a change, so
we have to choose which parts are consistent with one another.

For a small system, this is everything you need to go and play with the
ideas of domain-driven design. You now have the tools to build

database-agnostic domain models that represent the shared language of
your business experts. Hurrah!

NOTE

At the risk of laboring the point—we’ve been at pains to point out that each
pattern comes at a cost. Each layer of indirection has a price in terms of
complexity and duplication in our code and will be confusing to programmers
who’ve never seen these patterns before. If your app is essentially a simple
CRUD wrapper around a database and isn’t likely to be anything more than that
in the foreseeable future, you don’t need these patterns. Go ahead and use
Django, and save yourself a lot of bother.

In Part II, we’ll zoom out and talk about a bigger topic: if aggregates
are our boundary, and we can update only one at a time, how do we
model processes that cross consistency boundaries?

1  Perhaps we could get some ORM/SQLAlchemy magic to tell us when an object is dirty,
but how would that work in the generic case—for example, for a CsvRepository?

2  time.sleep() works well in our use case, but it’s not the most reliable or efficient way
to reproduce concurrency bugs. Consider using semaphores or similar synchronization
primitives shared between your threads to get better guarantees of behavior.

3  If you’re not using Postgres, you’ll need to read different documentation. Annoyingly,
different databases all have quite different definitions. Oracle’s SERIALIZABLE is
equivalent to Postgres’s REPEATABLE READ, for example.
