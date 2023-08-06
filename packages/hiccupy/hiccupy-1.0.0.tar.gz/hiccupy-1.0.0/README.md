# hiccupy

Rendering HTML from [hiccup-style lists](https://github.com/weavejester/hiccup) in python.

### Usage

First, install `hiccupy`:
```bash
python3 -m pip install hiccupy
```

Then simply import `render` and render lists to HTML!
```python
from hiccupy import render

lst = [
    "body",
    [
        "div",
        {"id": "myDiv"},
        [
            "h1",
            {"class": "header"},
            "Hello World!",
        ],
    ],
]
print(render(lst))
```
