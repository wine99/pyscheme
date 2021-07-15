(define (a-plus-abs-b a b)
  ((if (> b 0) + -) a b))


(define (fib n)
  (if (<= n 1)
      1
      (+ (fib (- n 1))
         (fib (- n 2)))))


(define (sqrt x)
  (define (try guess old-guess)
    (if (good-enough? guess old-guess)
        guess
        (try (improve guess) guess)))

  (define (good-enough? guess old-guess)
    (= guess old-guess))

  (define (improve guess)
    (/ (+ guess (/ x guess)) 2))

  (try 1.0 x))


(define (map proc l)
  (if (null? l)
      nil
      (cons (proc (car l))
            (map proc (cdr l)))))

(define (one-to-n n)
  (define (iter i)
    (if (= i n)
        (cons i ())
        (cons i (iter (+ i 1)))))
  (iter 1))

(let ((one-to-5 (one-to-n 5)))
  (map (lambda (x) (* x x))
       one-to-5))
