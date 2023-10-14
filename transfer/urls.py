from django.urls import path

from .views import TransferDepositView, TransferWithdrawView, TransferHistoryView

urlpatterns = [
    path('deposit/', TransferDepositView.as_view()),
    path('withdraw/', TransferWithdrawView.as_view()),
    path('history/', TransferHistoryView.as_view()),
]