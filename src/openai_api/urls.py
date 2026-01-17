from django.urls import path
from . import views

urlpatterns = [
    # Chat completions endpoint
    path(
        "chat/completions", views.ChatCompletionsView.as_view(), name="chat_completions"
    ),
    # Embeddings endpoint
    path("embeddings", views.EmbeddingsView.as_view(), name="embeddings"),
    # Moderations endpoint
    path("moderations", views.ModerationsView.as_view(), name="moderations"),
    # Images generation endpoint
    path(
        "images/generations",
        views.ImagesGenerationsView.as_view(),
        name="images_generations",
    ),
    # Models listing endpoint
    path("models", views.ModelsView.as_view(), name="models"),
    # Model details endpoint
    path(
        "models/<str:model_id>", views.ModelDetailsView.as_view(), name="model_details"
    ),
    # Vector stores endpoints
    path(
        "vector_stores",
        views.VectorStoreListCreateView.as_view(),
        name="vector_stores_list_create",
    ),  # GET, POST
    path(
        "vector_stores/<str:vector_store_id>",
        views.VectorStoreRetrieveUpdateDeleteView.as_view(),
        name="vector_store_retrieve_update_delete",
    ),  # GET, POST, DELETE
    path(
        "vector_stores/<str:vector_store_id>/search",
        views.VectorStoreSearchView.as_view(),
        name="vector_store_search",
    ),  # POST
]
