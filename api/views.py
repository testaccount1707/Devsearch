from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from projects.models import Project
from .serializers import ProjectSerializer

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {"GET": 'api/projects'},
        {"GET": 'api/projects/1'},
        {"POST": 'api/projects/id/vote'},
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    # print("USER:", request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request,pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    print('DATA', data)

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)