### Restaurant menu API
### Зависимости:
1. У меню есть подменю, которые к ней привязаны. 
2. У подменю есть блюда.
### Условия:
1. Блюдо не может быть привязано напрямую к меню, минуя подменю. 
2. Блюдо не может находиться в 2-х подменю одновременно. 
3. Подменю не может находиться в 2-х меню одновременно. 
4. Если удалить меню, должны удалиться все подменю и блюда этого меню. 
5. Если удалить подменю, должны удалиться все блюда этого подменю. 
6. Цены блюд выводить с округлением до 2 знаков после запятой. 
7. Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню. 
8. Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю. 
9. Во время запуска тестового сценария БД должна быть пуста.