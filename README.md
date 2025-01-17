# disco - Deep dIScovery COmpany parser

Unce upon a time, in a land far, far away, there was a package called [`cleanco`](https://github.com/psolin/cleanco). The package was quite useful when it came to company names parsing/cleaning (especially for initial experiments and straightforward name matching). However, it seemed that `cleanco` bit the Evil Queen's poisoned apple which caused that `cleanco` was not able to properly parse names in many non-western languages (Polish, Czech, and essentially all names in cyrillic, greek alphabet, chinese, etc). That's why the charming princes of Deep Discovery decided to take `cleanco` and enhance it, so that they can live happily ever after and parse whatever they need. And that's, dear kids, how `disco` was born.

![image](https://user-images.githubusercontent.com/8523511/127518999-6bec4568-4dff-421f-90a9-7cd3bdd4aa02.png)

#### Why disco?

Parsing companies through heuristics and keyword matching is like disco dancing. It was cool 30 years ago but when nobody is watching everybody does it. And also it comes from `deep DIScovery COmpany parsing` or `Deep dIScovery COmpany parsing`. And it was already damn confusing to distinguish the custom and original package, so it needed the rename.

### Goal

As of now, `disco` is a heavily enhanced `cleanco` that we want to keep in private (for now). There is a lot of suboptimal parts but we can fix that once it starts being an issue.

## Usage
A few examples of the most frequent use cases.

**Basic use**
```python
from disco.legaltype import search
company_name = "Some Big Pharma, LLC"
search(company_name)

>>> {'countries': ['Philippines', 'United States of America'], 'types': ['Limited Liability Company'], 'basename': 'Some Big Pharma'}
```

*Note: This is most likely what you want to use in big data processing when you want all parts of the result. `basename`, `country`, `legaltype` methods are more or less just wrapper methods so it will not be more efficient.*

-----
 **Remove legal type hints (suffix or prefix) and get only base name:**

Either use the previous example and get `countries` or run the following:

```python
from disco.legaltype import basename
company_name = "Some Big Pharma, LLC"
basename(company_name)

>>> 'Some Big Pharma'
```

-----

**Detection of legal types using only either prefixes or suffixes**
Normally, `disco` searches for legal forms from both directions (using both prefixes and suffixes). You can change this through arguments:

```python
from disco.legaltype import basename
company_name = "Some Big Pharma, LLC"
basename(company_name, prefix=True, suffix=False)

>>> 'Some Big Pharma, LLC' # LLC was ignored because of `suffix=False`
```

-----

**Detection of legal entity type only**

Use the first basic example and get `types` or run the following:

```python
from disco.legaltype import legaltype
company_name = "Some Big Pharma, LLC"
legaltype(company_name)

>>> ['Limited Liability Company']
```

-----

**Detection of jurisdiction based on legal entity**

Use the first basic example and get `countries` or run the following:

```python
from disco.legaltype import country
company_name = "Some Big Pharma, LLC"
country(company_name)

>>> ['Philippines', 'United States of America']
```

### Quality

As of July 29, `disco` is able to identify 37.62 % more company patterns in a list of 50k randomly sampled company names (sampled from Sayari) when compared to `cleanco`. Specifically, `disco` identifies 20375 patterns while `cleanco` identifies 14805.

Sample of companies which can be identified by `disco` and not by `cleanco`. Chinese support has obviously a big influence.

```
 '上海聪优贸易有限公司',
 'NEWCOS, společnost s ručením omezeným',
 'MONNARI TRADE STYLE SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
 '烟台实覃商贸有限公司',
 '广州曜业科技有限公司',
 '三门峡众亿实业有限公司',
 'COVACI OANA ÎNTREPRINDERE INDIVIDUALĂ',
 '青岛金元素装饰设计工程有限公司',
 '山东安驰钢铁贸易有限公司',
 '深圳市勇搏会体育文化推广有限公司',
 '乐山市黄光喜商贸有限公司',
 '重庆笛远投资有限公司',
 '南通基石信息技术有限公司',
 '霍尔果斯三淑文化传媒有限公司',
```

_Note: I will add performance results also for Open Corporates soon._

### Space for improvement

There is still space for improvement for Cyrillic names and `disco` should be improved based on analysis of Sayari data. The previous enhancement iteration was based on Open Corporates data.

---

## Links:

- Wikipedia: [Types of Business Entity article](http://en.wikipedia.org/wiki/Types_of_business_entity)

# Original documentation follows

**Note: You need to change cleanco to disco everywhere in the following examples.**

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
