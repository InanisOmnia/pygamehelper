
# Getting Started

## Getting and Importing

PyGameHelper is currently accessed through GitHub and is not available on pypi or other python module installer services
Therefore to use PyGameHelper, go to the projects  [Releases](https://github.com/LordFarquhar/pygamehelper/releases/) navigate to the most recent full release and download the source code  
  
Extract it using your favoured method  
  
Locate the `PyGameHelper.py` file and copy and paste it into your project directory  

```bash
.
└── project
    ├── PyGameHelper.py
    └── app.py
```

Then it needs importing 
  
```python
import PyGameHelper as pgh
```

You can change the name you would like to import it as but for the purposes of this documentation we will use `pgh`

Now PyGameHelper is in your project and ready to be used!

## Window

The window is what the user sees and the thing they interact with so its important to have one  
    
The Window class takes three arguments:
 - Size: a tuple in the form (width, height)
 - Title: a string that will be displayed in the title bar

Create one by typing `window = pgh.Window(500, 500, "Hello World")`  
  
