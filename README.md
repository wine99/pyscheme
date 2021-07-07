# pyscheme
Minimal Scheme interpreter in Python.

Basically line to line translation from the code of meta-circular evaluator in section 4.1 in the book SICP.

**NB:**

- do not support rational
- do not use `'...`, use `(quote ...)`
- `#t` is a primitive True Value, while `true` is a global variable with True value, same for `#f` and `false`
- tail recursions are not optimized

**TODO:**

- `(list ...)`
- `(let* ...)`
