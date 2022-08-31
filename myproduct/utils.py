from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from myproduct.custom_exceptions import BadRequestError

class ListCreateUserOwnedView(ListCreateAPIView):
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            author_id = self.request.query_params.get("author", None)
            if not author_id:
                author_id = self.request.user.pk
            if int(author_id) == self.request.user.pk:
                return self.queryset.model.objects.filter(author=user.pk)
            else:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

class RetrieveUpdateDestroyUserOwnedView(RetrieveUpdateDestroyAPIView):

    def get_object(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_object()
        else:
            try:
                return self.queryset.model.objects.get(pk=self.kwargs[self.lookup_field] ,author=user.pk)
            except Exception:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")