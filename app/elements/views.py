from rest_framework.viewsets import ModelViewSet

from elements.models import Word, Character, Grammar


class WordModelViewSet(ModelViewSet):
    queryset = Word.objects.all()


class CharacterModelViewSet(ModelViewSet):
    queryset = Character.objects.all()


class GrammarModelViewSet(ModelViewSet):
    queryset = Grammar.objects.all()
