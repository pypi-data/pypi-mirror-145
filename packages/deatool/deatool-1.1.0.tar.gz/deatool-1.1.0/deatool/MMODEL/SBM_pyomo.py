from pyomo.environ import *  
import pandas as pd
import numpy as np

class MSBM_pyomo():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, un_output_cols: list, vv, solver):
        self.data = data
        self.N = list(range(0,data.shape[0]))
        self.input = input_cols
        self.output = output_cols
        self.undes = un_output_cols
        self.key = vv
        self.solvers = solver
        
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
            model = ConcreteModel()
            model.lambdas = Var(self.N, within=NonNegativeReals)
            model.slacks_input = Var(self.input, within=NonNegativeReals)
            model.slacks_output = Var(self.output, within=NonNegativeReals)
            model.slacks_undes = Var(self.undes, within=NonNegativeReals)
            model.t =  Var(within=NonNegativeReals)
            model.constraints = ConstraintList()
            for p in self.input:
                model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,p] for j in self.N) + model.slacks_input[p] -  model.t * data.loc[i,p] == 0)
            for q in self.output:
                model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,q] for j in self.N) - model.slacks_output[q]-  model.t * data.loc[i,q] == 0)
            for u in self.undes:
                model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,u] for j in self.N) + model.slacks_undes[u]-  model.t * data.loc[i,u] == 0)
            model.constraints.add(expr=model.t + 1/(len(self.output)+ len(self.undes))* (sum(model.slacks_output[q] / data.loc[i,q] for q in self.output) + sum(model.slacks_undes[u] / data.loc[i,u] for u in self.undes)) == 1)
            if self.key == '规模报酬可变VRS':
                model.constraints.add(expr=sum(model.lambdas[j] for j in self.N) == model.t)
            model.obj = Objective(expr=model.t - 1/len(self.input) * sum(model.slacks_input[p] / data.loc[i,p] for p in self.input))
            solver = SolverFactory(self.solvers)
            opt = solver.solve(model)
            eff = value(model.obj)
            x_slack = {p: value(model.slacks_input[p]) / value(model.t) if np.abs(value(model.slacks_input[p]) / value(model.t)) >= 1e-7 else 0 for p in self.input}
            y_slack = {q: value(model.slacks_output[q]) / value(model.t) if np.abs(value(model.slacks_output[q]) / value(model.t)) >= 1e-7 else 0 for q in self.output}
            u_slack = {u: value(model.slacks_undes[u]) / value(model.t) if np.abs(value(model.slacks_undes[u]) / value(model.t)) >= 1e-7 else 0 for u in self.undes}
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
            model = ConcreteModel()
            model.lambdas = Var(self.N, within=NonNegativeReals)
            model.slacks_input = Var(self.input, within=NonNegativeReals)
            model.slacks_output = Var(self.output, within=NonNegativeReals)
            model.t =  Var(within=NonNegativeReals)
            model.constraints = ConstraintList()
            for p in self.input:
                model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,p] for j in self.N) + model.slacks_input[p] -  model.t * data.loc[i,p] == 0)
            for q in self.output:
                model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,q] for j in self.N) - model.slacks_output[q]-  model.t * data.loc[i,q] == 0)
            model.constraints.add(expr=model.t + (1/len(self.output)) * sum(model.slacks_output[q] / data.loc[i,q] for q in self.output) == 1)
            if self.key == '规模报酬可变VRS':
                model.constraints.add(expr=sum(model.lambdas[j] for j in self.N) == model.t)
            model.obj = Objective(expr=model.t - 1/len(self.input) * sum(model.slacks_input[p] / data.loc[i,p] for p in self.input))
            solver = SolverFactory(self.solvers)
            opt = solver.solve(model)
            eff = value(model.obj)
            x_slack = {p: value(model.slacks_input[p]) / value(model.t) if np.abs(value(model.slacks_input[p]) / value(model.t)) >= 1e-7 else 0 for p in self.input}
            y_slack = {q: value(model.slacks_output[q]) / value(model.t) if np.abs(value(model.slacks_output[q]) / value(model.t)) >= 1e-7 else 0 for q in self.output}
            for s_input in self.input:
                x_slacks[s_input].append(x_slack[s_input])
            for s_output in self.output:
                y_slacks[s_output].append(y_slack[s_output])       
            efficiencies_SBM_model.append(eff) 
        return efficiencies_SBM_model, x_slacks, y_slacks