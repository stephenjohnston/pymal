What is this project?
=====================
This project is a python interpreter for the ["mal language" - Make a lisp.](https://github.com/kanaka/mal)
It is a lisp that includes the following features: 
* REPL (the read-eval-print loop for interactive tinkering) 
* Tail call optimization
* Macro system w/ quasiquote, unquote, splice-unquote, etc
* Support to load .mal files into the REPL

A few features that are not implemented or where it deviates from mal:
* try/catch (not implemented)
* self hosting (not implemented)
* Uses defn instead of def! combined with fn* (my preference)
* Does not follow the guide precisely, so it doesn't use the mal make/build system and doesn't use the mal testsuite

Why?
====
The project is for academic and learning purposes only.   
I've often heard it's a rite-of-passage for a programmer to implement a LISP dialect.  I believe the journey makes 
one a better programmer and opens your mind to new ideas and new ways of thinking.

I chose python as the implementation language because I wanted to learn more about it.  I'm surprised to see
how expressive it can be.  I believe this project weighs in at less than 600 lines of python code.


How to run?
===========

Run "python3 pymal.py" to start the REPL.
Load .mal files into the REPL with (load-file "/path/to/file.mal") 

There is now a core library of functions available (see core.py) 

Example usage:
```
user> (defn inc [n] (+ n 1)) ; a function to increment by 1
#<function>
user> (defn dec [n] (- n 1)) ; a function to decrement by 1
#<function>
user> (inc 1)
2
user> (dec 9)
8
user> ; Let define a factorial function.  Factorial of 0 is 1.  Otherwise is n * fac(n-1)
user> (defn fac [n] (if (= n 0) 1 (* n (fac (dec n)))))
#<function>
user> ; fac(3) is 1 * 2 * 3 = 6
user> (fac 3) 
6
user> ; fac(5) is 1 * 2 * 3 * 4 * 5 = 120
user> (fac 5)
120
user> (defn zero? [n] (= 0 n))
#<function>
user> (zero? 10)
false
user> (zero? 0)
true
user> (defn fac [n] (if (zero? n) 1 (* n (fac (dec n)))))
#<function>
user> (fac 5)
120
```
