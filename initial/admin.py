from django.contrib import admin
from .models import Product,Order, OrderItem
# Register your models here.
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'created_at', 'is_ordered','user']
    inlines = [OrderItemInline]

    def user_name(self, obj):
        return obj.user.username if obj.user else "Anonymous"

    user_name.admin_order_field = 'user__username'  # Enable sorting by username

    user_name.short_description = 'User Name'  # Customize column header

    # Customize fieldsets to show the user's name
    fieldsets = (
        (None, {
            'fields': ('id', 'user_name', 'created_at', 'is_ordered')
        }),
    )

    def get_inline_instances(self, request, obj=None):
        """
        Override to display only order items of the specific order.
        """
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        return []

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity','created_at','user']  # Add product_name to list display

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Product Name'  # Customize column header