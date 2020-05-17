from rest_framework import serializers
from user.models import User
import re

class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        if attrs['name'].isalpha() is False:
            raise serializers.ValidationError("이름은 한글 혹은 영어만 입력 가능합니다.")
        if attrs['nickname'] != re.sub('[^a-z]', '', attrs['nickname']):
            raise serializers.ValidationError("별명은 영어(소문자)만 입력 가능합니다.")
        if not re.search('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', attrs['password']) or not re.search('[A-Z]', attrs['password']) or not re.search('[a-z]', attrs['password']) or not re.search('[0-9]', attrs['password']) or len(attrs['password']) < 10:
            raise serializers.ValidationError("패스워드는 영어 대문자, 영어 소문자, 특수 문자, 숫자 각 하나 이상 포함된 10자리 이상의 문자여야합니다.")
        if attrs['phone'] != re.sub('[^0-9]', '', attrs['phone']):
            raise serializers.ValidationError("전화번호는 숫자만 입력 가능합니다.")
        return attrs

    class Meta:
        model = User
        fields = ('email', 'name', 'nickname', 'phone', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


