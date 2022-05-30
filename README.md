# aov_krakout
Nuke tool. Creates a tree of lightgroups or illumination passes and recombines them.
![screenshot](https://raw.githubusercontent.com/artandmath/aov_krakout/master/aov_krakout_screenshot.gif)

## Install instructions

- Install aov_krakout.py into somewhere nuke can find it (~/.nuke is fine for single user)
- Paste contents of aov_krakout.nk into nuke.

## Properties:

__krackout to: (direction)__  >>  break out tree to left or right

__x grid units: (xgu)__  >>  this is the amount of horizontal working space generated between each aov

__y grid units small: (ygu_small)__  >>  vertically space out dots and shuffles Y grid units

__y grid units large: (ygu_large)__  >>  this is the amount of vertical working space generated

__aov pattern: (aov_pattern)__  >>  Uses a bash style query system for searching AOV layers. Comma delineated. AOVs will vary depending on show and facility.

__half x grid units for ^/ queries: (x_half)__  >>  Use half the amount of horizontal working space between each aov if dividing or multiplying one AOV by another using the '/' or '^' query terms.

__subtract sum of aovs from rgb: subtract_aovs__  >>  Gather up any left over data that wasn't captured by the renderer by subtracting the queried AOVs from the rgb. Useful for debugging lighting. Final production renders should not need to use this functionality.

__krakout! (krackout)__ >> Create the nuke tree.

### Pattern query syntax:
- __,__  >>  separates each AOV search query
-   __/__  >> divide AOV by another AOV and multiply back together
-  __^__  >>  multiply AOV by another
-  __!__  >>  exclude this AOV
-  __*__  >>  wildcard to capture multiple AOVs - works with /,^,!
-  __$__  >>  parse an environment variable

### Pattern query examples:
<i>lg*,!lg0</i>  >>  Fetch all AOVs starting with 'lg', ignore 'lg0'.

<i>light/diffuse,reflect,refract_raw^refract_filter,spec,gi</i>  >>  Explicitly break out some aovs. Divide 'light' by 'diffuse' multiply 'refract_raw' by 'refract_filter'.

<i>$char_aovs, emission</i>  >> Will fetch the string contained in the environment variable 'char_aovs' and then parse that string into the query system. Then move onto 'emission'.

## The original krakout

https://www.c64-wiki.com/wiki/Krakout

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
