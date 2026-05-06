from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Task
from .forms import TaskForm

# Create your views here.
def home_page(request):
    # Hiển thị theo thứ tự từ mới nhất
    tasks = Task.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status')

    if status_filter == 'done':
        tasks = tasks.filter(completed = True)
    elif status_filter == 'active':
        tasks = tasks.filter(completed = False)

    form = TaskForm() # Default input rỗng
    #Check xem có đang edit không
    edit_id = request.GET.get('edit')
    task_to_edit = None

    if edit_id:
        # 1. Nếu dùng: Task.objects.get(id=edit_id)
        #    -> Sập web (Lỗi 500 Server Error) nếu người dùng gõ bậy bạ một ID không có thực lên thanh URL.
        # 2. LUÔN LUÔN DÙNG: get_object_or_404(Task, id=edit_id)
        #    -> An toàn tuyệt đối! Nếu không tìm thấy, nó sẽ ném ra trang "Lỗi 404 - Không tìm thấy" (chuyên nghiệp như các web lớn).
        task_to_edit = get_object_or_404(Task, id=edit_id)
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
            return redirect('home')  # Xong thì tải lại trang chủ ('/')
    
    # Render ra trang HTML với data
    return render(request, 'tasks/list.html', {
        'tasks': tasks, 
        'form': form, 
        'task_to_edit': task_to_edit,
        'current_status': status_filter
    })

def delete_task(req, pk):
    # Tìm cái task có ID đó, không thấy thì báo lỗi 404
    task = get_object_or_404(Task, id = pk)

    task.delete()
    return redirect('home')

def edit_task(req, pk):
    # Tìm cái task có ID đó
    task = get_object_or_404(Task, id=pk)

    if req.method == "POST":
        form = TaskForm(req.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('home')

    # Nếu vô tình truy cập bằng đường link (GET request) thì đá về trang chủ chế độ sửa
    return redirect(f"/?edit={task.id}")
