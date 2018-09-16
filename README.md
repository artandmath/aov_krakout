# aov_krakout
Nuke tool. Creates a tree of lightgroups or illumination passes and recombines them.

Controls:

krackout to: (direction) - break out tree to left or right

x grid units: (x_space) - this is the amount of horizontal working space generated between each aov

y grid units small: (y_space) - vertically space out dots and shuffles Y grid units

y grid units large: (y_space_large) - this is the amount of vertical working space generated

aov pattern: (match_pattern) - Uses a wildcard system for searching aov layers. Comma deliniated. AOVs will vary depending on show and facility. Example:

    -> *group*,*emission* <- use this to break out lightgroups if they contain the word 'group' 
    -> *coat*,*dir*,*spec*,*sss*,*mission* <- an example to break out illumination
  
krakout! (krackout) - Breakout that the nuke tree.

![screenshot](https://raw.githubusercontent.com/artandmath/aov_krakout/master/aov_krakout_screenshot.png)

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
