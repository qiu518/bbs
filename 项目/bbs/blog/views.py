from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from blog.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO

# Create your views here.
class Login(View):

    def get(self, request):
        form_obj = LoginForm()
        return render(request, 'login.html', {'form_obj': form_obj})

    def post(self, request):
        print(request.POST)
        res = {'code': 0}
        username = request.POST.get('user')
        pwd = request.POST.get('pwd')
        v_code = request.POST.get('v_code')
        # 判断验证码是否正确
        print(request.session.get('v_code',''))
        if v_code.upper() != request.session.get('v_code',''):
            res['code'] = 1
            res['msg'] = '验证码错误'
        else:
            # 校验用户名密码是否正确
            user = authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                login(request, user)
                print('登陆成功')
            else:
                # 用户名或密码错误
                res["code"] = 1
                res["msg"] = "用户名或密码错误"

        return JsonResponse(res)


class Index(View):

    def get(self, request):
        return render(request, 'index.html')


class V_code(View):

    # 随机颜色的方法
    def random_color(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def get(self,request):
        # 创建一张颜色随机的图片
        img_obj = Image.new(
            "RGB",
            (250, 34),
            self.random_color()
        )
        # 声明写字的图片及所用字体
        draw_obj = ImageDraw.Draw(img_obj)
        font_obj = ImageFont.truetype('static/font/kumo.ttf',30)
        tmp = []
        for i in range(5):
            n = str(random.randint(0,9))
            u = chr(random.randint(65,90))
            l = chr(random.randint(97,122))
            c = random.choice([n,u,l])
            tmp.append(c)
            draw_obj.text(
                (i*40+40,0),
                c,
                fill=self.random_color(),
                font = font_obj
            )
        # 加干扰线
        width = 250  # 图片宽度（防止越界）
        height = 35
        for i in range(5):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw_obj.line((x1, y1, x2, y2), fill=self.random_color())

        # 加干扰点
        for i in range(40):
            draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=self.random_color())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=self.random_color())

        tmp = ''.join(tmp)
        request.session['v_code'] = tmp.upper()

        f = BytesIO()
        img_obj.save(f,'png')
        data = f.getvalue()
        return HttpResponse(data)