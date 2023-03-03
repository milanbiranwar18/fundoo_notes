from rest_framework import serializers

from note.models import Labels, Note


class LabelSerializer(serializers.ModelSerializer):
    """
     Class for label serializer
    """

    class Meta:
        model = Labels
        fields = ['id', 'user', 'label_name']

    def create(self, validated_data):
        lab = validated_data.get("label_name")
        user = validated_data.get("user")
        lab_name = Labels.objects.filter(label_name=lab, user=user)
        if lab_name.exists():
            raise Exception("label name already exist, use another one")
        else:
            lab_name = Labels.objects.create(label_name=lab, user=user)
            return lab_name


class NoteSerializer(serializers.ModelSerializer):
    """
    Class for Note serializer
    """

    class Meta:
        model = Note
        fields = ['id', 'user', 'label', 'title', 'description', 'collaborator', 'isArchive', 'isTrash', 'color',
                  'reminder', 'image', 'created_at', 'modified_at']
        read_only_fields = ['collaborator', 'label']

    def create(self, validated_data):

        label_names = self.initial_data.get("label")
        user = validated_data.get("user")
        note = Note.objects.create(**validated_data)
        for lab in label_names:
            labels = Labels.objects.filter(label_name=lab, user=user)
            if labels.exists():
                note.label.add(labels.first())
            else:
                labels = Labels.objects.create(label_name=lab, user=user)
                note.label.add(labels)
        return note
