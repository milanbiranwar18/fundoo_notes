import logging

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response

from note.models import Labels
from note.serializers import LabelSerializer


logging.basicConfig(filename="note_label.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class LabelLC(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Labels.objects.all()
    serializer_class = LabelSerializer

    def get(self, request, *args, **kwargs):
        try:
            request.data.update({"user": request.user.id})
            response = self.list(request, *args, **kwargs)
            return Response({"Message": "All Labels Are", "data":response.data, "status":200})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        try:
            request.data.update({"user":request.user.id})
            response = self.create(request, *args, **kwargs)
            return Response({"Message": "Label Created Successfully", "data":response.data, "status":201})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)


class LabelRUD(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Labels.objects.all()
    serializer_class = LabelSerializer

    def get(self, request, *args, **kwargs):
        try:
            request.data.update({"user": request.user.id})
            response = self.retrieve(request, *args, **kwargs)
            return Response({"Message": "Label Retrieve Successfully", "data": response.data, "status": 201})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            request.data.update({"user": request.user.id})
            response = self.update(request, *args, **kwargs)
            return Response({"Message": "Label Updated Successfully", "data": response.data, "status": 202})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            request.data.update({"user": request.user.id})
            response = self.destroy(request, *args, **kwargs)
            return Response({"Message": "Label Deleted Successfully", "data": response.data, "status": 204})
        except Exception as e:
            logging.error(e)
            return Response({"Message": str(e)}, status=400)
