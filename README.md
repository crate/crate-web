# crate-web

This is the content repository for the [crate.io](https://crate.io) website.

The content is built into a static website using the static website generator
tool [Cactus](https://github.com/koenbok/Cactus).

The build tool can be found in the repo [crate/crate-cactus](https://github.com/crate/crate-cactus).

**Happy writing!**


## Plugins

The `crate-web` Cactus site contains following plugins:

* `collection.py`
* `events.py`

### Collection

Collections are groups of pages within a certain common path,
e.g. the blog collection is located in `./pages/blog`.

Collections are configured in the `config.json`. Collection objects must contain
following key-value pairs: `title` (name of the collection), `path` (directory
in which pages for this collection are located), `template` (default template for
pages).
The `order` object is optional and must contain `key` or `file` and `reverse` if present,
where `key` is the header after which should be sorted.  
The `toc` attribute receives an absolute or relative file path to a file that
contains the table of contents (toc). The order of the sites is defined as they
are listed in the toc-file.

`doc/toc`
```
index.html
docs/faq.html
docs/clients.html
```

`config.json`
```json
{
  ...
  "collections": {
    "blog": {
      "title": "Blog",
      "path": "blog/",
      "template": "post.html",
      "order": {
        "key": "date",
        "reverse": true
      }
    },
    "doc": {
      "title": "Doc",
      "path": "doc/",
      "template": "doc.html",
      "order": {
        "toc": "doc/toc",
      }
    }
  },
  ...
}
```

The key of the collection object defines the name under which the collection
can be accessed inside the page templates:

```html
{% for page in blog.pages %}
<div><h2>{{ page.title }}</h2></div>
{% endfor %}
```

### Events

Provides information about upcoming and past events.
Event pages can be edited as simple Markdown files.


### Interactive console

To embed the interactive console into a page you have to declare several
parameters in the metadata section of your `.html` site.

```html
console: true
consolequery: select * from sys.cluster
```

Embed this in your page context and assign the metadata-variable to the `query`
template variable:

```html
{% include "includes/interactive_console.html" with query=consolequery %}
```