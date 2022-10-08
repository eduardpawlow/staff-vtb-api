from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt  
from django.contrib.auth.models import User
from api.blockchain import BlockchainService
from api.models import Achievement
from api.serializers import UserSerializer

from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.response import Response

blockchainService = BlockchainService()

@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Укажите полные данные для авторизации'},
                        status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password, )
    if not user:
        return Response({'error': 'Некорректный логин и/или пароль'}, status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=HTTP_200_OK)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_user_details(request):
    ser_user = UserSerializer(request.user)
    return Response(ser_user.data, status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def reward_user(request):
  reward_amount = request.data.get('amount')
  target_user_id = request.data.get('user_id')
  msg = request.data.get('message')

  if not reward_amount or not target_user_id:
    return Response({'error': ''}, status=HTTP_400_BAD_REQUEST)

  target_user = User.objects.get(id=target_user_id)

  if not target_user:
    return Response({'error': 'target user is not found'}, status=HTTP_404_NOT_FOUND)

  source_wallet = request.user.person.wallet
  if not source_wallet:
    return Response({'error': 'your wallet is not defined'}, status=HTTP_404_NOT_FOUND)

  target_wallet = target_user.person.wallet
  if not target_wallet:
    return Response({'error': 'target user wallet is not defined'}, status=HTTP_404_NOT_FOUND)
  
  result = blockchainService.send_coins(
    source_private_key=source_wallet.private_key,
    target_public_key=target_wallet.public_key,
    amount=reward_amount
  )

  if result:
    return Response({'success': True}, status=HTTP_200_OK)

  return Response({'error': 'something_wrong'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def thank_user(request):
  reward_amount = request.data.get('amount')
  target_user_id = request.data.get('user_id')
  msg = request.data.get('message')

  if not reward_amount or not target_user_id:
    return Response({'error': ''}, status=HTTP_400_BAD_REQUEST)

  target_user = User.objects.get(id=target_user_id)

  if not target_user:
    return Response({'error': 'target user is not found'}, status=HTTP_404_NOT_FOUND)

  source_wallet = request.user.person.wallet
  if not source_wallet:
    return Response({'error': 'your wallet is not defined'}, status=HTTP_404_NOT_FOUND)

  target_wallet = target_user.person.wallet
  if not target_wallet:
    return Response({'error': 'target user wallet is not defined'}, status=HTTP_404_NOT_FOUND)
  
  result = blockchainService.send_coins(
    source_private_key=source_wallet.private_key,
    target_public_key=target_wallet.public_key,
    amount=reward_amount
  )

  if result:
    return Response({'success': True}, status=HTTP_200_OK)

  return Response({'error': 'something_wrong'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def give_achievement(request):
  achievement_id = request.data.get('achievement_id')
  target_user_id = request.data.get('user_id')

  if not achievement_id or not target_user_id:
    return Response({'error': ''}, status=HTTP_400_BAD_REQUEST)

  achievement = Achievement.objects.get(id=achievement_id)
  if not achievement:
    return Response({'error': 'achievement is not found'}, status=HTTP_404_NOT_FOUND)

  target_user = User.objects.get(id=target_user_id)
  if not target_user:
    return Response({'error': 'target user is not found'}, status=HTTP_404_NOT_FOUND)

  source_wallet = request.user.person.wallet
  if not source_wallet:
    return Response({'error': 'your wallet is not defined'}, status=HTTP_404_NOT_FOUND)

  target_wallet = target_user.person.wallet
  if not target_wallet:
    return Response({'error': 'target user wallet is not defined'}, status=HTTP_404_NOT_FOUND)

  achievement.users.add(target_user.person)

  result = blockchainService.send_coins(
    source_private_key=source_wallet.private_key,
    target_public_key=target_wallet.public_key,
    amount=achievement.reward
  )

  if result:
    achievement.save()
    return Response({'success': True}, status=HTTP_200_OK)

  return Response({'error': 'something_wrong'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_my_achievements(request):
  pass

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_achievements(request):
  pass

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_my_challenges(request):
  pass

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_challenges(request):
  pass
