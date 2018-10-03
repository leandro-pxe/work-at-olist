from .models import CallRecord
from .serializers import CallRecordSerializer, BillSerializer
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta


class CallsViewSet(viewsets.ModelViewSet, viewsets.ViewSet):
    serializer_class = CallRecordSerializer
    permission_classes = (AllowAny,)
    queryset = CallRecord.objects.all()

    def get_start_call(self, data, call_id):
        # get call id to find the start call on db
        # and get source and destination phone number.
        # Returns a copy of data to serialize.

        self.data = data.copy()
        try:
            call_start = CallRecord.objects.get(call_id=call_id, type='START')
            if call_start:
                self.data.update({
                    'source': call_start.source,
                    'destination': call_start.destination
                })

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return self.data

    def create(self, request, *args, **kwargs):
        data = request.data
        type_call = data.get('type', None)
        call_id = data.get('call_id', None)
        db_call = CallRecord.objects.filter(call_id=call_id, type=type_call)
        if db_call:
            return Response('This call register already exist',
                            status=status.HTTP_400_BAD_REQUEST)

        if type_call == 'END':
            data = self.get_start_call(data, call_id)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
