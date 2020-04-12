from django.db import models        # needed for blog date"
from modelcluster.fields import ParentalKey        # needed for images
from modelcluster.contrib.taggit import ClusterTaggableManager        # needed for tagging, and next
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
        # inline added for  jpg  ;   MultiFieldPanel for combining date and tagging
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    author = models.ForeignKey(
        'auth.user',
        # on_delete=models.PROTECT       #   .SET_NULL,      #SINON TRY "=models.PROTECT"
        on_delete=models.CASCADE, null=True
    )


    def main_image(self):           # method
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

# here another unused model, but debugged ok, for introducing author field, I copy in BlogPage
class Post(models.Model) :
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.user',
        # on_delete=models.PROTECT       #   .SET_NULL,      #SINON TRY "=models.PROTECT"
        on_delete=models.CASCADE, null=True
    )
    body = models.TextField()

    def __str__(self) :
        return self.title

