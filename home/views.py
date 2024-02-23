from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User, Trainer, Customer, CustomerTrainer


class Home(APIView):
    def get(self, request):
        user = request.user

        if user.is_authenticated and user.type == User.Types.CUSTOMER:
            customer = Customer.objects.get(user=user)
            trainers = Trainer.objects.all()
            relation = CustomerTrainer.objects.filter(customer=customer)
            isCustomer = True
            isSchedule = False
            schedule = CustomerTrainer.objects.filter(customer=customer)
            if schedule:
                isSchedule = True
            return Response(status=status.HTTP_200_OK)

        elif user.is_authenticated and user.type == User.Types.TRAINER:
            trainer = Trainer.objects.get(user=user)
            customers = Customer.objects.all()
            relation = CustomerTrainer.objects.filter(trainer=trainer)
            isTrainer = True
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
