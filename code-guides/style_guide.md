# C++ Style Guide
The purpose of this document is to add amendments or enhance the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html). Therefore please refer to that for anything that is not explicitly covered in this document.

##### Table of Contents
[If statements](#if-statements)  
[UNIT-E tag](#unit-e-tag)  
[Constructors](#constructors)  
[Includes](#includes)    

## If statements
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

## UNIT-E tag
In case of comments and TODOs that are pertinent only to the UNIT-E code please create a code comment like:
```cpp
//UNIT-E: very specific comment about unit-e
```

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

## Includes
Make sure always to use <> notation instead of the "". There is not of a big difference but this is done mostly for consistency with the current codebase.

```cpp
// DO
#include <chain.h>

// DON'T
#include "chain.h"
```

## Doxygen comments
Doxygen multiline comments must be written using `/**`.  
Doxygen singline comments must be written using `//!`.  
Document the parameters if not obvious with `@param` and make sure to add the direction using `[in]`, `[out]` or `[in,out]`.  
The result should be documented using `@return` and imperative tense.
The main rationale for this is to stick to Bitcoin most used format.

```cpp
/**
* This is a comment for Foo()
* @param[in] param
* @param[out] pOut
* @param[in,out] p3
* @return a result code
**/
int Foo(const A& param, B* pOut, int& p3)
{
    ...
}
```
