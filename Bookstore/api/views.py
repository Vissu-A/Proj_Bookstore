from functools import partial
from django.contrib import auth
from django.views.decorators.http import require_http_methods
from cuser.models import User
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404

from api.serializers import User_create_serializer, User_info_serializer, User_password_reset_handle_serializer, User_password_reset_serializer, User_password_change_serializer
from cuser.tasks import Account_Activate_Send_Mail, Reset_Password_Send_Mail
from cuser.utils import token_generator

@api_view(http_method_names=['POST'])
@authentication_classes([])
@permission_classes([])
def creating_user(request):
    serialized = User_create_serializer(data = request.data)

    if serialized.is_valid(raise_exception=False):
        print(serialized.validated_data)
        user = serialized.save()

        if user:
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = token_generator.make_token(user)

            activate_link = reverse('account-activate-api', kwargs={'uidb64':uidb64, 'token':token}, request=request)

            task = Account_Activate_Send_Mail.delay(user.email, user.full_name, activate_link)
            print(task.task_id)

            return Response({'message':"User created successfully. We have sent an email with the link to activate your account"}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({'error':'Something went wrong while creating the user.'}, status = status.HTTP_400_BAD_REQUEST)

    else:
        print(serialized.errors)
        return Response({'error': serialized.errors}, status = status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([])
@permission_classes([])
def account_activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)

    if not token_generator.check_token(user, token):
        return Response({'message':'Token is invalid.'}, status = status.HTTP_401_UNAUTHORIZED)

    elif user.is_active:
        return Response({'message':'Your Account already activated, Please login.'}, status = status.HTTP_200_OK)
    
    else:
        user.is_active = True
        user.email_verified = True
        user.save()

        return Response({'message':'Your account is activated successfully, please login.'}, status = status.HTTP_200_OK)


# If we not specified any authentication_classes and permission_classes on a view then that view will use the
# DEFAULT_AUTHENTICATION_CLASSES and DEFAULT_PERMISSION_CLASSES from settings.py file
@api_view(http_method_names=['GET'])
def users_list(request):
    queryset = User.objects.all()
    serialized = User_info_serializer(queryset, many = True)
    if serialized.data:
        return Response({'users':serialized.data}, status = status.HTTP_200_OK)
    else:
        return Response({'error':serialized.errors}, status = status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([JWTAuthentication])  # This view is authenticated by the specified list of authentication classess.
def user_info(request):
    serialized = User_info_serializer(request.user)
    if serialized.data:
        return Response({'user':serialized.data}, status = status.HTTP_200_OK)
    else:
        return Response({'error':serialized.errors}, status = status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def user_info_edit(request):
    print('####################DATA#####################')
    print('#########', request.data, '###########')
    print('####################DATA#####################')
    serialized = User_info_serializer(data = request.data, instance=request.user, partial=True)
    if serialized.is_valid(raise_exception=True):
        serialized.save()
        return Response({"message":"Information updated successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"error":serialized.errors}, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@authentication_classes([])
@permission_classes([])
def user_password_reset(request):
    serialized = User_password_reset_serializer(data = request.data)
    if serialized.is_valid(raise_exception=True):
        mail = serialized.validated_data.get('email')
        
        user = get_object_or_404(User, email=mail)  # Args: Model class, lookup field
            
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        reset_link = reverse('user-password-reset-link-mail', kwargs={'uidb64': uidb64, 'token':token}, request=request)

        task = Reset_Password_Send_Mail.delay(user.email, user.full_name, reset_link)
        print('Celery Task id is: ', task.task_id)

        return Response({'message':"We have sent an email with the link to reset your password."}, status=status.HTTP_200_OK)

    else:
        return Response({'errors': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['POST'])
@authentication_classes([])
@permission_classes([])
def user_password_reset_link_click(request, uidb64, token):
    serialized = User_password_reset_handle_serializer(data=request.data)
    
    if serialized.is_valid(raise_exception=True):
        password = serialized.validated_data.get('password2', None)
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id = uid)

        if not token_generator.check_token(user, token):
            return Response({'error':'Token is invalid.'}, status = status.HTTP_401_UNAUTHORIZED)

        elif not user.is_active:
            return Response({'message':'Please activate your account first.'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            if password:
                user.set_password(password)
                user.save()
                    
                return Response({'message':'Password Reset completed.'}, status=status.HTTP_200_OK)

    else:
        return Response({'errors':serialized.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
def user_password_change(request):
    serialized = User_password_change_serializer(data=request.data)

    if serialized.is_valid(raise_exception=True):
        old_password = serialized.validated_data.get('old_password')
        password = serialized.validated_data.get('confirm_password')

        user = User.objects.get(id = request.user.id)

        if not user.check_password(old_password):
            response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'error': 'Old password is not correct.',
                'message': '',
                'data': []
            }

            return Response(response)

        else:
            user.set_password(password)
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'error': '',
                'message': 'Password changed successfully.',
                'data': []
            }

            return Response(response)

    else:
        return Response({'errors': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)