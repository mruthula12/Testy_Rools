from django.urls import path
import kfd.views

urlpatterns = [
    path('', kfd.views.home, name='index'),
    path('index', kfd.views.home, name='index'),

    path('register_admin',kfd.views.register_admin,name='register_admin'),
    path('register_custmer',kfd.views.register_custmer,name='register_custmer'),
    path('register_supplier', kfd.views.register_supplier, name='register_supplier'),

    path('login',kfd.views.login,name='login'),
    path('logout', kfd.views.logout, name='logout'),

    path('customer_home',kfd.views.customer_home,name='customer_home'),
    path('admin_home',kfd.views.admin_home,name = 'admin_home'),
    path('supplier_home', kfd.views.supplier_home, name='supplier_home'),
    path('iteams', kfd.views.iteams, name='iteams'),
    path('edit_product_adm/<int:id>/', kfd.views.edit_product_adm, name='edit_product_adm'),
    path('delete_product_adm/<int:id>/', kfd.views.delete_product_adm, name='delete_product_adm'),
    path('add_product_adm', kfd.views.add_product_adm, name='add_product_adm'),

    path('custmer_cart', kfd.views.custmer_cart, name='custmer_cart'),
    path('add_to_cart/<int:product_id>', kfd.views.add_to_cart, name='add_to_cart'),
    path('update_cart_decr_ajax/', kfd.views.update_cart_decr_ajax, name='update_cart_decr_ajax'),
    path('update_cart_incr_ajax/', kfd.views.update_cart_incr_ajax, name='update_cart_incr_ajax'),
    path('remove_from_cart/<int:item_id>/', kfd.views.remove_from_cart, name='remove_from_cart'),

    path('del_addr_cust/<id>', kfd.views.del_addr_cust, name='del_addr_cust'),
    path('edit_addr_cust/<id>', kfd.views.edit_addr_cust, name='edit_addr_cust'),

    path('checkout/', kfd.views.checkout, name='checkout'),
    path('contact_mail',kfd.views.contact_mail, name='contact_mail'),
    path('orders_customer',kfd.views.orders_customer, name='orders_customer'),
    path('custmer_order_adm', kfd.views.custmer_order_adm, name='custmer_order_adm'),
    path('approve_order/<int:order_id>/',kfd.views.approve_order, name='approve_order'),
    path('prepare-order/<int:order_id>/', kfd.views.prepare_order, name='prepare_order'),
    path('delivery_partner_arrived/<int:order_id>/',kfd.views.delivery_partner_arrived, name='delivery_partner_arrived'),
    path('deliver_order/<int:order_id>/',kfd.views.deliver_order, name='deliver_order'),
    path('approve_order/<int:order_id>/',kfd.views.approve_order, name='approve_order'),

    path('update-status/', kfd.views.update_status, name='update-status'),
    path('delete_suppl_stats_adm/<id>', kfd.views.delete_suppl_stats_adm, name='delete_suppl_stats_adm'),
    path('supplier_detail/',kfd.views.supplier_details, name='supplier_detail'),

    path('save-location/',kfd.views.save_location, name='save-location'),
    path('assign_delivery_boy/<int:order_id>/', kfd.views.assign_delivary_boy, name='assign_delivary_boy'),
    path('supplier_assigned_orders/', kfd.views.supplier_assigned_orders, name='supplier_assigned_orders'),
    path('update_order_status/',kfd.views.update_order_status, name='update_order_status'),
    path('track_order_adm/<int:order_id>/', kfd.views.track_order_adm, name='track_order_adm'),
    path('purchase_history_customer',kfd.views.purchase_history_customer, name='purchase_history_customer'),
    path('update-delivery-boy-location/', kfd.views.update_supplier_location, name='update-delivery-boy-location'),
    path('track-supplier/<int:checkout_id>/',kfd.views.track_supplier, name='track_supplier'),
    path('checkout_new_adr', kfd.views.checkout_new_adr, name='checkout_new_adr'),
    path('check_total_amount/', kfd.views.check_total_amount, name='check_total_amount'),
]