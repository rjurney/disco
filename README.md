# disco - Deep dIScovery COmpany parser

Unce upon a time, in a land far, far away, there was a package called [`cleanco`](https://github.com/psolin/cleanco). The package was quite useful when it came to company names parsing/cleaning (especially for initial experiments and straightforward name matching). However, it seemed that `cleanco` bit the Evil Queen's poisoned apple which caused that `cleanco` was not able to properly parse names in many non-western languages (Polish, Czech, and essentially all names in cyrillic, greek alphabet, chinese, etc). That's why the charming princes of Deep Discovery decided to take `cleanco` and enhance it, so that they can live happily ever after and parse whatever they need. And that's, dear kids, how `disco` was born.

![image](https://user-images.githubusercontent.com/8523511/127518999-6bec4568-4dff-421f-90a9-7cd3bdd4aa02.png)

#### Why disco?

Parsing companies through heuristics and keyword matching is like disco dancing. It was cool 30 years ago but when nobody is watching everybody does it. And also it comes from `deep DIScovery COmpany parsing` or `Deep dIScovery COmpany parsing`.

### Goal

As of now, `disco` is a heavily enhanced `cleanco` that we want to keep in private (for now). There is a lot of suboptimal parts but we can fix that once it starts being an issue.

---
### Original documentation follows
# cleanco - clean organization names

![Python package](https://github.com/psolin/cleanco/workflows/Python%20package/badge.svg)
![CodeQL](https://github.com/psolin/cleanco/workflows/CodeQL/badge.svg)

## What is it / what does it do?

This is a Python package that processes company names, providing cleaned versions of the
names by stripping away terms indicating organization type (such as "Ltd." or "Corp").

Using a database of organization type terms, It also provides an utility to deduce the
type of organization, in terms of US/UK business entity types (ie. "limited liability
company" or "non-profit").

Finally, the system uses the term information to suggest countries the organization could
be established in. For example, the term "Oy" in company name suggests it is established
in Finland, whereas "Ltd" in company name could mean UK, US or a number of other
countries.

## How do I install it?

Just use 'pip install cleanco' if you have pip installed (as most systems do). Or download the zip distribution from this site, unzip it and then:

- Mac: `cd` into it, and enter `sudo python setup.py install` along with your system password.
- Windows: Same thing but without `sudo`.

## How does it work?

Let's look at some sample code. To get the base name of a business without legal suffix:

    >>> from cleanco import prepare_terms, basename
    >>> business_name = "Some Big Pharma, LLC"
    >>> terms = prepare_terms()
    >>> basename(business_name, terms, prefix=False, middle=False, suffix=True)
    >>> 'Some Big Pharma'

Note that sometimes a name may have e.g. two different suffixes after one another. The cleanco
term data covers many of these but you may want to run `basename()` twice, just in case.

To get the business type or country:

    >>> from cleanco import typesources, matches
    >>> classification_sources = typesources()
    >>> matches("Some Big Pharma, LLC", classification_sources)
    ['Limited Liability Company']

To get the possible countries of jurisdiction:

    >>> from cleanco import countrysources, matches
    >>> classification_sources = countrysources()
    >>> matches("Some Big Pharma, LLC", classification_sources) ´
    ['United States of America', 'Philippines']

The legacy (versions < 2.0) way can still be used, too, but will eventually be discontinued:

Import the utility class:

    >>> from cleanco import cleanco

Prepare a string of a company name that you want to process:

    >>> business_name = "Some Big Pharma, LLC"

Throw it into the instance:

    >>> x = cleanco(business_name)

You can now get the company types:

    >>> x.type()
    ['Limited Liability Company']

...the possible countries...

    >>> x.country()
    ['United States of America', 'Philippines']

...and a clean version of the company name.

    >>> x.clean_name()
    'Some Big Pharma'

## Are there bugs?

See the issue tracker. If you find a bug or have enhancement suggestion or question, please file an issue and provide a PR if you can. For example, some of the company suffixes may be incorrect or there may be suffixes missing.

To run tests, simply install the package and run `python setup.py test`. To run tests on multiple Python versions, install `tox` and run it (see the provided tox.ini).

## Special thanks to:

- Wikipedia's [Types of Business Entity article](http://en.wikipedia.org/wiki/Types_of_business_entity), where I spent hours of research.
- Contributors: [Petri Savolainen](https://github.com/petri)
