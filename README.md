Confluence Publisher
====================

I've been using this to update some reports in Confluence recently and I don't
want to keep it in Errata Tool's main repo because it doesn't really belong
there, and also because it might be useful separately to others.

Example Usage
=============

Note that only kerberos authentication is supported currently.

In your own python script:

````
from confluence_publish import ConfluenceSession, ConfluencePage

ConfluenceSession("https://confluence.example.com")
page = ConfluencePage(space_key="ABC", page_title="My Page")

print(page)
page.update_page_body("Hello there!")

# We can also list child pages
for child in page.get_child_pages():
    print(child)
````

As a command line tool:

````
./confluence-publish \
  --jira=https://docs.engineering.redhat.com \
  --space-key=SOMEKEY \
  --page-title="My Page Title" \
  --content=path/to/newcontent.html
````

Author
======

Simon Baird <<sbaird@redhat.com>>

See Also
========

* [Confluence Python API][confluence-api]

...which I didn't know about when starting on this. Perhaps it would have been
a viable alternative.

[confluence-api]: https://github.com/pycontribs/confluence
