# PERPY——Functions commonly used in computer paper writing and scientific research.
## INSTALL
```Python
pip install perpy
```
## IMPORT
```Python
import perpy as py
```
## LOAD——load dataset from file
### TEST FILE——test1.txt
>**1 5 0**  
>**2 4 0**  
>**3 3 0**  
>**4 2 1**  
>**5 1 1**  
### CASE 1——Non label & No max min scaling
```Python
path = r'D:\perpy' # file directory
col_labels = None # non label
scaling = False # no max min scaling

x= py.load(path, col_labels, scaling)
```
![image](https://user-images.githubusercontent.com/82493254/119089849-5d899080-ba3d-11eb-9863-0da34fc741f4.png)

```Python
print(x)
```
![image](https://user-images.githubusercontent.com/82493254/119089890-6f6b3380-ba3d-11eb-8b97-1397267b630f.png)
### CASE 2——The labels is in the first column & To max min scaling
```Python
path = r'D:\perpy' # file directory
col_labels = 0 # the labels is in the first column
scaling = True # to max min scaling

x, r = py.load(path, col_labels, scaling)

print(x, '\n', r)
```
![image](https://user-images.githubusercontent.com/82493254/119095915-78f89980-ba45-11eb-90a4-cfbc4c14179c.png)
### CASE 3——The labels is in the last column & No max min scaling
```Python
path = r'D:\perpy' # file directory
col_labels = 2 # the labels is in the last column. non-zero number
scaling = False # no max min scaling

x, r = py.load(path, col_labels, scaling)

print(x, '\n', r)
```
![image](https://user-images.githubusercontent.com/82493254/119096315-050ac100-ba46-11eb-943c-1dba6f603e47.png)

## DIST——Calculate the euclidean distance between point A and point B
```Python
A = np.mat([1,2,3,4]) # point A
B = np.mat([4,3,2,1]) # point B

dist = py.dist(A, B)

print(dist)
```
4.47213595499958
## PLT_SCATTER——Drawing scatter plot
```Python
path = r'D:\perpy' # file directory
col_labels = 2 # the labels is in the last column. non-zero number
scaling = False # no max min scaling

x, r = py.load(path, col_labels, scaling)

py.plt_scatter(x=x, labels=r, fig_label=['X——label','Y——label'], fig_legend=['Cluster','01']) # 00-upper left, 01-upper right, 10-down left, 11-down right
```
![image](https://user-images.githubusercontent.com/82493254/119098644-9d09aa00-ba48-11eb-86cc-771cacee594e.png)
## PLT_RUNTIME——Drawing runtime plot
```Python
times = [[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0], # Runtime list, times[0] is A times, times[1] is B times.
        [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7]]
instances = [1,2,3,4,5,6,7,8] # x
labels = ['$A$','$B$'] # labels

py.plt_runtime(times, instances, labels)
```
![image](https://user-images.githubusercontent.com/82493254/119100505-9aa84f80-ba4a-11eb-8078-d6904f06ec2b.png)

## PLT_RADAR——Drawing radar plot
### TEST FILE——test2.txt
>**1.0 0.8 0.6 0.5 0.9**  
>**0.6 0.9 0.7 0.7 0.3**  
>**0.4 0.1 1.0 0.8 0.5**  
```Python
data = np.loadtxt(r'D:\perpy\test2.txt')
algorithm = ['a', 'b','c']
labels = np.array(['A','B','C','D','E'])

py.plt_radar(labels, data, algorithm, legend=(1.7,0.68))
```
![image](https://user-images.githubusercontent.com/82493254/119101950-1d7dda00-ba4c-11eb-9422-76e120d71849.png)
