import tkinter
from lrp_solver import *
from data_generation import *
from global_data import *

def create_circle(x, y, r, canvas,f="purple"): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill=f)

def create_square(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_rectangle(x0, y0, x1, y1, fill='red', outline='red')

colors = ["blue","red","green","black","cyan","magenta","pink","violet","yellow","grey","gold","brown","beige","silver","AliceBlue", "AntiqueWhite", "AntiqueWhite1", "AntiqueWhite2", "AntiqueWhite3",    "AntiqueWhite4", "aquamarine", "aquamarine1", "aquamarine2", "aquamarine3",    "aquamarine4", "azure", "azure1", "azure2", "azure3", "azure4", "beige",    "bisque", "bisque1", "bisque2", "bisque3", "bisque4", "black", "BlanchedAlmond",    "blue", "blue1", "blue2", "blue3", "blue4", "BlueViolet", "brown", "brown1",    "brown2", "brown3", "brown4", "burlywood", "burlywood1", "burlywood2", "burlywood3",    "burlywood4", "CadetBlue", "CadetBlue1", "CadetBlue2", "CadetBlue3", "CadetBlue4",    "chartreuse", "chartreuse1", "chartreuse2", "chartreuse3", "chartreuse4"]
'''
def display_routes(R):
    global colors,points
    N=len(points)
    x=[float(points[i][0]) for i in range(N)]
    y=[float(points[i][1]) for i in range(N)]
    mx=min(x)
    Mx=max(x)
    my=min(y)
    My=max(y)
    height=720
    width=1280
    Ep=[[(x[i]-mx)*width/(Mx-mx),(y[i]-my)*height/(My-my),i] for i in range(N)]
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=height, width=width)
    for r in range(len(R)):
        
        for e in R[r]:
            create_circle(int(Ep[e][0]),int(Ep[e][1]),4,C,colors[r])
        for i in range(len(R[r])-1):
            C.create_line(Ep[R[r][i]][0],Ep[R[r][i]][1],Ep[R[r][i+1]][0],Ep[R[r][i+1]][1], fill=colors[r], width=1)
        
        
    C.pack()
    top.mainloop()


def display_routes(R):
    global colors, points
    N = len(points)
    x = [float(points[i][0]) for i in range(N)]
    y = [float(points[i][1]) for i in range(N)]
    mx = min(x)
    Mx = max(x)
    my = min(y)
    My = max(y)
    height = 720
    width = 1280
    Ep = [[(x[i] - mx) * width / (Mx - mx), (y[i] - my) * height / (My - my), i] for i in range(N)]
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=height, width=width)
    for r in range(len(R)):

        for e in R[r]:
            create_circle(int(Ep[e][0]), int(Ep[e][1]), 4, C, colors[r])
        for i in range(len(R[r]) - 1):
            C.create_line(Ep[R[r][i]][0], Ep[R[r][i]][1], Ep[R[r][i + 1]][0], Ep[R[r][i + 1]][1], fill=colors[r],
                          width=1)

    C.pack()
    top.mainloop()

def display_facilities(opened_facilities,serving_matrix,locations):
    global colors, points
    N = len(points)
    x = [float(points[i][0]) for i in range(N)]
    y = [float(points[i][1]) for i in range(N)]
    mx = min(x)
    Mx = max(x)
    my = min(y)
    My = max(y)
    height = 720
    width = 1280
    Ep = [[(x[i] - mx) * width / (Mx - mx), (y[i] - my) * height / (My - my), i] for i in range(N)]
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="black", height=height, width=width)

    for j in locations:
        if opened_facilities[j]==1:
            create_square(int(Ep[j][0]), int(Ep[j][1]), 4, C)
        else:
            create_circle(int(Ep[j][0]), int(Ep[j][1]), 4, C)

    for i in locations:
        for j in locations:
            if serving_matrix[i][j]==1:
                C.create_line(Ep[i][0], Ep[i][1], Ep[j][0], Ep[j][1], fill='black', width=1)
    C.pack()
    top.mainloop()
'''


height = canvas_height
width = canvas_width
top = tkinter.Tk()
canvas = tkinter.Canvas(top, bg="black", height=height, width=width)

def refresh_canvas():
    global canvas
    canvas.delete("all")

def draw_location_routing(locations, opened_facilities=None, routes=None, allocation=None):
    global canvas, colors, points, canvas, top
    if allocation == None:
        allocation = [0 for _ in locations]
    if routes == None:
        routes = []
    if opened_facilities == None:
        opened_facilities = [0 for _ in locations]
    N = len(points)
    x = [float(points[i][0]) for i in range(N)]
    y = [float(points[i][1]) for i in range(N)]
    mx = min(x)
    Mx = max(x)
    my = min(y)
    My = max(y)
    points = [[0.80*(x[i] - mx) * (width) / (Mx - mx) + width*0.10, 0.80*(y[i] - my) * (height) / (My - my) + height*0.10, i] for i in range(N)]
    circle_size = 4

    for location in locations:
        create_circle(int(points[location][0]), int(points[location][1]), circle_size, canvas, "purple")
        canvas.create_text(int(points[location][0]), int(points[location][1]) + 12, text=str(allocation[location]), fill="white")

    for r in range(len(routes)):
        for i in range(len(routes[r]) - 1):
            canvas.create_line(points[routes[r][i]][0], points[routes[r][i]][1], points[routes[r][i + 1]][0], points[routes[r][i + 1]][1], fill='green',
                               width=1)
    for j in locations:
        if opened_facilities[j] == 1:
            create_square(int(points[j][0]), int(points[j][1]), circle_size, canvas)
            canvas.create_text(int(points[j][0]), int(points[j][1]) + 3*circle_size, text=str(allocation[j]), fill="white")

def fn_button_mip_allocation():
    global canvas
    refresh_canvas()

    solver_lrp = lrp_solver(locations, opening_costs, arc_costs, truck_capacity, production)
    print("Optimal value", solver_lrp.solve_optimal(fairness=True))
    print("Allocation", solver_lrp.cost_allocation)
    routes = solver_lrp.routes
    opened_facilities = solver_lrp.opened_facilities
    allocation = solver_lrp.cost_allocation
    draw_location_routing(locations, opened_facilities, routes, allocation)

def fn_button_core_allocation():
    global canvas
    refresh_canvas()

    solver_lrp = lrp_solver(locations, opening_costs, arc_costs, truck_capacity, production)
    print("Optimal value", solver_lrp.solve_optimal(fairness=False))
    print("Allocation", solver_lrp.core_procedure())
    routes = solver_lrp.routes
    opened_facilities = solver_lrp.opened_facilities
    allocation = solver_lrp.cost_allocation
    draw_location_routing(locations, opened_facilities, routes, allocation)

def fn_solve_only_lrp():
    global canvas
    refresh_canvas()
    solver_lrp = lrp_solver(locations, opening_costs, arc_costs, truck_capacity, production)
    print("Optimal value", solver_lrp.solve_optimal(fairness=False))
    routes = solver_lrp.routes
    opened_facilities = solver_lrp.opened_facilities
    draw_location_routing(locations, opened_facilities, routes)

def fn_regenerate_data():
    global canvas, points, locations, arc_costs, opening_costs, n, truck_capacity, production
    refresh_canvas()
    points, locations, arc_costs, opening_costs, n, truck_capacity, production = generate_random_points()
    draw_location_routing(locations)

def fn_proportional_allocation():
    refresh_canvas()
    solver_lrp = lrp_solver(locations, opening_costs, arc_costs, truck_capacity, production)
    print("Optimal value", solver_lrp.solve_optimal(fairness=False))
    print("Allocation", solver_lrp.proportional_allocation())
    routes = solver_lrp.routes
    opened_facilities = solver_lrp.opened_facilities
    allocation = solver_lrp.cost_allocation
    draw_location_routing(locations, opened_facilities, routes, allocation)

def main_ui(locations):
    global colors, points, canvas, top
    draw_location_routing(locations)

    button_mip_allocation = tkinter.Button(top, text="Solve LRP + MIP allocation", command=fn_button_mip_allocation)
    button_solve_lrp = tkinter.Button(top, text="Solve LRP", command=fn_solve_only_lrp)
    button_refresh = tkinter.Button(top, text="Clear", command=refresh_canvas)
    button_core = tkinter.Button(top, text="Solve LRP + Core allocation", command=fn_button_core_allocation)
    button_random = tkinter.Button(top, text="Re-generate points", command=fn_regenerate_data)
    button_prop_alloc = tkinter.Button(top, text="Solve LRP + Proportional allocation", command=fn_proportional_allocation)
    canvas.grid(row=0, column=0, columnspan=6)
    button_mip_allocation.grid(row=1, column=1)
    button_solve_lrp.grid(row=1,column=0)
    button_refresh.grid(row=1, column=5)
    button_core.grid(row=1, column=2)
    button_prop_alloc.grid(row=1,column=3)
    button_random.grid(row=1, column=4)
    top.mainloop()
