from rest_framework.decorators import api_view
from rest_framework import exceptions,viewsets,status,generics,mixins
from rest_framework.response import Response
from admin.pagination import CustPagination
from users.authentication import JWTAuthentification, generate_access_token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import PermissionSerializer, RoleSerializer, UserSerializer
from .models import Permission, Role, User
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register(request): 
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions('Password do not match! ')
    serializer = UserSerializer(data = data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def users(request):
    serializer=UserSerializer(User.objects.all(),many=True)
    return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password= request.data.get('password')
    user=User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User Not Found')
    if not user.check_password(password):
        print(password)
        raise exceptions.AuthenticationFailed('Invalid Password ')
    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key='token', value=token , httponly=True)
    response.data = {
        'token':token
    }
    return response

@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie(key='token')
    response.data = {
        'message' : 'Logout Success'
    }
    return response


class AuthentificatedUser(APIView):
    authentication_classes = [JWTAuthentification]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        data= UserSerializer(request.user).data
        data['permissions'] = [p['name'] for p in data['role']['permissions']]
        return Response({
            'data':data
        })

class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentification]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = PermissionSerializer(Permission.objects.all(),many=True)

        return Response({
            'data' : serializer.data
        })


class RoleViewSet(viewsets.ViewSet):
    authentication_classes=[JWTAuthentification]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        serializer = RoleSerializer(Role.objects.all(),many=True)
        return Response({
            'data' : serializer.data
        })

    
    def create(self,request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data':serializer.data
        },status = status.HTTP_201_CREATED)


    def retrieve(self,request,pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)
        return Response({
            'data':serializer.data
        })


    def update(self,request,pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data':serializer.data
        },status = status.HTTP_202_ACCEPTED)


    def destroy(self, request,pk=None):
        role = Role.objects.get(id=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserGenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    authentication_classes=[JWTAuthentification]
    permission_classes = [IsAuthenticated]
    queryset  = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustPagination

    def get(self,request,pk=None):
        if pk:
            return Response({
                'data':self.retrieve(request, pk).data
                })
       
        return self.list(request)

    def post(self,request):
        request.data.update({
            'password':1234,
            'role':request.data['role_id']
        })
        return Response ({
            'data':self.create(request).data
        })

    def put(self,request,pk=None):
        if request.data['role_id']:
            request.data.update({
            'role':request.data['role_id']
        })

        return Response({
            'data':self.partial_update(request,pk).data
        })
    
    def delete(self,request,pk=None):
        return Response(self.destroy(request,pk).data)
  


class ProfileInfoAPIView(APIView):
    authentication_classes=[JWTAuthentification]
    permission_classes = [IsAuthenticated]
    def put(self,request,pk=None):
        user = request.user
        serializer = UserSerializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentification]
    permission_classes = [IsAuthenticated]
    def put(self,request,pk=None):

        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('Password does Not match')
       
        serializer= UserSerializer(user, data=request.data,partial= True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

       


















