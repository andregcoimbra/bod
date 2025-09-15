from dataclasses import dataclass
from scipy.optimize import minimize
from typing import List

import warnings
from scipy.optimize import OptimizeWarning
warnings.filterwarnings("ignore", category=OptimizeWarning)

import numpy as np

@dataclass
class Result:
    weights: List[float]
    ci: float

def normalizar_dados(dados, orientacao="Min"):
    """
    Normaliza os dados usando o método Min-Max.

    Parâmetros:
        dados (list ou numpy.ndarray): Lista ou array de valores numéricos.
        orientacao (str): "Min" para normalização padrão (0 a 1, onde menor valor é 0 e maior é 1),
                          "Max" para inversão (0 a 1, onde menor valor é 1 e maior é 0).

    Retorno:
        list: Dados normalizados.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")

    minimo = min(dados)
    maximo = max(dados)
    intervalo = maximo - minimo

    if intervalo == 0:
        return [0.5] * len(dados)  # Caso todos os valores sejam iguais

    if orientacao == "Min":
        return [(valor - minimo) / intervalo for valor in dados]
    elif orientacao == "Max":
        return [(maximo - valor) / intervalo for valor in dados]
    else:
        raise ValueError('A orientação deve ser "Min" ou "Max".')


def padronizar_dados(dados):
    """
    Padroniza os dados usando z-score.

    Parâmetros:
        dados (list ou numpy.ndarray): Lista ou array de valores numéricos.

    Retorno:
        list: Dados padronizados.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")

    media = sum(dados) / len(dados)
    variancia = sum((valor - media) ** 2 for valor in dados) / len(dados)
    desvio_padrao = variancia ** 0.5

    if desvio_padrao == 0:
        return [0] * len(dados)  # Caso todos os valores sejam iguais

    return [(valor - media) / desvio_padrao for valor in dados]


class BOD_Calculation:
    def __init__(self, data, aggregation_function=np.dot, bounds=None):
        self.data = np.array(data)
        self.regs, self.n = self.data.shape
        self.aggregation_function = aggregation_function
        
        if bounds is None:
            self.bounds = [(0, 1)] * self.n
        else:
            self.bounds = bounds
    
    # Objective function
    def objective(self, x, idx):
        return -self.aggregation_function(self.data[idx], x)
        
    # Constraints function
    def constraints(self, data):
        cons = []
        for row in data:
            cons.append({'type': 'ineq', 'fun': lambda x, row=row: 1 - self.aggregation_function(row, x)})

        cons.append({'type': 'eq', 'fun': lambda x: 1 - np.sum(x)})  # Constraints sum = 1
        return cons

    # Optmize weights
    def optmizer(self, idx):
        x0 = np.full(self.n, 1 / self.n)

        cons = self.constraints(self.data)

        # Minimize objective function (objective function return negative for maximize)
        result = minimize(lambda x: self.objective(x, idx), x0, constraints=cons, bounds=self.bounds, method='SLSQP')
        
        if result.success:
                return result.x, -result.fun
        else:
            raise ValueError(f"Optimize failure: {result.message}")
    
    def composite_indicator(self, idx, weights):
        if idx >= self.regs or idx < 0:
            raise IndexError("Index outside data limits.")
        
        #Benchmark
        best_ci = 0
        for i in self.data:
            best_ci = max(self.aggregation_function(i, weights), best_ci)

        return self.aggregation_function(self.data[idx], weights) / best_ci
    
    def run(self):
        result = []
        for idx in range(self.regs):
            weights, _ = self.optmizer(idx)
            ci = self.composite_indicator(idx, weights)
            result.append(Result(weights=weights, ci=ci))
        
        return result