from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View, DetailView, UpdateView
from django.db.models.query_utils import Q
from team.forms import CoachCreateForm, AthleteCreateForm, TeamCreateForm
from team.utils import dump_queries
from .models import Coach, Athlete, Team
from django.contrib.auth.mixins import LoginRequiredMixin

class TeamListView(ListView):
    model = Team
    template_name = "team/team_list.html"

    def get(self, request) :
        objects = Team.objects.all()
        ctx = {'team_list' : objects}
        retval = render(request, self.template_name, ctx)

        return retval

class TeamDetailView(DetailView):
    model = Team
    template_name = "team/team_detail.html"
    def get(self, request, pk) :
        x = Team.objects.get(id=pk)

        context = { 'team' : x }
        return render(request, self.template_name, context)

class TeamCreateView(CreateView):
    template_name = 'team/team_form.html'
    success_url = reverse_lazy('team:all_teams')

    def get(self, request, pk=None):
        form = TeamCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = TeamCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        new_obj = form.save(commit=False)
        new_obj.save()

        form.save_m2m()
        
        return redirect(self.success_url)

class TeamUpdateView(UpdateView, LoginRequiredMixin):
    model = Team
    fields = '__all__'
    template_name = 'team/team_form.html'
    success_url = reverse_lazy('team:all_teams')


########################################################
############ Coaches Views #############################

class CoachListView(ListView):
    model = Coach
    template_name = "team/coach_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        objects = Coach.objects.all()
        ctx = {'coach_list' : objects}
        retval = render(request, self.template_name, ctx)
        return retval

class CoachDetailView(DetailView):
    model = Coach
    template_name = "team/coach_detail.html"
    def get(self, request, pk) :
        x = Coach.objects.get(id=pk)

        context = { 'coach' : x }
        return render(request, self.template_name, context)

class CoachCreateView(CreateView):
    template_name = 'team/coach_form.html'
    success_url = reverse_lazy('team:all_coaches')

    def get(self, request, pk=None):
        form = CoachCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CoachCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)


        coach = form.save(commit=False)
        coach.save()

        form.save_m2m()
        return redirect(self.success_url)

class CoachUpdateView(View):
    model = Coach
    template_name = 'team/coach_form.html'
    success_url = reverse_lazy('team:all_coaches')

    def get(self, request, pk):
        team = get_object_or_404(Coach, id=pk)
        form = CoachCreateForm(instance=team)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        team = get_object_or_404(Coach, id=pk)
        form = CoachCreateForm(request.POST, request.FILES or None, instance=team)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        coach = form.save(commit=False)
        coach.save()

        form.save_m2m()

        return redirect(self.success_url)


##################################################################
# ############## Athlete Views ###################################    


class AthleteListView(ListView):
    model = Athlete
    template_name = "team/athlete_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        objects = Athlete.objects.all()
        ctx = {'athlete_list' : objects}
        retval = render(request, self.template_name, ctx)
        return retval

class AthleteDetailView(DetailView):
    model = Athlete
    template_name = "team/athlete_detail.html"
    def get(self, request, pk) :
        x = Athlete.objects.get(id=pk)
        team = Team.objects.filter(athletes__id=pk).first()

        context = { 'athlete' : x , 'team' : team}
        return render(request, self.template_name, context)

class AthleteCreateView(CreateView):
    template_name = 'team/athlete_form.html'
    success_url = reverse_lazy('team:all_athletes')

    def get(self, request, pk=None):
        form = AthleteCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = AthleteCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)


        athlete = form.save(commit=False)
        athlete.save()

        form.save_m2m()
        return redirect(self.success_url)

class AthleteUpdateView(View):
    model = Athlete
    template_name = 'team/athlete_form.html'
    success_url = reverse_lazy('team:all_athletes')

    def get(self, request, pk):
        team = get_object_or_404(Athlete, id=pk)
        form = AthleteCreateForm(instance=team)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        team = get_object_or_404(Athlete, id=pk)
        form = AthleteCreateForm(request.POST, request.FILES or None, instance=team)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        athlete = form.save(commit=False)
        athlete.save()

        form.save_m2m()

        return redirect(self.success_url)
