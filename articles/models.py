import diff_match_patch
from colorful.fields import RGBColorField

from django.db import models

from blog.utils import html2text
from users.models import User



class History(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True)
    patch = models.TextField()
    patch_reverse = models.TextField()
    author = models.ForeignKey(User)

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

    def get_contents(self):
        history = [self]
        h = self.parent
        while h:
            history.insert(0, h)
            h = h.parent
        dmp = diff_match_patch.diff_match_patch()
        dmp.Diff_Timeout = 0
        contents = ""
        for h in history:
            patchs = dmp.patch_fromText(h.patch_reverse)
            contents = dmp.patch_apply(patchs, contents)[0]
        return contents


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    color = RGBColorField()


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    contents = models.TextField()
    contents_text = models.TextField()
    history = models.ForeignKey(History, null=True, on_delete=models.CASCADE,)
    authors = models.ManyToManyField(User)
    tags = models.ManyToManyField(Tag)
    LANGUAGES_CHOICES = (
        ('FR', 'Français'),
        ('EN', 'English'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGES_CHOICES)
    STATE_CHOICES = (
        ('PU', 'Published'),
        ('DR', 'Draft'),
        ('DE', 'Removed'),
        ('RE', 'Review'),
    )
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='DR')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def update_contents(self, author, new_contents):
        dmp = diff_match_patch.diff_match_patch()
        dmp.Diff_Timeout = 0
        patchs = dmp.patch_make(new_contents, self.contents)
        if patchs == []:
            return
        patchs_reverse = dmp.patch_make(self.contents, new_contents)
        patch = dmp.patch_toText(patchs)
        patch_reverse = dmp.patch_toText(patchs_reverse)
        new_history = History(patch=patch,
                              patch_reverse=patch_reverse,
                              author=author,
                              parent=self.history)
        new_history.save()
        self.history = new_history
        self.authors.add(author)
        self.contents = new_contents
        self.contents_text = html2text(new_contents)
        self.save()

    def created_by(self):
        if self.history:
            history = self.history
            while history:
                if history.parent is None:
                    return history.author
                history = history.parent

    def last_modified_by(self):
        if self.history:
            return self.history.author
