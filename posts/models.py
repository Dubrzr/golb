import diff_match_patch
from colorful.fields import RGBColorField
from django.db import models
from blog.models import User



class History(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True)
    patch = models.TextField()
    author = models.ForeignKey(User)

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

    def get_contents(self, base):
        contents = base
        parent = self.parent
        patch = self.patch
        dmp = diff_match_patch.diff_match_patch()
        while parent:
            patchs = dmp.patch_fromText(patch)
            contents = dmp.patch_apply(patchs, contents)[0]
            parent = parent.parent
            patch = parent.patch


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    color = RGBColorField()


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    contents = models.TextField()
    history = models.ForeignKey(History, null=True)
    authors = models.ManyToManyField(User)
    tags = models.ManyToManyField(Tag)
    LANGUAGES_CHOICES = (
        ('FR', 'Français'),
        ('EN', 'English'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGES_CHOICES)

    def update_contents(self, author, new_contents):
        dmp = diff_match_patch.diff_match_patch()
        dmp.Diff_Timeout = 0
        patchs = dmp.patch_make(new_contents, self.contents)
        patch = dmp.patch_toText(patchs)
        new_history = History(patch, author, self.history)
        new_history.save()
        self.history = new_history
        for user in new_history.get_authors():
            self.authors.add(user)
        self.save()

    def created_by(self):
        history = self.history
        while history:
            if history.parent is None:
                return history.author
            history = history.parent

    def last_modified_by(self):
        return self.history.author