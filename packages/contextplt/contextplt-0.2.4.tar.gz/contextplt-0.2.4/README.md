# contextplt
[![python](https://img.shields.io/pypi/pyversions/contextplt)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/contextplt.svg)](https://pypi.org/project/contextplt/)
[![license](https://img.shields.io/pypi/l/contextplt?color=blue)](https://github.com/toshiakiasakura/contextplt/blob/main/LICENSE)

Source code repository for the contextplt package.

You can create a matplotlib figure using context manager. 
This package enables you to write short code and 
create a lot of figures in a simple manner. 

# Installation 
```bash
pip install contextplt
```

# Usage
You can write the matplotlib figure with context manager like this. 
```python
import contextplt as cplt
x = [1,2,3]
y = [1,2,3]
with cplt.Single(xlim=[0,5], ylim=[0,5], xlabel="xlabel", ylabel="ylabel",
        title="title", figsize=(6,6), dpi=150) as p:
    p.ax.plot(x,y)
```

The same figure without context manager becomes,
```python
x = [1,2,3]
y = [1,2,3]
fig = plt.figure(figsize=(6,6), dpi=150)
ax = fig.add_subplot(111)
ax.plot(x,y)
ax.set_xlabel("xlabel")
ax.set_ylabel("ylabel")
ax.set_xlim([0,5])
ax.set_ylim([0,5])
plt.title("title")
```

The benefit of context manager is recursive use of parameters using keyword arguments.
```python
kargs = dict(xlim=[0,5], ylim=[0,5], xlabel="xlabel", ylabel="ylabel",
        title="title", figsize=(6,6), dpi=150)
with cplt.Single(**kargs) as p:
    p.ax.plot(x,y)
```
If you want to replicate this figure options with different values, you just change inside contents of values.

# Note 
Dockerfile and docker-compose.yml are prepared for running example codes.


