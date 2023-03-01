from rest_framework import serializers

from note.models import Labels, Note


class LabelSerializer(serializers.ModelSerializer):
    """
     Class for label serializer
    """

    class Meta:
        model = Labels
        fields = ['id', 'user', 'label_name']


class NoteSerializer(serializers.ModelSerializer):
    """
    Class for Note serializer
    """

    class Meta:
        model = Note
        fields = ['id', 'user', 'label', 'title', 'description', 'collaborator', 'isArchive', 'isTrash', 'color',
                  'reminder', 'image', 'created_at', 'modified_at']
