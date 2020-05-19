from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

import os, random, docx

def RabinMiller(n, t):
    a = random.randint(2, (n - 2) - 2)
    x = pow(a, int(t), n)
    if x == 1 or x == n - 1:
        return True

    while t != n - 1:
        x = pow(x, 2, n)
        t *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True

    return False

def isPrime(n):
    if n < 2:
        return False

    lowPrimes = [
                    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                    41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                    89, 97, 101, 103, 107, 109, 113, 127, 131,
                    137, 139, 149, 151, 157, 163, 167, 173, 179,
                    181, 191, 193, 197, 199, 211, 223, 227, 229,
                    233, 239, 241, 251, 257, 263, 269, 271, 277,
                    281, 283, 293, 307, 311, 313, 317, 331, 337,
                    347, 349, 353, 359, 367, 373, 379, 383, 389,
                    397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499,
                    503, 509, 521, 523, 541, 547, 557, 563, 569,
                    571, 577, 587, 593, 599, 601, 607, 613, 617,
                    619, 631, 641, 643, 647, 653, 659, 661, 673,
                    677, 683, 691, 701, 709, 719, 727, 733, 739,
                    743, 751, 757, 761, 769, 773, 787, 797, 809,
                    811, 821, 823, 827, 829, 839, 853, 857, 859,
                    863, 877, 881, 883, 887, 907, 911, 919, 929,
                    937, 941, 947, 953, 967, 971, 977, 983, 991,
                    997
    ]

    if n in lowPrimes:
        return True

    for prime in lowPrimes:
        if n % prime == 0:
            return False

    c = n - 1
    while c % 2 == 0:
        c /= 2

    for i in range(128):
        if not RabinMiller(n, c):
            return False

    return True

def gcd(p, q):
    while p != q:
        if p > q:
            p = p - q
        else:
            q = q - p
    return p

def isCoPrime(p, q):
    return gcd(p, q) == 1

def Karatsuba(x, y):
    str_x = str(x)
    str_y = str(y)

    n = max(len(str_x), len(str_y))

    if len(str_x) - len(str_y) < 0 or len(str_y) - len(str_x) < 0:
        return x * y

    n_2 = int(n/2)

    x_h = int(str_x[:-n_2])
    y_h = int(str_y[:-n_2])

    x_l = int(str_x[-n_2:])
    y_l = int(str_y[-n_2:])

    a = x_h * y_h
    d = x_l * y_l
    e = (x_h + x_l) * (y_h + y_l) - a - d

    dob = a*pow(10, 2*n_2) + e*pow(10, n_2) + d

    return dob

def generateLargePrime(keysize):
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isPrime(num)):
            return num

def generateKeys(keysize):
    e = int()

    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)

    n = Karatsuba(p, q)
    fn = Karatsuba(p - 1, q - 1)

    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, fn)):
            break
    d = pow(e, -1, fn)

    return e, d, n

def enc(e, n, msg):
    enc = ""

    for c in msg:
        m = ord(c)
        enc += str(pow(m, e, n)) + " "

    return enc

def dec(d, n, enc):
    msg = ""

    parts = enc.split()
    for part in parts:
        if part:
            c = int(part)
            msg += chr(pow(c, d, n))

    return msg

def home(request):
    return render(request, 'RSA/home.html')

def inform(request):
    return render(request, 'RSA/RSA.html')

def instruct(request):
    return render(request, 'RSA/instructions.html')

def encrypt(request):
    return render(request, 'RSA/encrypt.html')

def encrypt_data(request):

    if 'text' in request.POST:

        msg = str(request.POST.get('text'))
        keysize = int(request.POST.get('key'))
        e, d, n = generateKeys(keysize)

        res1 = enc(e, n, msg)

        enc_file = docx.Document()
        par1 = enc_file.add_paragraph('Public key: ')
        par1.add_run(str(e))
        par2 = enc_file.add_paragraph('Private key: ')
        par2.add_run(str(d))
        par3 = enc_file.add_paragraph('Module: ')
        par3.add_run(str(n))
        enc_file.add_paragraph('')
        enc_file.add_paragraph(res1)
        enc_file.save(settings.MEDIA_ROOT + '/documents/enc.docx')

        request.session.flush()

        request.session['e'] = e
        request.session['d'] = d
        request.session['n'] = n
        request.session['res1'] = res1

        request.session.modified = True

    return redirect('RSA:encrypt')

def encrypt_file(request):
    return render(request, 'RSA/encrypt_file.html')

def encrypt_file_data(request):

    if 'file' in request.FILES:

        keysize = int(request.POST.get('key'))
        e, d, n = generateKeys(keysize)

        f = docx.Document(request.FILES['file'])

        text = []
        for paragraph in f.paragraphs:
            text.append(paragraph.text)

        z = [str(char) for char in text]
        msg = ''.join(z)

        res2 = enc(e, n, msg)

        enc_file = docx.Document()
        par1 = enc_file.add_paragraph('Public key: ')
        par1.add_run(str(e))
        par2 = enc_file.add_paragraph('Private key: ')
        par2.add_run(str(d))
        par3 = enc_file.add_paragraph('Module: ')
        par3.add_run(str(n))
        enc_file.add_paragraph('')
        enc_file.add_paragraph(res2)
        enc_file.save(settings.MEDIA_ROOT + '/documents/enc.docx')

        request.session.flush()

        request.session['e'] = e
        request.session['d'] = d
        request.session['n'] = n
        request.session['res2'] = res2

        request.session.modified = True

    return redirect('RSA:encrypt_file')

def download_enc_file(request):

    with open(settings.MEDIA_ROOT + '/documents/enc.docx', 'rb') as file:

        response = HttpResponse(
            file.read(),
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'inline; filename="encrypt.docx"'

    file.close()

    enc_file = settings.MEDIA_ROOT + '/documents/enc.docx'
    os.remove(enc_file)

    return response

def decrypt(request):
    return render(request, 'RSA/decrypt.html')

def decrypt_data(request):

    if 'text' in request.POST:

        enc = str(request.POST.get('text'))
        d = int(request.POST.get('key'))
        n = int(request.POST.get('prod'))

        res3 = dec(d, n, enc)

        dec_file = docx.Document()
        dec_file.add_paragraph(res3)
        dec_file.save(settings.MEDIA_ROOT + '/documents/dec.docx')

        request.session.flush()

        request.session['d'] = d
        request.session['n'] = n
        request.session['res3'] = res3

        request.session.modified = True

    return redirect('RSA:decrypt')

def decrypt_file(request):
    return render(request, 'RSA/decrypt_file.html')

def decrypt_file_data(request):

    if 'file' in request.FILES:

        f = docx.Document(request.FILES['file'])

        text = []
        for paragraph in f.paragraphs:
            text.append(paragraph.text)

        z = [str(char) for char in text]
        enc = ''.join(z)

        d = int(request.POST.get('key'))
        n = int(request.POST.get('prod'))

        res4 = dec(d, n, enc)

        dec_file = docx.Document()
        dec_file.add_paragraph(res4)
        dec_file.save(settings.MEDIA_ROOT + '/documents/dec.docx')

        request.session.flush()

        request.session['d'] = d
        request.session['n'] = n
        request.session['res4'] = res4

        request.session.modified = True

    return redirect('RSA:decrypt_file')

def download_dec_file(request):

    with open(settings.MEDIA_ROOT + '/documents/dec.docx', 'rb') as file:

        response = HttpResponse(
            file.read(),
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'inline; filename="decrypt.docx"'

    file.close()

    dec_file = settings.MEDIA_ROOT + '/documents/dec.docx'
    os.remove(dec_file)

    return response

def your_key_encrypt(request):
    return render(request, 'RSA/your_key_encrypt.html')

def your_key_encrypt_data(request):

    if 'text' in request.POST:

        msg = str(request.POST.get('text'))
        e = int(request.POST.get('key'))
        n = int(request.POST.get('prod'))

        res5 = enc(e, n, msg)

        enc_file = docx.Document()
        enc_file.add_paragraph(res5)
        enc_file.save(settings.MEDIA_ROOT + '/documents/enc.docx')

        request.session.flush()

        request.session['e'] = e
        request.session['n'] = n
        request.session['res5'] = res5

        request.session.modified = True

    return redirect('RSA:your_key_encrypt')

def your_key_encrypt_file(request):
    return render(request, 'RSA/your_key_encrypt_file.html')

def your_key_encrypt_file_data(request):

    if 'file' in request.FILES:

        f = docx.Document(request.FILES['file'])

        text = []
        for paragraph in f.paragraphs:
            text.append(paragraph.text)

        z = [str(char) for char in text]
        msg = ''.join(z)

        e = int(request.POST.get('key'))
        n = int(request.POST.get('prod'))

        res6 = enc(e, n, msg)

        enc_file = docx.Document()
        enc_file.add_paragraph(res6)
        enc_file.save(settings.MEDIA_ROOT + '/documents/enc.docx')

        request.session.flush()

        request.session['e'] = e
        request.session['n'] = n
        request.session['res6'] = res6

        request.session.modified = True

    return redirect('RSA:your_key_encrypt_file')