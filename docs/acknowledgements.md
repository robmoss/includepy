---
icon: lucide/thumbs-up
---

# Acknowledgements

I was motivated to write this extension because I have found the [literalinclude](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude) directive and [pyobject](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-option-literalinclude-pyobject) option to be extremely useful when using [Sphinx](https://www.sphinx-doc.org/) to write documentation for Python packages.
I'm now using [Zensical](https://zensical.org/) for most of my new projects, and wanted a similar feature.

The [snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/) extension comes close to meeting my needs, but I didn't want to add snippet markers to my source code.
However, I found this extension to be a useful reference for understanding how [Python-Markdown](https://python-markdown.github.io/) preprocessors actually work.
It also provides many features that are well beyond the scope of `includepy`.

The [mkdocs_graphviz](https://github.com/EastSunrise/mkdocs-graphviz) extension inspired me to allow the user to adjust the extension priority, in case the default value happens to cause issues with other extensions.
