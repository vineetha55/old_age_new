from django.urls import path
import oldd.views

urlpatterns = [
    path('',oldd.views.home,name='home'),
    path('home', oldd.views.home, name='home'),
    path('register', oldd.views.register, name='register'),
    path('login', oldd.views.login, name='login'),
    path('admin_home', oldd.views.admin_home, name='admin_home'),
    path('upd_pr_adm', oldd.views.upd_pr_adm, name='upd_pr_adm'),
    path('logout', oldd.views.logout, name='logout'),
    path('about_us', oldd.views.about_us, name='about_us'),
    path('about_us_admin', oldd.views.about_us_admin, name='about_us_admin'),
    path('new_arrivals', oldd.views.new_arrivals, name='new_arrivals'),
    path('daily_needs', oldd.views.daily_needs, name='daily_needs'),

    path('cat_admin', oldd.views.cat_admin, name='cat_admin'),
    path('add_cat_admin', oldd.views.add_cat_admin, name='add_cat_admin'),
    path('edit_cat_admin/<id>', oldd.views.edit_cat_admin, name='edit_cat_admin'),
    path('delete_cat_admin/<id>', oldd.views.delete_cat_admin, name='delete_cat_admin'),

    path('cat_product_admin/<id>', oldd.views.cat_product_admin, name='cat_product_admin'),
    path('add_prod_adm', oldd.views.add_prod_adm, name='add_prod_adm'),
    path('edit_prod_adm/<id>', oldd.views.edit_prod_adm, name='edit_prod_adm'),
    path('delete_prod_adm/<id>', oldd.views.delete_prod_adm, name='delete_prod_adm'),

    path('product_view/<id>', oldd.views.product_view, name='product_view'),
    path('surgical_view', oldd.views.surgical_view, name='surgical_view'),

    path('syrin_disp', oldd.views.syrin_disp, name='syrin_disp'),
    path('belts_and_supports', oldd.views.belts_and_supports, name='belts_and_supports'),
    path('supports_products', oldd.views.supports_products, name='supports_products'),
    path('gloves', oldd.views.gloves, name='gloves'),
    path('dressings_and_bandaids', oldd.views.dressings_and_bandaids, name='dressings_and_bandaids'),
    path('hot_water_bags', oldd.views.hot_water_bags, name='hot_water_bags'),
    path('thermometers', oldd.views.thermometers, name='thermometers'),
    path('stethescopes', oldd.views.stethescopes, name='stethescopes'),
    path('nebulizers', oldd.views.nebulizers, name='nebulizers'),
    path('bp_apparatus', oldd.views.bp_apparatus, name='bp_apparatus'),
    path('diapers', oldd.views.diapers, name='diapers'),
    path('hygiene_products', oldd.views.hygiene_products, name='hygiene_products'),
    path('new_mother_and_baby_products', oldd.views.new_mother_and_baby_products, name='new_mother_and_baby_products'),
    path('masks', oldd.views.masks, name='masks'),
    path('vaporizers', oldd.views.vaporizers, name='vaporizers'),
    path('cotton', oldd.views.cotton, name='cotton'),
    path('beauty_products', oldd.views.beauty_products, name='beauty_products'),
    path('other_products', oldd.views.other_products, name='other_products'),
]