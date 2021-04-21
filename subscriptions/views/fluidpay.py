import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from subscriptions.fluidpay import FluidPay
from subscriptions.models import UserPayment
from subscriptions.serializers.fluidpay import FluidPayTransactionSerializer


class FluidPayTransaction(CreateAPIView):
    serializer_class = FluidPayTransactionSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': "Transaction is success"}, status=HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def fluidpay_refund(request):
    user = request.user
    last_transaction_detail_db = UserPayment.objects.filter(user_id=user, payment_gateway='fluidpay').latest('paid_at')
    last_transaction_id = last_transaction_detail_db.payment_id
    fp = FluidPay()
    transaction_detail_fluid_pay = fp.request_handler('GET', ['transaction', last_transaction_id], body={})
    res = json.loads(transaction_detail_fluid_pay.text)
    amount = {
        "amount": int(res['data']['amount']/100)
    }
    amount_json_data = json.dumps(amount)

    response = fp.request_handler('POST', ['transaction', last_transaction_id, 'refund'], body=amount_json_data)  # refund transaction
    if not response.status_code == 200:
        response_body = response.json()
        response_message = response_body.get('msg', 0)
        return Response({'message': response_message}, status=HTTP_400_BAD_REQUEST)
    return Response({
        'message': "$" + str(amount["amount"]) + " has been successfully refunded"}, status=HTTP_200_OK
    )

