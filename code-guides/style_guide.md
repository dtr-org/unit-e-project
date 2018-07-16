# C++ Style Guide
The purpose of this document is to have a common reference to the accepted and common code practices,in order to maintain quality, readability and consistency with the existing codebase.  
The document is still a work in progress, missing also the integrations from the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).

##### Table of Contents
[If statements](#if_statements)  
[UNIT-E tag](#UNIT-E_tag)  
[Constructors](#Constructors)  
[Includes](#Includes)    

<a name="if_statements">
## If statemets
Please always use braces around if statements, even for one liners since the case where a `;` is inserted after the
rightmost parenthesis is basically undetectable and really hard to debug.

*DO:*
```cpp
if(condition) {
  return value;
}
```
*DON'T:*
```cpp
if(condition)
  return value;
```
<a name="UNIT-E_tag">
## UNIT-E tag
In case of comments and TODOs that are pertinent only to the UNIT-E code please create a code comment like:
```cpp
//UNIT-E: very specific comment about unit-e
```
<a name="Constructors">
## Constructors
Constructors should be declared in the `*.h` file but defined in the `*.cpp` file. Also always use the *member initializer list* when possible.

*foo.h*
```cpp
class Foo
{
public:
  foo();
  foo(int fooVal_, bool isFool_);

  int fooVal;
  bool isFool;
}
```
*foo.cpp*
```cpp
Foo::foo() : fooVal(0), isFool(false) {};

Foo::foo(int fooVal_, bool isFool_) :
  fooVal(fooVal_),
  isFool(isFool_) {};
```
<a name="Includes">
## Includes
Make sure always to use <> notation instead of the "". There is not of a big difference but this is done mostly for consistency with the current codebase.

```cpp
// DO
#include <chain.h>

// DON'T
#include "chain.h"
```
