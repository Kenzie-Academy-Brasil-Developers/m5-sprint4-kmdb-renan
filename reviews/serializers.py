from rest_framework import serializers
from accounts.models import User
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Review


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=["movie_id", "critic"],
            message="Review already exists.",
        )]

    def create(self, validated_data):
        instance = Review.objects.create(**validated_data)
        serializer = ReviewSerializer(instance)
        critic = User.objects.get(id=validated_data["critic"].id)
        criticSerialized = CriticSerializer(critic)
        return {**serializer.data, "critic": criticSerialized.data}


class ReviewListSerializer(serializers.ModelSerializer):
    critic = CriticSerializer()

    class Meta:
        model = Review
        fields = "__all__"
