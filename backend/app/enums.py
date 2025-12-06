from enum import Enum


class OrderStatus(Enum):
    PENDING = 'Pendente'
    PREPARING = 'Em Preparação'
    DELIVERED = 'Entregue'
    CANCELED = 'Cancelado'
