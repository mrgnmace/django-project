from django.db import models

class YourModel(models.Model):
    customer = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    
class ExtraField(models.Model):
    your_model = models.ForeignKey(YourModel, related_name='extra_fields', on_delete=models.CASCADE)
    field_value = models.TextField()

    def __str__(self):
        return f"Extra field: {self.field_value}"
    
class ImageField(models.Model):
    your_model = models.ForeignKey(YourModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    index = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    def __str__(self):
        return f"Image field: {self.image}"
    
class Accordion(models.Model):
    your_model = models.ForeignKey(YourModel, related_name='accordions', on_delete=models.CASCADE)
    index = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    def __str__(self):
        return f"Accordion {self.index} in section {self.section}"

class AccordionItem(models.Model):
    accordion = models.ForeignKey(Accordion, related_name='items', on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True)
    content = models.TextField(default='', blank=True)

    def __str__(self):
        return f"Item in Accordion {self.accordion.id}"
    
class Cards(models.Model):
    your_model = models.ForeignKey(YourModel, related_name='cards', on_delete=models.CASCADE)
    index = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    def __str__(self):
        return f"Cards {self.index} in section {self.section}"
    
class CardItem(models.Model):
    cards = models.ForeignKey(Cards, related_name='cardItem', on_delete=models.CASCADE)
    previewIMage = models.ImageField(upload_to='cards_image_preview/')
    header = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    
class Quotes(models.Model):
    your_model = models.ForeignKey(YourModel, related_name='quotes', on_delete=models.CASCADE)
    index = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    def __str__(self):
        return f"Quotes {self.index} in section {self.section}"
    
class QuotesItem(models.Model):
    quote = models.ForeignKey(Quotes, related_name='quoteItem', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
