from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Post, Comment

# コメント、返信フォーム
CommentForm = forms.modelform_factory(Comment, fields=('text', ))


class PostList(generic.ListView):
    """記事一覧"""
    model = Post


class PostDetail(generic.DetailView):
    """記事詳細"""
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['comment_list'] = self.object.comment_set.filter(parent__isnull=True)
        return context


def comment_create(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('comcom:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'comcom/comment_form.html', context)


def reply_create(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.save()
        return redirect('comcom:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'comcom/comment_form.html', context)
