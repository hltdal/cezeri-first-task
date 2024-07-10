#x3+x2+x denklem katsayısı gir
#d=0.1 uzaklık optional gir
#n=100 iterasyon sayısı optional gir
#x0=-5 başlangıç değeri optional gir
import pandas as pd
""""
a=int(input("x3 katsayısı: "))
b=int(input("x2 katsayısı: "))
c=int(input("x katsayısı: "))
d=int(input("adım degerleri : "))
n=int(input("iterasyon sayısı: "))
x0=int(input("başlangıç değeri: "))

"""
x_a,x_b,x_c,x_d,x_n,x0=5,-1,5,0.1,100,-5

y_a,y_b,y_c,y_d,y_n,y0=-3,1/2,-8,0.1,100,-5

x_values=[]
y_values=[]
def x_cord_function(a,b,c,d,n,x0,x_values):
    for i in range(n):
        x=x0+(i*d)
        x_values.append(a*(pow(x,3))+b*(pow(x,2))+c*(x))
    x_round_values=[round(val,2) for val in x_values]
    return x_round_values

def y_cord_function(a,b,c,d,n,y0,y_values):
    for i in range(n):
        y=y0+(i*d)
        y_values.append(a*(pow(y,3))+b*(pow(y,2))+c*(y))
        y_round_values=[round(val,2) for val in y_values]
    return y_round_values


x_round_values=x_cord_function(x_a,x_b,x_c,x_d,x_n,x0,x_values)
y_round_values=y_cord_function(y_a,y_b,y_c,y_d,y_n,y0,y_values)
data = pd.DataFrame({
        "cords x":x_round_values,
        "cords y":y_round_values
})
data.to_csv("files.csv", index=False)


