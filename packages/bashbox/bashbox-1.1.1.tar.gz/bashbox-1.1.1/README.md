![bashbox](https://user-images.githubusercontent.com/42397332/161363655-26bb5c3c-a09a-4279-85fc-597fbb2692ae.png)

<div align="center">
	<br>
	<img src="https://img.shields.io/github/workflow/status/bash-elliott/bashbox/Upload%20Python%20Package?label=Package%20Status&style=for-the-badge&logo=python&logoColor=white">
	<img src="https://img.shields.io/github/v/tag/bash-elliott/bashbox?style=for-the-badge">
	<img src="https://img.shields.io/github/release-date/bash-elliott/bashbox?style=for-the-badge">
	<img src="https://img.shields.io/github/commit-activity/w/bash-elliott/bashbox?style=for-the-badge">
	<br><br>
</div>

Bashbox is a textbox package for Python that provides a simple and easy to use system for creating simplistic and professional looking boxes to use in your Python programs.

Bashbox is developed with the intention to make important warnings or errors during runtime easier to see by drawing them in a distinct box that stands out among other output infromation, and includes customization options to allow for further distinction between different errors.

However, Bashbox can also be used as a simple tool for generating a simple box with preset text which may be helpful for displaying important information such as use policies or instructions at the start of a program.

# Table of Contents
- [Installation](#installation)
  * [Using pip](#using-pip)
  * [Using setup.py](#using-setuppy)
- [Usage](#usage)

# Installation
## Using pip
Run `python -m pip install bashbox` in the context of your choice, and Bashbox will be installed into your Python installation's site-packages.
## Using setup.py
Download the latest release's source code and run `python setup.py install` in the root directory.

# Usage
<details><summary>Basic Bashbox</summary>
	<br>
	
**Input**
```python
from bashbox import bashbox

box = bashbox()
box.setText(0, "This is a Bashbox!")
box.draw()
```

**Output**
```
╔════════════════════╗
║ This is a bashbox! ║
╚════════════════════╝
```
	
</details>

<details><summary>Multiple Columns</summary>
	<br>
	
**Input**
```python
from bashbox import bashbox

box = bashbox()
box.setColumns(2)
box.setText(0, "Some Text!")
box.setText(1, "Another column of text!")
box.draw()
```

**Output**
```
╔════════════╦═════════════════════════╗
║ Some Text! ║ Another column of text! ║
╚════════════╩═════════════════════════╝
```
</details>

<details><summary>Multiple lines</summary>
	<br>
	
**Input**
```python
from bashbox import bashbox

box = bashbox()
box.setText(0, "Here's one line.", "Here's another! Wow!")
box.draw()
```

**Output**
```
╔══════════════════════╗
║ Here's one line.     ║
║ Here's another! Wow! ║
╚══════════════════════╝
```
</details>

<details><summary>Adding a title</summary>
	<br>
	
**Input**
```python
from bashbox import bashbox

box = bashbox()
box.setTitle("Look, this is a title!")
box.setText(0, "There's a title up there!")
box.draw()
```

**Output**
```
╔═══════════════════════════╗
║ Look, this is a title!    ║
╠═══════════════════════════╣
║ There's a title up there! ║
╚═══════════════════════════╝
```
</details>

<details><summary>Theming a bashbox</summary>
	<br>
	
**Input**
```python
from bashbox import bashbox

double = bashbox()
double.setTheme('double')
double.setText(0, "Themed bashbox!")
double.draw()

single = bashbox()
single.setTheme('single')
single.setText(0, "Themed bashbox!")
single.draw()

curved = bashbox()
curved.setTheme('curved')
curved.setText(0, "Themed bashbox!")
curved.draw()

barebone = bashbox()
barebone.setTheme('barebone')
barebone.setText(0, "Themed bashbox!")
barebone.draw()
```
	
**Output**
```
╔═════════════════╗
║ Themed bashbox! ║
╚═════════════════╝
┌─────────────────┐
│ Themed bashbox! │
└─────────────────┘
╭─────────────────╮
│ Themed bashbox! │
╰─────────────────╯
+-----------------+
| Themed bashbox! |
+-----------------+
```
</details>

<details><summary>Everything all together</summary>
	<br>

**Input**
```python
from bashbox import bashbox

box = bashbox()
box.setColumns(3)
box.setTheme('curved')
box.setTitle("Friends")
box.setText(0, "Bob", "Regina", "Terry")
box.setText(1, "bobtheman@email.com", "regina.disney@email.com", "terrymaster@email.com")
box.setText(2, "+1 (111) 222-3333", "+1 (444) 555-666", "+1 (777) 888-9999")
box.draw()
```

**Output**
```
╭──────────────────────────────────────────────────────╮
│ Friends                                              │
├────────┬─────────────────────────┬───────────────────┤
│ Bob    │ bobtheman@email.com     │ +1 (111) 222-3333 │
│ Regina │ regina.disney@email.com │ +1 (444) 555-666  │
│ Terry  │ terrymaster@email.com   │ +1 (777) 888-9999 │
╰────────┴─────────────────────────┴───────────────────╯
```
</details>