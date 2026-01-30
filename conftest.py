import warnings

# Silenciar advertencia de deprecación de google.generativeai con mensaje multilinea
warnings.filterwarnings(
    "ignore",
    message=r"(?s).*google\.generativeai.*",
    category=FutureWarning,
)