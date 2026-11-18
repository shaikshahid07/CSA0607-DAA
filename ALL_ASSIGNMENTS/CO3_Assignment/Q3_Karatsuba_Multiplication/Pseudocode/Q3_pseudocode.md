# Q3 Pseudocode - Standard and Karatsuba Multiplication

## Standard (school-book) multiplication

```
STANDARD(x, y)
    a = digits of x, b = digits of y
    result = array of zeros, length |a| + |b|
    for i = 0 .. |a|-1
        carry = 0
        for j = 0 .. |b|-1
            total = result[i+j] + a[i]*b[j] + carry
            result[i+j] = total mod 10
            carry = total div 10
        result[i + |b|] = result[i + |b|] + carry
    return number formed by result          // n^2 single-digit multiplications
```

## Karatsuba

```
KARATSUBA(x, y)
    if x < 10 or y < 10  return x * y                 // base case: one digit
    n = max(digits of x, digits of y)
    m = n / 2
    p = 10^m
    x_high, x_low = x div p, x mod p                  // DIVIDE each number in two halves
    y_high, y_low = y div p, y mod p
    z0 = KARATSUBA(x_low, y_low)                      // 3 recursive calls only
    z2 = KARATSUBA(x_high, y_high)
    z1 = KARATSUBA(x_low + x_high, y_low + y_high) - z0 - z2
    return z2 * p^2 + z1 * p + z0                     // COMBINE: additions and shifts
```

Why it works: (xl + xh)(yl + yh) = xl*yl + (xl*yh + xh*yl) + xh*yh, so the middle term z1 = (xl*yh + xh*yl) is obtained from one multiplication instead of two.

Recurrence: T(n) = 3T(n/2) + cn -> Theta(n^(log2 3)) = Theta(n^1.585).

## Hybrid (used in the crossover experiment)

```
HYBRID(x, y, cutoff)
    if x < 10 or y < 10  return x * y
    if x < 10^cutoff or y < 10^cutoff  return STANDARD(x, y)
    ... same as KARATSUBA but recursive calls use HYBRID
```
