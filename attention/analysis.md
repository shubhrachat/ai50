# Analysis

## Layer 3, Head 1

This head pays extreme attention to the succeeding words in the sentence.
The values are evenly distributed along a diagonal each paying attention to the next word.


Example Sentences:
- CS50 is a computer [MASK] course.
- I love [MASK] music.

## Layer 6, Head 6

This head pays strong attention to [SEP] token.
Every word's pixel strongly pays attention to the [SEP] token.
This is the case where there is no good word to pay attention to in this attention head[Head 6].

Example Sentences:
- CS50 is a computer [MASK] course.
- I love [MASK] music.
