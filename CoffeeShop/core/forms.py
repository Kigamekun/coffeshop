from django import forms

from .models import *

class ItemForms(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name','price','description','image']
		widgets = {

		'name':forms.TextInput(
			attrs = {
			'class':'form-control',
			'placeholder':'Name of coffee',


			}



			),
  'price':forms.TextInput(
    
			attrs = {
			'class':'form-control',
			'placeholder':'fill this body of News',

			}
			


			
  ),
		'description':forms.TextInput(
			attrs = {
			'class':'form-control',
			'placeholder':'fill this body of News',

			}
			


			),
		'image':forms.FileInput(
			attrs = {
			'class':'custom-file-input',
			'id': 'inputGroupFile01',	
			
			}
			 


			),


		}