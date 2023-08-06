
# cp-template


This is a very simple utility to generate directories based on templates.


## Install


```bash
pip install cp-template
```


## Usage

```
cp-template TEMPLATE_PATH DESTINATION_PATH key=value ...
```


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
cp-template './{{project}}' pineapple author=me
```

And it will generate this in the current directory:

```
pineapple/
  .gitignore
  README.md        # File contains "pineapple by me"
  pineapple/
    __init__.py
```

The template directory does not have to contain `{{...}}`. If it does not, the stem of the destination path (last part of the path minus the extension) is placed in the `STEM` variable, so you can refer to it in the files using `{{STEM}}`.

More features will be added as I need them, but feel free to make PRs to contribute some.
