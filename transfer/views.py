from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Transfer
from .serializers import TransferSerializer, TransferHistorySerializer

Customer = get_user_model()


class TransferDepositView(ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        customer = request.user
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            amount = serializer.validated_data.get('amount')
            if amount is None or amount <= 0:
                return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)       
            customer.wallet += amount
            customer.save()
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        amount = serializer.validated_data.get('amount')
        transfer_type = 'DEPOSIT'
        customer = self.request.user
        serializer.save(amount=amount, transfer_type=transfer_type, customer=customer)

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(customer=request.user)    

class TransferWithdrawView(ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        customer = request.user
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            amount = serializer.validated_data.get('amount')
            if amount is None or amount <= 0:
                return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)  
            if amount > customer.wallet:
                return Response({'error': 'insufficient balance'})     
            customer.wallet -= amount
            customer.save()
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        amount = serializer.validated_data.get('amount')
        transfer_type = 'WITHDRAW'
        customer = self.request.user
        serializer.save(amount=amount, transfer_type=transfer_type, customer=customer)

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(customer=request.user)


class TransferHistoryView(ListAPIView):
    serializer_class = TransferHistorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        request = self.request
        return Transfer.objects.filter(customer=request.user).order_by('-created_time')[:1]