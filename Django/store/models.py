from django.db import models
from images.models import Image
import os

class BaseModel(models.Model):
    name = models.CharField(max_length=30)
    render_name = models.CharField(max_length=30)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.render_name

class Subdirectory(models.Model):
    name = models.CharField(max_length=30)
    render_name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
class Catalog(BaseModel):
    subdirectories = models.ManyToManyField(Subdirectory, blank=True)  
    def get_cells(self): # getting cells for page rendering
        return {"name": self.name, 
                "render_name": self.render_name,
                "image":"/media/images/" + os.path.basename(str(self.image)),
                "subdirectories": self.subdirectories.all(),
                }

class Product(models.Model):
    render_name = models.CharField(max_length=30)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    subdirectories = models.ManyToManyField(Subdirectory, blank=True) 
    price = models.IntegerField() # number
    price_render = models.CharField(max_length=30) 
    about_product = models.TextField(blank=True) # html content
    character = models.TextField(blank=True) # html content
    images = models.ManyToManyField(Image, related_name='main_slider+', blank=True) # first image - main image
    additional_images = models.ManyToManyField(Image, related_name='last_slider+', blank=True) # image list
    available = models.BooleanField(default=True)
    def get_cells(self): # getting cells for page rendering
        return {"name": self.render_name, 
                "catalog": self.catalog,
                "subdirectories": [ sub.name for sub in list(self.subdirectories.all())],
                "price": self.price,
                "about_product": self.about_product,
                "character": self.character,
                "images": [ "/media/images/" + os.path.basename(str(image.image.url)) for image in list(self.images.all())],
                "additional_images": [ "/media/images/" + os.path.basename(str(image.image.url)) for image in list(self.additional_images.all())],
                "price_render":  self.price_render
                }
    def __str__(self):
        return self.render_name

class Service(BaseModel):
    service_description = models.TextField(blank=True) # html content
    mini_description = models.TextField(blank=True) # text
    def get_cells(self): # getting cells for page rendering
        return {"name": self.name, 
                "image": self.image.image.url,
                "render_name": self.render_name,
                "service_description": self.service_description,
                "mini_description": self.mini_description,
                }
