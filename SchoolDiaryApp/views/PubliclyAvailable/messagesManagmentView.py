from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from SchoolDiaryApp.permissions import *
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.models_directory.structures import Message, Class, Classes, School
from SchoolDiaryApp.models import CustomUser, Student, Director, Teacher, Admin
from SchoolDiaryApp.serializers import MessageSerializer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    data = request.data

    content = data.get('content')
    topic = data.get('topic')
    address_id = data.get('address_id')

    if not content or not topic or not address_id:
        return Response(
            {"error": "Wszystkie pola (content, topic, address_id) są wymagane."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        address = CustomUser.objects.get(id=address_id)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Użytkownik o podanym ID nie istnieje."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Tworzenie wiadomości
    new_message = Message.objects.create(
        content=content,
        topic=topic,
        sender=request.user,
        address=address
    )

    return Response(
        {"message": "Wiadomość została pomyślnie wysłana."},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_received_messages(request):
    user = request.user
    received_messages = Message.objects.filter(address=user).order_by('-date')
    serializer = MessageSerializer(received_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sent_messages(request):
    user = request.user
    sent_messages = Message.objects.filter(sender=user).order_by('-date')
    serializer = MessageSerializer(sent_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_message_status(request, message_id):
    user = request.user  # Aktualny użytkownik

    try:
        message = Message.objects.get(id=message_id, address=user)
    except Message.DoesNotExist:
        return Response(
            {"error": "Wiadomość nie istnieje lub nie masz do niej dostępu."},
            status=status.HTTP_404_NOT_FOUND
        )

    read_status = request.data.get('read')
    if read_status is not None:
        message.read = read_status

    message.save()

    return Response(
        {"message": "Status wiadomości został zaktualizowany."},
        status=status.HTTP_200_OK
    )
