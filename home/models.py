from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from datetime import date
from django.urls import reverse
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]




