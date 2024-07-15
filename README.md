# Game Engine
Back-End python game engine used to handle all back end for a text-based RPG.

This engine is object-oriented and will have options to create a personalised build. For example, you can create a build with personalised character stats, character flags, and game flags.

Eventually a front-end engine will be created, intended to directly communicate with this project. 

##Features

- 


## Standards

### Object Oriented Programming

Cannot stress enough how important the object-style approach for this project. 

Each individual feature should be an individual python file that communicates with a higher object in a hierarchy. They should all link back to main.py, which will have commands within to perform developer commands. 

For example:
A "create_character" function will be available within Main.py. This command will be passed down a branch to the lowest level and only the objects involved in creating a character such as an object that handles the turn order, an object that handles stat creation, etc.

### When committing

- You name it like this: xx.yy.zz - Notes
  - xx
    - 00 - BETA (Pre-complete)
    - 01 - ALPHA (Complete)
  - yy
    - Milestone
  - zz
    - Update

```text
e.g. 
00.05.24  - BETA, 5th milestone, 24th update
```

## Docstrings

Each file should be properly documented in the following format 
```python
"""
Information about the object 
"""
```

Each function/procedure should follow the same documentation
```python
"""
Information about the function/procedure
"""
```

And any additional docstrings can follow these formats
```python
"""
:param parameter1: Description of parameter 1
:return: str/int/bool etc.
"""
```

Ensure that effective docstrings are made for easier collaboration.

## Notes for collaborators

Kai (15/07/24) - We will keep to the main branch for any further updates for now since updates are infrequent