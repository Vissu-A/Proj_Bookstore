from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget

from cuser.models import User
from cuser.forms import AdminUserChangeForm, AdminUserCreationForm


def make_inactive(self, request, queryset):
    updated = queryset.update(is_active=False)
    self.message_user(request, ngettext(
        " '"+str(updated)+"' user was successfully marked as inactive.",
        " '"+str(updated)+"' users were successfully marked as inactive.",
        updated
    ), messages.SUCCESS)
make_inactive.allowed_permissions = ('change',)                      # Setting permissions for actions
make_inactive.short_description = "Mark selected users as inactive"

def make_active(self, request, queryset):
    updated = queryset.update(is_active=True)
    self.message_user(request, ngettext(
        "%d user was successfully marked as active.",
        "%d users were successfully marked as active.",
        updated
    ), messages.SUCCESS)
make_active.allowed_permissions = ('change',)                         # Setting permissions for actions
make_active.short_description = "Mark selected users as active"


class MyUserAdmin(UserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
   
    formfield_overrides = {
        PhoneNumberField: {'widget': PhoneNumberPrefixWidget},
    }

    list_display = ['email', 'full_name', 'phone', 'email_verified', 'is_active', 'is_superuser']
    list_display_links = ['email', 'full_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['email']
    search_fields = ['email', 'full_name']
    filter_horizontal = []

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'phone', 'date_of_birth', 'gender', 'img')}),
        (_('Verification'), {'fields': ('email_verified', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password1', 'password2'),
        }),
    )

    exclude = []

    # By default the admin shows all fields as editable. Any fields in this option will display its data as-is and 
    # non-editable; they are also excluded from the ModelForm used for creating and editing.
    readonly_fields = ['date_joined']

    filter_horizontal = ['user_permissions']
    filter_vertical = ['groups']

    # Set save_on_top to add save buttons across the top of your admin change forms.
    save_on_top = True

    actions = [make_inactive, make_active]

    # Controls where on the page the actions bar appears. 
    actions_on_top = True
    actions_on_bottom = False

    # Controls whether a selection counter is displayed next to the action dropdown.
    actions_selection_counter = True

    # This will intelligently populate itself based on available data, e.g. if all the dates are in one month, 
    # it’ll show the day-level drill-down only. date_hierarchy uses QuerySet.datetimes() internally. Please refer to its 
    # documentation for some caveats when time zone support is enabled (USE_TZ = True).
    date_hierarchy = 'date_joined'

    # This attribute overrides the default display value for record’s fields that are empty (None, empty string, etc.). 
    # The default value is - (a dash)
    empty_value_display = '-empty-'

    # Set list_max_show_all to control how many items can appear on a “Show all” admin change list page. The admin will
    # display a “Show all” link on the change list only if the total result count is less than or equal to this setting. 
    # By default, this is set to 200.
    list_max_show_all = 200

    # Set list_per_page to control how many items appear on each paginated admin change list page. By default, 
    # this is set to 100.
    list_per_page = 100

    # Set list_select_related to tell Django to use select_related() in retrieving the list of objects on the admin 
    # change list page. The value should be either a boolean, a list or a tuple. Default is False.
    list_select_related = False

    # By default, Django’s admin uses a select-box interface (<select>) for fields that are ForeignKey or have choices set.
    # If a field is present in radio_fields, Django will use a radio-button interface instead. radio_fields = {"group": admin.VERTICAL}
    radio_fields = {}





admin.site.register(User, MyUserAdmin)


# Registering actions on admin panel to make availabile through out the admin site.
# admin.site.add_action(make_active, 'mark as active')
# admin.site.add_action(make_inactive, 'mark as inactive')

# If you need to disable a site-wide action you can call admin.site.disable_action().
# admin.site.disable_action('make as inactive')
# admin.site.disable_action('make as active')