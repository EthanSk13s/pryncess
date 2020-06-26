# Pryncess (W.I.P)
A Python REST API wrapper for Princess
## https://api.matsurihi.me/

## About Princess
Princess is a public REST API that allows developers to get data from 
[Mirishita](https://www.project-imas.com/wiki/THE_iDOLM@STER_Million_Live!:_Theater_Days) 
using the website, matsurihi.

## Example
```py
import pryncess

# Pass versions of mirishita ("ja", "ko", "zh")
session = pryncess.Pryncess("ja")
card = session.get_card(704)

print(card.name)
```

## Installation
For now clone the repo or download the pryncess folder

***However, this project will update frequently since it's not ready for code use. 
So I recommend cloning the repo to make it simple to update.***

## Dependencies
- At least Python 3.6 (NOTE: I've only tested with 3.8)
- Requests

## Note
I'm not in anyway affiliated with the development of matsurihi. Pryncess is a project that I made to allow easier interactions with the REST API.
