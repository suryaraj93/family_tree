from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import deque
from .models import Member, Relationship
from .serializers import MemberSerializer, RelationshipSerializer
from rest_framework.permissions import IsAuthenticated


class MemberView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetailView(APIView):
    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return None

    def get(self, request, pk):
        member = self.get_object(pk)
        if member is None:
            return Response(
                {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        member = self.get_object(pk)
        if member is None:
            return Response(
                {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        member = self.get_object(pk)
        if member is None:
            return Response(
                {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
            )
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RelationshipView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        relationships = Relationship.objects.all()
        serializer = RelationshipSerializer(relationships, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RelationshipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PathApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from_member_id = request.query_params.get("from_member_id")
        to_member_id = request.query_params.get("to_member_id")

        if not from_member_id or not to_member_id:
            return Response(
                {"error": "Both 'from_member_id' and 'to_member_id' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from_member = Member.objects.get(pk=from_member_id)
        except Member.DoesNotExist:
            return Response(
                {"error": f"Member with id '{from_member_id}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            to_member = Member.objects.get(pk=to_member_id)
        except Member.DoesNotExist:
            return Response(
                {"error": f"Member with id '{to_member_id}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        paths = self.find_paths_between(from_member, to_member)

        return Response({"paths": paths})

    def find_paths_between(self, from_member, to_member):
        queue = deque([[from_member]])
        visited = set()
        paths = []

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current in visited:
                continue

            visited.add(current)

            for relationship in current.relationships_from.all():
                new_path = list(path)
                new_path.append(relationship.member_to)

                if relationship.member_to == to_member:
                    paths.append([member.fullname for member in new_path])
                else:
                    queue.append(new_path)

        return paths
