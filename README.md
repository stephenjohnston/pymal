Use the main pymal.py to start the lisp shell.

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
user> (defn is-zero? [n] (= 0 n))
#<function>
user> (is-zero? 10)
false
user> (is-zero? 0)
true
user> (defn fac [n] (if (is-zero? n) 1 (* n (fac (dec n)))))
#<function>
user> (fac 5)
120
```
