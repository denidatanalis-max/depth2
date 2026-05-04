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
        fields = ['writing_clarity', 'problem_clarity', 'solution_quality', 'positive_impact', 'risk_awareness', 'recommendation', 'note']
        widgets = {
            'writing_clarity': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'}),
            'problem_clarity': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'}),
            'solution_quality': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'}),
            'positive_impact': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'}),
            'risk_awareness': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'}),
            'recommendation': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Catatan dan saran untuk penulis...'}),
        }
        labels = {
            'writing_clarity': 'Kejelasan Penulisan (0-100)',
            'problem_clarity': 'Identifikasi Masalah (0-100)',
            'solution_quality': 'Kualitas Solusi (0-100)',
            'positive_impact': 'Dampak Positif (0-100)',
            'risk_awareness': 'Identifikasi Risiko (0-100)',
            'recommendation': 'Rekomendasi',
            'note': 'Catatan Penilai',
        }
