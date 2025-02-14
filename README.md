# Django cursor pagination [![Build Status](https://travis-ci.org/photocrowd/django-cursor-pagination.svg?branch=master)](https://travis-ci.org/photocrowd/django-cursor-pagination)

A cursor based pagination system for Django. Instead of referring to specific
pages by number, we give every item in the QuerySet a cursor based on its
ordering values. We then ask for subsequent records by asking for records
*after* the cursor of the last item we currently have. Similarly we can ask for
records *before* the cursor of the first item to navigate back through the
list.

This approach has two major advantages over traditional pagination. Firstly, it
ensures that when new data is written into the table, records cannot be moved
onto the next page. Secondly, it is much faster to query against the database
as we are not using very large offset values.

There are some significant drawbacks over "traditional" pagination. The data
must be ordered by some database field(s) which are unique across all records.
A typical use case would be ordering by a creation timestamp and an id. It is
also more difficult to get the range of possible pages for the data.

The inspiration for this project is largely taken from [this
post](http://cra.mr/2011/03/08/building-cursors-for-the-disqus-api) by David
Cramer, and the connection spec for [Relay
GraphQL](https://facebook.github.io/relay/graphql/connections.htm). Much of the
implementation is inspired by [Django rest framework's Cursor
pagination.](https://github.com/tomchristie/django-rest-framework/blob/9b56dda91850a07cfaecbe972e0f586434b965c3/rest_framework/pagination.py#L407-L707).
The main difference between the Disqus approach and the one used here is that
we require the ordering to be totally determinate instead of using offsets.

## Installation

```bash
pip install django-cursor-pagination
```

## Usage

```python
from cursor_pagination import CursorPaginator

from myapp.models import Post


def posts_api(request, after=None):
    qs = Post.objects.all()
    page_size = 10
    paginator = CursorPaginator(qs, ordering=('-created', '-id'))
    page = paginator.page(first=page_size, after=after)
    data = {
        'objects': [serialize_post(post) for post in page],
        'has_next_page': page.has_next(),
        'after': page.after()
    }
    return data
```

Reverse pagination can be achieved by using the `last` and `before` arguments
to `paginator.page`.

## Caveats

- The ordering specified **must** uniquely identify the object.
- If a cursor is given and it does not refer to a valid object, the values of
  `has_previous` (for `after`) or `has_next` (for `before`) will always return
  `True`.
- `NULL` comes at the end in query results with `ORDER BY` both for `ASC` and `DESC`.

## Developing

1. clone this repo
1. install pre-commit.  If you have [mise](https://github.com/jdx/mise) you can install with `mise install`
1. `pre-commit install`

Now each change will be formatted with black.

## Running tests

```bash
docker compose up -d # start postgres server
poetry install # install django and postgres client
poetry run ./runtests.py
```
