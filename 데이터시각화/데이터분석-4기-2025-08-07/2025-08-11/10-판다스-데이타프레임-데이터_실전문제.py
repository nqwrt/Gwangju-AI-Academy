import pandas as pd
import numpy as np

emp = pd.read_csv("D:\\여름방학특강\\데이터분석-4기-2025-08-07\\2025-08-11\\emp.csv")

emp.info()
print(emp.describe())
print(emp.head())

# 1번) 사원이름과 월급을 출력하시오.
print(emp[['ename','sal']])
print(emp.loc[   :   ,['ename','sal']])

# 2번) 사원번호(empno), 이름(ename), 월급(sal), 직업(job)을 출력하시오.
print(emp[['empno','ename','sal','job']])
print(emp.loc[   :   ,['empno','ename','sal','job']])

# 3번) 월급이 3000 이상인 사원들의 이름과 월급을 출력하시오.
print(emp[['ename','sal']][emp['sal'] >= 3000 ])
#print(emp.loc[  emp['sal'] >= 3000  ,['ename','sal']])

# 4번  직업이  SALESMAN 인 사원들의 이름과 월급과 직업을 출력하시오 
print(emp[['ename','sal']][emp['job'] >= 'SALESMAN' ])
print(emp.loc[  emp['job'] >= 'SALESMAN'  ,['ename','sal']])

# 5번 월급이 1000 에서 3000 사이인 사원들의 이름과 월급을 출력하시오 !
#print(emp[['ename','sal']][emp['job'] >= 'SALESMAN' ])
print(emp.loc[  (emp['sal'] > 1000) & (emp['sal'] < 3000) , ['ename','sal']])
print(emp.loc[  emp['sal'].between(1000,3000) , ['ename','sal']])

# 6번 sal이 가장 높은 사원의 이름과 급여를 출력하시오.
#max_sal = emp['sal'].max()
print(emp.loc[  emp['sal'] == emp['sal'].max() , ['ename','sal']])

# 7번 부서번호별 평균 급여를 계산하시오.
print(emp.groupby("deptno")[['sal']].mean())

# 8번 comm이 NULL인 사원들만 출력하시오. 또는 comm이 NULL인 아닌사원을 출력하시오.
print(emp.loc[  emp['comm'].isnull() ])
print(emp.loc[  ~emp['comm'].isnull() ])


# 9번 이름이 'SMITH'인 사원의 부서번호를 출력하시오.
print(emp.loc[ emp['ename'] == "SMITH" , 'deptno'])

# 10번 매니저 번호가 같은 사원들끼리 묶어 부서번호별 평균 급여를 구하시오.
print(emp.groupby(["mgr","deptno"])['sal'].mean(numeric_only=True))