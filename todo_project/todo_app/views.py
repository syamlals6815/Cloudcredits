from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task

def todo_list(request):
    tasks = Task.objects.all()
    
    if request.method == 'POST':
        # Add a new task
        if 'add_task' in request.POST:
            title = request.POST.get('title')
            if title:
                Task.objects.create(title=title)
                messages.success(request, 'Task added successfully!')
            return redirect('todo_list')
        
        # Mark task as completed
        elif 'complete_task' in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.completed = not task.completed
                task.save()
                status = "completed" if task.completed else "marked as incomplete"
                messages.success(request, f'Task {status}!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found!')
            return redirect('todo_list')
        
        # Delete task
        elif 'delete_task' in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                messages.success(request, 'Task deleted successfully!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found!')
            return redirect('todo_list')
    
    return render(request, 'todo_app/todo_list.html', {'tasks': tasks})