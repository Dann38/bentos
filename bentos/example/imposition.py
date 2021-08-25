import main as m
import matplotlib.pyplot as plt


bd = m.PopulationData(name_file='bd.xls')
tbl = bd[0] + bd[1] + bd[2] # Выбираем базы данных (нужные таблицы)

tbl.limit_depth(0, 350) # Указываем глубину

tbl.print_locals()
ans = int(input('Выбор локации:'))
num_loc = ans
tbl_loc = tbl.limit_local(num_loc)

kinds = tbl.get_kinds()
tbl_loc.print_kinds()
locals = tbl.get_locals()


a = int(input('Первый график:'))
b = int(input('Второй график:'))
name_graph = 'Наложение видов ' + kinds[a] + '' + kinds[b] + ' (' + locals[num_loc] + ')'

for num in [a, b]:

    name = kinds[num] + '\n' + locals[num_loc]

    tbl_kind = tbl_loc.limit_kind(num)

    res = tbl_kind.filter_columns([0, 7, 11])
    res.group_by_column([0, 1])
    res.group_date()
    print(res)
    res.plot([2], name=name, stl='--')

plt.legend()
plt.show()
# plt.savefig(name_graph)