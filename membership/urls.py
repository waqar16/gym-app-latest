from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MemberDataViewSet,
    MemberShipViewSet,
    GymIncomeExpenseViewSet,
    GymInoutViewSet,
    # GymAttendanceViewSet,
    MemberShipPaymentViewSet,
    FingerModeView,
    CustomLogin,
    TokenRefreshViewWithAdminPermission,
    AuthenticationCheckAPIView,
    AcceptPaymentView,
    GymInoutAttendanceViewSet
)


attendance_list = GymInoutAttendanceViewSet.as_view({"get": "list"})

# from .views import CustomLogin, TokenRefreshViewWithAdminPermission
# from .views import (
#     TotalMembersAPIView,
#     ActiveMembersAPIView,
#     LeftMembersAPIView,
#     TotalRevenueAPIView,
#     TotalExpensesAPIView,
#     IncomeExpenseAPIView,
#     MembershipCountsAPIView,
#     MonthlyIncomeExpenseProfitAPIView,
#     AuthenticationCheckAPIView,
# )

# Default router for viewsets
router = DefaultRouter()
router.register(r'members', MemberDataViewSet)
router.register(r'membership', MemberShipViewSet)
router.register(r'membership-payment', MemberShipPaymentViewSet)
router.register(r'income-expense', GymIncomeExpenseViewSet)
# router.register(r'inout', GymInoutViewSet)

# router.register(r'attendance', GymAttendanceViewSet)
# router.register(r'finger-mode', FingerModeViewSet, basename='finger-mode')

# router.register(r'expenses', ExpenseDataViewSet)
# router.register(r'memberships', MembershipDataViewSet)
# router.register(r'payments', PaymentDataViewSet)

# # Register APIViews manually
urlpatterns = [
    # Include the default router URLs
    path('api/', include(router.urls)),
    path('api/finger-mode/', FingerModeView.as_view(), name='finger-mode'),
    path('finger_mode/', FingerModeView.as_view(), name='finger_mode'),
    path('api/accept-payment/', AcceptPaymentView.as_view(), name='accept-payment'),
    path('api/inout/', GymInoutViewSet.as_view({'get': 'list'}), name='inout'),
    path("api/inout/attendance/<str:member_reg_code>/", attendance_list, name="member-attendance"),

#     # Register APIViews
#     path('api/total-members/', TotalMembersAPIView.as_view(), name='total-members'),
#     path('api/active-members/', ActiveMembersAPIView.as_view(), name='active-members'),
#     path('api/left-members/', LeftMembersAPIView.as_view(), name='left-members'),
#     path('api/total-revenue/', TotalRevenueAPIView.as_view(), name='total-revenue'),
#     path('api/total-expenses/', TotalExpensesAPIView.as_view(), name='total-expenses'),
#     path('api/income-expense/', IncomeExpenseAPIView.as_view(), name='income-expense'),
#     path('api/membership-counts/', MembershipCountsAPIView.as_view(), name='membership-counts'),
#     path('api/monthly-income-expense-profit/', MonthlyIncomeExpenseProfitAPIView.as_view(), name='monthly-income-expense-profit'),

    # Token Authentication Endpoints
    path('api/token/', CustomLogin.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshViewWithAdminPermission.as_view(), name='token_refresh'),
    path('api/auth-check/', AuthenticationCheckAPIView.as_view(), name='auth-check'),
]
