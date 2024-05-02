from django.urls import path
from apps.product.views.views_template import views_comment

urlpatterns = [
    # path('comment-create/<int:pk>/', views_comment.CommentReplyCreateView.as_view(), name='comment_create'),
    # # path('admin-comment-list/', views_category.AdminCommentListView.as_view(), name='admin_comment_list'),
    # # path('comment-detail/<int:pk>/', views_category.CommentDetailView.as_view(), name='comment_detail'),
    # # path('comment-update/<int:pk>/', views_category.CommentUpdateView.as_view(), name='comment_update'),
    # path('comment-delete/<int:pk>/', views_comment.CommentDeleteView.as_view(), name='comment_delete'),
]
