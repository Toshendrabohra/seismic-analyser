from django.shortcuts import render
import math
# Create your views here.


def sa_g(t, soil):
    sa_g = 2.50
    if soil == 0:
        if t >= 0.0 and t <= 0.10:
            sa_g = 1 + 15*t
        elif 0.1 <= t and t <= 0.40:
            sa_g = 2.50
        elif t >= 0.40 and t <= 4.00:
            sa_g = 1.0/t
    elif soil == 1:
        if t >= 0.0 and t <= 0.10:
            sa_g = 1 + 15*t
        elif 0.1 <= t and t <= 0.55:
            sa_g = 2.50
        elif t >= 0.55 and t <= 4.00:
            sa_g = 1.36/t
    else:
        if t >= 0.0 and t <= 0.10:
            sa_g = 1 + 15*t
        elif 0.1 <= t and t <= 0.67:
            sa_g = 2.50
        elif t >= 0.67 and t <= 4.00:
            sa_g = 1.67/t

    return sa_g


def home(request):
    data = {
        "flag": 1
    }

    if request.method == "POST":
        height = float(request.POST["height"])
        base_d = float(request.POST["height"])
        I = float(request.POST["I"])
        Z = float(request.POST["Z"])
        soil = int(request.POST["soil"])
        weight = float(request.POST["weight"])
        stories = int(request.POST["stories"])
        floor_weights = request.POST["floor_weights"].split()
        floor_heights = request.POST["floor_heights"].split()

        R = 5.0
        vib_winfill = .075*pow(height, 0.75)
        vib_infill = (.09*height)/math.sqrt(base_d)
        Sa_g = sa_g(vib_winfill, soil)
        A_h = (Z*I*Sa_g)/(2.0*R)
        V_h = (A_h*2)/3
        V_b = A_h*weight
        wh = 0
        for i in range(stories):
            floor_weights[i] = float(floor_weights[i])
            floor_heights[i] = float(floor_heights[i])
            wh += floor_weights[i]*floor_heights[i]*floor_heights[i]

        lfi = []

        for i in range(stories):
            lfi.append(
                (V_b*floor_weights[i]*floor_heights[i]*floor_heights[i])/wh)

        data = {
            "vib_winfill": vib_winfill,
            "vib_infill": vib_infill,
            "Z": Z,
            "I": I,
            "Sa_g": Sa_g,
            "A_h": A_h,
            "V_h": V_h,
            "weight": weight,
            "V_b": V_b,
            "stories": stories,
            "lfi": lfi,
            "flag": 2,
        }

        return render(request, 'home.html', data)
    return render(request, 'home.html', data)
