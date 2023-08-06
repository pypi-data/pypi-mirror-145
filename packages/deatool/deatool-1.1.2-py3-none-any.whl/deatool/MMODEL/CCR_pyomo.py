from pyomo.environ import *  
import pandas as pd
class MCCR_pyomo():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list,un_output_cols: list, vv, solver):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols+un_output_cols
        self.output = output_cols
        self.solvers = solver

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
        return self.data[self.input+self.output+['TE','PTE','SE','规模报酬分析']]
    
    def __CCRmodel(self, i):
        model = ConcreteModel()
        model.lambdas = Var(self.K, within=NonNegativeReals)
        model.sita = Var(within=NonNegativeReals)
        model.constraints = ConstraintList()
        for p in self.output:
            model.constraints.add(expr=sum(model.lambdas[j] * self.data.loc[j,p] for j in self.K) - self.data.loc[i,p] >=0)
        for q in self.input:
            model.constraints.add(expr=sum(model.lambdas[j] * self.data.loc[j,q] for j in self.K) - model.sita * self.data.loc[i,q] <=0)
        model.obj = Objective(expr=model.sita, sense=minimize)
        solver = SolverFactory(self.solvers)
        opt = solver.solve(model)
        eff = value(model.sita)
        Type = '规模报酬固定' if sum(value(model.lambdas[j]) for j in self.K) == 1 else '规模报酬递增' if sum(value(model.lambdas[j]) for j in self.K)  < 1 else '规模报酬递减'
        return eff, Type
    
    def __BCCmodel(self, i):
        model = ConcreteModel()
        model.lambdas = Var(self.K, within=NonNegativeReals)
        model.sita = Var(within=NonNegativeReals)
        model.constraints = ConstraintList()
        for p in self.output:
            model.constraints.add(expr=sum(model.lambdas[j] * self.data.loc[j,p] for j in self.K) - self.data.loc[i,p] >=0)
        for q in self.input:
            model.constraints.add(expr=sum(model.lambdas[j] * self.data.loc[j,q] for j in self.K) - model.sita * self.data.loc[i,q] <=0)
        model.constraints.add(expr=sum(model.lambdas[j] for j in self.K) == 1)
        model.obj = Objective(expr=model.sita, sense=minimize)
        solver = SolverFactory(self.solvers)
        opt = solver.solve(model)
        eff = value(model.sita)
        return eff

if __name__ == '__main__':
    data = pd.read_excel(r'C:\Users\wangy\Desktop\测试数据.xlsx')
    input_cols = ['输入1','输入2']
    output_cols = ['输出1','输出2']
    un_output_cols = ['非期望输出1']
    model = MCCR_pyomo(data=data, input_cols = input_cols, output_cols = output_cols,un_output_cols = un_output_cols, vv = 1, solver = 'cplex' )
    print(model.res())