from multiprocessing import context
import re
from xmlrpc.client import ResponseError
from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import Todos
from api.serializers import TodoSerializers,RegistrationSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions


# Create your views here.
class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializers(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kw):
        serializer=TodoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializers(qs,many=False)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serializer=TodoSerializers(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



class TodosModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    serializer_class=TodoSerializers
    queryset=Todos.objects.all()

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)


    def create(self,request,*args,**kw):
        serializer=TodoSerializers(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
        

    
    # def list(self,request,*args,**kw):
    #     qs=Todos.objects.filter(data=request.user)
    #     serializer=TodoSerializers(qs,many=True)
    #     return Response(data=serializer.data)



    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializers(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)



    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False,user=request.user)
        serializer=TodoSerializers(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializers(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.filter(id=id)
        object.update(status=True)
        serializer=TodoSerializers(object,many=True)
        return Response(data="updated")



class UsersView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    

    