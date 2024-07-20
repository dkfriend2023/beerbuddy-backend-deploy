# BeAbuddy-backend

🍻 Server-Side of BeABuddy Developed with Django

- API Document:[🍻BeABuddy🍻](https://www.notion.so/API-Documentation-1d3c8ffa841045258f1fdc07355f48d3)
- 관리자 계정 정보:[개발Repo ReadMe 확인](https://github.com/dkfriend2023/beerbuddy-backend-legacy/blob/main/README.md)
<br>

<hr>

##### **,,,절대 python [manage.py](http://manage.py) runserver로 실행하면 안됩니다,,,,,**

### 1) 서버 코드 수정하거나 gunicorn script 변경 시(로직부분)

1. sudo systemctl restart dkfriend.service
2. sudo systemctl status dkfriend.service 확인하기
3. 에러 로그 보기: `tail -n 100 /home/ubuntu/BEERBUDDY/error.log`

### 2) 정적파일이나 nginx script 변경시

1. sudo systemctl restart nginx
2. sudo systemctl status nginx
3. 에러 로그 보기: `sudo tail -n 100 /var/log/nginx/error.log`

### 3) 장고 로그 보기 
- `tail -n 100 /home/ubuntu/BEERBUDDY/dkfriend-backend-latest/dkfriend_back/django_debug.log`
