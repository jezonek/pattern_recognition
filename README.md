# Pattern_recognition

Script for automatic generating regex from given string list.

## Requirements
* Python>= 3.6

## Assumptions
* We use only build-in Python libraries. Some calculations may be done with numpy or Pandas, but I decided to use only fast build-ins.
* The data that we are going to process have a structured structure and a specified length. E.g. Iban numbers, postal codes, telephone numbers, etc.
* We try to find the exact sign on a given place, if it is not possible then we are looking for the most accurate category

## Algorithm
1. Finding the most common length of one entry
1. Rejection of entries that are not of a specified length (we assume that they are erroneous for various reasons) 
1. Transposition of the clean data matrix, example:

    >[DE123, DE456, DE789]

    Will be:
    >[DDD, EEE, 147, 258, 369]

    This allows us to calculate the frequency of occurrence of each character.

1. Knowing the frequency of occurrence of characters we determine what is in a given place:
    * If a particular character occurs at 98%, it assigns this character to this place.
    * If a group occurs at 90%, it assigns this group to this place.
    * If no condition is met, return the dot.
    
    The mechanism allows adding additional conditions, e.g. selection of several candidates at selected probabilities.

1. After generating regex we check which data are not detected and add them to the pool of rejected data.

