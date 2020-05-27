from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from UserSettings import views as user_views


class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, user_views.login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_choose_plan_url_is_resolved(self):
        url = reverse('choose_plan')
        self.assertEquals(resolve(url).func, user_views.choose_plan)

    def test_review_subscription_url_is_resolved(self):
        url = reverse('review_subscription', args=['Premium'])
        self.assertEquals(resolve(url).func, user_views.review_subscription)

    def test_register_url_is_resolved(self):
        url = reverse('register', args=['Free'])
        self.assertEquals(resolve(url).func, user_views.register)

    def test_upgrade_plan_url_is_resolved(self):
        url = reverse('upgrade_account')
        self.assertEquals(resolve(url).func, user_views.upgrade_account)

    def test_upgrade_url_is_resolved(self):
        url = reverse('upgrade')
        self.assertEquals(resolve(url).func, user_views.upgrade)

    def test_reset_password_url_is_resolved(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetView)

    def test_reset_password_done_url_is_resolved(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetDoneView)

    def test_reset_password_confirm_url_is_resolved(self):
        url = reverse('password_reset_confirm', args=[
                      'NQ', '43a-fda06baa91ccfff3484e'])
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetConfirmView)

    def test_reset_password_complete_url_is_resolved(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetCompleteView)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, user_views.profile)

    def test_edit_profile_url_is_resolved(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func, user_views.edit_profile)

    def test_change_password_url_is_resolved(self):
        url = reverse('change_password')
        self.assertEquals(resolve(url).func, user_views.change_password)

    def test_settings_profile_url_is_resolved(self):
        url = reverse('settings_profile')
        self.assertEquals(resolve(url).func, user_views.settings)

    def test_delete_profile_url_is_resolved(self):
        url = reverse('delete_profile')
        self.assertEquals(resolve(url).func, user_views.del_user)

    def test_cancel_subscription_url_is_resolved(self):
        url = reverse('cancel_subscription')
        self.assertEquals(resolve(url).func, user_views.cancel_subscription)

    def test_reactivate_subscription_url_is_resolved(self):
        print("\nTesting the URL resolves for UserSettings app..\n")
        url = reverse('reactivate_subscription')
        self.assertEquals(resolve(url).func,
                          user_views.reactivate_subscription)
