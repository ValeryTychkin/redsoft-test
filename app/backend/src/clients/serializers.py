from rest_framework import serializers

from clients.models import Client, ClientsPhoto


class ClientsPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientsPhoto
        fields = ('id', 'file')


class ClientSerializer(serializers.ModelSerializer):
    photo = ClientsPhotoSerializer(allow_null=True)

    class Meta:
        model = Client
        fields = ('id', 'f_name', 'l_name', 'born', 'photo')

    def create(self, validated_data):
        photo = None
        if validated_data.get('photo'):
            photo = ClientsPhoto.objects.create(photo=validated_data['photo']['file'])
        return Client.objects.create(f_name=validated_data['f_name'],
                                     l_name=validated_data['l_name'],
                                     born=validated_data['born'],
                                     sex=validated_data['sex'],
                                     photo=photo)
