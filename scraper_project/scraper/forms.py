from django import forms


class SearchForm(forms.Form):
    search_subject = forms.CharField(max_length=200, required=False)
    search_page_count = forms.IntegerField(
        min_value=1, max_value=10, required=False)
