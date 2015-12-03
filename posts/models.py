import diff_match_patch

from django.db import models
from blog.models import User



class History(models.Model):
    parent = models.ForeignKey('self', null=True)
    patch = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, patch, author, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patch = patch
        self.author = author
        if parent:
            self.parent = parent

    def __str__(self):
        return ''

    def get_authors(self):
        authors_ids = [self.author.id]
        authors = [self.author]
        if self.parent:
            parent_authors = self.parent.get_authors()
            for author in parent_authors:
                if not author.id in authors_ids:
                    authors_ids.append(author.id)
                    authors.append(author)
        return authors



class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    contents = models.TextField()
    history = models.ForeignKey(History, null=True)
    authors = models.ManyToManyField(User)

    def update_contents(self, author, new_contents):
        dmp = diff_match_patch.diff_match_patch()
        dmp.Diff_Timeout = 0
        # Create a patch
        patchs = dmp.patch_make(new_contents, self.contents)
        patch = dmp.patch_toText(patchs)
        new_history = History(patch, author, self.history)
        new_history.save()
        self.history = new_history
        for user in new_history.get_authors():
            self.authors.add(user)
        self.save()
