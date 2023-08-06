from gurobipy import *
import pandas as pd
import numpy as np
class MSBM():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, un_output_cols: list, vv):
        self.data = data
        self.N = list(range(0,data.shape[0]))
        self.input = input_cols
        self.output = output_cols
        self.undes = un_output_cols
        self.key = vv
        
    def res(self):
        if self.undes == []:
            return self.ress()
        else:
            return self.ress_u()
        
    def ress_u(self):
        efficiencies_SBM_model, x_slacks, y_slacks, u_slacks = self.__SBMmodel_u(self.data)
        df_1 = pd.DataFrame(x_slacks)
        df_2 = pd.DataFrame(y_slacks)
        df_3 = pd.DataFrame(u_slacks)
        df = pd.concat([df_1,df_2,df_3],axis=1)
        df.insert(0,'DMU',self.data.iloc[:,0])
        df.insert(1,'效率',efficiencies_SBM_model)    
        return df
    
    def ress(self):
        efficiencies_SBM_model, x_slacks, y_slacks = self.__SBM_model(self.data)
        df_1 = pd.DataFrame(x_slacks)
        df_2 = pd.DataFrame(y_slacks)
        df = pd.concat([df_1,df_2],axis=1)
        df.insert(0,'DMU',self.data.iloc[:,0])
        df.insert(1,'效率',efficiencies_SBM_model)
        return df
    
    def __SBMmodel_u(self, data):
        efficiencies_SBM_model=[]
        x_slacks = {p: [] for p in self.input}
        y_slacks= {q: [] for q in self.output}
        u_slacks = {u: [] for u in self.undes}
        for i in self.N:
            model = Model('SBMu_model')
            model.Params.LogToConsole = 0
            lambdas = model.addVars(self.N,lb=0,vtype=GRB.CONTINUOUS,name='lambdas')
            slacks_input = model.addVars(self.input,lb=0.0,vtype=GRB.CONTINUOUS, name='slacks_input')
            slacks_output = model.addVars(self.output,lb=0.0,vtype=GRB.CONTINUOUS, name='slacks_output')
            slacks_undes = model.addVars(self.undes,lb=0.0,vtype=GRB.CONTINUOUS, name='slacks_undes')
            t =  model.addVar(lb=0.0,vtype=GRB.CONTINUOUS, name='t')
            model.addConstrs((quicksum(lambdas[j] * data.loc[j,p] for j in self.N) + slacks_input[p] -  t * data.loc[i,p] == 0 for p in self.input))
            model.addConstrs((quicksum(lambdas[j] * data.loc[j,q] for j in self.N) - slacks_output[q]-  t * data.loc[i,q] == 0 for q in self.output))
            model.addConstrs((quicksum(lambdas[j] * data.loc[j,u] for j in self.N) + slacks_undes[u]-  t * data.loc[i,u] == 0 for u in self.undes))
            model.addConstr(t + 1/(len(self.output)+ len(self.undes))* (quicksum(slacks_output[q] / data.loc[i,q] for q in self.output) + quicksum(slacks_undes[u] / data.loc[i,u] for u in self.undes)) == 1)
            if self.key == '规模报酬可变VRS':
                model.addConstr(quicksum(lambdas[j] for j in self.N) == t)
            model.setObjective(t - 1/len(self.input) * quicksum(slacks_input[p] / data.loc[i,p] for p in self.input))
            model.optimize()
            eff = model.getObjective().getValue()
            x_slack = {p: slacks_input[p].x / t.x if np.abs(slacks_input[p].x / t.x) >= 1e-7 else 0 for p in self.input}
            y_slack = {q: slacks_output[q].x / t.x if np.abs(slacks_output[q].x / t.x) >= 1e-7 else 0 for q in self.output}
            u_slack = {u: slacks_undes[u].x / t.x if np.abs(slacks_undes[u].x / t.x) >= 1e-7 else 0 for u in self.undes}
            for s_input in self.input:
                x_slacks[s_input].append(x_slack[s_input])
            for s_output in self.output:
                y_slacks[s_output].append(y_slack[s_output])
            for s_undes in self.undes:
                u_slacks[s_undes].append(u_slack[s_undes])
            efficiencies_SBM_model.append(eff) 
        return efficiencies_SBM_model, x_slacks, y_slacks, u_slacks
    
    def __SBM_model(self,data):
        efficiencies_SBM_model=[]
        x_slacks = {i: [] for i in self.input}
        y_slacks= {j: [] for j in self.output}
        for i in self.N:
            model = Model('SBM_model')
            model.Params.LogToConsole = 0
            lambdas = model.addVars(self.N,lb=0,vtype=GRB.CONTINUOUS,name='lambdas')
            slacks_input = model.addVars(self.input,lb=0.0,vtype=GRB.CONTINUOUS, name='slacks_input')
            slacks_output = model.addVars(self.output,lb=0.0,vtype=GRB.CONTINUOUS, name='slacks_output')
            t =  model.addVar(lb=0.0,vtype=GRB.CONTINUOUS, name='t')
            model.addConstrs((quicksum(lambdas[j] * data.loc[j,p] for j in self.N) + slacks_input[p] -  t * data.loc[i,p] == 0 for p in self.input))
            model.addConstrs((quicksum(lambdas[j] * data.loc[j,q] for j in self.N) - slacks_output[q]-  t * data.loc[i,q] == 0 for q in self.output))
            model.addConstr(t + (1/len(self.output)) * quicksum(slacks_output[q] / data.loc[i,q] for q in self.output) == 1)
            if self.key == '规模报酬可变VRS':
                model.addConstr(quicksum(lambdas[j] for j in self.N) == t)
            model.setObjective(t - 1/len(self.input) * quicksum(slacks_input[p] / data.loc[i,p] for p in self.input))
            model.optimize()
            eff = model.getObjective().getValue()
            x_slack = {p: slacks_input[p].x / t.x if np.abs(slacks_input[p].x / t.x) >= 1e-7 else 0 for p in self.input}
            y_slack = {q: slacks_output[q].x / t.x if np.abs(slacks_output[q].x / t.x) >= 1e-7 else 0 for q in self.output}
            for s_input in self.input:
                x_slacks[s_input].append(x_slack[s_input])
            for s_output in self.output:
                y_slacks[s_output].append(y_slack[s_output])       
            efficiencies_SBM_model.append(eff) 
        return efficiencies_SBM_model, x_slacks, y_slacks