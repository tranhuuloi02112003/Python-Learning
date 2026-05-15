from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from .forms import ProjectForm
from .models import Project
from . import selectors, services


class ProjectCreateView(View):
    # Dùng View thay vì CreateView vì flow hiện tại là POST-only từ modal.
    # Không có màn GET riêng để render form tạo project.
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            # cleaned_data là dữ liệu đã qua validate của ProjectForm.
            # Ví dụ form submit name/color/status hợp lệ thì Django đưa vào dict này.
            project = services.create_project(form.cleaned_data)
            # Lưu thông báo thành công tạm thời; template đọc biến messages để hiển thị.
            messages.success(request, "Project created.")
            return redirect("projects:detail", pk=project.pk)
        messages.error(request, "Project could not be created.")
        # Nếu form có input hidden name="next" thì quay lại URL đó.
        # Nếu không có next, fallback về dashboard:index.
        # Dùng khi create project từ nhiều page/modal khác nhau.
        return redirect(request.POST.get("next") or "dashboard:index")


class ProjectUpdateView(View):
    # Dùng View thay vì UpdateView vì edit cũng submit từ modal/detail page.
    # View này chỉ cần xử lý POST rồi redirect lại project detail.
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            services.update_project(project, form.cleaned_data)
            messages.success(request, "Project updated.")
        else:
            messages.error(request, "Project could not be updated.")
        return redirect("projects:detail", pk=project.pk)


class ProjectDetailView(DetailView):
    # DetailView phù hợp khi cần hiển thị chi tiết một Project theo pk trên URL.
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "project"
        context["project_tasks"] = selectors.get_project_tasks(self.object)
        context["edit_project_form"] = ProjectForm(instance=self.object)
        total = context["project_tasks"].count()
        done = context["project_tasks"].filter(status="done").count()
        context["progress_percent"] = int((done / total) * 100) if total else 0
        context["done_tasks"] = done
        context["total_tasks"] = total
        return context


def project_archive(request, pk):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=pk)
        services.archive_project(project)
        messages.success(request, "Project archived.")
    return redirect("dashboard:index")


def project_restore(request, pk):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=pk)
        services.restore_project(project)
        messages.success(request, "Project restored.")
    return redirect("projects:detail", pk=pk)
