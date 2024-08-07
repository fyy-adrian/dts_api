from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import authenticate
from .base64 import encrypt, decrypt
from rest_framework_simplejwt.views import TokenObtainPairView
import os

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Login View
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Username atau password salah')

        refresh = CustomRefreshToken.for_user(user)
        access_token = refresh.access_token

        # Enkripsi refresh token
        try:
            encrypted_refresh_token = encrypt(str(refresh))
            encrypted_access_token = encrypt(str(access_token))
        except Exception as e:
            raise AuthenticationFailed(f'Gagal mengenkripsi token: {str(e)}')

        # Ambil grup pengguna
        groups = user.groups.values_list('name', flat=True)

        response = Response({
            'access': encrypted_access_token,
            'refresh': encrypted_refresh_token,
            'groups': groups,  # Sertakan informasi grup di respons
        })  

        response.set_cookie(
            'access_token',
            encrypted_refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=24 * 60 * 60,
        )

        return response
    
class LogoutView(APIView):

    def post(self, request):
        encrypted_refresh_token = request.COOKIES.get('access_token')
        
        if encrypted_refresh_token:
            try:
                refresh_token = decrypt(encrypted_refresh_token)
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Log the error if necessary
                print(f"Error processing token: {str(e)}")
        
        # Regardless of the outcome, delete the access_token cookie
        response = Response({"success": "Logged out successfully."}, status=200)
        response.delete_cookie('access_token')

        return response

class UserAuth(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        # Ambil refresh token dari cookie
        encrypted_refresh_token = request.COOKIES.get('access_token')
        if not encrypted_refresh_token:
            raise AuthenticationFailed('Access token not found in cookies.')

        try:
            refresh_token = decrypt(encrypted_refresh_token) 
            token = RefreshToken(refresh_token)
            user_id = token.payload['user_id']  
            user = User.objects.filter(id=user_id).first()
            if user is None:
                raise AuthenticationFailed('User not found.')
        except Exception as e:
            raise AuthenticationFailed(f'Failed to process token: {str(e)}')


        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    permission_classes = [IsStaffView]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsStaffView]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'

class RegisterView(APIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        requesting_user = self.request.user
        
        # Periksa apakah pengguna yang akan dihapus adalah anggota grup superuser
        if instance.groups.filter(name='superuser').exists():
            # Jika pengguna yang sedang login bukan anggota grup superuser, batalkan penghapusan
            if not requesting_user.groups.filter(name='superuser').exists():
                raise PermissionDenied("gagal dihapus! user memiliki pangkat diatas anda")

        # Jika pengguna yang sedang login adalah anggota grup 'superuser' atau pengguna yang akan dihapus bukan anggota grup superuser, maka bisa dihapus
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'User berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)
    
class LandingPage(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Mengambil hero dengan kolom 'aktif' === true
        hero = Home.objects.filter(active=True).first()

        # Mengambil semua partnership
        partnerships = Partnership.objects.all().order_by('id')

        # Mengambil 3 prices
        prices = Price.objects.all().order_by('id')[:3]

        # Mengambil 3 services
        services = Service.objects.all().order_by('id')[:3]

        # Mengambil semua portofolio
        portofolios = Portofolio.objects.all().order_by('id')

        # Mendapatkan request untuk membangun URL absolut
        request = self.request

        # Mengambil data dari serializer
        hero_data = HeroSerializer(hero).data if hero else None
        partnerships_data = PartnershipSerializer(partnerships, many=True).data
        prices_data = PriceSerializer(prices, many=True).data
        services_data = ServiceSerializer(services, many=True).data
        portofolios_data = PortofolioSerializer(portofolios, many=True).data

        # Menambahkan host dan port ke gambar untuk hero
        if hero_data:
            add_absolute_url(hero_data, request, ['image'])

        for data in [partnerships_data, services_data, portofolios_data]:
            for item in data:
                add_absolute_url(item, request, ['image'])

        data = {
            'hero': hero_data,
            'partnerships': partnerships_data,
            'prices': prices_data,
            'services': services_data,
            'portofolios': portofolios_data
        }

        return Response(data)

# CRUD Hero
class HeroList(generics.ListCreateAPIView):
    queryset = Home.objects.all().order_by('id')
    serializer_class = HeroSerializer
    permission_classes = [IsStaffView]

class HeroCreate(generics.CreateAPIView):
    serializer_class = HeroSerializer
    queryset = Home.objects.all().order_by('id')
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Hero berhasil ditambahkan', 'data': response.data}, status=status.HTTP_201_CREATED)

class HeroUpdate(generics.RetrieveUpdateAPIView):
    queryset = Home.objects.all().order_by('id')
    permission_classes = [IsAdmin]
    serializer_class = HeroSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Hero berhasil diperbarui', 'data': response.data}, status=status.HTTP_200_OK)

class HeroDelete(generics.DestroyAPIView):
    queryset = Home.objects.all().order_by('id')
    permission_classes = [IsAdmin]
    serializer_class = HeroSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Get the image path
        image_path = instance.image.path
        # Delete the object
        super().destroy(request, *args, **kwargs)
        # Delete the image file if it exists
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response({'message': 'Hero berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)
    
# hero active start
class HeroActive(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, home_id, *args, **kwargs):
        try:
            # Fetch the specific Home instance
            home = Home.objects.get(id=home_id)
        except Home.DoesNotExist:
            return Response({"error": "Home instance not found."}, status=status.HTTP_404_NOT_FOUND)

        # Set all Home instances to inactive
        Home.objects.all().update(active=False)

        # Set the specified Home instance to active
        home.active = True
        home.save()

        # Serialize the updated Home instance
        serializer = HeroSerializer(home)
        return Response({'message': 'Hero berhasil diaktifkan', 'data': serializer.data}, status=status.HTTP_200_OK)
# hero active end

# CRUD Price
class PriceCreate(generics.CreateAPIView):
    permission_classes = [IsStaff]
    serializer_class = PriceSerializer
    queryset = Price.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Harga berhasil ditambahkan', 'data': response.data}, status=status.HTTP_201_CREATED)

class PriceList(generics.ListAPIView):
    queryset = Price.objects.all().order_by('id')
    serializer_class = PriceSerializer

class PriceUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsStaff]
    queryset = Price.objects.all().order_by('id')
    serializer_class = PriceSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Harga berhasil diperbarui', 'data': response.data}, status=status.HTTP_200_OK)

class PriceDelete(generics.DestroyAPIView):
    permission_classes = [IsStaff]
    queryset = Price.objects.all().order_by('id')
    serializer_class = PriceSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Harga berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)

# CRUD Service
class ServiceCreate(generics.CreateAPIView):
    permission_classes = [IsStaff]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Service berhasil ditambahkan', 'data': response.data}, status=status.HTTP_201_CREATED)

class ServiceList(generics.ListAPIView):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer

class ServiceDetailView(APIView):
    def get(self, request, service_id, *args, **kwargs):
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service instance not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service)
        data = serializer.data
        add_absolute_url(data, request, ['image '])

        return Response(data)
    

class ServiceUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsStaff]
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Service berhasil diperbarui', 'data': response.data}, status=status.HTTP_200_OK)

class ServiceDelete(generics.DestroyAPIView):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = [IsStaff]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image_path = instance.image.path
        super().destroy(request, *args, **kwargs)
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response({'message': 'Service berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)


# CRUD Portofolio
class PortofolioCreate(generics.CreateAPIView):
    permission_classes = [IsStaff]
    serializer_class = PortofolioSerializer
    queryset = Portofolio.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Portofolio berhasil ditambahkan', 'data': response.data}, status=status.HTTP_201_CREATED)

class PortofolioList(generics.ListAPIView):
    queryset = Portofolio.objects.all().order_by('id')
    serializer_class = PortofolioSerializer
    permission_classes = [IsStaffAndView]

class PortofolioUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsStaff]
    queryset = Portofolio.objects.all().order_by('id')
    serializer_class = PortofolioSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Portofolio berhasil diperbarui', 'data': response.data}, status=status.HTTP_200_OK)

class PortofolioDelete(generics.DestroyAPIView):
    permission_classes = [IsStaff]
    queryset = Portofolio.objects.all().order_by('id')
    serializer_class = PortofolioSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image_path = instance.image.path
        super().destroy(request, *args, **kwargs)
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response({'message': 'Portofolio berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)

# CRUD Contact
class ContactCreate(generics.CreateAPIView):
    # permission_classes = [IsAdmin]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Pesan berhasil dikirimkan', 'data': response.data}, status=status.HTTP_201_CREATED)

class ContactList(generics.ListAPIView):
    queryset = Contact.objects.all().order_by('id')
    serializer_class = ContactSerializer
    permission_classes = [IsStaffView]

class ContactDelete(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Contact.objects.all().order_by('id')
    serializer_class = ContactSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Pesan berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)

# CRUD Partnership
class PartnershipCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = PartnershipSerializer
    queryset = Partnership.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Partnership berhasil ditambahkan', 'data': response.data}, status=status.HTTP_201_CREATED)

class PartnershipList(generics.ListAPIView):
    queryset = Partnership.objects.all().order_by('id')
    serializer_class = PartnershipSerializer
    permission_classes = [IsStaffAndView]

class PartnershipUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = Partnership.objects.all().order_by('id')
    serializer_class = PartnershipSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Partnership berhasil diperbarui', 'data': response.data}, status=status.HTTP_200_OK)

class PartnershipDelete(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Partnership.objects.all().order_by('id')
    serializer_class = PartnershipSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image_path = instance.image.path
        super().destroy(request, *args, **kwargs)
        if os.path.isfile(image_path):
            os.remove(image_path)
        return Response({'message': 'Partnership berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)
