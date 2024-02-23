from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trainer, Customer, User, CustomerTrainer, Category, Train, Schedule
from .serializers import TrainerRegisterSerializer, CustomerRegisterSerializer, UserLoginSerializer, \
    UserSerializer, TrainerEditSerializer, CustomerEditSerializer, ScheduleSerializer, TrainSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class TrainerRegister(APIView):
    def post(self, request):
        ser_data = TrainerRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            user = User.objects.create_user(username=ser_data.validated_data['username'],
                                            password=ser_data.validated_data['password'],
                                            email=ser_data.validated_data['email'],
                                            type=User.Types.TRAINER)
            Trainer.objects.create(user=user, username=ser_data.validated_data['username'],
                                   password=ser_data.validated_data['password'],
                                   email=ser_data.validated_data['email'],
                                   age=ser_data.validated_data['age'],
                                   bio=ser_data.validated_data['bio'],
                                   experience=ser_data.validated_data['experience'])
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegister(APIView):
    def post(self, request):
        ser_data = CustomerRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            user = User.objects.create_user(username=ser_data.validated_data['username'],
                                            password=ser_data.validated_data['password'],
                                            email=ser_data.validated_data['email'],
                                            type=User.Types.CUSTOMER)
            Customer.objects.create(user=user, username=ser_data.validated_data['username'],
                                    password=ser_data.validated_data['password'],
                                    email=ser_data.validated_data['email'],
                                    age=ser_data.validated_data['age'],
                                    bio=ser_data.validated_data['bio'],
                                    historyOfBloodPressure=ser_data.validated_data['historyOfBloodPressure'],
                                    historyOfDiabetes=ser_data.validated_data['historyOfDiabetes'],
                                    height=ser_data.validated_data['height'],
                                    weight=ser_data.validated_data['weight'],
                                    days=ser_data.validated_data['days'])
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        ser_data = UserLoginSerializer(data=request.POST)
        if ser_data.is_valid():
            user = authenticate(request, username=ser_data.validated_data['username'],
                                password=ser_data.validated_data['password'])
            if user is not None:
                login(request, user)
                return Response({"result": "با موفقیت وارد شدید"}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(LoginRequiredMixin, APIView):
    def get(self, request):
        logout(request)
        return Response('خارج شدید', status=status.HTTP_200_OK)


class UserProfile(LoginRequiredMixin, APIView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        ser_data = UserSerializer(instance=user)
        return Response(data=ser_data.data)


class UserEdit(LoginRequiredMixin, APIView):
    def get(self, request):
        global ser_data
        if request.user.type == User.Types.TRAINER:
            trainer = Trainer.objects.get(user=request.user)
            ser_data = TrainerEditSerializer(instance=trainer, data=request.data, partial=True)
        elif request.user.type == User.Types.CUSTOMER:
            customer = Customer.objects.get(user=request.user)
            ser_data = CustomerEditSerializer(instance=customer, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollow(LoginRequiredMixin, APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        trainer = Trainer.objects.get(user=user)
        customer = Customer.objects.get(user=request.user)
        relation = CustomerTrainer.objects.filter(customer=customer, trainer=trainer)
        if relation.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            CustomerTrainer(customer=customer, trainer=trainer).save()
            return Response(f'{trainer.user} trains {customer.user}', status=status.HTTP_200_OK)


class UserUnfollow(LoginRequiredMixin, APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        trainer = Trainer.objects.get(user=user)
        customer = Customer.objects.get(user=request.user)
        relation = CustomerTrainer.objects.filter(customer=customer, trainer=trainer)
        if relation.exists():
            relation.delete()
            return Response(f'{trainer.user} untrains {customer.user}', status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserScheduleWrite(LoginRequiredMixin, APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(user=user)
        trainer = Trainer.objects.get(user=request.user)
        ser_data = ScheduleSerializer(data=request.data, many=True)
        relation = CustomerTrainer.objects.filter(customer=customer, trainer=trainer)
        if relation.exists() and ser_data.is_valid():
            for dataum in ser_data.data:
                if dataum['day'] > customer.days:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                train = Train.objects.get(id=dataum['train'])
                Schedule.objects.create(relation=CustomerTrainer.objects.get(customer=customer, trainer=trainer),
                                        train=train,
                                        day=dataum['day'],
                                        number=dataum['number'])
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserScheduleSee(LoginRequiredMixin, APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        trainer = Trainer.objects.get(user=user)
        customer = Customer.objects.get(user=request.user)
        schedule = Schedule.objects.filter(relation=CustomerTrainer.objects.get(customer=customer, trainer=trainer))
        ser_data = ScheduleSerializer(instance=schedule, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ListExercise(LoginRequiredMixin, APIView):
    def get(self, request):
        queryset = Train.objects.all()
        if request.GET.get('exercise'):
            queryset = queryset.filter(category=Category.objects.get(id=request.GET.get('exercise')))
        ser_data = TrainSerializer(instance=queryset, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
