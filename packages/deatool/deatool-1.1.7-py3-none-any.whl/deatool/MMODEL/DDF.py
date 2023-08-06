from gurobipy import *
import pandas as pd
class MDDF():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, un_output_cols: list, vv, dd):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols
        self.output = output_cols
        self.unoutput = un_output_cols
        self.key = vv
        self.dd = dd
        
    def res(self):
        TE = []
        for i in self.K:
            eff = self.__DDFmodel(i,self.data)
            TE.append(eff)
        self.data['DDF效率'] = TE
        return self.data[[self.data.columns.values[0]]+self.input+self.output+self.unoutput+['DDF效率']]
    
    def __DDFmodel(self, i,data):
        model = Model('DDF')
        model.Params.LogToConsole = 0
        lambdas = model.addVars(self.K, lb=0, vtype=GRB.CONTINUOUS, name='lambdas')
        beta = model.addVar(vtype = GRB.CONTINUOUS, name = 'beta')
        model.addConstrs(quicksum(lambdas[j] * data.loc[j,p] for j in self.K) 
                         <= (1-beta) * data.loc[i,p]  for p in self.input)
        model.addConstrs(quicksum(lambdas[j] * data.loc[j,q] for j in self.K) 
                         >= (1+beta) * data.loc[i,q]  for q in self.output)
        if self.unoutput!= []:
            if self.dd == '(-x,y,-b)弱可处置性=':
                    model.addConstrs(quicksum(lambdas[j] * data.loc[j,u] for j in self.K) 
                         == (1-beta) * data.loc[i,u]  for u in self.unoutput)
            elif self.dd == '(-x,y,-b)强可处置性>=':
                    model.addConstrs(quicksum(lambdas[j] * data.loc[j,u] for j in self.K) 
                         >= (1-beta) * data.loc[i,u]  for u in self.unoutput)
            elif self.dd == '(-x,y,-b)强可处置性<=':
                    model.addConstrs(quicksum(lambdas[j] * data.loc[j,u] for j in self.K) 
                         <= (1-beta) * data.loc[i,u]  for u in self.unoutput)
        if self.key == '规模报酬可变VRS':
            model.addConstr(quicksum(lambdas[j] for j in self.K) == 1)
        model.setObjective(beta, GRB.MAXIMIZE)
        model.optimize()
        eff = model.getObjective().getValue() if model.status == gurobipy.GRB.Status.OPTIMAL else 'N/A'
        return eff