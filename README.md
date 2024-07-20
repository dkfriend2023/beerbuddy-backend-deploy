# BeAbuddy-backend

🍻 Server-Side of BeABuddy Developed with Django

- **API URL**: [🍻BeABuddy🍻](https://beerbuddy2023.com/)
- **API Documentation**: [🍻BeABuddy API Documentation🍻](https://www.notion.so/API-Documentation-1d3c8ffa841045258f1fdc07355f48d3)
- **Admin Account Information**: [Check the development Repo ReadMe](https://github.com/dkfriend2023/beerbuddy-backend-legacy/blob/main/README.md) (Developers Only)

<br>
<hr>

## Overview

BeerBuddy is a restaurant reservation application designed to help users discover menus and make group reservations at restaurants around university campuses.

<br>

## Technologies Used

- **Backend Framework**: Django Rest Framework
- **Database**: SQLite3
- **Deployment**: AWS Lightsail
- **Server**: Gunicorn, Nginx
- **HTTPS**: Let's Encrypt (certificate renewal every 3 months)
  - **Current Certificate Validity**:
    - **notBefore**: Jul 12 16:12:05 2024 GMT (2024년 7월 12일 16시 12분 5초)
    - **notAfter**: Oct 10 16:12:04 2024 GMT (2024년 10월 10일 16시 12분 4초)

<br>

## Features

- User authentication and authorization
- Restaurant listing and detail views
- Menu management
- Group reservation system
- Search functionality for restaurants and menus
- User information management
- Email verification

<br>

## Admin Pages

- The admin interface is available at: [Admin Page](https://beerbuddy2023.com/admin/)

<br>

## Contributors

- Seulmi Kang(Kiara⚡️): [GitHub](https://github.com/2020147542)
- Subin Shin: ()

<br>

## Deployment and Maintenance Instructions

> #### **Important: Never run the server using `python manage.py runserver` in a production environment.**

### 1) When modifying server code or Gunicorn script (logic part):

1. Restart the service:
    ```bash
    sudo systemctl restart dkfriend.service
    ```
2. Check the status:
    ```bash
    sudo systemctl status dkfriend.service
    ```
3. View error logs:
    ```bash
    tail -n 100 /home/ubuntu/BEERBUDDY/error.log
    ```

<br>

### 2) When modifying static files or Nginx script:

1. Restart Nginx:
    ```bash
    sudo systemctl restart nginx
    ```
2. Check the status:
    ```bash
    sudo systemctl status nginx
    ```
3. View error logs:
    ```bash
    sudo tail -n 100 /var/log/nginx/error.log
    ```

<br>

### 3) To view Django logs:

- Use the following command:
    ```bash
    tail -n 100 /home/ubuntu/BEERBUDDY/dkfriend-backend-latest/dkfriend_back/django_debug.log
    ```

<br>

### 4) To renew Let's Encrypt certificates:

- Certificates need to be renewed every 3 months. Use the following command to renew:
    ```bash
    sudo certbot renew
    ```
- Verify the renewal:
    ```bash
    sudo systemctl status nginx
    ```

<br>

### 5) To check the current certificate information:

- Use the following command to check the current certificate's validity:
    ```bash
    sudo openssl x509 -in /etc/letsencrypt/live/beerbuddy2023.com/fullchain.pem -noout -dates
    ```

<br>

## License

This project is part of the Workstation Project by [the Institute for Higher Education Innovation at Yonsei University](https://ihei.yonsei.ac.kr/ihei/workstation.do).
