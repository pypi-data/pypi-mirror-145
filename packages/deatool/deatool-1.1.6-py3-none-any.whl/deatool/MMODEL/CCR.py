from gurobipy import *
import pandas as pd
class MCCR():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list,un_output_cols: list, vv):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols+un_output_cols
        self.output = output_cols

    def res(self):
        TE = []
        PTE = []
        SE = []
        Type = []
        for i in self.K:
            eff_C, Types = self.__CCRmodel(i)
            eff_B = self.__BCCmodel(i)
            eff_S = eff_C/eff_B
            TE.append(eff_C)
            PTE.append(eff_B)
            SE.append(eff_S)
            Type.append(Types)
        self.data['TE'] = TE
        self.data['PTE'] = PTE
        self.data['SE'] = SE
        self.data['规模报酬分析'] = Type
        return self.data[[self.data.columns.values[0]]+self.input+self.output+['TE','PTE','SE','规模报酬分析']]
    
    def __CCRmodel(self, i):
        model = Model('CCR')
        model.Params.LogToConsole = 0
        model.Params.LogFile= 'result.log'
        lambdas = model.addVars(self.K, lb=0, vtype=GRB.CONTINUOUS, name='lambdas')
        sita = model.addVar(vtype = GRB.CONTINUOUS, name = 'sita')
        model.addConstrs(quicksum(lambdas[j] * self.data.loc[j,p] for j in self.K) - self.data.loc[i,p] >=0 for p in self.output)
        model.addConstrs(quicksum(lambdas[j] * self.data.loc[j,q] for j in self.K) - sita * self.data.loc[i,q] <=0 for q in self.input)
        model.setObjective(sita, GRB.MINIMIZE)
        model.optimize()
        eff = model.getObjective().getValue() if model.status == gurobipy.GRB.Status.OPTIMAL else 'N/A'
        Type = '规模报酬固定' if lambdas.sum().getValue() == 1 else '规模报酬递增' if lambdas.sum().getValue() < 1 else '规模报酬递减'
        return eff, Type
    
    def __BCCmodel(self, i):
        model = Model('BCC')
        model.Params.LogToConsole = 0
        lambdas = model.addVars(self.K, lb=0, vtype=GRB.CONTINUOUS, name='lambdas')
        sita = model.addVar(vtype = GRB.CONTINUOUS, name = 'sita')
        model.addConstrs(quicksum(lambdas[j] * self.data.loc[j,p] for j in self.K) - self.data.loc[i,p] >=0 for p in self.output)
        model.addConstrs(quicksum(lambdas[j] * self.data.loc[j,q] for j in self.K) - sita * self.data.loc[i,q] <=0 for q in self.input)
        model.addConstr(quicksum(lambdas[j] for j in self.K) == 1)
        model.setObjective(sita, GRB.MINIMIZE)
        model.optimize()
        eff = model.getObjective().getValue() if model.status == gurobipy.GRB.Status.OPTIMAL else 'N/A'
        return eff