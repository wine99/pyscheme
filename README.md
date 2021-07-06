# pyscheme
Minimal Scheme interpreter in Python.

**NB:**

- do not support rational
- do not use `'...`, use `(quote ...)`
- `#t` is a primitive True Value, while `true` is a global variable with True value, same for `#f` and `false`
- tail recursions are not optimized
