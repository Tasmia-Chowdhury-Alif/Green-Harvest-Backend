from rest_framework import serializers
from .models import User, Profile

class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=20)
    street_address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)
    postcode = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=20)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'street_address',
            'city',
            'country',
            'postcode',
            'image',
        ]
        read_only_fields = ['email', 'id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Safely get profile
        profile = getattr(instance, 'profile', None)

        # Populate profile fields in response
        if profile:
            ret.update({
                'phone': profile.phone or '',
                'street_address': profile.street_address or '',
                'city': profile.city or '',
                'country': profile.country or '',
                'postcode': profile.postcode or '',
                'image': profile.image.url if profile.image else None,
            })
        else:
            ret.update({
                'phone': '',
                'street_address': '',
                'city': '',
                'country': '',
                'postcode': '',
                'image': None,
            })

        return ret

    def update(self, instance, validated_data):
        # Extract and update Profile fields 
        profile_data = {}
        profile_fields = ['phone', 'street_address', 'city', 'country', 'postcode', 'image']

        for field in profile_fields:
            if field in validated_data:
                profile_data[field] = validated_data.pop(field)

        profile, _ = Profile.objects.get_or_create(user=instance)

        if profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        # the parent serializer updates the User fields
        return super().update(instance, validated_data)