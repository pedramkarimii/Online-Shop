from django.shortcuts import render, redirect
from apps.core.permission.template_permission_admin import CRUD
from .tasks import delete_object_task, all_buckets_objects_task, download_object_task
from django.contrib import messages


class BucketView(CRUD.AdminPermissionRequiredMixinView):
    template_name = 'bucket/bucket.html'
    http_method_names = ['get']

    def get(self, request):
        objects = all_buckets_objects_task()
        return render(request, self.template_name, {'objects': objects})


class BucketDeleteObjView(CRUD.AdminPermissionRequiredMixinView):
    http_method_names = ['get', 'delete']

    def get(self, request, key):
        delete_object_task.delay(key)
        messages.success(request, 'Your objects will be delete soon', extra_tags='info')
        return redirect('bucket_main')


class BucketDownloadObjView(CRUD.AdminPermissionRequiredMixinView):
    http_method_names = ['get']

    def get(self, request, key):
        download_object_task.delay(key)
        messages.success(request, 'Your download will be start soon', extra_tags='info')
        return redirect('bucket_main')
