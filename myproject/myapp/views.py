from django.shortcuts import render, get_object_or_404
from .models import StudentDetails , Signup
from .serializers import StudentDetailsSerializer , SignupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from django.core.mail import send_mail
from django.conf import settings
 
def generate_otp():
    return str(random.randint(100000, 999999))

class custompermissions:
    def has_permission(self,request,view): 
        if request.session.get('is_authenticated'):
            return True
        return False
  
  
class StudentDetailsView(APIView):
    permission_classes=[custompermissions]
    def get (self ,request ):
        students= StudentDetails.objects.all()
        serializer=StudentDetailsSerializer(students,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=StudentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self,request,pk):
        student=StudentDetails.objects.get(pk=pk) 
        serializer=StudentDetailsSerializer(student,data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self,request,pk):
        student=StudentDetails.objects.get(pk=pk) 
        serializer=StudentDetailsSerializer(student,data=request.data,partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):    
        student=get_object_or_404(StudentDetails,pk=pk)
        student.delete() 
        return Response({"message":"Student deleted successfully"})


class SignupView(APIView):
    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            otp=generate_otp()
            user.otp=otp
            user.save()
            send_mail(
                'Your OTP for Signup',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,# from 
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data)
        return Response(serializer.errors)
    
class verifyOTPView(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp=request.data.get('otp')
        try:
            user=Signup.objects.get(email=email)
            if user.otp == otp:
                user.is_verified=True
                user.save()
                return Response({"message":"OTP verified successfully"})
            else:
                return Response({"error":"Invalid OTP"},status=400)
        except Signup.DoesNotExist:
            return Response({"error":"User does not exist"},status=404)
    

class loginView(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        if not username or not password:
            return Response({"error":"Username and password are required"},status=400)
        user = Signup.objects.get(username=username)
        if user is not None and not user.is_verified:
            return Response({"error":"Your account is not verified"},status=403)
        try :
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['is_authenticated'] = True
                
                return Response({"message":"Login successful"})
            else:
                return Response({"error":"Invalid credentials"},status=400)
        except Signup.DoesNotExist:
            return Response({"error":"User does not exist"},status=404)
        
        
class forgotPasswordView(APIView):
    def post(self,request):
        email=request.data.get('email')
        try:
            user=Signup.objects.get(email=email)
            otp=generate_otp()
            user.otp=otp
            user.save()
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({"message":"OTP sent to your email"})
        except Signup.DoesNotExist:
            return Response({"error":"User does not exist"},status=404)
        
class resetPasswordView(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp=request.data.get('otp')
        new_password=request.data.get('new_password')
        try:
            user=Signup.objects.get(email=email)
            if user.otp == otp:
                user.password=new_password
                user.save()
                return Response({"message":"Password reset successful"})
            else:
                return Response({"error":"Invalid OTP"},status=400)
        except Signup.DoesNotExist:
            return Response({"error":"User does not exist"},status=404)
        
class logoutView(APIView):
    def post(self,request):
        request.session.flush()
        return Response({"message":"Logout successful"})


class Updatepassword(APIView):
    def post(self,request):
        email=request.data.get('email')
        old_password=request.data.get('old_password')
        new_password=request.data.get('new_password')
        try:
            user=Signup.objects.get(email=email)
            if user.password == old_password:
                user.password=new_password
                user.save()
                return Response({"message":"Password updated successfully"})
            else:
                return Response({"error":"Invalid old password"},status=400)
        except Signup.DoesNotExist:
            return Response({"error":"User does not exist"},status=404)
        


class ResendOTPView(APIView):
    def post(self,request):
        email=request.data.get('email')
        try:
            user=Signup.objects.get(email=email)
            otp=generate_otp()
            user.otp=otp
            user.save()
            send_mail(
                'Your OTP for Signup',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({"message":"OTP resent to your email"})
        except Signup.DoesNotExist:
            return Response({"error":"User does not exist"},status=404)



class StudentSearchView(APIView):
    permission_classes=[cusomerpermission]
    def get (self,request):
        if name:
            students=StudentDetails.objects.filter(name__icontains=name)
            serializer=StudentDetailsSerializer(students,many=True)
            return Response(serializer.data)
        return Response({"error":"Name query parameter is required"},status=400)
