from rest_framework import serializers

from core.boto_client import send_message_to_sqs_queue
from user_app.models import UserProfile


class PinDragAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('id', 'phone_number', 'user', 'address_updated', 'is_preprocessed')

    def validate(self, data):
        error = {}
        address = data.get('address', {})
        if not ('lat' in address and 'lng' in address and 'displayText' in address):
            error['address'] = "Address information invalid. Please add 'lat', 'lng' and 'displayText' fields to address."

        if error:
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        address = validated_data.get('address')
        city = validated_data.get('city')
        state = validated_data.get('state')
        zip_code = validated_data.get('zip_code')
        user = self.context['request'].user

        try:
            user_profile = UserProfile.objects.get(user=user)
            user_profile.address = address
            user_profile.city = city
            user_profile.state = state
            user_profile.zip_code = zip_code
            user_profile.address_updated += 1
            user_profile.save()
        except Exception as err:
            raise err
        
        # send message to SQS on user signup
        try:
            send_message_to_sqs_queue(str(user.id), user_profile.address)
        except Exception as err:
            logger.warning(f"Failed sending message to SQS queue; Error: {str(err)}")
            raise Exception("Error sending message to SQS queue.")

        return user_profile