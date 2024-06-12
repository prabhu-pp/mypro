import requests
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.decorators import action

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_destroy(self, instance):
        
        instance.destinations.all().delete()
        instance.delete()

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def get_destinations_by_account(self, request):
        account_id = request.query_params.get('account_id')
        try:
            account = Account.objects.get(account_id=account_id)
            destinations = account.destinations.all()
            serializer = DestinationSerializer(destinations, many=True)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class IncomingDataView(APIView):
    def post(self, request):
        
        if not request.data:
            return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

        
        app_secret_token = request.headers.get('AL-XTOKEN')
        if not app_secret_token:
            return Response({'error': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        
        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response({'error': 'Invalid app secret token'}, status=status.HTTP_401_UNAUTHORIZED)

        
        for destination in account.destinations.all():
            url = destination.url
            http_method = destination.http_method
            headers = destination.headers

            if http_method.lower() == 'get':
                
                response = requests.get(url, params=request.data, headers=headers)
            else:
               
                response = requests.request(http_method, url, json=request.data, headers=headers)

            if response.status_code in [200, 201]:
                print(f"Data sent successfully to {url}")
            else:
                print(f"Error sending data to {url}: {response.status_code} - {response.text}")

        return Response({'message': 'Data sent to destinations'}, status=status.HTTP_200_OK)