from django.urls import path
from .views import (
    RegisterUserView, LoginView, DeleteUserView,
    UpdateWalletView, GetWalletBalanceView, ViewOtherUserWallet,
    TransferWalletView, TransferListView
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("delete/", DeleteUserView.as_view(), name="delete-user"),
    path("wallet/update/", UpdateWalletView.as_view(), name="update-wallet"),
    path("wallet/", GetWalletBalanceView.as_view(), name="get-wallet-balance"),
    path("wallet/<str:name>/", ViewOtherUserWallet.as_view(), name="view-other-wallet"),
    path("transfer/", TransferWalletView.as_view(), name="transfer-wallet"),
    path("transfer/list/", TransferListView.as_view(), name="transfer-list"),
]
