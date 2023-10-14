from django.db import models
from django.contrib.auth import get_user_model
from datetime import timezone

Customer = get_user_model()


class Transfer(models.Model):
    DEPOSIT = 0
    WITHDRAW = 1

    OPTIONS = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW ', 'Withdraw'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='transfers')
    transfer_type = models.CharField(max_length=9, choices=OPTIONS, default=DEPOSIT)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{},{}'.format(self.amount, self.transfer_type)
   