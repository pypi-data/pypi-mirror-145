from pathlib import Path

# This is the only variable to be changed from elsewhere. All the rest should 
# remain constant.
cur_file = Path()

bold_md_syntax = ("**", "__")
bold_md_ignore = (
    "- ", "> ", "# ", "`", 
    "--", ">> ", "## ",
    "***", "___", "---", ">>> ", "### ", "```", "===",
    "####", "#####", "######"
    )
italic_md_syntax = ("*", "_")
italic_md_ignore = (
    "**", "__", "- ", "> ", "# ", "`", 
    "--", ">> ", "## ",
    "***", "___", "---", ">>> ", "### ", "```", "===",
    "####", "#####", "######"
    )
default_md_string = """
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

Heading 1
=========

Heading 2
---------

Some paragraph text.

Line Breaks with two spaces on the end of the line.  
Line two.  
Line three.

- item one
- item two
    - item one
    - item two
- item three

Horizontal rule.

---

1. item one
2. item two
    1. item one
    2. item two
3. item three

_Italic_

*italic*

**bold**

__Bold__

***Bold Italic***

___Bold Italic___

> Blockquotes.
>
> Multiple paragraphs with a > symbol on the empty line.

> Blockquotes.
>
>> Nested paragraphs with a >> symbol.

> #### Using other elements
>
> - works with blockquotes
> - just like it would
>
>  *do* **normally**.


Here is an `inline` code block.


```
This is a fenced code block.
```
"""