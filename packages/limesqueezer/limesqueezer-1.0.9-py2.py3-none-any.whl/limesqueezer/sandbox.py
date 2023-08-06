import numpy as np
# import matplotlib.pyplot as plt
# import time
# import API



###═════════════════════════════════════════════════════════════════════
def fastcompress(x, y, atol=1e-5, mins = 100):
    '''Fast compression using sampling and splitting from largest error
    x: 1D numpy array
    y: 1D numpy array
    atol: absolute error tolerance
    mins: minimum number of samples, don't change if you don't understand
    '''
    def r(a, b):
        '''Recurser'''
        n = b-a-1
        step = 1 if n<=mins*2 else round(n / (2*(n - mins)**0.5 + mins))

        e = lambda xf, yf: np.abs((y[b]- y[a]) /(x[b] - x[a])* (xf - x[a]) + y[a] - yf)
        i = a + step*np.argmax(e(x[a+1:b-1:step], y[a+1:b-1:step]))

        return np.concatenate((r(a,i), r(i,b)[1:])) if e(x[i], y[i]) > atol else (a,b)

    return r(0,len(x)-1)



path_home = pathlib.Path(__file__).parent.absolute()

path_figures = path_home / 'figures'

###═════════════════════════════════════════════════════════════════════
n_data = int(float(sys.argv[1]))
ytol = float(sys.argv[2])
mins = int(float(sys.argv[3]))
b = int(float(sys.argv[4]))
data = ls.Data(n_data=n_data,b=b)
data.x_compressed, data.y_compressed = ls.compress(data.x,data.y,
                                                   ytol=ytol, mins = mins,
                                                   verbosity = verbosity,
                                                   is_timed = is_timed)
print(data.x_compressed[-1])
y0 = np.array([data.y[0],data.y[0]+data.x[0]])

with ls.Compressed(data.x[0], y0,ytol=ytol, mins=mins) as compressed:
    plt.ion()
    
    fig, ax = plt.subplots()
    ax.set_title("interactive test")
    ax.set_xlabel("x")
    ax.set_xlim(-0.1,1.1)
    ax.set_ylim(-0.1,1.1)
    ax.plot(data.x,data.y)
    ln = ax.plot(compressed.x,compressed.y[:,0],'-o')
    t_start = time.perf_counter()
    xlim = 0
    for x,y in zip(data.x,data.y):
        compressed(x,np.array([y, y+x]))
        # print(compressed.x)
        # print(compressed.y)
        if x>xlim:
            xlim += 0.01
            if type(ln) == list:
                for index, line in enumerate(ln):
                    line.set_xdata(compressed.x)
                    line.set_ydata(compressed.y[:,index])
            else:
                ln.set_xdata(compressed.x)
                ln.set_ydata(compressed.y)
            fig.canvas.draw()
    plt.show()
    time.sleep(2)
    # if verbosity>0: 
    #     text = 'Length of compressed array\t%i'%len(x_c)
    #     text += '\nCompression factor\t%.3f %%' % (100*len(x_c)/len(x))
    #     if is_timed: text += '\nCompression time\t%.1f ms' % (t*1e3)
    #     print(text)
print("compression time",time.perf_counter()-t_start)
# # print(compressed)

# # for x,y in zip(compressed.x,data.x_compressed):
# #     print(x,y)
plt.show()
print(len(compressed))
# # print(compressed.y[:,0])
# print(compressed.x[-1])
# print(data.x[-1])
# print(data.x_compressed - compressed.x)
#───────────────────────────────────────────────────────────────────
if is_plot:
    plt.figure()
    plt.plot(data.x,data.y)
    plt.plot(data.x_compressed,data.y_compressed,'-o')
    title = 'LSQ compressed data'
    plt.title(title)
    if is_save: plt.savefig(path_figures/(title+'.pdf'), bbox_inches='tight')
    #───────────────────────────────────────────────────────────────────
    data.make_lerp()
    print(data.NRMSE)
    print('maxres: function',max(abs(data.residuals)))
    plt.figure()
    plt.plot(data.x,data.residuals)
    title = 'LSQ compressed residuals'
    plt.title(title)
    if is_save: plt.savefig(path_figures/(title+'.pdf'), bbox_inches='tight')

    lerp = interpolate.interp1d(compressed.x,compressed.y[:,0], assume_sorted=True)
    residuals = lerp(data.x) - data.y
    print('max relative residual',np.amax(np.abs(residuals))/ytol)

    plt.figure()
    plt.plot(compressed.x,compressed.y[:,0],'-o')
    title = 'Loooped compressed data'
    plt.title(title)
    if is_save: plt.savefig(path_figures/(title+'.pdf'), bbox_inches='tight')

    plt.figure()
    plt.plot(data.x,residuals,'-')
    title = 'Loooped compressed residuals'
    plt.title(title)
    if is_save: plt.savefig(path_figures/(title+'.pdf'), bbox_inches='tight')

if is_show: plt.show()