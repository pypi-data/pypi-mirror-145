
# cp-template


This is a very simple utility to generate directories based on templates.


## Install


```bash
pip install cp-template
```


## Usage


Suppose you have the following directory structure (**Note: the {{}}s are part of the filenames**)

```
{{project}}/
  .gitignore
  README.md        # File contains "{{project}} by {{author}}"
  {{project}}/
    __init__.py
```

Then you can run the following command:

```
cp-template './{{project}}' project=pineapple author=me
```

And it will generate this in the current directory:

```
pineapple/
  .gitignore
  README.md        # File contains "pineapple by me"
  pineapple/
    __init__.py
```

More features will be added as I need them, but feel free to make PRs to contribute some.
