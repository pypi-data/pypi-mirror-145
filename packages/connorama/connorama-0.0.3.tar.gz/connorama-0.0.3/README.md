# Connorama

colours for python terminal
includes **text** and **background** colouring
also includes **style**/font formatting

## Instructions
1. Install:
```
pip install connorama
```
2. Initialise in project:
``` python
from connorama import Text, Back, Style
```
3. Use the features!
``` python
print(Text.red + Back.light_black + Style.bold + Style.underlined + "Hello world!" + Style.RESET_ALL)
```

## Options
### Text + Back
> black, white, red, green, yellow, blue, magenta, cyan  
> light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan

**RESET**: *removes any colouring*

### Style
> bold: *thicker text*  
> dim: *dim text (same thickness as normal)*  
> underlined: *underline under the text*  
> reverse: *swithches the text's Text and Back colours*  
> hidden: *hidden text*

**RESET_ALL**: *removes Text, Back and Style*
**RESET_(style)**: *removes the specific style*