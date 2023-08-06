from math import sin, asin, cos, acos, sqrt, degrees, radians
'''

a, b and c are the sides of a triangle
A, B and C are the corresponding opposite angles in degrees
'''
# Functions to calculate cos,acos,sin and asin in degrees

def cosd(theta):
    return cos(radians(theta))

def acosd(x):
    return degrees(acos(x))

def sind(theta):
    return sin(radians(theta))

def asind(x):
    return degrees(asin(x))

#Law of Cosines implementations

def cosSide(a, C, b):
    #To solve for side c
    return sqrt(a**2 + b**2 - 2*a*b*cosd(C))

def cosAngle(a, b, c):
    #To solve for angle C
    return acosd((a**2 + b**2 - c**2) / (2*a*b))

#Law of Sines implementations

def sinSide(A, b, B):
    #To solve for side a
    return sind(A) / sind(B) * b

def sinAngle(a, B, b):
    #To solve for angle A
    return asind(sind(B) * a / b)

def findThirdAngle(A, B):
    #To find the third angle
    return 180 - A - B

def isTriangle(a, b, c):
    #To check for a malformed triangle
    return c < a + b and a < b + c and b < c + a

#Implementations of Side-Angle-Side, Angle-Side-Angle and Side-Side-Side theorems

def SAS(a, C, b):
    c = cosSide(a, C, b)
    A = sinAngle(a, C, c)
    B = sinAngle(b, C, c)
    return (a, b, c, A, B, C)

def ASA(A, c, B):
    C = findThirdAngle(A, B)
    a = sinSide(A, c, C)
    b = sinSide(B, c, C)
    return (a, b, c, A, B, C)

def SSS(a, b, c):
    if isTriangle(a, b, c):
        C = cosAngle(a, b, c)
        A = cosAngle(b, c, a)
        B = findThirdAngle(A, C)
        return (a, b, c, A, B, C)