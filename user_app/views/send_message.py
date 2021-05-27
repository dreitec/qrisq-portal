from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.generics import CreateAPIView

from user_app.utils import mail_sender
from user_app.serializers import SendMessageSerializer


class SendMessageView(CreateAPIView):
    serializer_class = SendMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
       
        try:
            mail_sender(
                template='user_app/send_message.html',
                context= serializer.data,
                subject="Contact me",
                recipient_list=['admin@qrisq.com']
            )
            return Response({'message': "Message Sent Successfully"})
            
        except Exception as error:
            return Response({'message': "Error sending message."})
