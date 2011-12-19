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

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    slug = models.SlugField(max_length=50, verbose_name=_("Slug"),
        help_text=_("A slug is a user- and SEO-friendly short text used in a "
            "URL to identify and describe a resource"))
    path = models.CharField(max_length=255, db_index=True, unique=True, blank=True)
    contact = models.ForeignKey(User, blank=True, null=True, 
        on_delete=models.SET_NULL, verbose_name=_("Contact"),
        limit_choices_to={'groups__name' : CONTACT_GROUP})
    parent = TreeForeignKey('self', blank=True, null=True,
        verbose_name=_("Parent"))

    # Cache for storing the denormalized path
    _denormalized_path = None

    class Meta:
        ordering = ['name']
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")

    class MPTTMeta:
        # Order the nodes on insert by name
        order_insertion_by = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_denormalized_path(self):
        """
        Returns the denormalized path of a category.

        This method must not be called on a unsaved object. The result of the
        denormalized path is cached.
        """
        if not self._denormalized_path:
            ancestors = self.get_ancestors()
            slugs = [a.slug for a in ancestors] + [self.slug]
            self._denormalized_path = '/'.join(slugs) + '/'
        return self._denormalized_path

    def update_path(self):
        """
        Update the path attribute of a category.
        """
        self.path = self.get_denormalized_path()
        self.save()

    def save(self, *args, **kwargs):
        """
        Denormalizes the path of a category on save since this is a expensive
        operation and makes lookups a lot easier.
        """
        # Save the category first, since we need an instance for retrieving
        # all the ancestors.
        super(Category, self).save(*args, **kwargs)

        denormalized_path = self.get_denormalized_path()

        # Denormalize paths if category was moved
        if self.path != denormalized_path:
            self.path = denormalized_path
            super(Category, self).save(*args, **kwargs)
            descendants = self.get_descendants()
            [d.update_path() for d in descendants]

        # Normalize path of descendants
        descendants = self.get_descendants()

    @models.permalink
    def get_absolute_url(self):
        """
        Return the absolute path of a category.
        """
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
