from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .models import Note
from .forms import NoteForm, SignUpForm



def home(request):
    return redirect('notes:list')

class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'   # путь к шаблону
    context_object_name = 'note'               # как переменная будет называться в шаблоне


class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user) if self.request.user.is_authenticated else Note.objects.none()

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('notes:list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes:list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
