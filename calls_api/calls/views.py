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


class BillViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def get_price(self, start, duration):
        # get start time and duration to apply pricing rules and returns the call price.
        standing_charge = 0.36
        min_time = datetime.strptime('06:00:00', '%H:%M:%S').strftime('%H:%M:%S')
        max_time = datetime.strptime('22:00:00', '%H:%M:%S').strftime('%H:%M:%S')
        duration_minutes, duration_seconds = divmod(duration.seconds, 60)
        minutes_extra = 0

        # for each minute, it sum to the start time and verify if the time is on
        # standard time or in the reduced tariff time
        for i in range(0, duration_minutes):
            time = start + timedelta(minutes=i, seconds=duration_seconds)
            minutes_extra += 1 if max_time > time.strftime('%H:%M:%S') > min_time else 0

        extra = minutes_extra * 0.09
        # get the price (standing + call charge minute)
        price = round(standing_charge + extra, 2)

        return 'R$ ' + str(price)

    def get_bill_details(self, call):
        # get the call ended record, and returns destination phone, call start date,
        # call start time, call duration, call price in a dict

        # get start register by call_id
        start_time = CallRecord.objects.get(call_id=call.call_id, type='START').date_register
        end_time = call.date_register

        # get and apply formatting on duration time
        duration = end_time - start_time
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_time = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

        call_register = {
            'destination': call.destination,
            'call_start_date': start_time.strftime('%Y-%m-%d'),
            'call_start_time': start_time.strftime('%H:%M:%S'),
            'call_duration': duration_time,
            'call_price': self.get_price(start_time, duration)
        }

        return call_register

    def get_period(self, period):
        # get and returns the sent period if there is any,
        # otherwise get the last month.
        if period:
            try:
                period_list = period.split('/')
                bill_month = int(period_list[0])
                bill_year = int(period_list[1])
            except Exception as e:
                print(e)
                raise serializers.ValidationError('Wrong period.')

        else:
            bill_month = datetime.now().month - 1 if datetime.now().month != 1 else 12
            bill_year = datetime.now().year if datetime.now().month != 1 else datetime.now().year - 1

        return bill_month, bill_year

    def list(self, request, *args, **kwargs):
        # get args and return a list of call register (a bill) serialized data
        # or return error message if the args are not satisfied
        phone = self.request.query_params.get('phone', None)
        period = self.request.query_params.get('period', None)
        data = []

        if not phone:
            raise serializers.ValidationError('Phone number is required')

        # get month and year from the period arg
        bill_month, bill_year = self.get_period(period)

        # queryset to get all ended calls using parameters received by request
        calls = CallRecord.objects.filter(source=phone,
                                          date_register__year=bill_year,
                                          date_register__month=bill_month,
                                          type='END')

        for call in calls:
            call_register = self.get_bill_details(call)
            data.append(call_register)

        serializer = BillSerializer(data=data, many=True)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO Criar testes
# todo SUBIR NO HEROKU