# Поиск и группировка объектов на графах
## Описание задачи
Дано множество объектов, каждый объект характеризуется набором свойств, для любой пары объектов задается отношение на основе сопоставления их свойств. 
Например, для объектов типа производственные задания имеют место моменты начала и завершения, т.о. отношение между парами заданий может быть задано, как пересечение их временных  интервалов.
Необходимо объединить задания в  группы не более указанного количества  таким образом, чтобы их временные интервалы  пересекались наибольшим образом.

## Подходы к  решению
### Методы вычислений на графах
Предполагется, что каждый объект представлен, как  вершина графа, т.о. отношения между парами объектов отображаются в виде ребер графа.
Тогда вес ребра  отображает степень отношения между объектами.
Образуется полносвязный граф. (граф может быть неполносвязным в случаях, когда ребра с неудовлетворительным весом удаляются из графа!)  
В таком представлении задачи необходимо  найти наилучшее разбиение множества вершин на непесекающиеся подмножества (клики, т.е. полносвязные компоненты) размерности не больше указанного занчения, для которых сумма  весов ребер клики (вес клики) имеет наибольшее значение.  

### Алгоритм
* Инициализация графа      
* find k-clique communities
* Find all cliques in k-clique communities among all graph
* prepare_clique - расчет весов клик
* Сортировка клик по убыванию веса
* Прохождение по списку клик: на каждой итерации отбирается клика, если все вершины клики не были рассмотрены на предыд.итериациях, цикл прекращается, когда все вершины графа покрыты отобранными кликами. 

### Временная и пространственная сложность алгоритма
ДОРАБОТАТЬ!!!
* find k-clique communities ( nx.find_cliques = O(3^n/3) - )



## Функции 
* Построение графа - [graph_structure.py](https://github.com/plaguedoctor39/graph-search/blob/main/func/graph_structure.py)
  * graphPreparation - создание графа
  * DrawGraph - отрисовка графа
* Вспомогательные функции для вычислений - [Auxiliary_functions.py](https://github.com/plaguedoctor39/graph-search/blob/main/func/Auxiliary_functions.py)
  * ReadSource - чтение эксель-датафрейма
  * calcCross - нахождение временного интервала между двумя вершинами
  * calcRowOverlap - преображение двух временных интервалов в часы
  * removeSameElemtPairs - удаление дубликатов
  * getAprovePairs - получение пар элементов из списка
  * CalcFitness - преобразование списка вершин в список элементов для датафрейма
  * FormatResult - с использованием CalcFitness преобразование в результирующий датафрейм
  * do_process - функция для использования параллельности
* Поиск лучших групп(клик) - [search.py](https://github.com/plaguedoctor39/graph-search/blob/main/func/search.py)
  * findCliquesSizeK - нахождение клик размера k
  * process - функция для параллельности
  * runShipsAllocation - нахождение клик, их отбор и получение лучших
  * prepare_clique - преобразование списка клик в отсортированный по весу клики список
  * process_clique_nx - отбор лучших клик из полученного в prepare_clique списка.

## Оптмизация производительности

<p> Изначальное время выполнения программы составляло ~27 минут, было выдвинуто предположение, что это проблема библиотеки networkx, которая написана на чистом python.
Была попробована библиотека graph_tool, в ходе написания было выясненно, что в graph_tool отсутствуют многие методы упрощающие работу с графами. 
Так например поиск сообществ клик. Также разницы в скорости выполнения не было. Оказалось, долгое выполнение кода следствие использования питоновских циклов и pandas для работы с большим объемом данных. </p>

<p> Первым делом была добавленна параллельность (joblib.Parallel) для обработки каждой клики. Это сократило время выполнения с ~27 минут до 8 минут. </p>

Функция [prepare_clique](https://github.com/plaguedoctor39/graph-search/blob/ae08a00a8373da8b163811c4ba8370ccdd448495/func/search.py#LL70C44-L70C44).


```
all_cliques_with_weights = all_cliques_with_weights + Parallel(n_jobs=-1, timeout=99999)(delayed(process_clique_nx)(clique, g) for clique in reversed(k_cliques)) 
```

<p> Далее был изменен подход к формированию результирующего датафрейма. Изначально все клики были представленны в виде массива numpy, далее для каждой найдена сумма весов и потом клики с суммами весов были отсортированы по сумме весов.
После сортировки применяется функция для поиска лучших групп(клик) с вхождением всех вершин. Как итог вместо >2млн строк в датафрейме получаем сразу 16 лучших на 80 вершинах.
Это сократило время выполнения с 8 минут до 1.5 минуты. </p>

[Код](https://github.com/plaguedoctor39/graph-search/blob/83eafe639278b62d02daa5d2c7a2255c73e27fa3/search.py#L95)

<p> Следующим шагом было решено попробовать использовать метод библиотеки networkx get_edge_attributes упрощенного поиска ребер, что дало время выполнения в 50 секунд при 80 вершинах. </p>

` _edges = nx.get_edge_attributes(g.subgraph(clique), 'weight')`

<p> Последним шагом для оптимизации было урезание weight_threshold с -20 до -1 для уменьшения количества клик, так как клики с отрицательными весами нам для результата не нужны.
Это сократило время выполнения с 50 секунд до 30 секунд на 80 вершинах. </p>

<p> При попытке проверить работоспособность кода на 200 вершинах всплыло предупреждение о нехватке оперативной памяти для выполнения, что говорит о необходимости в больших вычислительных мощностях чем личный ноутбук.
На 100 вершинах код выполнялся 1.5 минуты. </p>

<p> Как итог, предполагается, что код будет отрабатывать в приемлемое время на больших вычистельных мощностях, так как используется параллельность(joblib.Parallel), которое использует по возможности максимально допустимое количество ядер процессора для параллельной обработки в цикле. </p>

<p> Если сравнивать networkx и graph_tool, нельзя не подметить удобство и обширность методов и готовых алгоритмов реализованных в networkx, что делает работу с этой библиотекой значительно проще. Что говоря о времени выполнения, то на данной задаче разницы во времени выполнения между networkx и graph_tool, если брать создание и заполнение графа, выявленно не было.
В остальном же с использованием методов networkx, которые отствуют в graph_tool, код с networkx выполнялся быстрее. </p>

## Graph approach benchmark
Бенчмарки зависят от мощностей машины, на которой будет запускаться код. В данном случае 10 CPU.

WEIGHT_THRESHOLD отсутствует

| n | Time     |
|----|----------|
| 10  |  761 ms    |
| 30  |  3.86 s    |
| 80  |  17min 11s    |
| 200 | недостаточно вычислительных мощностей     |

WEIGHT_THRESHOLD = -19

| n   | Time                                  |
|-----|---------------------------------------|
| 10  | 533 ms                                |
| 30  | 1.89 s                                |
| 80  |  31.3 s                                     |
| 200 | недостаточно вычислительных мощностей |

WEIGHT_THRESHOLD = -1

| n  | Time     |
|-----|----------|
| 10  |  563 ms    |
| 30  |  1.87 s    |
| 80  |  30.1 s    |
| 200 |  недостаточно вычислительных мощностей    |

WEIGHT_THRESHOLD = 3

| n  | Time   |
|-----|--------|
| 10  | 489 ms |
| 30  | 1.62 s |
| 80  | 16.2 s |
| 200 | недостаточно вычислительных мощностей       |

### Методы целочисленного програмирования (MIP)
Формализация задачи в канонической постановке: 

Пусть на множестве объектов {N} имеет место вещественная полуматрица С, задающая силу связи между всеми парами объектов. 
Тогда X - бинарная полуматрица, определяющая вариант группирования объектов. Т.о. каждый элемент матрицы, принимающий единичное значение указывает на то, что соответствующие объекты i и j попадают в одну группу. 

Тогда ограничение на размер группы задается следующим неравенством:
для любого i, должно выполнятся следующее уравнение:
\begin{align*}
\[ \sum_{j=0}^{N} x_i_j <= maxGR \]
\end{align*}

Введем дополнительное ограничение "треугольника" на группировку пар объектов:
Если пара объектов i и j в одной группе: \begin{align*} \[ x_i_j =1 \] , а также объекты j и k в одной группе: \begin{align*} \[ x_j_k =1 \] \end{align*}
, то объекты i и к также должны быть в группе \begin{align*} \[\rightarrow x_i_k =1 \] \end{align*}

Т.е. для любого i, должно выполнятся следующее уравнение: \begin{align*} \[ x_i_j + x_i_j_+_1 = x_j_j_+_1 +1 \] \end{align*}

Отметим, что вводить полные матрицы C и X было бы избыточно, как по числу переменных и уравнений ограничений, так и с точки зрения расхода памяти.

Группировку, т.е. поиск бинарной полуматрицы X следует провести так, чтобы достигался максимум целевой функции:
\begin{align*}
\[ \sum_{i=0}^{N}\sum_{j=i}^{N} x_i_j*c_i_j \rightarrow max \] 
\end{align*}

### Алгоритм
Пояснить какие алгоритмы применялись в библиотеках: Симплексы. барьерный метод (эллипсойды, методы внутренней точки), метод ветвей и границ
* PULP_CBC_CMD - precompiled version of cbc provided with the package
* COIN_CMD - The COIN CLP/CBC LP solver now only uses cbc
* GLPK_CMD - GLPK LP solver
* CP-SAT - solver uses an algorithm that's built on principles of both Constraint Programming (CP) and Boolean Satisfiability (SAT)
* SCIP - branch-and-bound algorithm and dual simplex algorithm
     
### Временная и пространственная сложность алгоритма
ДОРАБОТАТЬ!!!

## Функции
Расписать вызов функций!

## LP solvers benchmark
n = 30

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

