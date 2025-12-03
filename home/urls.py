from .views import *
from .api import *

from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('services', services, name='services'),
    path('service_details/<int:id>/', service_details, name='service_details'),
    path('category_services/<int:id>/', category_services, name='category_services'),
    path('projects', projects, name='projects'),
    path('project_details/<int:id>/', project_details, name='project_details'),
    path('products', products, name='products'),
    path('product_details/<int:id>/', product_details, name='product_details'),
    path('team', team, name='team'),
    path('team_details/<int:id>/', team_details, name='team_details'),
    path('blog', blog, name='blog'),
    path('blog_details/<int:id>/', blog_details, name='blog_details'),
    path('category_events/<int:id>/', category_events, name='category_events'),
    path('cart', cart, name='cart'),
    path('my-likes', my_likes, name='my_likes'),
    path('faq', faq, name='faq'),
    path('search', search, name='search'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('email-verification/', email_verification_view, name='email_verification'),
    path('logout', logout_view, name='logout'),
    path('checkout', checkout, name='checkout'),
    
    # PASSWORD RESET URLs
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-verify/', password_reset_verify, name='password_reset_verify'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    # api paths can be added here as needed
    path('api/user/<int:product_id>/likes/', user_product_like_api, name='user_product_like_api'),
    path('api/user/<int:product_id>/like/add', user_like_add_api, name='user_like_add_api'),
    path('api/user/<int:product_id>/cart/', cart_api, name='cart_api'),
    path('api/user/<int:product_id>/cart/add', add_to_cart_api, name='add_to_cart_api'),
    path('api/cart/count/', cart_count_api, name='cart_count_api'),
    path('api/likes/count/', likes_count_api, name='likes_count_api'),
    
    # CART MANAGEMENT API'LAR
    path('api/cart/remove/<int:cart_id>/', remove_from_cart_api, name='remove_from_cart_api'),
    path('api/cart/update/<int:cart_id>/', update_cart_quantity_api, name='update_cart_quantity_api'),
    path('api/cart/increase/<int:cart_id>/', increase_cart_quantity_api, name='increase_cart_quantity_api'),
    path('api/cart/decrease/<int:cart_id>/', decrease_cart_quantity_api, name='decrease_cart_quantity_api'),
    path('api/cart/clear/', clear_cart_api, name='clear_cart_api'),

    # CHAT API'LAR
    path('api/chat/init/', chat_init, name='chat_init'),
    path('api/chat/send/', chat_send_message, name='chat_send_message'),
    path('api/chat/messages/<str:session_token>/', chat_get_messages, name='chat_get_messages'),
    path('api/chat/admin/reply/', chat_admin_reply, name='chat_admin_reply'),
]
