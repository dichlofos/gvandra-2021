The cells of pipe tables cannot contain block elements like paragraphs and lists, and cannot span multiple lines. If a pipe table contains a row whose Markdown content is wider than the column width (see --columns), then the table will take up the full text width and the cell contents will wrap, with the relative cell widths determined by the number of dashes in the line separating the table header from the table body. (For example ---|- would make the first column 3/4 and the second column 1/4 of the full text width.) On the other hand, if no lines are wider than column width, then cell contents will not be wrapped, and the cells will be sized to their contents.

Note: pandoc also recognizes pipe tables of the following form, as can be produced by Emacs’ orgtbl-mode:

| One | Two   |
|-----+-------|
| my  | table |
| is  | nice  |


| One | Two   |
|-----+----------------------------|
| is  | nice  |
| my  | table more lorem ipsum text table more lorem ipsum texttable more lorem ipsum text table more lorem ipsum texttable more lorem ipsum texttable more lorem ipsum texttable more lorem ipsum texttable more lorem ipsum text |
| is  | nice  |
| my  | table more lorem ipsum text table more lorem ipsum texttable more lorem ipsum text table more lorem ipsum texttable more lorem ipsum texttable more lorem ipsum texttable more lorem ipsum texttable more lorem ipsum text |


The difference is that + is used instead of |. Other orgtbl features are not supported. In particular, to get non-default column alignment, you’ll need to add colons as above.
