from projects.forms import ProjectForm
from projects.selectors import get_active_projects
from tasks.forms import TaskForm


def app_shell(request):
    # Context processor dùng cho layout chung của app.
    # Function này được khai báo trong settings.TEMPLATES["OPTIONS"]["context_processors"],
    # nên mỗi lần Django render template, các biến bên dưới sẽ tự có trong context.
    return {
        "sidebar_projects": get_active_projects(),
        "task_form": TaskForm(),
        "project_form": ProjectForm(),
    }
