from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils import translation
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from parler.models import TranslatableModel, TranslatedFields


@python_2_unicode_compatible
class Article(TranslatableModel):
    """
    Example translatable model.
    """

    # The translated fields:
    translations = TranslatedFields(
        title = models.CharField("Title", max_length=200),
        slug = models.SlugField("Slug", unique=True),
        content = models.TextField()
    )

    # Regular fields
    published = models.BooleanField("Is published", default=False)
    category = models.ForeignKey("Category", null=True, blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        # Fetching the title just works, as all
        # attributes are proxied to the translated model.
        # Fallbacks are handled as well.
        return "{0}".format(self.title)

    def get_absolute_url(self):
        # The override is only needed because we use the /##/ prefix by i18n_patterns()
        # If the language is part of the URL parameters, you can pass it directly off course.
        with translation.override(self.get_current_language()):
            return reverse('article-details', kwargs={'slug': self.slug})

    def get_all_slugs(self):
        # Example illustration, how to fetch all slugs in a single query:
        return dict(self.translations.values_list('language_code', 'slug'))


@python_2_unicode_compatible
class Category(models.Model):
    """
    Example model for inline edition of Articles
    """

    name = models.CharField("Name", max_length=200)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        # Fetching the title just works, as all
        # attributes are proxied to the translated model.
        # Fallbacks are handled as well.
        return "{0}".format(self.name)


class StackedCategory(Category):

    class Meta:
        verbose_name = "Stacked Category"
        verbose_name_plural = "Stacked Categories"
        proxy = True


class TabularCategory(Category):

    class Meta:
        verbose_name = "Tabular Category"
        verbose_name_plural = "Tabular Categories"
        proxy = True
