from django.shortcuts import render, redirect
from apps.core.permission.template_permission_admin import CRUD
from .tasks import delete_object_task, all_buckets_objects_task, download_object_task
from django.contrib import messages


class BucketView(CRUD.AdminPermissionRequiredMixinView):
    """
    Class-based view for handling bucket-related operations.
    Inherits from AdminPermissionRequiredMixinView and provides the necessary methods.
    """
    template_name = 'bucket/bucket.html'
    http_method_names = ['get']

    def get(self, request):
        """
        Retrieve all objects from the S3 bucket and render the template with the objects data.
        Returns:
            HttpResponse: The rendered template with the objects data.
        """
        objects = all_buckets_objects_task()
        return render(request, self.template_name, {'objects': objects})


class BucketDeleteObjView(CRUD.AdminPermissionRequiredMixinView):
    """
    Class-based view for handling the deletion of objects from the S3 bucket.
    Inherits from AdminPermissionRequiredMixinView and provides the necessary methods.
    """
    http_method_names = ['get', 'delete']

    def get(self, request, key):
        """
        Render the confirmation template for deleting an object.
        Returns:
            HttpResponse: The rendered confirmation template.
        """
        delete_object_task.delay(key)
        messages.success(request, 'Your objects will be delete soon', extra_tags='info')
        return redirect('bucket_main')


class BucketDownloadObjView(CRUD.AdminPermissionRequiredMixinView):
    """
    Class-based view for handling the download of objects from the S3 bucket.
    Inherits from AdminPermissionRequiredMixinView and provides the necessary methods.
    """
    http_method_names = ['get']

    def get(self, request, key):
        download_object_task.delay(key)
        messages.success(request, 'Your download will be start soon', extra_tags='info')
        return redirect('bucket_main')
