# webfast
Fast HTML Abstraction and Generator for Python.

You're building the next big thing and definitely writing the perfect HTML file is not on the priority.

**WebFast** let's you create HTML documents on the go and inside your Python scripts! It is built on top of **wbuilder** plus with another level of abstraction, so you can code with no trouble of messing up with closing tags--it's quick and easy.

Here's a sample syntax:
```python
page[".selector"] = "tag #id.class1.class2.class3 data-x='10' data-y='false' style='font-size:12px;color:#000;' hidden > inner text"
```
And scroll down below for more examples.

## Official Release
**WebFast** can now be used on your Python projects through PyPi by running pip command on a Python-ready environment.

`pip install -U webfast`

Current version is 1.0.0, but more updates are coming soon.

This is compatible with Python 3.9+, and will require other third-party libraries during installation.


## Usage
**Import Package**
```python
from webfast import WebFast
```

**Initialization**
```python
page = WebFast()
page = WebFast("home.html")
```

**Import Package**
```python
page["head"] = "title > WebFast v1.0"
```

**Import Package**
Basically, you set the parent selector to append the new element.
```python
# create container box
page["body"] = "div #content"
page["#content"] = "div #box.container.light"

# create the popup text
page["#box"] = "div #title.header > WebFast"
page["#box"] = "div .message data-default='Lorem impsum...' > Hello, world!"

# populate the action buttons
page["#box"] = "div #action.btn-list"
page["#action"] = "button #btn1.btn.btn-no style='background-color:#b22222;' > CLOSE"
page["#action"] = "button #btn2.btn.btn-yes > CONTINUE"
```

**Setting Properties**
```python
page["html"] = "lang=en"
page["body"] = "#canvas"
```

```python
html = page.build()
print(html)
```
