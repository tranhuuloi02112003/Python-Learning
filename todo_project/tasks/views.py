from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Task
from .forms import TaskForm

# Create your views here.
def home_page(request):
    tasks = Task.objects.all()
    form = TaskForm() # Default input rỗng
    #Check xem có đang edit không
    edit_id = request.GET.get('edit')
    task_to_edit = None

    if edit_id:
        task_to_edit = Task.objects.get(id = edit_id)
        form = TaskForm(instance=task_to_edit)

    else: 
        form = TaskForm()

    # Nếu người dùng bấm nút "Thêm việc"
    if request.method == "POST":
        # Lấy dữ liệu người dùng vừa nhập
        form = TaskForm(request.POST)

        # Kiểm tra dữ liệu hợp lệ không
        if form.is_valid():
            form.save()
            return redirect("/")  # Xong thì tải lại trang chủ ('/')
    
    # Render ra trang HTML với data
    return render(request, 'tasks/list.html', {
        'tasks': tasks, 
        'form': form, 
        'task_to_edit': task_to_edit
    })

def delete_task(req, pk):
    # Tìm cái task có ID đó, không thấy thì báo lỗi 404
    task = get_object_or_404(Task, id = pk)
    task.delete()
    return redirect("/")

def edit_task(req, pk):
    # Tìm cái task có ID đó
    task = get_object_or_404(Task, id=pk)

    if req.method == "POST":
        form = TaskForm(req.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect("/")

    # Nếu vô tình truy cập bằng đường link (GET request) thì đá về trang chủ chế độ sửa
    return redirect(f"/?edit={task.id}")
