#lang racket

;Q1

;Compute the sum of squares of the two largest out of three integers
;It is also possible to write functions for an arbitrary number of arguments!

(define (msum-squares a b c)
  (define (square x) (* x x))
  (- (+ (square a)
        (square b)
        (square c))
     (square (min a b c))))

(display "Sum of the squares of two largest of 2, 3 and 4:") (newline)
(display (msum-squares 2 3 4)) (newline)

;While this is certainly not an efficient way of writing the function
;(for instance you end up doing 2 extra squarings on top of the 2 required ones)
;it illustrates maybe an unusual way of solving this problem with avoiding to use
;any conditionals through the use of the built-in min.

;Q2

;Compute the sum of integers from a to b
(define (intsum a b)
  (if (> a b)
    0
    (+ a
       (intsum (+ a 1) b))))

(display "Sum of integers from 3 to 10:") (newline)
(display (intsum 3 10)) (newline)

;Notice that this function generates a linear recursive process
;Turn it into an iterative process!
;What if you want to sum up the squares of integers from a to b? What about the cubes?
;Rather than writing a new procedure for each, we can abstract this to resemble the
;usual sigma notation in mathematics

(define (sum f a b)
  (if (> a b)
    0
    (+ (f a)
       (sum f (+ a 1) b))))

;So then the sum of integers could just be

(define (identity x) x)

(define (newintsum a b)
  (sum identity a b))

;Similarly the sum of cubes would be

(define (cube x) (* x x x))

(define (cubesum a b)
  (sum cube a b))

;Q3

;This is simple, just add 100 and 200 to the list in (define (first-coin n) ...
;But try to think why this actually works e.g. for sums which are smaller than 100!

;Q4

;For this I refer you to various answers available online by googling "iterative counting change scheme"

;Q5

;In order to do this we need some kind of recursive relation for the binomial coefficients
;(just like we needed one for the factorial or for the Fibonacci numbers)
;From Pascal's triangle (or directly from the definition) it is not too difficult to see that
;the (n k) binomial coefficient satisfies (n k) = (n-1 k-1) + (n-1 k), hence using the same
;"recipe" as before:

(define (binomial n k)
  (if (or (= n 0)
          (= n 1)
          (= k 0)
          (= k n))
    1
    (+ (binomial (- n 1) (- k 1))
       (binomial (- n 1) k))))

(display "The (5 3) binomial coefficient is") (newline)
(display (binomial 5 3)) (newline)

;What kind of a recursive process does this function generate?
