# sklearnFunctions - eleka12

This package is built on top of functions which are mostly required in a Data processing lifecycle.

As of now This package contains a function which can remove outliers present in the Dataset

More number of functions will be added... 

# How to use sklearnFunctions

* install the latest package 

> * in jupyter notebook -
```
    !pip install sklearnFunctions
```

> * in command prompt -
```bash    
    pip install sklearnFunctions
```

* Now run below snippets of code in your jupyter-notebooks / python project 

## Importing sklearnFunctions

```python

from sklearnFunctions.preprocessing import outliers

```

## The input for the outlier function must be in DataFrame

```python

old_df = pd.DataFrame({"X":xvals,"Y":yvals})


```

## Checking for outliers | .is_present() function will return a percentage of outlier present in each column

```python

outliers().is_present(old_df)

```

## Removing outliers from DataFrame | .outliers_removal() function will remove all the outliers present in DataFrame

```python

new_df = outliers().outliers_removal(old_df)

```

## pypi repo link -

[mongoops - PYPI](https://pypi.org/project/sklearnFunctions/)

## Github repo link - 

[mongoops - Github](https://github.com/Karthik-VG/sklearnFunctions)

