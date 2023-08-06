#!/usr/bin/env python3
# coding=UTF-8

from builtins import property
class Fraction(object) :
    """Complex Fraction class with built-in class int arithmetic."""
    
    # NOTE: THIS IS A COMPLEX TYPE!
    # IT HAS NO __int__, __float__, __round__, __gt__, ETC.
    
    __slots__ = ("numerator", "denominator")
    
    def __new__(cls, numerator=0, *args, **kwargs) :
        """Create a complex fraction instance.
        
        >>> Fraction(8, 9)
        Fraction(8, 9)
        >>> Fraction(-8, 9)
        Fraction(-8, 9)
        >>> Fraction(8, -9)
        Fraction(-8, 9)
        >>> Fraction(8)
        Fraction(8)
        >>> Fraction(9, 3)
        Fraction(3)
        >>> Fraction()
        Fraction(0)
        >>> Fraction(0, 0)
        Traceback: ZeroDivisionError
        >>> Fraction(1j, 8)
        Fraction(1j, 8)"""
        
        from builtins import AttributeError, IndexError, TypeError
        try :
            numerator.__Fraction__
        except AttributeError :
            pass
        else :
            return numerator.__Fraction__(*args, **kwargs)
        
        try :
            denominator = args[0]
        except IndexError :
            denominator = 1
        
        # Do this because the types may not be built-in
        from builtins import int, float, complex, tuple, str, object, len
        
        if isinstance(numerator, complex) :
            numerator = (numerator.real.as_integer_ratio(),
                         numerator.imag.as_integer_ratio())
        elif isinstance(numerator, float) :
            numerator = (numerator.as_integer_ratio(), (0, 1))
        elif isinstance(numerator, int) :
            numerator = ((numerator, 1), (0, 1))
        elif isinstance(numerator, tuple) :
            if len(numerator) == 0 :
                numerator = ((0, 1), (0, 1))
            elif len(numerator) == 1 :
                if isinstance(numerator[0], int) :
                    numerator = ((numerator[0], 1), (0, 1))
                else :
                    raise TypeError("Unacceptable type: "+\
                                    str(type(numerator[0])))
            else :
                if isinstance(numerator[0], int) :
                    if isinstance(numerator[1], int) :
                        numerator = ((numerator[0], 1), (numerator[1], 1))
                    else :
                        raise TypeError("Unacceptable type: "+\
                                        str(type(numerator[1])))
                else :
                    raise TypeError("Unacceptable type: "+\
                                    str(type(numerator[0])))
        else :
            raise TypeError("Unacceptable type: "+str(type(numerator)))
        
        from math import gcd
        if isinstance(denominator, complex) :
            # Use the fractional complex division formula:
            # (a/b+c/di)/(p/q+r/si)
            #=(adpqqsss+bcqqqrss)/(bdppqsss+bdqqqrrs)
            #+(bcpqqsss-adqqqrss)/(bdppqsss+bdqqqrrs) i
            a, b = numerator[0]
            c, d = numerator[1]
            p, q = denominator.real.as_integer_ratio()
            r, s = denominator.imag.as_integer_ratio()
            numerator = \
            (a*d*p*q*q*s**3+b*c*q**3*r*s*s, b*c*p*q*q*s**3-a*d*q**3*r*s*s)
            denominator = b * d * (p*p*q*s**3+q**3*r*r*s)
            g = gcd(gcd(*numerator), denominator)
            numerator = (numerator[0]//g, numerator[1]//g)
            denominator //= g
        elif isinstance(denominator, float) :
            # Use the fractional complex division formula:
            # (a/b+c/di)/(p/q)=adq/bdp+bcq/bdpi
            a, b = numerator[0]
            c, d = numerator[1]
            p, q = denominator.as_integer_ratio()
            numerator = (a*d*q, b*c*q)
            denominator = b * d * p
            g = gcd(gcd(*numerator), denominator)
            numerator = (numerator[0]//g, numerator[1]//g)
            denominator //= g
        elif isinstance(denominator, int) :
            a, b = numerator[0]
            c, d = numerator[1]
            p, q = denominator, 1
            numerator = (a*d*q, b*c*q)
            denominator = b * d * p
            g = gcd(gcd(*numerator), denominator)
            numerator = (numerator[0]//g, numerator[1]//g)
            denominator //= g
        else :
            raise TypeError("Unacceptable type: "+str(type(denominator)))
        
        if denominator == 0 :
            from builtins import ZeroDivisionError
            raise ZeroDivisionError("Fraction denominator is zero")
        elif denominator < 0 :
            numerator = (-numerator[0], -numerator[1])
            denominator = -denominator
        
        self = object.__new__(cls)
        
        self.numerator = numerator
        self.denominator = denominator
        return self
    
    def __repr__(self) :
        if self.numerator[1] > 0 :
            if self.numerator[0] == 0 :
                if self.denominator == 1 :
                    return "%s(%dj)" % (type(self).__qualname__,
                                        self.numerator[1])
                return "%s(%dj, %d)" % (type(self).__qualname__,
                                        self.numerator[1], self.denominator)
            else :
                if self.denominator == 1 :
                    return "%s(%d+%dj)" % (type(self).__qualname__,
                                           *(self.numerator))
                return "%s(%d+%dj, %d)" % (type(self).__qualname__,
                                           *(self.numerator), self.denominator)
        elif self.numerator[1] < 0 :
            if self.numerator[0] == 0 :
                if self.denominator == 1 :
                    return "%s(%dj)" % (type(self).__qualname__,
                                        self.numerator[1])
                return "%s(%dj, %d)" % (type(self).__qualname__,
                                        self.numerator[1], self.denominator)
            else :
                if self.denominator == 1 :
                    return "%s(%d%dj)" % (type(self).__qualname__,
                                          *(self.numerator))
                return "%s(%d%dj, %d)" % (type(self).__qualname__,
                                          *(self.numerator), self.denominator)
        else :
            if self.denominator == 1 :
                return "%s(%d)" % (type(self).__qualname__, self.numerator[0])
            return "%s(%d, %d)" % (type(self).__qualname__,
                                   self.numerator[0], self.denominator)
    
    def __bool__(self) :
        return self.numerator != (0, 0)
    
    def __hash__(self) :
        from builtins import hash
        return hash(self.numerator[0]+\
                    (self.numerator[1]-(self.numerator[1]<0))*1000003+\
                    (self.denominator-1)*13199005877)
    
    def as_integer_ratio(self) :
        if self.numerator[1] == 0 :
            return self.numerator[0], self.denominator
        from builtins import ValueError
        raise ValueError("%s imag part is not zero"%self.__qualname__)
    
    @property
    def type(self) :
        if self.numerator[1] == 0 :
            from builtins import abs
            if abs(self.numerator[0]) < self.denominator :
                return "proper"
            return "improper"
        return "imag"
    
    def __str__(self, form="c/d") :
        if form == "c/d" :
            if self.numerator[1] > 0 :
                if self.numerator[0] == 0 :
                    return "%dj/%d" % (self.numerator[1], self.denominator)
                return "(%d+%dj)/%d" % (*(self.numerator), self.denominator)
            elif self.numerator[1] < 0 :
                if self.numerator[0] == 0 :
                    return "%dj/%d" % (self.numerator[1], self.denominator)
                return "(%d%dj)/%d" % (*(self.numerator), self.denominator)
            return "%d/%d" % (self.numerator[0], self.denominator)
        elif form == "repr" :
            return self.__repr__()
        from builtins import ValueError
        raise ValueError("Invalid form")
    
    def __pos__(self) :
        from builtins import type
        return type(self)(self.numerator, self.denominator)
    
    def __neg__(self) :
        from builtins import type
        return type(self)(self.numerator, -self.denominator)
    
    def __abs__(self) :
        # I can't ensure the result of it is a rational :(
        
        from builtins import abs
        return abs((self.numerator[0]+self.numerator[1]*1j)/self.denominator)
    
    def __complex__(self) :
        return (self.numerator[0]+self.numerator[1]*1j)/self.denominator
    
    @property
    def real(self) :
        from builtins import type
        return type(self)(self.numerator[0], self.denominator)
    
    @property
    def imag(self) :
        from builtins import type
        return type(self)(self.numerator[1], self.denominator)
    
    def __eq__(self, value) :
        from builtins import type, isinstance, Exception, NotImplemented
        if not isinstance(value, type(self)) :
            try :
                value = type(self)(value)
            except Exception :
                return False
        return self.numerator == value.numerator and \
               self.denominator == value.denominator
    
    def __ne__(self, value) :
        return not self.__eq__(value)
    
    def __add__(self, value) :
        from builtins import type, isinstance, Exception, NotImplemented
        if not isinstance(value, type(self)) :
            try :
                value = type(self)(value)
            except Exception :
                return NotImplemented
        return type(self)((self.numerator[0]*value.denominator+\
                           value.numerator[0]*self.denominator,
                           self.numerator[1]*value.denominator+\
                           value.numerator[1]*self.denominator),
                          self.denominator*value.denominator)
    
    __radd__ = __add__
    
    def __sub__(self, value) :
        return self + -value
    
    def __rsub__(self, value) :
        return value + -self
    
    def __mul__(self, value) :
        from builtins import type, isinstance, Exception, NotImplemented
        if not isinstance(value, type(self)) :
            try :
                value = type(self)(value)
            except Exception :
                return NotImplemented
        return type(self)((self.numerator[0]*value.numerator[0]-\
                           self.numerator[1]*value.numerator[1],
                           self.numerator[0]*value.numerator[1]+\
                           self.numerator[1]*value.numerator[0]),
                          self.denominator*value.denominator)
    
    __rmul__ = __mul__
    
    def __truediv__(self, value) :
        from builtins import type, isinstance, Exception, NotImplemented
        if not isinstance(value, type(self)) :
            try :
                value = type(self)(value)
            except Exception :
                return NotImplemented
        a, b = self.numerator
        c = self.denominator
        p, q = value.numerator
        r = value.denominator
        return type(self)((a*r*c*p+b*r*c*q, b*r*c*p-a*r*c*q), c*c*(p*p+q*q))
    
    def __rtruediv__(self, value) :
        from builtins import type
        return value * (type(self)(1)/self)
    
    def conjugate(self) :
        from builtins import type
        return type(self)((self.numerator[0], -self.numerator[1]),
                          self.denominator)
    
    def arg(self) :
        from math import atan, pi
        if self.numerator[0] > 0 :
            return atan(self.numerator[1]/self.numerator[0])
        elif self.numerator[0] < 0 :
            if self.numerator[1] > 0 :
                return atan(self.numerator[1]/self.numerator[0]) + pi
            elif self.numerator[1] < 0 :
                return atan(self.numerator[1]/self.numerator[0]) - pi
            return pi
        if self.numerator[1] > 0 :
            return pi / 2
        elif self.numerator[1] < 0 :
            return pi / -2
        from builtins import ValueError
        raise ValueError("Complex is equal to 0")
    
    def __pow__(self, value, mod=None) : # mod must be None
        if mod is not None :
            from builtins import TypeError
            raise TypeError("complex modulo")
        
        from builtins import type, isinstance, Exception, NotImplemented
        if not isinstance(value, type(self)) :
            try :
                value = type(self)(value)
            except Exception :
                return NotImplemented
        
        # Would you like to improve this?
        if value.numerator[1] == 0 and value.denominator == 1 :
            res = type(self)(1)
            if value.numerator[0] > 0 :
                for _ in range(value.numerator[0]) :
                    res *= self
            elif value.numerator[0] < 0 :
                if self.numerator == (0, 0) :
                    from builtins import ZeroDivisionError
                    raise ZeroDivisionError("0 to a negative or complex power")
                for _ in range(-value.numerator[0]) :
                    res /= self
            return res
        return self.__complex__() ** value.__complex__()
    
    def __rpow__(self, value, mod=None) :
        from builtins import pow
        return pow(value, self.__complex__(), mod)
    
    def __Fraction__(self, value=1) :
        return self / value
    
    # No __lshift__; use self * 2 ** value
    # No __rshift__; use self / 2 ** value
    # No __invert__: use -1 - self
