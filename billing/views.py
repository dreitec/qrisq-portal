import os
from unicodedata import name
from rest_framework import viewsets
from user_app.permissions import IsAdminUser
from billing.models import Billing
from billing.serializers import BillingSerializer
from billing.custom_storage import MediaStorage


class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = BillingSerializer
    permission_classes = [IsAdminUser]
    queryset = Billing.objects.all()

    def perform_create(self, serializer):
        file_obj = self.request.FILES.get('file', None)

        if file_obj:
            # do your validation here e.g. file size/type check

            # organize a path for the file in bucket
            file_directory_within_bucket = 'city_wkt'

            # synthesize a full file path note that we included the filename
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                file_obj.name
            )

            media_storage = MediaStorage()

            # if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing file
            media_storage.save(file_path_within_bucket, file_obj)
            serializer.save(shape_file=file_obj.name)
        return super().perform_create(serializer)
