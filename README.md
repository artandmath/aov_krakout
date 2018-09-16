# aov_krakout
Nuke tool. Creates a tree of lightgroups or illumination passes and recombines them.

Controls:

krackout to: (direction) - break out tree to left or right

x grid units: (x_space) - this is the amount of horizontal working space generated between each aov

y grid units small: (y_space) - vertically space out dots and shuffles Y grid units

y grid units large: (y_space_large) - this is the amount of vertical working space generated

aov pattern: (match_pattern) - Uses a wildcard system for searching aov layers. Comma deliniated. AOVs will vary depending on show and facility. Example:

  *group*,*emission* <- use this to break out lightgroups if they contain the word 'group'
  *coat*,*dir*,*spec*,*sss*,*mission* <- an example to break out illumination
  
krakout! (krackout) - Breakout that the nuke tree.
