from core.models import  Product  , Category
from django import forms


class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Product Title'}))
    image = forms.ImageField( required=False , widget=forms.FileInput(attrs={'class':'form-control', 'id':'productImage'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control' , 'placeholder':'Product Description' , 'style':'height:100px'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Product Price'}))
    old_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Old Price'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Product Type'}))
    stock_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Stock Count'}))
    life = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Product Life'}))
    mfd = forms.DateTimeField(widget=forms.DateInput(attrs={'class':'form-control' , 'placeholder':'Manufacturing Date'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Product Tags'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  
        widget=forms.Select(attrs={'class': 'form-select'}),  
        required=True,
    )

    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price' ,
            'specifications' ,
            'type' ,
            'stock_count' ,
            'life' ,
            'mfd' ,
            'tags' ,
            'digital' ,
            'category' ,
            ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }