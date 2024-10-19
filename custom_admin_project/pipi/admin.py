from django.contrib import admin
from .models import YourModel, ExtraField, ImageField, Accordion, AccordionItem
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
import json

class ExtraFieldInline(admin.TabularInline):
    model = ExtraField
    extra = 1  # Display at least 1 extra field by default

class YourModelAdmin(admin.ModelAdmin):
    change_form_template = 'admin/pipi/change_form.html'
    exclude = ['customer', 'status']

    def get_form(self, request, obj=None, **kwargs):
        # Get the form from the default get_form
        form = super().get_form(request, obj, **kwargs)

        # Add the enctype attribute to the form
        form.enctype = 'multipart/form-data'
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Clear previous data
        ExtraField.objects.filter(your_model=obj).delete()
        ImageField.objects.filter(your_model=obj).delete()
        Accordion.objects.filter(your_model=obj).delete()

        images_data = request.session.get('images_data', [])

        # Now you have access to the images data and can process it
        if images_data:
            print(1)
            for image_data in images_data:
                print(f"Image URL: {image_data['image_url']}, Index: {image_data['index']}, Section: {image_data['section']}")

        combined_data = []
        # Save fields, images, and accordions
        for key in request.POST:
            if key.startswith('rich_text_content'):
                index = key.split('_')[-2]
                section = key.split('_')[-1]
                a = request.POST.get(f'rich_text_content_{index}_{section}', '')
                combined_data.append({
                    'type': 'field',
                    'index': index,
                    'section': section,
                    'value': a.replace('"', '&quot;')
                })

                ExtraField.objects.create(your_model=obj, field_value=combined_data[-1])  

            elif key.startswith(f'ac_description_'):
                index = key.split('_')[-3]
                section = key.split('_')[-2]

                if not Accordion.objects.filter(your_model=obj, index=index, section=section).exists():
                    accordion = Accordion.objects.create(your_model=obj, index=index, section=section)
                    for item in request.POST:
                        if item.startswith(f'ac_description_{index}_{section}_'):
                            itemCount = item.split('_')[-1]
                            description = request.POST.get(f'ac_description_{index}_{section}_{itemCount}')
                            contents = request.POST.get(f'ac_content_{index}_{section}_{itemCount}')
                            AccordionItem.objects.create(accordion=accordion, description=description, content=contents)

            elif key.startswith(f'dynamic_images_'):
                index = key.split('_')[-2]
                section = key.split('_')[-1]

                b = False

                if b:
                    for key, image_file in request.FILES.items():
                        if key.startswith(f'dynamic_images_{index}_{section}'):
                            ImageField.objects.create(your_model=obj, image=image_file, index=index, section=section)
                else:
                    for image_data in images_data:
                        if image_data['index'] == index and image_data['section'] == section:
                            ImageField.objects.create(your_model=obj, image=image_data['image_url'].replace('media/', '', 1), index=image_data['index'], section=image_data['section'])
                                    


        for key, image_file in request.FILES.items():
            if key.startswith('dynamic_images'):
                index = key.split('_')[-2]
                section = key.split('_')[-1]
                ImageField.objects.create(your_model=obj, image=image_file, index=index, section=section)



        # Optionally: sorting logic based on `index`


    def change_view(self, request, object_id, form_url='', extra_context=None):
        instance = get_object_or_404(YourModel, id=object_id)
        extra_fields_queryset = ExtraField.objects.filter(your_model=instance)
        images_queryset = ImageField.objects.filter(your_model=instance)
        accordions_queryset = Accordion.objects.filter(your_model=instance).prefetch_related('items')


        images_data = [
            {
                'id': image.id,
                'image_url': image.image.url,
                'index': image.index,
                'section': image.section
            }
            for image in images_queryset
        ]

        request.session['images_data'] = images_data

        combined = []

        # Add extra fields data
        for extra_field in extra_fields_queryset:
            try:
                field_value = json.loads(extra_field.field_value.replace("'", '"'))

                combined.append({
                    'type': field_value.get('type'),
                    'index': field_value.get('index'),  # Use existing index from field_value
                    'section': field_value.get('section'),
                    'value': field_value.get('value')
                })
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON for field {extra_field.id}")

        # Add images data
        for image in images_queryset:
            combined.append({
                'type': 'image',
                'index': image.index,
                'section': image.section,
                'imageSrc': str(image.image.url)  # Image URL for display
            })

        # Add accordion data
        for accordion in accordions_queryset:
            items = []
            for item in accordion.items.all():
                items.append({'description': item.description, 'content': item.content})
            combined.append({
                'type': 'accordion',
                'index': accordion.index,
                'section': accordion.section,
                'items': items
            })


        combined.sort(key=lambda x: (int(x['section']), int(x['index'])))
        context = {'extra_fields': json.dumps(combined)}
        print(context)
        return super().change_view(request, object_id, form_url, extra_context=context)

from django.urls import path
from django.conf import settings
from django.http import HttpResponse
from django.template.response import TemplateResponse
import os
class FileBrowserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/file_browser.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('file_browser/', self.admin_site.admin_view(self.file_browser_view)),
        ]
        return custom_urls + urls

    def file_browser_view(self, request):
        file_list = []
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_list.append({
                    'file_name': file,
                    'file_url': os.path.join(settings.MEDIA_URL, os.path.relpath(os.path.join(root, file), media_root))
                })
        context = dict(
            self.admin_site.each_context(request),
            file_list=file_list,
        )
        return TemplateResponse(request, 'admin/file_browser.html', context)


admin.site.register(YourModel, YourModelAdmin)