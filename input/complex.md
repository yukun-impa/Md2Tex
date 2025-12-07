---
title: "A Complex Document"
author: "Test User"
---

# This is a Complex Document

This document demonstrates more advanced Markdown features and how they are converted to LaTeX.

## Images

Here is an image. The LLM should be able to convert this to a `figure` environment.

![A placeholder image](./input/placeholder.png)

## A More Complex Table

This table has alignment.

| Left-aligned | Center-aligned | Right-aligned |
|:-------------|:--------------:|--------------:|
| 1            | 2              | 3             |
| 10           | 20             | 30            |
| 100          | 200            | 300           |

## Nested Lists

Here is a list with mixed ordered and unordered items.

1. First ordered item
   - An unordered sub-item
   - Another unordered sub-item
2. Second ordered item
   1. A nested ordered sub-item
   2. Another nested ordered sub-item

## Footnotes

Here is a footnote[^1]. And another one[^2].

[^1]: This is the first footnote.
[^2]: This is the second footnote.

## Mathematical Equations

Here is an inline equation: $E = mc^2$.

And here is a block equation:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
