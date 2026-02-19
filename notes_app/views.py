"""
Notes App Views
Handles authentication (register) and full CRUD operations for notes.
Uses Class-Based Views with LoginRequiredMixin and UserPassesTestMixin
to enforce access control.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Note
from .forms import UserRegisterForm, NoteForm


# =============================================================================
# Authentication Views
# =============================================================================

def register(request):
    """
    Handle user registration.
    GET  -> Display the registration form.
    POST -> Validate and create a new user, then auto-login and redirect.
    """
    if request.user.is_authenticated:
        return redirect('notes_app:note-list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('notes_app:note-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'notes_app/register.html', {'form': form})


def custom_logout(request):
    """
    Log out the user and redirect to the login page.
    Accepts both GET and POST requests.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('notes_app:login')


# =============================================================================
# Notes CRUD Views
# =============================================================================

class NoteListView(LoginRequiredMixin, ListView):
    """
    Display a list of notes belonging to the logged-in user.
    """
    model = Note
    template_name = 'notes_app/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        """Only return notes owned by the current user."""
        return Note.objects.filter(user=self.request.user)


class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Display the full detail of a single note.
    Only the owning user may view the note.
    """
    model = Note
    template_name = 'notes_app/note_detail.html'
    context_object_name = 'note'

    def test_func(self):
        """Ensure the requesting user owns this note."""
        note = self.get_object()
        return self.request.user == note.user


class NoteCreateView(LoginRequiredMixin, CreateView):
    """
    Allow the logged-in user to create a new note.
    Automatically assigns the note to the requesting user.
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes_app/note_form.html'

    def form_valid(self, form):
        """Assign the logged-in user as the note owner before saving."""
        form.instance.user = self.request.user
        messages.success(self.request, 'Note created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Note'
        context['submit_text'] = 'Create Note'
        return context


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow the owning user to edit their note.
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes_app/note_form.html'

    def test_func(self):
        """Ensure the requesting user owns this note."""
        note = self.get_object()
        return self.request.user == note.user

    def form_valid(self, form):
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Note'
        context['submit_text'] = 'Save Changes'
        return context


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Confirm and delete a note owned by the logged-in user.
    """
    model = Note
    template_name = 'notes_app/note_confirm_delete.html'
    context_object_name = 'note'
    success_url = reverse_lazy('notes_app:note-list')

    def test_func(self):
        """Ensure the requesting user owns this note."""
        note = self.get_object()
        return self.request.user == note.user

    def form_valid(self, form):
        messages.success(self.request, 'Note deleted successfully!')
        return super().form_valid(form)
