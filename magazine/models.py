from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    # Predefined category choices
    class CategoryType(models.TextChoices):
        TECHNOLOGY = 'technology', 'Technology'
        LIFESTYLE = 'lifestyle', 'Lifestyle'
        HEALTH = 'health', 'Health & Wellness'
        BUSINESS = 'business', 'Business'
        EDUCATION = 'education', 'Education'
        TRAVEL = 'travel', 'Travel'
        FOOD = 'food_cooking', 'Food & Cooking'
        SPORTS = 'sports', 'Sports'
        ENTERTAINMENT = 'entainment', 'Entertainment'
        OTHER = 'other', 'Other'
    
    name = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        unique=True,
        default=CategoryType.OTHER
    )
    
    def __str__(self):
        return self.get_name_display()
    

def get_other_category():
    from .models import Category  # Import inside function to avoid circular import
    other, created = Category.objects.get_or_create(name='other')
    return other.pk

class Magazine(models.Model):
    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='magazines')
    title=models.CharField(max_length=100)
    content=models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_DEFAULT, 
        default=get_other_category,
        related_name='magazines'  # Allows Category.magazines.all()
    )
    image=models.ImageField(upload_to='media/magazine_images/',blank=True,null=True)
    created_at=models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the initial slug
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
                
            # Check if slug exists and add number if needed
            while Magazine.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    