import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np
import copy
def quadratic_to_piecewise(a,a0,a00,xmin,xmax,piece_number=2,steps_ize=0.1,mode_hanging=False,hanging_sigma=0.01,show_result=False,result_type='complete'):
    '''
    Convert quadratic into piecewise (linear function) of:
        y = m*x_delta + y_ref, where:
            x_delta=x-x_ref
            x_ref,y_ref is point of piecewise
            ...

    ## Example:
    xmin=0
    xmax=100
    a=0.1
    a0=1
    a00=10
    w=quadratic_to_piecewise(a,a0,a00,xmin,xmax)   
    print(w)

    result_type (default is complete):
        (1) 'complete' = points in x,y,m coordinates including both end
        (2) 'gradients' = points in x,m coordinates including both end 
        (3) 'points' = points in x,y coordinates including both end
        (4) 'weights' = result in m_start,(points),m_end format excluding both end points 
        Last m will be equal to the previous points m value.
    '''

    def func_2piecewise(x, m_0, x_1, y_1, m_1):
        y = np.piecewise(x, [x <= x_1, x > x_1],
                        [lambda x: m_0*(x-x_1) + y_1, lambda x: m_1*(x-x_1) + y_1])
        return y

    def func_3piecewise(x, m_0, x_1, y_1, x_2, y_2, m_2):
        y = np.piecewise(x, [x <= x_1, (x > x_1) & (x <= x_2), x > x_2],
                        [lambda x: m_0*(x-x_1) + y_1, lambda x: y_1+(y_2-y_1)*(x-x_1)/(x_2-x_1), lambda x: m_2*(x-x_2) + y_2])
        return y

    def func_4piecewise(x, m_0, x_1, y_1, x_2, y_2, x_3, y_3, m_3):
        y = np.piecewise(x, [x <= x_1, (x > x_1) & (x <= x_2), (x > x_2) & (x <= x_3), x > x_3],
                        [lambda x: m_0*(x-x_1) + y_1, lambda x: y_1+(y_2-y_1)*(x-x_1)/(x_2-x_1), lambda x: y_2+(y_3-y_2)*(x-x_2)/(x_3-x_2), lambda x: m_3*(x-x_3) + y_3])
        return y

    def func_5piecewise(x, m_0, x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4, m_4):
        y = np.piecewise(x, [x <= x_1, (x > x_1) & (x <= x_2), (x > x_2) & (x <= x_3), (x > x_3) & (x <= x_4), x > x_4],
                        [lambda x: m_0*(x-x_1) + y_1, lambda x: y_1+(y_2-y_1)*(x-x_1)/(x_2-x_1), lambda x: y_2+(y_3-y_2)*(x-x_2)/(x_3-x_2), lambda x: y_3+(y_4-y_3)*(x-x_3)/(x_4-x_3), lambda x: m_4*(x-x_4) + y_4])
        return y

    def func_quadratic(x,a,a0,a00):
        y=a*x*x+a0*x+a00
        return y    

    def func_gradients(x_list,y_list):
        if isinstance(x_list, list): 
            m_list=[]
            for idx in range(len(x_list)-1):
                if (x_list[idx+1]-x_list[idx]) == 0:
                    m_list.append([0])
                else:
                    m_list.append((y_list[idx+1]-y_list[idx])/(x_list[idx+1]-x_list[idx]))
            return m_list 
        else: #x_list == delta_x and y_list == delta_y
            if x_list == 0:
                m_list = 0
            else:
                m_list=y_list/x_list
            return m_list

    def func_linear(x_delta,y_ref,m):
        y=y_ref+m*x_delta
        return y

    def func_piecewise(x_sample,x_piece,y_piece,m_piece):
        midle_points_number=piece_number-1
        y_list=[]
        for x in x_sample:
            for piece in range(piece_number):
                if piece == midle_points_number:
                    y_list.append(func_linear(x-x_piece[piece],y_piece[piece],m_piece[piece]))
                elif x <= x_piece[piece+1]:
                    y_list.append(func_linear(x-x_piece[piece],y_piece[piece],m_piece[piece]))
                    break
        return y_list

    def func_show_result(x_list,a,a0,a00,x_piece,y_piece,m_piece,marker_number=20):
        # Get points
        x_sample_show=np.linspace(x_piece[0],x_piece[-1],marker_number)
        y_real_show = func_quadratic (x_sample_show,a,a0,a00)
        y_model_show = func_piecewise(x_sample_show,x_piece,y_piece,m_piece)

        # Plot
        plt.plot(x_sample_show,y_real_show,c='#1f77b4',marker='+',label="Data")
        plt.plot(x_sample_show,y_model_show,c='#ff7f0e',marker='*',label="Fit")
        plt.title("Piecewise to Real Comparison")
        plt.legend(loc="upper left")
        plt.show()
        pass

    ## Get sample
    numberOfStep=int(1+(xmax-xmin)/steps_ize)
    midle_points_number=piece_number-1
    x_sample=np.linspace(xmin,xmax,numberOfStep)
    y_sample=[a*x*x+a0*x+a00 for x in x_sample]

    ## Sigma (wighting)
    sigma=np.ones(numberOfStep)
    if mode_hanging==True:
        sigma[[0,-1]]=hanging_sigma

    ## Start and End Points
    x_0 = copy.deepcopy(xmin)
    x_end = copy.deepcopy(xmax)

    ## Bounds and Initial Guesses
    lower_bounds=[-np.inf]
    upper_bounds=[np.inf]
    p0=[(y_sample[1]-y_sample[0])/(x_sample[1]-x_sample[0])]
    for idx in range(midle_points_number):
        lower_bounds.extend([xmin,-np.inf])
        upper_bounds.extend([xmax,np.inf])
        x_val=x_0+(idx+1)*(x_end-x_0)/piece_number
        y_val=a*x_val*x_val+a0*x_val+a00
        p0.extend([x_val,y_val])
    lower_bounds.extend([-np.inf])
    upper_bounds.extend([np.inf])
    p0.extend([(y_sample[-1]-y_sample[-2])/(x_sample[-1]-x_sample[-2])])

    ## Solve
    if piece_number==2:
        w, _ = opt.curve_fit(func_2piecewise, x_sample, y_sample,bounds=(lower_bounds,upper_bounds),sigma=sigma,p0=p0)
        w = w.tolist()
        y_0 = func_2piecewise(x_0, *w).tolist()
        y_end = func_2piecewise(x_end, *w).tolist()
    elif piece_number==3:
        w, _ = opt.curve_fit(func_3piecewise, x_sample, y_sample,bounds=(lower_bounds,upper_bounds),sigma=sigma,p0=p0)
        w = w.tolist()
        y_0 = func_3piecewise(x_0, *w).tolist()
        y_end = func_3piecewise(x_end, *w).tolist()
    elif piece_number==4:
        w, _ = opt.curve_fit(func_4piecewise, x_sample, y_sample,bounds=(lower_bounds,upper_bounds),sigma=sigma,p0=p0)
        w = w.tolist()
        y_0 = func_4piecewise(x_0, *w).tolist()
        y_end = func_4piecewise(x_end, *w).tolist()
    elif piece_number==5:
        w, _ = opt.curve_fit(func_5piecewise, x_sample, y_sample,bounds=(lower_bounds,upper_bounds),sigma=sigma,p0=p0)
        w = w.tolist()
        y_0 = func_5piecewise(x_0, *w).tolist()
        y_end = func_5piecewise(x_end, *w).tolist()
    else:
        print('Number of piece is unsupported')
        return []
    
    x_piece=[x_0]
    y_piece=[y_0]
    m_piece=[w[0]]
    for idx in range(midle_points_number):
        x_piece.append(w[1+idx*2])
        y_piece.append(w[2+idx*2])
        if idx < midle_points_number-1:
            m_val=func_gradients(w[1+(idx+1)*2]-w[1+idx*2],w[2+(idx+1)*2]-w[2+idx*2])
            m_piece.append(m_val)
    x_piece.append(x_end)
    y_piece.append(y_end)
    m_piece.extend([w[-1],w[-1]])

    ## Result Type
    result=[]
    if result_type == 'complete':
        for x_val,y_val,m_val in zip(x_piece,y_piece,m_piece):
            result.append([x_val,y_val,m_val])
    elif result_type == 'gradients':
        for x_val,m_val in zip(x_piece,m_piece):
            result.append([x_val,m_val])
    elif result_type == 'points':
        for x_val,y_val in zip(x_piece,y_piece):
            result.append([x_val,y_val])
    elif result_type == 'weights':
        result=w

    ## Show result
    if show_result==True:
        func_show_result(x_sample,a,a0,a00,x_piece,y_piece,m_piece,marker_number=50)
    
    return result
