# Triangles

![Version](https://img.shields.io/badge/Version-1.0.0-green) ![Author](https://img.shields.io/badge/Author-Hemendu%20Roy-red)

## Overview

Using the [Law of Cosines](https://en.wikipedia.org/wiki/Law_of_cosines) and the [Law of Sines](https://en.wikipedia.org/wiki/Law_of_sines), this library can be used to calculate all remaining sides and angles of a triangle when any one of the following sets of inputs are available.
 1. The length of 2 adjacent sides and their interior angle (SAS)
 2. The value of 2 angles and the length of the common side (ASA)
 3. The lengths of all 3 sides of the triangle (SSS)

## Installation

```sh
pip install triangles
```

## Usage

Import the module
```sh
from triangles import triangles
```

Use the functions to calculate the sides and angles of a triangle

```sh
>>> triangles.SSS(1,1,1)
(1, 1, 1, 60.00000000000001, 59.99999999999999, 60.00000000000001)

>>> triangles.SAS(1,60,1)
(1, 1, 0.9999999999999999, 60.00000000000001, 60.00000000000001, 60)

>>> triangles.ASA(60,1,60)
(1.0, 1.0, 1, 60, 60, 60)

```