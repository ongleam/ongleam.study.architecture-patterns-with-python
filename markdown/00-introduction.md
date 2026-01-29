Introduction

Why Do Our Designs Go Wrong?

What comes to mind when you hear the word chaos? Perhaps you think
of a noisy stock exchange, or your kitchen in the morning—everything
confused and jumbled. When you think of the word order, perhaps you

think of an empty room, serene and calm. For scientists, though, chaos

is characterized by homogeneity (sameness), and order by complexity
(difference).

For example, a well-tended garden is a highly ordered system.

Gardeners define boundaries with paths and fences, and they mark out
flower beds or vegetable patches. Over time, the garden evolves,

growing richer and thicker; but without deliberate effort, the garden
will run wild. Weeds and grasses will choke out other plants, covering

over the paths, until eventually every part looks the same again—wild
and unmanaged.

Software systems, too, tend toward chaos. When we first start building
a new system, we have grand ideas that our code will be clean and
well ordered, but over time we find that it gathers cruft and edge cases

and ends up a confusing morass of manager classes and util modules.
We find that our sensibly layered architecture has collapsed into itself
like an oversoggy trifle. Chaotic software systems are characterized by
a sameness of function: API handlers that have domain knowledge and
send email and perform logging; “business logic” classes that perform

no calculations but do perform I/O; and everything coupled to
everything else so that changing any part of the system becomes fraught
with danger. This is so common that software engineers have their own
term for chaos: the Big Ball of Mud anti-pattern (Figure P-1).

Figure P-1. A real-life dependency diagram (source: “Enterprise Dependency: Big Ball
of Yarn” by Alex Papadimoulis)

TIP

A big ball of mud is the natural state of software in the same way that wilderness
is the natural state of your garden. It takes energy and direction to prevent the
collapse.

Fortunately, the techniques to avoid creating a big ball of mud aren’t
complex.

Encapsulation and Abstractions

Encapsulation and abstraction are tools that we all instinctively reach
for as programmers, even if we don’t all use these exact words. Allow
us to dwell on them for a moment, since they are a recurring
background theme of the book.

The term encapsulation covers two closely related ideas: simplifying
behavior and hiding data. In this discussion, we’re using the first

sense. We encapsulate behavior by identifying a task that needs to be
done in our code and giving that task to a well-defined object or
function. We call that object or function an abstraction.

Take a look at the following two snippets of Python code:

Do a search with urllib

import json
from urllib.request import urlopen
from urllib.parse import urlencode

params = dict(q='Sausages', format='json')

handle = urlopen('http://api.duckduckgo.com' + '?' + urlencode(params))
raw_text = handle.read().decode('utf8')
parsed = json.loads(raw_text)

results = parsed['RelatedTopics']
for r in results:
    if 'Text' in r:
        print(r['FirstURL'] + ' - ' + r['Text'])

Do a search with requests

import requests

params = dict(q='Sausages', format='json')
parsed = requests.get('http://api.duckduckgo.com/', params=params).json()

results = parsed['RelatedTopics']
for r in results:
    if 'Text' in r:
        print(r['FirstURL'] + ' - ' + r['Text'])

Both code listings do the same thing: they submit form-encoded values
to a URL in order to use a search engine API. But the second is
simpler to read and understand because it operates at a higher level of

abstraction.

We can take this one step further still by identifying and naming the

task we want the code to perform for us and using an even higher-level
abstraction to make it explicit:

Do a search with the duckduckgo module

import duckduckgo
for r in duckduckgo.query('Sausages').results:
    print(r.url + ' - ' + r.text)

Encapsulating behavior by using abstractions is a powerful tool for
making code more expressive, more testable, and easier to maintain.

NOTE

In the literature of the object-oriented (OO) world, one of the classic
characterizations of this approach is called responsibility-driven design; it uses
the words roles and responsibilities rather than tasks. The main point is to think
about code in terms of behavior, rather than in terms of data or algorithms.

1

ABST RACT IONS AND ABCS

In a traditional OO language like Java or C#, you m ight us e an abs tract bas e clas s  (ABC) or an
interface to define an abs traction. In Python you can (and we s om etim es  do) us e ABCs , but you
can als o happily rely on duck typing.

The abs traction can jus t m ean “the public API of the thing you’re us ing”—a function nam e plus
s om e argum ents , for exam ple.

Most of the patterns in this book involve choosing an abstraction, so
you’ll see plenty of examples in each chapter. In addition, Chapter 3
specifically discusses some general heuristics for choosing
abstractions.

Layering

Encapsulation and abstraction help us by hiding details and protecting
the consistency of our data, but we also need to pay attention to the
interactions between our objects and functions. When one function,
module, or object uses another, we say that the one depends on the
other. These dependencies form a kind of network or graph.

In a big ball of mud, the dependencies are out of control (as you saw in
Figure P-1). Changing one node of the graph becomes difficult because
it has the potential to affect many other parts of the system. Layered
architectures are one way of tackling this problem. In a layered
architecture, we divide our code into discrete categories or roles, and
we introduce rules about which categories of code can call each other.

One of the most common examples is the three-layered architecture
shown in Figure P-2.

Figure P-2. Layered architecture

Layered architecture is perhaps the most common pattern for building
business software. In this model we have user-interface components,

which could be a web page, an API, or a command line; these user-

interface components communicate with a business logic layer that
contains our business rules and our workflows; and finally, we have a
database layer that’s responsible for storing and retrieving data.

For the rest of this book, we’re going to be systematically turning this
model inside out by obeying one simple principle.

The Dependency Inversion Principle

You might be familiar with the dependency inversion principle (DIP)

already, because it’s the D in SOLID.

2

Unfortunately, we can’t illustrate the DIP by using three tiny code
listings as we did for encapsulation. However, the whole of Part I is

essentially a worked example of implementing the DIP throughout an
application, so you’ll get your fill of concrete examples.

In the meantime, we can talk about DIP’s formal definition:

1. High-level modules should not depend on low-level modules.

Both should depend on abstractions.

2. Abstractions should not depend on details. Instead, details

should depend on abstractions.

But what does this mean? Let’s take it bit by bit.

High-level modules are the code that your organization really cares
about. Perhaps you work for a pharmaceutical company, and your high-

level modules deal with patients and trials. Perhaps you work for a

bank, and your high-level modules manage trades and exchanges. The

high-level modules of a software system are the functions, classes, and
packages that deal with our real-world concepts.

By contrast, low-level modules are the code that your organization

doesn’t care about. It’s unlikely that your HR department gets excited
about filesystems or network sockets. It’s not often that you discuss

SMTP, HTTP, or AMQP with your finance team. For our nontechnical
stakeholders, these low-level concepts aren’t interesting or relevant.

All they care about is whether the high-level concepts work correctly.
If payroll runs on time, your business is unlikely to care whether that’s

a cron job or a transient function running on Kubernetes.

Depends on doesn’t mean imports or calls, necessarily, but rather a
more general idea that one module knows about or needs another

module.

And we’ve mentioned abstractions already: they’re simplified
interfaces that encapsulate behavior, in the way that our duckduckgo

module encapsulated a search engine’s API.

All problems in computer science can be solved by adding another
level of indirection.

—David Wheeler

So the first part of the DIP says that our business code shouldn’t

depend on technical details; instead, both should use abstractions.

Why? Broadly, because we want to be able to change them
independently of each other. High-level modules should be easy to

change in response to business needs. Low-level modules (details) are
often, in practice, harder to change: think about refactoring to change a

function name versus defining, testing, and deploying a database
migration to change a column name. We don’t want business logic

changes to slow down because they are closely coupled to low-level
infrastructure details. But, similarly, it is important to be able to

change your infrastructure details when you need to (think about
sharding a database, for example), without needing to make changes to

your business layer. Adding an abstraction between them (the famous
extra layer of indirection) allows the two to change (more)

independently of each other.

The second part is even more mysterious. “Abstractions should not
depend on details” seems clear enough, but “Details should depend on

abstractions” is hard to imagine. How can we have an abstraction that
doesn’t depend on the details it’s abstracting? By the time we get to

Chapter 4, we’ll have a concrete example that should make this all a

bit clearer.

A Place for All Our Business Logic: The
Domain Model

But before we can turn our three-layered architecture inside out, we
need to talk more about that middle layer: the high-level modules or

business logic. One of the most common reasons that our designs go

wrong is that business logic becomes spread throughout the layers of
our application, making it hard to identify, understand, and change.

Chapter 1 shows how to build a business layer with a Domain Model

pattern. The rest of the patterns in Part I show how we can keep the
domain model easy to change and free of low-level concerns by

choosing the right abstractions and continuously applying the DIP.

1  If you’ve come across class-responsibility-collaborator (CRC) cards, they’re driving at
the same thing: thinking about responsibilities helps you decide how to split things up.

2  SOLID is an acronym for Robert C. Martin’s five principles of object-oriented design:
single responsibility, open for extension but closed for modification, Liskov substitution,
interface segregation, and dependency inversion. See “S.O.L.I.D: The First 5 Principles
of Object-Oriented Design” by Samuel Oloruntoba.
