from django import forms
import os
from django.core.files import File
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.models import User
from instaMe.models import Profile, Photo, Comment, PLike 
from django.contrib.auth.hashers import check_password

import string
import re

class LoginForm(forms.Form):
	username = forms.CharField(initial='', label='Username', max_length=100, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': 'Unique',
			}))
	password = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '12345'
			}))


class SignUpForm(forms.Form):

	# Regular expressions:	first symbol is letter

	username = forms.RegexField(initial='', regex=r'^\w+[0-9a-zA-Z]+$', label='Username', max_length=50, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': 'Be unique',
			}))
	email = forms.EmailField(initial='', label='Email', max_length=100, 
		widget=forms.EmailInput(attrs={
			'class': 'form-control',
			'placeholder': 'Keep in touch'
			}))
	password = forms.CharField(label='Password', max_length=50, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '12345'
			}))
	pic = forms.ImageField(label='File input', required=False)


	def clean_email(self):
		check_email = self.cleaned_data.get('email')
		
		try:
			user = User.objects.get(email=check_email)
			raise ValidationError('This email is already exist')
		except User.DoesNotExist, e:
			pass

		return check_email


	def clean_username(self):
		check_username = self.cleaned_data.get('username')
		
		try:
			user = User.objects.get(username=check_username)
			raise ValidationError('This username is already exist')
		except User.DoesNotExist, e:
			pass

		return check_username


	def clean_pic(self):		
		max_size = 4
		check_pic = self.cleaned_data.get('pic',False)
		if check_pic:
			if check_pic._size > max_size * 1024 * 1024:
				raise ValidationError("large size")
			return check_pic


	def save(self):
		new_username = self.cleaned_data.get('username')
		new_email = self.cleaned_data.get('email')
		new_password = self.cleaned_data.get('password')

		check_pic = self.cleaned_data.get('pic',False)		# Check picture
		if check_pic:
			name_pic = handleUploadedFile(check_pic)	

		user = User.objects.create_user(new_username, new_email, new_password)
		if check_pic:
			Profile.objects.create(user=user, filename=name_pic)
			return user
		else:
			filename = 'default.jpg'		# Default avatar
        	Profile.objects.create(user=user, filename=filename)
        	return user

class EditProfileForm(forms.Form):
	first_name = forms.CharField(initial='', label='First name', max_length=100, required=True,
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': '',
			}))
	last_name = forms.CharField(initial='', label='Last name', max_length=100, required=False,
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': '',
			}))


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditProfileForm, self).__init__(*args, **kwargs)


	def save(self):
		new_first_name = self.cleaned_data['first_name']
		new_last_name = self.cleaned_data['last_name']

		try:
			user = self.request.user
		except User.DoesNotExist, e:
			return Http404

		if new_first_name:
			user.first_name = new_first_name
		if new_last_name:
			user.last_name = new_last_name

		user.save()

class InstaCommentForm(forms.Form):
	text = forms.CharField(label='Comment',  
		widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Details here',
			'rows':'5'
			}))
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(InstaCommentForm, self).__init__(*args, **kwargs)

	def save(self, photo):
		new_text = self.cleaned_data['text']
		author = self.request.user

		comment = Comment.objects.create(text=new_text, author=self.request.user, photo=photo)
		return comment

class InstaPhotoForm(forms.Form):
	pic = forms.ImageField(label='File input')

	text = forms.CharField(label='Comment',  
		widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Details here',
			'rows':'5'
			}))
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(InstaPhotoForm, self).__init__(*args, **kwargs)


	def clean_pic(self):		
		max_size = 4
		check_pic = self.cleaned_data.get('pic',False)
		if check_pic:
			if check_pic._size > max_size * 1024 * 1024:
				raise ValidationError("large size")
			return check_pic

	def save(self):
		new_text = self.cleaned_data['text']
		author = self.request.user

		check_pic = self.cleaned_data.get('pic',False)		# Check picture
		if check_pic:
			name_pic = handleUploadedFile(check_pic)
			print name_pic

		photo = Photo.objects.create(filename=name_pic, author=self.request.user)
		comment = Comment.objects.create(text=new_text, author=self.request.user, photo=photo)

class EditPhotoForm(forms.Form):
	pic = forms.ImageField(label='File input')

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditPhotoForm, self).__init__(*args, **kwargs)


	def clean_pic(self):		
		max_size = 4
		check_pic = self.cleaned_data.get('pic',False)
		if check_pic:
			if check_pic._size > max_size * 1024 * 1024:
				raise ValidationError("large size")
			return check_pic

	def save(self):
		check_pic = self.cleaned_data.get('pic',False)		# Check picture
		if check_pic:
			name_pic = handleUploadedFile(check_pic)

		user = self.request.user

		os.remove(os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + str(user.profile.filename))

		user.profile.filename = name_pic
		user.save()
		user.profile.save()


class ChangePasswordForm(forms.Form):
	password = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '12345'
			}))
	new_password = forms.CharField(label='New password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '54321'
			}))
	repeat_new_password = forms.CharField(label='Repeat new password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '54321'
			}))


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)


	def clean_password(self):
		check_pass = self.cleaned_data['password']
		user = self.request.user

		if not check_password(check_pass, user.password):
			raise ValidationError('Wrong password')
		return check_pass


	def clean(self):
		check_new_password = self.cleaned_data.get('new_password')
		check_repeat_new_password = self.cleaned_data.get('repeat_new_password')

		if check_new_password != check_repeat_new_password:
			self.add_error('new_password', 'Passwords do not match')
			raise ValidationError('Passwords do not match')


	def save(self):
		print self.cleaned_data.get('new_password')
		new_pass = self.cleaned_data.get('new_password')

		user = self.request.user

		user.set_password(new_pass)
		user.save()

		return user


def handleUploadedFile(f):
	# Generate random name
	new_filename = "%s.%s" % (User.objects.make_random_password(10), f.name.split('.')[-1])

	filename = os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + new_filename
	with open(filename, 'wb') as destination:
		destination.write(f.read())
	return new_filename