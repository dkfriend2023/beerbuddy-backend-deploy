# beerbuddy-backend-deploy

### **,,,절대 python [manage.py](http://manage.py) runserver로 실행하면 안됩니다,,,,,**

서버 코드 수정하거나 gunicorn script 변경 시(로직부분)

1. sudo systemctl restart dkfriend.service
2. sudo systemctl status dkfriend.service 확인하기
3. 에러 로그 보기: `tail -n 100 /home/ubuntu/BEERBUDDY/error.log`

정적파일이나 nginx script 변경시

1. sudo systemctl restart nginx
2. sudo systemctl status nginx
3. 에러 로그 보기: `sudo tail -n 100 /var/log/nginx/error.log`

장고 로그 보기 

- `tail -n 100 /home/ubuntu/BEERBUDDY/dkfriend-backend-latest/dkfriend_back/django_debug.log`
