# Unit-e naming conventions

There are certain naming conventions we follow across the project. This document
describes the conventions we follow for the overall project and the currency.
Naming conventions for code are laid out in the developer notes of the
individual repositories, e.g. the [unit-e developer
notes](https://github.com/dtr-org/unit-e/blob/master/doc/developer-notes.md).

## Project name

`Unit-e` (with upper-case `U`, a dash, and lower-case `e`) is the overall project
name and the name of the currency.

It's used when referring to the overall community, network, and other things not
tied to a specific client implementation, e.g. "the crytpocurrency Unit-e", "the
Unit-e protocol", "a Unit-e transaction", "the Unit-e developers".

A reference for its use is the [DTR web site](https://dtr.org/unit-e/).

## Client name

`unit-e` (with lower-case `u`) is the first Unit-e client implementation in C++
based on upstream bitcoin. It lives in the
[`dtr-org/unit-e`](https://github.com/dtr-org/unit-e) repository on GitHub. The
client is also known by its internal name `Feuerland`.

This is used when referring to the specific implementation, its code, or its
repository, e.g. "the unit-e git repository", "starting the unit-e client",
"unit-e is licensed under MIT".

A reference for its use is the [unit-e
README](https://github.com/dtr-org/unit-e/blob/master/README.md).

## Currency denominations

`UTE` is the abbreviation for the whole concrete unit of the currency and the
symbol of the currency. For units of the currency it can also be spelled out as
`unit of Unit-e`. Examples are "send me one unit", "the pizza costs 2 UTEs".

Smaller denominations are expressed through [metric unit
prefixes](https://en.wikipedia.org/wiki/Metric_prefix). Some special fractions
have specific names. The smallest unit is named `satoshi` to pay homage to the
inventor of Bitcoin. It's the Unit-e satoshi.

See the following table for details:

Denomination       | Unit (Abbreviation)
-------------------|--------------------
1.0                | unit (UTE)
0.01 (10^-2)       | ee (cUTE)
0.001 (10^-3)      | milliunit (mUTE)
0.000001 (10^-6)   | microunit (µUTE)
0.00000001 (10^-8) | satoshi

## Spelling alternatives

In some circumstances, for example in code or URLs, it's not possible to use the
names as they are, but they need to be capitalized differently or the dash needs
to be removed to adhere to stronger local convention or to make it a valid
identifier. In these cases we follow the strategy to keep the spirit of the
original name with the visibly separated `e` as much as it makes sense. This
means in detail:

* When different capitalization is required, e.g. all upper-case, keep the dash
  if possible, e.g `UNIT-E`.
* If the dash is not allowed or practical, convert it to an underscore, e.g.
  `unit_e` or `UNIT_E`.
* If no separating character at all is suitable, use camel-case to get
  separation, e.g. `UnitE`.
