from rest_framework import serializers
from .models import GymMember, Membership, GymIncomeExpense, GymInout, GymAttendance, MembershipPayment
from django.core.files import File
from io import BytesIO
import os
from django.conf import settings


class GymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if image exists and return the URL
        if instance.image:
            representation['image'] = instance.image.url

        return representation

# class GymMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GymMember
#         fields = '__all__'

#     def to_representation(self, instance):        
#         representation = super().to_representation(instance)
#         # Check if image exists
#         if instance.image:
#             image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
#             if os.path.exists(image_path):
#                 request = self.context.get('request')
#                 representation['image'] = request.build_absolute_uri(instance.image.url)
#             else:
#                 representation['image'] = None
#         else:
#             representation['image'] = None

#         return representation

#     def get_file_content(self, file):
#         """Returns the file content as a file-like object"""
#         file_content = BytesIO(file.read())
#         return File(file_content, name=file.name)

#     def create(self, validated_data):
#         image_file = validated_data.pop('image', None)
#         # Create the instance first to get an id
#         instance = GymMember.objects.create(**validated_data)
#         if image_file:
#             # Use the instance id to build the new file name
#             new_file_name = f"{instance.id}.jpeg"
#             instance.image.save(new_file_name, image_file, save=True)
#         return instance

#     def update(self, instance, validated_data):
#         image_file = validated_data.pop('image', None)
#         instance = super().update(instance, validated_data)
#         if image_file:
#             new_file_name = f"{instance.id}.jpeg"
#             instance.image.save(new_file_name, image_file, save=True)
#         return instance


class MembershipPaymentSerializer(serializers.ModelSerializer):
    # Adding member_info field to show member's name
    member_info = serializers.SerializerMethodField()
    # registration_fees = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    # due_amount = serializers.SerializerMethodField()


    # def get_registration_fees(self, obj):
    #     return obj.signupfee or 0

    def get_total_amount(self, obj):
        base = obj.membership_amount or 0
        reg = obj.signupfee or 0
        return base + reg

    # def get_due_amount(self, obj):
    #     total = self.get_total_amount(obj)
    #     paid = obj.paid_amount or 0
    #     return max(total - paid, 0)

    def get_member_info(self, obj):
        member = None
        try:
            # Try fetching the member by member_reg_code
            member = GymMember.objects.filter(members_reg_number=obj.member_id).first()
        except GymMember.DoesNotExist:
            try:
                # If not found, try fetching by member_id
                member = GymMember.objects.filter(member_id=obj.member_id).first()
            except GymMember.DoesNotExist:
                pass

        # If member is found, return the serialized data of first_name and last_name
        if member:
            return GymMemberSimpleSerializer(member).data
        else:
            return {
                "first_name": None,
                "last_name": None,
            }

    class Meta:
        model = MembershipPayment
        fields = '__all__' 
        


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = '__all__'


class GymIncomeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymIncomeExpense
        fields = '__all__'    


# class GymInoutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GymInout
#         fields = '__all__'


class GymAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymAttendance
        fields = '__all__'
        


# class ExpenseDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExpenseData
#         fields = '__all__'


# class MembershipDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MembershipData
#         fields = '__all__'


# class PaymentDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentData
#         fields = '__all__'

class GymMemberSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = ['first_name', 'last_name', 'membership_valid_from', 'membership_valid_to','membership_status', 'image']
        

class GymInoutSerializer(serializers.ModelSerializer):
    member_info = serializers.SerializerMethodField()

    def get_member_info(self, obj):
        member = None
        try:
            member = GymMember.objects.get(members_reg_number=obj.member_reg_code)
        except GymMember.DoesNotExist:
            try:
                member = GymMember.objects.get(member_id=obj.member_id)
            except GymMember.DoesNotExist:
                pass

        if member:
            return GymMemberSimpleSerializer(member).data
        else:
            return {
                "first_name": None,
                "last_name": None,
                "membership_valid_from": None,
                "membership_valid_to": None,
                "membership_status": None,
                "image": None
            }

    class Meta:
        model = GymInout
        fields = ['id', 'in_time', 'out_time', 'member_reg_code', 'member_info']