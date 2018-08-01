import json
from confluence_publish import ConfluenceSession

# Useful API examples:
#   https://developer.atlassian.com/server/confluence/confluence-rest-api-examples/

class ConfluencePage:
    def __init__(self, **kwargs):
        # Allow lazy reuse of an existing confluence session if the
        # caller doesn't provide a session
        self.session = kwargs.get('session', ConfluenceSession.session)
        if ConfluenceSession.session == None:
            raise ValueError('A session is required!')

        # For now we'll require that the space key is explicitly provided
        self.space_key = kwargs.get('space_key', None)
        if self.space_key == None:
            raise ValueError('A space_key is required!')

        # Read the rest of the args
        self.read_kwargs(kwargs)

        # If any of these values are not given then do a lookup to read them them up
        if None in [self.page_id, self.page_title, self.page_version]:
            self.get_info()

    def read_kwargs(self, kwargs):
        self.page_id = kwargs.get('page_id', None)
        self.page_title = kwargs.get('page_title', None)
        self.page_version = kwargs.get('page_version', None)
        self.page_body = kwargs.get('page_body', None)

    def info_from_result_hash(self, result_hash):
        return dict(
            page_id = result_hash['id'],
            page_title = result_hash['title'],
            page_version = result_hash['version']['number'],
            page_body = result_hash['body']['storage']['value'],
        )

    def get_info(self):
        if self.page_id:
            query = 'id=' + self.page_id
        elif self.page_title:
            query = 'title=' + self.page_title
        else:
            raise ValueError("You must specify a page_id or a page_title!")

        response = self.session.get('/rest/api/content?expand=version,body.storage&spaceKey=' + self.space_key + '&' + query)
        response.raise_for_status()
        result_hash = response.json()['results'][0]
        self.read_kwargs(self.info_from_result_hash(result_hash))

    def get_child_pages(self):
        response = self.session.get('/rest/api/content/search?expand=version,body.storage&cql=parent=' + self.page_id)
        response.raise_for_status()
        return [ConfluencePage(session=self.session, space_key=self.space_key, **self.info_from_result_hash(result)) for result in response.json()['results']]

    def update_page_body(self, new_body_content, new_page_title=None):
        response = self.session.put('/rest/api/content/' + self.page_id, {
            "id": self.page_id,
            "type": "page",
            "title": new_page_title if new_page_title else self.page_title,
            "space": { "key": self.space_key },
            "body": { "storage": { "value": new_body_content, "representation": "storage" } },
            "version": { "number": self.page_version + 1 }
        })
        response.raise_for_status()
        #print response.text

    def __str__(self):
        return "{} (ver {}) '{}'".format(self.page_id, self.page_version, self.page_title)
