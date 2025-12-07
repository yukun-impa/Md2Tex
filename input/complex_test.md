---
title: Complex Markdown Test Document
author: Gemini Agent
date: 2025-12-07
template: templates/main.tex
---

# Introduction to Complex Features

This document serves as a comprehensive test for the Markdown to LaTeX converter, showcasing various complex Markdown features and their expected LaTeX conversions.

## Text Formatting and Basic Elements

Here's some **bold text**, some *italic text*, and some ~~strikethrough text~~.
This is `inline code`.

---

## Lists

### Unordered Nested List

*   Item 1
    *   Sub-item 1.1
        *   Sub-sub-item 1.1.1
    *   Sub-item 1.2
*   Item 2
    *   Sub-item 2.1

### Ordered Nested List

1.  First item
    1.  First sub-item
        1.  First sub-sub-item
    2.  Second sub-item
2.  Second item

---

## Code Blocks

```python
def hello_world():
    print("Hello, LaTeX!")

if __name__ == "__main__":
    hello_world()
```

```
This is a generic code block
without a specified language.
```

---

## Links and Images

Visit our [website](https://www.example.com) for more information.

![Placeholder Image](input/placeholder.png "A beautiful placeholder")

---

## Mathematics

Inline math: $E=mc^2$.

Display math:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

Another display math:
\$\$
a^2 + b^2 = c^2
\$\$

---

## Tables

| Header 1 | Header 2 | Header 3 |
| :------- | :------: | -------: |
| Left     |  Center  |    Right |
| Cell A   |  Cell B  |    Cell C |
| 123      |   456    |      789 |

| Item     | Quantity | Price    |
| :------- | --------:| :------- |
| Apples   | 5        | \$1.00   |
| Bananas  | 10       | \$0.50   |
| Oranges  | 3        | \$1.25   |

---

## Blockquotes

> This is a simple blockquote.
> It can span multiple lines.
>
> > This is a nested blockquote.
> > Very interesting, isn't it?

---

## Horizontal Rule

***

## Mixed HTML and Markdown

This text contains <b>bold HTML</b> and <i>italic HTML</i>. Also, <u>underlined HTML</u>.
Some `code` within <b>HTML bold</b>.
