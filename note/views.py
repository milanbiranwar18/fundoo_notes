import logging

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from note.models import Labels, Note
from note.serializers import LabelSerializer, NoteSerializer
from user.models import User
from note.redis_task import RedisNote
from user.utils import verify_token

logging.basicConfig(filename="note_label.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class LabelLC(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    Class for create and retrieve label using mixins
    """
    queryset = Labels.objects.all()
    serializer_class = LabelSerializer

    @verify_token
    @swagger_auto_schema(operation_summary='GET Labels')
    def get(self, request, *args, **kwargs):
        try:
            response = self.list(request, *args, **kwargs)
            return Response({"Message": "List of Labels", "data": response.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(request_body=LabelSerializer, operation_summary='POST Label')
    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
            return Response({"Message": "Label Created Successfully", "data": response.data, "status": 201})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)


class LabelRUD(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """
    Class for retrieve, update and delete the label using mixins
    """
    queryset = Labels.objects.all()
    serializer_class = LabelSerializer


    @swagger_auto_schema(operation_summary='Retrieve One Label')
    def get(self, request, *args, **kwargs):
        try:
            response = self.retrieve(request, *args, **kwargs)
            return Response({"Message": "Label Retrieve Successfully", "data": response.data, "status": 201})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(request_body=LabelSerializer, operation_summary='PUT Label')
    def put(self, request, *args, **kwargs):
        try:
            response = self.update(request, *args, **kwargs)
            return Response({"Message": "Label Updated Successfully", "data": response.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary='DELETE Label')
    def delete(self, request, *args, **kwargs):
        try:
            response = self.destroy(request, *args, **kwargs)
            return Response({"Message": "Label Deleted Successfully", "data": response.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)


class NoteViewSet(viewsets.ViewSet):
    """
    Class for creating, deleting, retrieving and updating the note
    """
    serializer_class = NoteSerializer

    @verify_token
    @swagger_auto_schema(operation_summary='Get Notes')
    def list(self, request):
        try:
            redis_note_data = RedisNote().get(request.user.id)
            if redis_note_data is not None:
                return Response({'Message': "List of Notes", "Data": redis_note_data, "status": 200})
            note = Note.objects.filter(Q(user=request.user.id) | Q(collaborator__id=request.user.id), isArchive=False,
                                       isTrash=False).distinct()
            serializer = NoteSerializer(note, many=True)
            return Response({"Message": "List of Notes", "data": serializer.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary='Retrieve One Note')
    def retrieve(self, request, pk):
        try:
            redis_note_data = RedisNote().get(request.user.id)
            if str(pk) in redis_note_data.keys():
                return Response({'Message': "Note Retrieve Successfully", "Data": redis_note_data, "status": 200})
            else:
                note = Note.objects.get(id=pk, user=request.user.id)
                serializer = NoteSerializer(note)
                return Response({'Message': "Note Retrieve Successfully", "Data": serializer.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(request_body=NoteSerializer, operation_summary='POST Notes')
    def create(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().save(serializer.data, request.user.id)
            return Response({'Message': "Note Created Successfully", "Data": serializer.data, "status": 201})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(request_body=NoteSerializer, operation_summary='PUT Note')
    def update(self, request):
        try:
            note = Note.objects.get(id=request.data.get('id'))
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().save(request.data, request.user.id)
            return Response({'Message': "Note Updated Successfully", "Data": serializer.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary='DELETE Note')
    def destroy(self, request, pk):
        try:
            note = Note.objects.get(id=pk)
            note.delete()
            RedisNote().delete(pk, request.user.id)
            return Response({'Message': 'Note Deleted Successfully', "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)


class IsArchive(APIView):
    @verify_token
    @swagger_auto_schema(operation_summary='PUT Archive')
    def put(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            if not note.isArchive:
                note.isArchive = True
                note.save()
                return Response({"Message": "Note Archive successfully",  "status": 200})
            elif note.isArchive:
                note.isArchive = False
                note.save()
                return Response({"Message": "Note UnArchive successfully", "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary='GET Archive')
    def get(self, request):
        try:
            note = Note.objects.filter(isArchive=True, isTrash=False, user=request.user.id)
            serialiser = NoteSerializer(note, many=True)
            return Response({"Message": "List of Archive Notes", "data": serialiser.data,  "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)


class IsTrash(APIView):
    @verify_token
    @swagger_auto_schema(operation_summary='PUT Trash')
    def put(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            if not note.isTrash:
                note.isTrash = True
                note.save()
                return Response({"Message": "Note Trash successfully",  "status": 200})
            elif note.isTrash:
                note.isTrash = False
                note.save()
                return Response({"Message": "Note UnTrash successfully",  "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(operation_summary='GET Trash')
    def get(self, request):
        try:
            note = Note.objects.filter(isTrash=True, isArchive=False, user=request.user.id)
            serialiser = NoteSerializer(note, many=True)
            return Response({"Message": "List of Trash Notes", "data": serialiser.data,  "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)


class Collaborator(APIView):
    @verify_token
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, properties={
            'collaborator': openapi.Schema(type=openapi.TYPE_ARRAY,
                                           items=openapi.Items(type=openapi.TYPE_STRING))}),
        responses={201: "ok", 400: "BAD REQUEST"})
    def post(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            collab_list = request.data.get('collaborator')
            for user_name in collab_list:
                c_user = User.objects.get(username=user_name)
                if request.user != c_user:
                    note.collaborator.add(c_user)
            return Response({"Message": "Collaborator Added Successfully", 'status': 201})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    @verify_token
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, properties={
            'collaborator': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))}),
        responses={201: "ok", 400: "BAD REQUEST"})
    def delete(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            collab_list = request.data.get('collaborator')
            for user_name in collab_list:
                user = User.objects.get(username=user_name)
                if request.user != user:
                    note.collaborator.remove(user)
            return Response({"Message": "Collaborator Deleted Successfully", 'status': 200})
        except Exception as e:
            return Response({"message": str(e)}, status=400)
