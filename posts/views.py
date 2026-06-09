from django.shortcuts import render, redirect
from .models import Post

from nlp_engine.detector import (
    detect_threat,
    calculate_risk
)

from nlp_engine.models import Threat
from alerts.models import Alert


def post_list(request):

    posts = Post.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'posts.html',
        {
            'posts': posts
        }
    )


def add_post(request):

    if request.method == 'POST':

        content = request.POST['content']

        category = detect_threat(
            content
        )

        risk_score = calculate_risk(
            category
        )

        Post.objects.create(
            source=request.POST['source'],
            author=request.POST['author'],
            content=content,
            threat_score=risk_score
        )

        if category != 'Unknown':

            Threat.objects.create(
                threat_name=content[:50],
                category=category,
                risk_score=risk_score
            )

            if risk_score >= 80:

                Alert.objects.create(
                    title='High Risk Threat Detected',
                    risk_level='High',
                    description=content
                )

        return redirect('posts')

    return render(
        request,
        'add_post.html'
    )


def edit_post(request, pk):

    post = Post.objects.get(id=pk)

    if request.method == 'POST':

        post.source = request.POST['source']
        post.author = request.POST['author']
        post.content = request.POST['content']
        post.threat_score = request.POST['threat_score']

        post.save()

        return redirect('posts')

    return render(
        request,
        'edit_post.html',
        {
            'post': post
        }
    )


def delete_post(request, pk):

    post = Post.objects.get(id=pk)

    if request.method == 'POST':

        post.delete()

        return redirect('posts')

    return render(
        request,
        'delete_post.html',
        {
            'post': post
        }
    )