from django.contrib import admin


from .models import Person, Wallet, Team, Challenge, Achievement

class PersonAdmin(admin.ModelAdmin):
  list_display = ['_user', 'email']

  def _user(self, obj):
      return obj.__str__()

  def email(self, obj):
    if obj.user:
      return obj.user.email
    
    return 'Не привязано'

  _user.short_description = 'Пользователь'
  email.short_description = 'Почта'

admin.site.register(Team)
admin.site.register(Person, PersonAdmin)
admin.site.register(Challenge)
admin.site.register(Wallet)
admin.site.register(Achievement)