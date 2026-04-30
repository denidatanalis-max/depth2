from django import forms
from .models import Journal, JournalScore


class JournalCreateForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title', 'abstract']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Masukkan judul jurnal'}),
            'abstract': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Masukkan ringkasan jurnal'}),
        }


class JournalUploadForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['file']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f and not f.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Hanya file PDF yang diperbolehkan.')
        return f


class JournalUploadWithAbstractForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['abstract', 'file']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ringkasan dapat diperbarui sebelum upload...'}),
        }
        labels = {
            'abstract': 'Ringkasan',
            'file': 'File Jurnal (PDF)',
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f and not f.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Hanya file PDF yang diperbolehkan.')
        return f


class ReviewForm(forms.Form):
    note = forms.CharField(
        label='Catatan',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tulis catatan...'}),
        required=False,
    )


class ScoringForm(forms.ModelForm):
    class Meta:
        model = JournalScore
        fields = ['originality', 'methodology', 'writing_quality', 'relevance', 'recommendation', 'note']
        widgets = {
            'originality': forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'form-control'}),
            'methodology': forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'form-control'}),
            'writing_quality': forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'form-control'}),
            'relevance': forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'form-control'}),
            'recommendation': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Catatan dan saran untuk penulis...'}),
        }
        labels = {
            'originality': 'Orisinalitas (1-100)',
            'methodology': 'Metodologi (1-100)',
            'writing_quality': 'Kualitas Penulisan (1-100)',
            'relevance': 'Relevansi (1-100)',
            'recommendation': 'Rekomendasi',
            'note': 'Catatan Penilai',
        }
