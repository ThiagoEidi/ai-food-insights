from enum import Enum


class UserRole(str, Enum):
    CLIENT = 'client'
    PARTNER = 'partner'
    ADMIN = 'admin'


class FoodType(str, Enum):
    LANCHES = "lanches"
    MARMITA = "marmita"
    BRASILEIRA = "brasileira"
    JAPONESA = "japonesa"
    CHINESA = "chinesa"
    PIZZA = "pizza"
    MASSAS = "massas"
    MEXICANA = "mexicana"
    VEGETARIANA = "vegetariana"
    SOBREMESAS = "sobremesas"
    AÇAÍ = "acai"
    BEBIDAS = "bebidas"
    SALGADOS = "salgados"
    HAMBURGUER = "hamburguer"
    HOT_DOG = "hot_dog"
