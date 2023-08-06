# Uranium Image Cleanup
--------

 This program was designed to take in user input (a directory where images of uranium are stored), ask for an output folder and then proceed to process images in specified directory to remove text/noise only from specific grayscale uranium images.

Below is an example of how our ideal user should use install and use this package (AFIT = ideal user).

***Note:*** This program was designed to run much like an executable. We have provided use cases outside of the program running as an exectuable where user input is required.

Start a python shell.

## To install:

```
    >>> pip install uranium-image-cleanup
```

## Run program using console script:

```
    >>> python3 -m uic
    >>> 
    >>> *** Uranium Image Cleanup  ***
    >>> Enter Image/s Retrieval Directory:
```

## Alternative way of running:

```
    >>> import uranium_image_cleanup_package as uic
    >>> 
    >>> uic.main()
    >>>
    >>> *** Uranium Image Cleanup  ***
    >>> Enter Image/s Retrieval Directory:
```

## This package is also capable of:

- Removing text/noise on a single image of uranium.
- Detecting white pixels on a single image.

Below are examples on how to implement these.

###### Remove labels on a single image:

``` 
    >>> import uranium_image_cleanup_package as uic
    >>> import opencv as cv2
    >>>
    >>> image uranium_nucleus_10593520                  
    >>> result_image = uic.removeLabel(uranium_nucleus_10593520)

```
###### Detect white pixels on a single image:
``` 
    >>> import uranium_image_cleanup_package as uic
    >>> import opencv as cv2
    >>>
    >>> image uranium_nucleus_10593520                  
    >>> white_pixel_image = uic.detectWhite(img)
```

For more info and access to all the methods available, consult the remove_label.py script.

----------------------------



