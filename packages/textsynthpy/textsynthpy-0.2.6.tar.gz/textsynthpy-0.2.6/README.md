# TextSynthPy
A small demo wrapper for a TextSynth api. To use, you need textsynth.com account to get api key. 

### Installation
```
pip install textsynthpy
```

### Get started
How to use:

```Python
from textsynthpy import TextSynth, Complete

# Initantiate a TextSynth object
con = TextSynth(API_KEY_HERE)

# text completion 
answer = con.text_complete("prompt")

# print generated text
print(answer.text)
```