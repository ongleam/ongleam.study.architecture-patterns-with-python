# Chapter 3. A Brief Interlude: On Coupling and Abstractions

Chapter 3. A Brief Interlude:
On Coupling and
Abstractions

Allow us a brief digression on the subject of abstractions, dear reader.
We’ve talked about abstractions quite a lot. The Repository pattern is
an abstraction over permanent storage, for example. But what makes a

good abstraction? What do we want from abstractions? And how do
they relate to testing?

The code for this chapter is in the chapter_03_abstractions branch on GitHub:

TIP

git clone https://github.com/cosmicpython/code.git
git checkout chapter_03_abstractions

A key theme in this book, hidden among the fancy patterns, is that we
can use simple abstractions to hide messy details. When we’re writing

1

code for fun, or in a kata,  we get to play with ideas freely, hammering
things out and refactoring aggressively. In a large-scale system, though,
we become constrained by the decisions made elsewhere in the
system.

When we’re unable to change component A for fear of breaking
component B, we say that the components have become coupled.
Locally, coupling is a good thing: it’s a sign that our code is working
together, each component supporting the others, all of them fitting in

place like the gears of a watch. In jargon, we say this works when
there is high cohesion between the coupled elements.

Globally, coupling is a nuisance: it increases the risk and the cost of
changing our code, sometimes to the point where we feel unable to
make any changes at all. This is the problem with the Ball of Mud
pattern: as the application grows, if we’re unable to prevent coupling

between elements that have no cohesion, that coupling increases
superlinearly until we are no longer able to effectively change our
systems.

We can reduce the degree of coupling within a system (Figure 3-1) by
abstracting away the details (Figure 3-2).

Figure 3-1. Lots of coupling

Figure 3-2. Less coupling

In both diagrams, we have a pair of subsystems, with one dependent on
the other. In Figure 3-1, there is a high degree of coupling between the

two; the number of arrows indicates lots of kinds of dependencies
between the two. If we need to change system B, there’s a good chance
that the change will ripple through to system A.

In Figure 3-2, though, we have reduced the degree of coupling by
inserting a new, simpler abstraction. Because it is simpler, system A
has fewer kinds of dependencies on the abstraction. The abstraction

serves to protect us from change by hiding away the complex details of
whatever system B does—we can change the arrows on the right
without changing the ones on the left.

Abstracting State Aids Testability

Let’s see an example. Imagine we want to write code for synchronizing
two file directories, which we’ll call the source and the destination:

If a file exists in the source but not in the destination, copy the
file over.

If a file exists in the source, but it has a different name than in
the destination, rename the destination file to match.

If a file exists in the destination but not in the source, remove
it.

Our first and third requirements are simple enough: we can just
compare two lists of paths. Our second is trickier, though. To detect

renames, we’ll have to inspect the content of files. For this, we can use
a hashing function like MD5 or SHA-1. The code to generate a SHA-1
hash from a file is simple enough:

Hashing a file (sync.py)

BLOCKSIZE = 65536

def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()

Now we need to write the bit that makes decisions about what to do—
the business logic, if you will.

When we have to tackle a problem from first principles, we usually try
to write a simple implementation and then refactor toward better
design. We’ll use this approach throughout the book, because it’s how
we write code in the real world: start with a solution to the smallest
part of the problem, and then iteratively make the solution richer and
better designed.

Our first hackish approach looks something like this:

Basic sync algorithm (sync.py)

import hashlib
import os
import shutil
from pathlib import Path

def sync(source, dest):
    # Walk the source folder and build a dict of filenames and their hashes
    source_hashes = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder) / fn)] = fn

    seen = set()  # Keep track of the files we've found in the target

    # Walk the target folder and get the filenames and hashes
    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path = Path(folder) / fn
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            # if there's a file in target that's not in source, delete it
            if dest_hash not in source_hashes:
                dest_path.remove()

            # if there's a file in target that has a different path in source,
            # move it to the correct path
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])

    # for every file that appears in source but not target, copy the file to
    # the target
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source) / fn, Path(dest) / fn)

Fantastic! We have some code and it looks OK, but before we run it on
our hard drive, maybe we should test it. How do we go about testing
this sort of thing?

Some end-to-end tests (test_sync.py)

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a very useful file"
        (Path(source) / 'my-file').write_text(content)

        sync(source, dest)

        expected_path = Path(dest) /  'my-file'
        assert expected_path.exists()
        assert expected_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

def test_when_a_file_has_been_renamed_in_the_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a file that was renamed"
        source_path = Path(source) / 'source-filename'
        old_dest_path = Path(dest) / 'dest-filename'
        expected_dest_path = Path(dest) / 'source-filename'
        source_path.write_text(content)
        old_dest_path.write_text(content)

        sync(source, dest)

        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

Wowsers, that’s a lot of setup for two simple cases! The problem is
that our domain logic, “figure out the difference between two
directories,” is tightly coupled to the I/O code. We can’t run our
difference algorithm without calling the pathlib, shutil, and
hashlib modules.

And the trouble is, even with our current requirements, we haven’t

written enough tests: the current implementation has several bugs (the
shutil.move() is wrong, for example). Getting decent coverage and
revealing these bugs means writing more tests, but if they’re all as
unwieldy as the preceding ones, that’s going to get real painful real
quickly.

On top of that, our code isn’t very extensible. Imagine trying to
implement a --dry-run flag that gets our code to just print out what
it’s going to do, rather than actually do it. Or what if we wanted to

sync to a remote server, or to cloud storage?

Our high-level code is coupled to low-level details, and it’s making
life hard. As the scenarios we consider get more complex, our tests

will get more unwieldy. We can definitely refactor these tests (some of
the cleanup could go into pytest fixtures, for example) but as long as

we’re doing filesystem operations, they’re going to stay slow and be
hard to read and write.

Choosing the Right Abstraction(s)

What could we do to rewrite our code to make it more testable?

First, we need to think about what our code needs from the filesystem.
Reading through the code, we can see that three distinct things are

happening. We can think of these as three distinct responsibilities that
the code has:

1. We interrogate the filesystem by using os.walk and determine
hashes for a series of paths. This is similar in both the source
and the destination cases.

2. We decide whether a file is new, renamed, or redundant.

3. We copy, move, or delete files to match the source.

Remember that we want to find simplifying abstractions for each of
these responsibilities. That will let us hide the messy details so we can

focus on the interesting logic.

2

NOTE

In this chapter, we’re refactoring some gnarly code into a more testable structure
by identifying the separate tasks that need to be done and giving each task to a
clearly defined actor, along similar lines to the duckduckgo example.

For steps 1 and 2, we’ve already intuitively started using an
abstraction, a dictionary of hashes to paths. You may already have

been thinking, “Why not build up a dictionary for the destination folder
as well as the source, and then we just compare two dicts?” That

seems like a nice way to abstract the current state of the filesystem:

source_files = {'hash1': 'path1', 'hash2': 'path2'}
dest_files = {'hash1': 'path1', 'hash2': 'pathX'}

What about moving from step 2 to step 3? How can we abstract out the
actual move/copy/delete filesystem interaction?

We’ll apply a trick here that we’ll employ on a grand scale later in the

book. We’re going to separate what we want to do from how to do it.

We’re going to make our program output a list of commands that look
like this:

("COPY", "sourcepath", "destpath"),
("MOVE", "old", "new"),

Now we could write tests that just use two filesystem dicts as inputs,

and we would expect lists of tuples of strings representing actions as
outputs.

Instead of saying, “Given this actual filesystem, when I run my

function, check what actions have happened,” we say, “Given this
abstraction of a filesystem, what abstraction of filesystem actions

will happen?”

Simplified inputs and outputs in our tests (test_sync.py)

    def test_when_a_file_exists_in_the_source_but_not_the_destination():
        src_hashes = {'hash1': 'fn1'}
        dst_hashes = {}
        expected_actions = [('COPY', '/src/fn1', '/dst/fn1')]
        ...

    def test_when_a_file_has_been_renamed_in_the_source():
        src_hashes = {'hash1': 'fn1'}
        dst_hashes = {'hash1': 'fn2'}
        expected_actions == [('MOVE', '/dst/fn2', '/dst/fn1')]
        ...

Implementing Our Chosen Abstractions

That’s all very well, but how do we actually write those new tests,
and how do we change our implementation to make it all work?

Our goal is to isolate the clever part of our system, and to be able to

test it thoroughly without needing to set up a real filesystem. We’ll
create a “core” of code that has no dependencies on external state and

then see how it responds when we give it input from the outside world
(this kind of approach was characterized by Gary Bernhardt as

Functional Core, Imperative Shell, or FCIS).

Let’s start off by splitting the code to separate the stateful parts from
the logic.

And our top-level function will contain almost no logic at all; it’s just

an imperative series of steps: gather inputs, call our logic, apply
outputs:

Split our code into three (sync.py)

def sync(source, dest):
    # imperative shell step 1, gather inputs
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    # imperative shell step 3, apply outputs
    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        if action == 'move':
            shutil.move(*paths)
        if action == 'delete':
            os.remove(paths[0])

Here’s the first function we factor out,
read_paths_and_hashes(), which isolates the I/O part of our
application.

Here is where carve out the functional core, the business logic.

The code to build up the dictionary of paths and hashes is now trivially
easy to write:

A function that just does I/O (sync.py)

def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes

The determine_actions() function will be the core of our business
logic, which says, “Given these two sets of hashes and filenames, what

should we copy/move/delete?”. It takes simple data structures and
returns simple data structures:

A function that just does business logic (sync.py)

def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield 'copy', sourcepath, destpath

        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes[sha]
            newdestpath = Path(dst_folder) / filename
            yield 'move', olddestpath, newdestpath

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield 'delete', dst_folder / filename

Our tests now act directly on the determine_actions() function:

Nicer-looking tests (test_sync.py)

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {}
    actions = determine_actions(src_hashes, dst_hashes, Path('/src'),
Path('/dst'))
    assert list(actions) == [('copy', Path('/src/fn1'), Path('/dst/fn1'))]
...

def test_when_a_file_has_been_renamed_in_the_source():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {'hash1': 'fn2'}
    actions = determine_actions(src_hashes, dst_hashes, Path('/src'),
Path('/dst'))
    assert list(actions) == [('move', Path('/dst/fn2'), Path('/dst/fn1'))]

Because we’ve disentangled the logic of our program—the code for

identifying changes—from the low-level details of I/O, we can easily
test the core of our code.

With this approach, we’ve switched from testing our main entrypoint
function, sync(), to testing a lower-level function,
determine_actions(). You might decide that’s fine because sync()
is now so simple. Or you might decide to keep some
integration/acceptance tests to test that sync(). But there’s another
option, which is to modify the sync() function so it can be unit tested

and end-to-end tested; it’s an approach Bob calls edge-to-edge

testing.

Testing Edge to Edge with Fakes and Dependency
Injection

When we start writing a new system, we often focus on the core logic

first, driving it with direct unit tests. At some point, though, we want to
test bigger chunks of the system together.

We could return to our end-to-end tests, but those are still as tricky to

write and maintain as before. Instead, we often write tests that invoke
a whole system together but fake the I/O, sort of edge to edge:

Explicit dependencies (sync.py)

def sync(reader, filesystem, source_root, dest_root):

    source_hashes = reader(source_root)
    dest_hashes = reader(dest_root)

    for sha, filename in src_hashes.items():
        if sha not in dest_hashes:
            sourcepath = source_root / filename
            destpath = dest_root / filename
            filesystem.copy(destpath, sourcepath)

        elif dest_hashes[sha] != filename:
            olddestpath = dest_root / dest_hashes[sha]
            newdestpath = dest_root / filename
            filesystem.move(olddestpath, newdestpath)

    for sha, filename in dst_hashes.items():
        if sha not in source_hashes:
            filesystem.delete(dest_root/filename)

Our top-level function now exposes two new dependencies, a
reader and a filesystem.

We invoke the reader to produce our files dict.

We invoke the filesystem to apply the changes we detect.

TIP

Although we’re using dependency injection, there is no need to define an abstract
base class or any kind of explicit interface. In this book, we often show ABCs
because we hope they help you understand what the abstraction is, but they’re not
necessary. Python’s dynamic nature means we can always rely on duck typing.

Tests using DI

class FakeFileSystem(list):

    def copy(self, src, dest):
        self.append(('COPY', src, dest))

    def move(self, src, dest):
        self.append(('MOVE', src, dest))

    def delete(self, dest):
        self.append(('DELETE', src, dest))

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source = {"sha1": "my-file" }
    dest = {}
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronise_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("COPY", "/source/my-file", "/dest/my-file")]

def test_when_a_file_has_been_renamed_in_the_source():
    source = {"sha1": "renamed-file" }
    dest = {"sha1": "original-file" }
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronise_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("MOVE", "/dest/original-file", "/dest/renamed-file")]

Bob loves using lists to build simple test doubles, even though his
coworkers get mad. It means we can write tests like assert foo
not in database.

Each method in our FakeFileSystem just appends something to
the list so we can inspect it later. This is an example of a spy
object.

The advantage of this approach is that our tests act on the exact same
function that’s used by our production code. The disadvantage is that

we have to make our stateful components explicit and pass them
around. David Heinemeier Hansson, the creator of Ruby on Rails,
famously described this as “test-induced design damage.”

In either case, we can now work on fixing all the bugs in our
implementation; enumerating tests for all the edge cases is now much
easier.

Why Not Just Patch It Out?

At this point you may be scratching your head and thinking, “Why don’t
you just use mock.patch and save yourself the effort?"”

We avoid using mocks in this book and in our production code too.
We’re not going to enter into a Holy War, but our instinct is that
mocking frameworks, particularly monkeypatching, are a code smell.

Instead, we like to clearly identify the responsibilities in our
codebase, and to separate those responsibilities into small, focused
objects that are easy to replace with a test double.

NOTE

You can see an example in Chapter 8, where we mock.patch() out an email-
sending module, but eventually we replace that with an explicit bit of dependency
injection in Chapter 13.

We have three closely related reasons for our preference:

Patching out the dependency you’re using makes it possible to
unit test the code, but it does nothing to improve the design.
Using mock.patch won’t let your code work with a --dry-
run flag, nor will it help you run against an FTP server. For
that, you’ll need to introduce abstractions.

Tests that use mocks tend to be more coupled to the
implementation details of the codebase. That’s because mock
tests verify the interactions between things: did we call
shutil.copy with the right arguments? This coupling
between code and test tends to make tests more brittle, in our
experience.

Overuse of mocks leads to complicated test suites that fail to
explain the code.

NOTE

Designing for testability really means designing for extensibility. We trade off a
little more complexity for a cleaner design that admits novel use cases.

M OCKS VERSUS FAKES; CLASSIC-ST YLE VERSUS LONDON-
SCHOOL T DD

Here’s  a s hort and s om ewhat s im plis tic definition of the difference between m ocks  and fakes :

Mocks  are us ed to verify how s om ething gets  us ed; they have m ethods  like
assert_called_once_with(). They’re as s ociated with London-s chool TDD.

Fakes  are working im plem entations  of the thing they’re replacing, but they’re des igned
for us e only in tes ts . They wouldn’t work “in real life”; our in-m em ory repos itory is  a
good exam ple. But you can us e them  to m ake as s ertions  about the end s tate of a
s ys tem  rather than the behaviors  along the way, s o they’re as s ociated with clas s ic-s tyle
TDD.

We’re s lightly conflating m ocks  with s pies  and fakes  with s tubs  here, and you can read the long,
correct ans wer in Martin Fowler’s  clas s ic es s ay on the s ubject called “Mocks  Aren’t Stubs ”.

It als o probably does n’t help that the MagicMock objects  provided by unittest.mock aren’t, s trictly
s peaking, m ocks ; they’re s pies , if anything. But they’re als o often us ed as  s tubs  or dum m ies .
There, we prom is e we’re done with the tes t double term inology nitpicks  now.

What about London-s chool vers us  clas s ic-s tyle TDD? You can read m ore about thos e two in
Martin Fowler’s  article that we jus t cited, as  well as  on the Software Engineering Stack Exchange
s ite, but in this  book we’re pretty firm ly in the clas s icis t cam p. We like to build our tes ts  around
s tate both in s etup and in as s ertions , and we like to work at the highes t level of abs traction
3
pos s ible rather than doing checks  on the behavior of interm ediary collaborators .

Read m ore on this  in “On Deciding What Kind of Tes ts  to Write”.

We view TDD as a design practice first and a testing practice second.
The tests act as a record of our design choices and serve to explain the

system to us when we return to the code after a long absence.

Tests that use too many mocks get overwhelmed with setup code that
hides the story we care about.

Steve Freeman has a great example of overmocked tests in his talk

“Test-Driven Development”. You should also check out this PyCon
talk, “Mocking and Patching Pitfalls”, by our esteemed tech reviewer,
Ed Jung, which also addresses mocking and its alternatives. And while
we’re recommending talks, don’t miss Brandon Rhodes talking about

“Hoisting Your I/O”, which really nicely covers the issues we’re
talking about, using another simple example.

TIP

In this chapter, we’ve spent a lot of time replacing end-to-end tests with unit tests.
That doesn’t mean we think you should never use E2E tests! In this book we’re
showing techniques to get you to a decent test pyramid with as many unit tests as
possible, and with the minimum number of E2E tests you need to feel confident.
Read on to “Recap: Rules of Thumb for Different Types of Test” for more
details.

SO WHICH DO WE USE IN T HIS BOOK? FUNCT IONAL OR
OBJECT-ORIENT ED COM POSIT ION?

Both. Our dom ain m odel is  entirely free of dependencies  and s ide effects , s o that’s  our functional
core. The s ervice layer that we build around it (in Chapter 4) allows  us  to drive the s ys tem  edge to
edge, and we us e dependency injection to provide thos e s ervices  with s tateful com ponents , s o
we can s till unit tes t them .

See Chapter 13 for m ore exploration of m aking our dependency injection m ore explicit and
centralized.

Wrap-Up

We’ll see this idea come up again and again in the book: we can make
our systems easier to test and maintain by simplifying the interface

between our business logic and messy I/O. Finding the right

abstraction is tricky, but here are a few heuristics and questions to ask
yourself:

Can I choose a familiar Python data structure to represent the
state of the messy system and then try to imagine a single
function that can return that state?

Where can I draw a line between my systems, where can I
carve out a seam to stick that abstraction in?

What is a sensible way of dividing things into components
with different responsibilities? What implicit concepts can I
make explicit?

What are the dependencies, and what is the core business
logic?

Practice makes less imperfect! And now back to our regular
programming…

1  A code kata is a small, contained programming challenge often used to practice TDD.

See “Kata—The Only Way to Learn TDD” by Peter Provost.

2  If you’re used to thinking in terms of interfaces, that’s what we’re trying to define here.

3  Which is not to say that we think the London school people are wrong. Some insanely

smart people work that way. It’s just not what we’re used to.
