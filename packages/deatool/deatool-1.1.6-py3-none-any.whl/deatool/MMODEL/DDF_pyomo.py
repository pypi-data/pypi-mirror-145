from pyomo.environ import *  
import pandas as pd

class MDDF_pyomo():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, un_output_cols: list, vv, dd,solver):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols
        self.output = output_cols
        self.unoutput = un_output_cols
        self.key = vv
        self.dd = dd
        self.solvers = solver
        
    def res(self):
        TE = []
        for i in self.K:
            eff = self.__DDFmodel(i,self.data)
            TE.append(eff)
        self.data['DDF效率'] = TE
        return self.data[[self.data.columns.values[0]]+self.input+self.output+self.unoutput+['DDF效率']]
    
    def __DDFmodel(self, i,data):
        model = ConcreteModel()
        model.lambdas = Var(self.K, within=NonNegativeReals)
        model.beta = Var(within=NonNegativeReals)
        model.constraints = ConstraintList()
        for p in self.input:
            model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,p] for j in self.K) 
                            <= (1-model.beta) * data.loc[i,p])
        for q in self.output:
            model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,q] for j in self.K) 
                            >= (1+model.beta) * data.loc[i,q] )
        if self.unoutput!= []:
            if self.dd == '(-x,y,-b)弱可处置性=':
                for u in self.unoutput:
                    model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,u] for j in self.K) 
                         == (1-model.beta) * data.loc[i,u])
            elif self.dd == '(-x,y,-b)强可处置性>=':
                for u in self.unoutput:
                    model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,u] for j in self.K) 
                         >= (1-model.beta) * data.loc[i,u])
            elif self.dd == '(-x,y,-b)强可处置性<=':
                for u in self.unoutput:
                    model.constraints.add(expr=sum(model.lambdas[j] * data.loc[j,u] for j in self.K) 
                         <= (1-model.beta) * data.loc[i,u])
        if self.key == '规模报酬可变VRS':
            model.constraints.add(expr=sum(model.lambdas[j] for j in self.K) == 1)
        model.obj = Objective(expr=model.beta, sense=maximize)
        solver = SolverFactory(self.solvers)
        opt = solver.solve(model)
        eff = value(model.obj)
        return eff