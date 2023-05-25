### Методы целочисленного програмирования (MIP)
Формализация задачи в канонической постановке: 
Пусть на множестве объектов ${N}$ имеет место вещественная полуматрица $С$ :

$$\begin{vmatrix}
NULL& c_{01} & c_{02} & ...  & ...&c_{0N}\\
NULL& NULL & c_{12} & ...  & ... &c_{1N}\\
NULL& NULL& NULL & c_{2_3} & ...&c_{2N}\\
...& ... & ... & ... & ... & ... \\
NULL& NULL& ...&c_{ij} &... &c_{iN}\\
...& ... & ... & ... & ... & ... \\
NULL& NULL& NULL &... &NULL &c_{NN}\\
\end{vmatrix}$$

, задающая силу связи между всеми парами объектов. Тогда $X$ :

$$\begin{vmatrix}
NULL& x_{01} & x_{02} & ...  & ...&x_{0N}\\
NULL& NULL & x_{12} & ...  & ... &x_{1N}\\
NULL& NULL& NULL & x_{2_3} & ...&x_{2N}\\
...& ... & ... & ... & ... & ... \\
NULL& NULL& ...&x_{ij} &... &x_{iN}\\
...& ... & ... & ... & ... & ... \\
NULL& NULL& NULL &... &NULL &x_{NN}\\
\end{vmatrix}$$

- бинарная полуматрица, определяющая вариант группирования объектов. Т.о. каждый элемент матрицы, принимающий единичное значение указывает на то, что соответствующие объекты $i$ и $j$ попадают в одну группу.

Тогда ограничение на размер группы задается следующим неравенством: для любого $i$, должно выполнятся следующее уравнение:

$$\sum_{j=0}^{N} x_{ij} \le maxGR$$

Введем дополнительное ограничение "треугольника" на группировку пар объектов: Если пара объектов $i$ и $j$ в одной группе:  $x_{ij} =1$ , а также объекты $j$ и $k$ в одной группе: $x_{jk} =1$ , то объекты $i$ и $к$ также должны быть в группе:  $\Rightarrow x_{ik} =1$

Т.е. для любого $i,j 	\in \{N\}$, должно выполнятся следующее уравнение: $$x_{ij} + x_{ij +1} = x_{jj+1} +1$$

Отметим, что вводить полные матрицы $C$ и $X$ было бы избыточно, как по числу переменных и уравнений ограничений, так и с точки зрения расхода памяти.

Группировку, т.е. поиск бинарной полуматрицы $X$ следует провести так, чтобы достигался максимум целевой функции: 
$$\sum_{i=0}^{N}\sum_{j=i}^{N} x_{ij}*c_{ij} \rightarrow max$$


### Алгоритм
Пояснить какие алгоритмы применялись в библиотеках: Симплексы. барьерный метод (эллипсойды, методы внутренней точки), метод ветвей и границ
* PULP_CBC_CMD - primarily uses the Simplex algorithm for LP problems and the branch-and-cut method for MIP problems.
* COIN_CMD - Simplex Algorithm, Barrier method, branch-and-cut
* GLPK_CMD - Simplex Algorithm, Barrier method, branch-and-cut
* CP-SAT - uses is the Conflict-Driven Clause Learning (CDCL) algorithm, which is a type of SAT solving algorithm.
* SCIP - Branch and Bound(core), cutting plane methods, primal heuristics, Constraint propagation, conflict analysis 
     
### Временная и пространственная сложность алгоритма
ДОРАБОТАТЬ!!!

## Функции
* ReadSource - чтение эксель-датафрейма
* calcCross - нахождение временного интервала между двумя вершинами
* calcRowOverlap - преображение двух временных интервалов в часы
* removeSameElemtPairs - удаление дубликатов
* getAprovePairs - получение пар элементов из списка
* merge_lists - функция для преобразования найденых ребер в группы

## LP solvers benchmark
n(количество вершин) = 30

<p>
gurobi trial ограничение сработало на n=30

xpress trial лимит на 5000 рядов и колонок
</p>

| Library | Solver       | Time     |
|---------|--------------|----------|
| pulp  | PULP_CBC_CMD | ~8 sec   |
|  pulp | COIN_CMD     | ~12 sec  |
| pulp  | GLPK_CMD     | ~18 sec  |
| ortools  | SAT          | ~1.5 sec |
| ortools  | CP-SAT       | ~1.5 sec |
| ortools  | SCIP         | ~7 sec   |
| ortools  | CBC          | ~17 sec  |

