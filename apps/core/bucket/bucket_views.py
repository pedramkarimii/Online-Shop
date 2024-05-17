from django.shortcuts import render, redirect
from django.views import View
from .tasks import delete_object_task, all_buckets_objects_task, download_object_task
from django.contrib import messages


class BucketView(View):
    template_name = 'bucket/bucket.html'
    http_method_names = ['get']

    def get(self, request):
        objects = all_buckets_objects_task()
        print('A' * 100, objects)
        return render(request, self.template_name, {'objects': objects})


class BucketDeleteObjView(View):
    http_method_names = ['get', 'delete']

    def get(self, request, key):
        delete_object_task.delay(key)
        messages.success(request, 'Your objects will be delete soon', extra_tags='info')
        return redirect('bucket_home')


class BucketDownloadObjView(View):
    http_method_names = ['get']

    def get(self, request, key):
        download_object_task.delay(key)
        messages.success(request, 'Your download will be start soon', extra_tags='info')
        return redirect('bucket_home')
