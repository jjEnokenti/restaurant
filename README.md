<h2> Restaurant menu API</h2>

<h4> API </h4>

#### Склонируйте репозиторий по команде:
    $ git clone https://github.com/jjEnokenti/restaurant.git
#### Для запуска докер-контейнера с приложением введите в терминале команду:
    $ docker-compose -f docker-compose.yml up -d
#### Для остановки остановки и удаления контейнеров введите:
    $ docker-compose -f docker-compose.yml down
<h6> Все зависимости и переменные окружения установятся автоматически </h6> 


<h4> Тесты </h4> 

#### Для запуска контейнера с тестами введите команду:
    $ docker-compose -f docker-compose-test.yml up -d
#### Для остановки остановки и удаления контейнеров введите:
    $ docker-compose -f docker-compose-test.yml down
<h6> Все зависимости и переменные окружения установятся автоматически </h6>

<h3> Удаление всех образов </h3>

    $ docker rmi $(docker -a -q)
