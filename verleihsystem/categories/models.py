from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Generic category with unlimited nesting.

    The tree of categories is stored as a nested set. The technique used by
    django-mptt for storing the hirarchical data is called Modified Preorder
    Tree Traversal.

        "The aim is to make retrieval operations very efficient."

    See http://django-mptt.github.com/django-mptt/ for more info and details.
    """
    CONTACT_GROUP = getattr(settings, 'CATEGORY_CONTACT_GROUP', 'Contact')

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    path = models.TextField(db_index=True, unique=True, blank=True)
    contact = models.ForeignKey(User, blank=True, null=True, 
        on_delete=models.SET_NULL, 
        limit_choices_to={'groups__name' : CONTACT_GROUP})
    parent = TreeForeignKey('self', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")

    class MPTTMeta:
        # Order the nodes by name
        order_insertion_by = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        """
        Denormalizes the path of a category on save since this is a expensive
        operation and makes lookups a lot easier.
        """
        # Save the category first, since we need an instance for retrieving
        # all the ancestors.
        super(Category, self).save(*args, **kwargs)

        # Denormalize path and save category
        ancestors = self.get_ancestors()
        slugs = [a.slug for a in ancestors]
        slugs += [self.slug]
        self.path = '/'.join(slugs) + '/'
        super(Category, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('category_detail', (), {'path': self.path})

    def get_contact_person(self):
        """
        Traverses all the ancestors and returns a valid administrator if no
        contact is directly assigned.
        """
        user_id = self.contact_id
        if not user_id:
            for c in self.get_ancestors(True):
                if c.contact_id != None:
                    user_id = c.contact_id
                    break
        user = User.objects.get(id=user_id)
        return user
