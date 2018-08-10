from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post
from accounts.api.serializers import UserDetailSerializer

post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
    )


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            #'slug',
            'content',
            'publish',
            'image'
        ]


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            'publish',
            'image'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.path
        except:
            image = None
        return image


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'publish'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

