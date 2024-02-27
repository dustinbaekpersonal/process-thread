"""The main reason that numpy is faster than pure Python 
when solving the same problem is that 
numpy is creating and manipulating the same object types at a very low level 
in contiguous blocks of RAM, 
rather than creating many higher-level Python objects 
that each require individual management and addressing."""
