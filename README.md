# your-visits-flask
간단한 웹사이트를 만들면서 여러 언어/프레임워크를 비교해보자 - Python/Flask편

### 웹사이트 요구사항 - 공통
1. 클라이언트의 IP를 기반으로 방문수를 DB에 저장한다
2. 회원가입 시, 현재 IP를 회원에게 귀속하고 방문수를 승계한다.
3. 다른 IP로 접속해도 로그인을 하면 회원정보에 추가해 방문수를 합산한다.

**(완성 스크린샷)**   
![image](https://user-images.githubusercontent.com/49602144/143662223-65c9c202-a0cc-4008-9d8b-f3865a1673d5.png)

---
### Flask 후기
1. 의존성 관리
> 파이썬은 `venv`, `conda` 외 여러 툴을 통해 분리된 가상환경을 지원한다. 또한 `pip freeze` 명령어를 통해 `requirements.txt`라는 파일로 의존성을 관리하는 관습이 있다.
2. 프레임워크 특징
> `flask`는 `micro-framework`이다. 대부분의 기능들이 써드파티 플러그인으로 존재하며, 대신 사용하지 않는 기능으로 인한 boilerplate가 적다. 따라서 초보자가 빠르게 결과물을 내고 기능을 천천히 확장시켜나가기 좋다. 대표적인 플러그인으로는 `flask-sqlalchemy`(ORM), `flask-wtf`(Form Validation) 등이 있다. 또한 전형적인 MVC 패턴을 따르고 있으며, `jinja` 템플릿 엔진을 탑재하여 프론트엔드를 처리한다.
3. DB(ORM) 사용 방식은 어떤가? (One-to-many 관계 설정 등)
> 플러그인을 별도로 설치해야 ORM을 사용할 수 있으며, `sqlalchemy`를 기반으로 만들어진 `flask-sqlalchemy` 플러그인을 사용한다. 파이썬의 간결한 문법 덕분에 모델 클래스를 정의하기 쉽고 관계 역시 `relationship` 메소드를 통해 손쉽게 설정할 수 있다. 특히 `backref` 옵션을 주면 상호 참조가 가능해진다. 데이터베이스 세션은 초반에 초기화한 `SQLAlchemy()`객체를 가져다가 쓴다.
4. request에 대한 정보는 어떻게 얻을 수 있는가 (클라이언트 IP, 헤더정보 등)
> Flask 패키지 안에 `request`라는 객체에 담겨있다. 클라이언트 IP의 경우 `request.remote_addr`, 헤더는 `request.headers`에 담겨있다.
5. 로그인, 세션관리는 어떻게 이루어지는가
> `flask-login`이라는 플러그인으로 한번에 처리할수도 있고, 기본적으로 세션은 `Flask.session` 객체를 활용하면 된다. 세션 객체 외에도 단일 request내에서 공유되는 `g` 객체라는 것이 있어 첫 request때 세션에 있는 유저정보를 여기에 저장해 사용한다.
7. 로깅은 어떻게 할 수 있는가
> `current_app.logger` 객체에 `.debug()`와 같은 메소드를 통해 로깅할 수 있다.
9. 배포는 편리한가
> 개발서버가 내장되어 있으며, 실배포를 위해서는 WSGI 인터페이스가 필요하다. 대표적으로 `gunicorn`이 있다.

End.
