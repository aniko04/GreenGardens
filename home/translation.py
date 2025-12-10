from modeltranslation.translator import register, TranslationOptions
from .models import (
    MainInfo, SocialLink, Mainslider, IntroOurCompany, MainFeature,
    OurService, ServiceCategory, OurWorkProcess, OurTestimonial,
    OurProject, OurFact, OurBenefit, OurBlog, Category, OurExpert,
    FAQ, Product
)


@register(MainInfo)
class MainInfoTranslationOptions(TranslationOptions):
    fields = ('site_name', 'address', 'description', 'footer_text', 'opening_hours')


@register(SocialLink)
class SocialLinkTranslationOptions(TranslationOptions):
    fields = ('platform',)


@register(Mainslider)
class MainsliderTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'button_1_name', 'button_2_name')


@register(IntroOurCompany)
class IntroOurCompanyTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'icon_text1', 'icon_text2',
              'list1', 'list2', 'list3', 'button_name')


@register(MainFeature)
class MainFeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(OurService)
class OurServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'pagename')


@register(ServiceCategory)
class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(OurWorkProcess)
class OurWorkProcessTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'pagename', 'page_text')


@register(OurTestimonial)
class OurTestimonialTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'name', 'position', 'feedback')


@register(OurProject)
class OurProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'content', 'category',
              'project_name', 'button_name')


@register(OurFact)
class OurFactTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'project_content',
              'customer_content', 'button_name', 'button_text')


@register(OurBenefit)
class OurBenefitTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'benefit1', 'benefit1_text',
              'benefit1_quality1', 'benefit1_quality2', 'benefit1_quality3',
              'benefit1_quality4', 'benefit2', 'benefit2_text', 'client_text')


@register(OurBlog)
class OurBlogTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'minititle', 'content', 'author')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(OurExpert)
class OurExpertTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'name', 'position', 'bio')


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'mini_description', 'description', 'specifications', 'status')
