from rest_framework import serializers
from genres.models import Genre

from genres.serializers import GenreSerializer
from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    premiere = serializers.DateField()
    duration = serializers.CharField(max_length=10)
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        newGenres = []
        for genre in validated_data["genres"]:
            newGenre, _ = Genre.objects.get_or_create(**genre)
            newGenres.append(newGenre)

        validated_data.pop("genres")
        instance = Movie.objects.create(**validated_data)
        instance.genres.set(newGenres)
        serializer = MovieSerializer(instance)
        return serializer.data

    def update(self, instance: Movie, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.premiere = validated_data.get("premiere", instance.premiere)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.classification = validated_data.get(
            "classification", instance.classification)
        instance.synopsis = validated_data.get("synopsis", instance.synopsis)

        instance.save()
        if (validated_data.get("genres")):
            newGenres = []
            for genre in validated_data["genres"]:
                newGenre, _ = Genre.objects.get_or_create(**genre)
                newGenres.append(newGenre)
            instance.genres.set(newGenres)

        return instance
