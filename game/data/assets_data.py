import enum

class AssetCategory(enum.Enum):
    SUSTENANCE = "sustenance" # Basic food. Maintains population.
    HEALTHCARE = "healthcare" # Medicine. Increases population growth.
    LUXURY = "luxury"         # Electronics/Art. Massive Happiness boost, no pop change.
    CONTRABAND = "contraband" # Weapons/Vices. High tax revenue, but DECREASES population.