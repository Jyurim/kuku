def emailTemplate(token: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>

        <body style = "font-family: Arial, Helvetica, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    text-align: center;
                    background-color: gainsboro;
                    margin-top: 35px;">
            <div style = "width: 560px;
                    height: calc(100vh - 120px - 35px);
                    margin: 0 auto;
                    background-color: white;">
                <header style = "Margin: 0;
                    color: #322f37;
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 36px;
                    font-weight: bold;
                    line-height: 2;
                    margin: 0;
                    padding: 0;
                    background-color: hsl(171, 100%, 41%);
                    font-style: italic;">
                    KUKU
                </header>
                <div style = "padding: 10px;">
                    <p style= "font-size: 24px;
                    font-weight: 400;
                    text-align: center;
                    margin-top: 1rem;">KUKU에 오신것을 환영합니다!</p>
                    <p style="margin-top: 1rem;">저희 KUKU 에 가입해주셔서 감사합니다.</p>
                    <p style="margin-top: 1rem;">이메일 인증을 완료 하셔야 KUKU의 모든 기능을 이용 하실 수 있으십니다.</p>
                    <br>
                    <a href="http://api.eyo.kr:8081/user/emailConfirm?token={token}"
                        target="_blank"
                        style = "margin-top: 1rem;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    text-decoration: none;
                    background: #0275d8;
                    color: white;">
                        이메일 인증하기
                    </a>
                    <br>
                    <br>
                    <p style="margin-top: 1rem;">비전공자도 참여할 수 있는 쉬운 난이도를 통하여</p>
                    <p style="margin-top: 1rem;">여러분의 코딩실력을 향상시켜보세요!</p>
                </div>
            </div>
        </body>
        <footer style = "line-height: 1;
                    color: #706a7c;
                    font-size: 14px">
            @KUKU
        </footer>

        </html>
        """


def successTemplate(name: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>

        <body style = "font-family: Arial, Helvetica, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    text-align: center;
                    background-color: gainsboro;
                    margin-top: 35px;">
            <div style = "width: 600px;
                    height: calc(100vh - 120px - 35px);
                    margin: 0 auto;
                    background-color: white;">
                <header style = "Margin: 0;
                    color: #322f37;
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 36px;
                    font-weight: bold;
                    line-height: 2;
                    margin: 0;
                    padding: 0;
                    background-color: hsl(171, 100%, 41%);
                    font-style: italic;">
                    KUKU
                </header>
                <div style = "padding: 10px;">
                    <p style= "font-size: 24px;
                    font-weight: 400;
                    text-align: center;
                    margin-top: 1rem;">이메일 인증에 성공하였습니다!</p>
                    <p style="margin-top: 1rem;"><b>{name}</b>님의 이메일이 정상적으로 인증되었습니다.</p>
                    <p style="margin-top: 1rem;">이제 KUKU의 모든 기능을 이용 하실 수 있습니다!</p>
                    <br>
                    <a href="http://eyo.kr"
                        style = "margin-top: 1rem;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    text-decoration: none;
                    background: #0275d8;
                    color: white;">
                        KUKU로 이동하기
                    </a>
                    <br>
                    <br>
                    <p style="margin-top: 1rem;">비전공자도 참여할 수 있는 쉬운 난이도를 통하여</p>
                    <p style="margin-top: 1rem;">여러분의 코딩실력을 향상시켜보세요!</p>
                </div>
            </div>
        </body>
        <br/>
        <footer style = "line-height: 1;
                    color: #706a7c;
                    font-size: 14px">
            @KUKU
        </footer>

        </html>
        """


def failTemplate() -> str:
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>

        <body style = "font-family: Arial, Helvetica, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    text-align: center;
                    background-color: gainsboro;
                    margin-top: 35px;">
            <div style = "width: 600px;
                    height: calc(100vh - 120px - 35px);
                    margin: 0 auto;
                    background-color: white;">
                <header style = "Margin: 0;
                    color: #322f37;
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 36px;
                    font-weight: bold;
                    line-height: 2;
                    margin: 0;
                    padding: 0;
                    background-color: hsl(171, 100%, 41%);
                    font-style: italic;">
                    KUKU
                </header>
                <div style = "padding: 10px;">
                    <p style= "font-size: 24px;
                    font-weight: 400;
                    text-align: center;
                    margin-top: 1rem;">이메일 인증에 실패하였습니다...</p>
                    <p style="margin-top: 1rem;">이메일 인증 도중 예상치 못한 오류가 발생하였습니다.</p>
                    <p style="margin-top: 1rem;">다시한번 이메일 검증 절차을 진행해주시거나</p>
                    <p style="margin-top: 1rem;">관리자에게 문의해주시면 감사하겠습니다.</p>
                    <br/>
                    <a href="http://eyo.kr"
                        style = "margin-top: 1rem;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    text-decoration: none;
                    background: #0275d8;
                    color: white;">
                        KUKU로 이동하기
                    </a>
                </div>
            </div>
        </body>
        <br/>
        <footer style = "line-height: 1;
                    color: #706a7c;
                    font-size: 14px">
            @KUKU
        </footer>

        </html>
        """
