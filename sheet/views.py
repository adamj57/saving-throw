from rest_framework.viewsets import ModelViewSet

from sheet.serializers import CharacterSheetSerializer


class CharacterSheetViewSet(ModelViewSet):
    serializer_class = CharacterSheetSerializer

    def get_queryset(self):
        return self.request.user.character_sheets.all()
