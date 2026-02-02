from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Property


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        qs = Property.objects.filter(is_sold=False).prefetch_related('images').order_by('-is_featured', '-created_at')
        
        property_type = self.request.GET.get('type')
        if property_type:
            qs = qs.filter(property_type=property_type)
        
        min_price = self.request.GET.get('min_price')
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass
        
        max_price = self.request.GET.get('max_price')
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        bedrooms = self.request.GET.get('bedrooms')
        if bedrooms:
            try:
                qs = qs.filter(bedrooms__gte=int(bedrooms))
            except ValueError:
                pass
        
        location = self.request.GET.get('location')
        if location:
            qs = qs.filter(location__icontains=location)
        
        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(translations__title__icontains=search) |
                Q(translations__short_description__icontains=search) |
                Q(location__icontains=search)
            )
        
        return qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_types'] = Property.PROPERTY_TYPE_CHOICES
        context['current_type'] = self.request.GET.get('type', '')
        context['current_min_price'] = self.request.GET.get('min_price', '')
        context['current_max_price'] = self.request.GET.get('max_price', '')
        context['current_bedrooms'] = self.request.GET.get('bedrooms', '')
        context['current_location'] = self.request.GET.get('location', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        locations = Property.objects.filter(is_sold=False).values_list('location', flat=True).distinct()
        context['available_locations'] = sorted(set(locations))
        
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'
    
    def get_queryset(self):
        return Property.objects.prefetch_related('images').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_properties'] = Property.objects.filter(
            property_type=self.object.property_type,
            is_sold=False
        ).exclude(id=self.object.id).prefetch_related('images')[:3]
        return context
