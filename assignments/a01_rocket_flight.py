from scipy.integrate import quadrature
from scipy import linspace
from numpy import array, empty_like, ones_like, empty, where, argmax
from scipy import sign, pi



def dm_p(t, t_0= 0, t_end = 5.0):
    if t_0 <= t <= t_end:
        return 20.
    return 0

def m_p(t, t_0 =0.,  m_p0 = 100):
    """ t time, m_p0 the initial weight of the rocket propellant"""    
    if t<t_0:
        return m_p0
    elif t_0 <= t :
        int_val, err_val = quadrature(dm_p, t_0, t, vec_func=False)
        return m_p0 - int_val

def m_p2(t, t_0 =0.,  m_p0 = 100):
    """ t time, m_p0 the initial weight of the rocket propellant"""    
    if t<t_0:
        return m_p0
    elif t_0 <= t <=5.0:
        int_val = t*20.
        return m_p0 - int_val
    else:
        return 0.0

def f_m(t, m=0):
    if 0 <= t <= 5:
        return -20.*ones_like(m)
    else:
        return 0.*ones_like(m)

def modified_euler_step(u, t, f, dt):
    t_mid = t + 0.5*dt
    u_mid = u + 0.5*dt*f(t, u)
    return u + dt * f(t_mid, u_mid)

def euler_step(u, t, f, dt):
    return u + dt * f(t, u)

dt = 0.01   
T_a = 3.2
N_a = int(T_a/dt)+1
t_a = linspace(0, T_a, N_a)
m_a = empty_like(t_a)
m_a[0] = 100.
for n, t in enumerate(t_a[1:]):
    m_a[n+1] = modified_euler_step(m_a[n], t, f_m, dt)


def f_h(t, u, **args):
    #the weight of the rocket shell
    m_s = 50
    # acceleration of gravity
    g = 9.81 
    #the average air density (assumed constant throughout flight)
    rho = 1.091  
    # is the maximum cross sectional area of the rocket, where $r = 0.5 m$
    r = 0.5
    A = pi*r**2 
    # the exhaust speed
    v_e = 325 

    # the drag coefficient
    C_D = 0.15
    m_tot = m_s + m_p2(t)    

    u_0 = u[1]
    u_1 = -g + (-v_e*f_m(t,) -0.5*rho*A*C_D*sign(u[1])*u[1]**2)/m_tot
    return array([u_0, u_1])

dt = 0.01   
T_b = 40.
#T_b = 2.
N_b = int(T_b/dt)+1
t_b = linspace(0, T_b, N_b)
u_b = empty((N_b, 2))
v_b = empty_like(t_b)
u_b[0] = array([0., 0.])
v_b[0] = 0.0
for n, t in enumerate(t_b[1:]):
    u_b[n+1] = modified_euler_step(u_b[n], t, f_h, dt)
    v_b[n+1] = f_h(t, u_b[n+1])[0]

# get the index of element of u_b where altitude becomes negative
idx_negative_h = where(u_b[:,0]<0.0)[0]

if len(idx_negative_h)==0:
    idx_ground = N_b-1
    print ('The rocket has not reached the ground yet!')
else:
    idx_ground = idx_negative_h[0]
    t_b_ground = t_b[idx_ground]
    v_b_ground = v_b[idx_ground]

max_speed_b = max(v_b)
t_max_speed_b = t_b[where(v_b==max_speed_b)]
h_max_speed_b = u_b[where(v_b==max_speed_b)][0]

max_h_idx = argmax(u_b[:,0])
h_max = u_b[max_h_idx, 0]
t_h_max = t_b[max_h_idx]

u_b_euler = empty((N_b, 2))
for n, t in enumerate(t_b[1:]):
    pass
    u_b_euler[n+1] = euler_step(u_b_euler[n], t, f_h, dt)

max_h_idx_euler = argmax(u_b_euler[:,0])
h_max_euler = u_b_euler[max_h_idx_euler, 0]
t_h_max_euler = t_b[max_h_idx_euler]
