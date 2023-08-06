<h1>Data_FolderSplit</h1>   
_____________________________________________  

Segregate the data table in a csv file into folders containing sub folders of sliced/ segmented data for a physical representation of a decision tree.

The package includes 2 methods to achieve this.

1. Using maximum uniques -> By limiting the system only use columns under a maximum number of uniques, there is lesser control (which could be better in certain instances.)

2. Using Split by columns -> The user can input the columns or Folder structure order which can create a customized folder structure.


_____________________________________________

<h2>Instructions.</h2>  

To install the package, perform:  

```python
pip install Data_FolderSplit
```
 
How to use the methods:  

<h3>1. To create the folder structure using 'max_uniques':  </h3>

```python
#Importing Library.
import Data_FolderSplit as DFS

# filepath -> File path for the csv.
# max_uniques -> Max uniques allowed.
# output_folderpath -> Folder within which sub folders will be formed.

#For example:
filepath = r'D:\LinkinPark\Forever\Datasheet1.csv'
max_uniques = 4
output_folderpath = r'D:\ChesterBennington\is\a\Legend'


#To create the folders with sub folders.
DFS.using_maxUniques(filepath, max_uniques, output_folderpath)
```
_____________________________________________


<h3>2. To create the folder structure using 'Split_with_columnNames':  </h3>

```python
#Importing Library.
import Data_FolderSplit as DFS

# filepath -> File path for the csv.
# output_folderpath -> Folder within which sub folders will be formed.

#For example:
filepath = r'D:\LinkinPark\Forever\Datasheet1.csv'
output_folderpath = r'D:\ChesterBennington\is\a\Legend'


#To create the folders with sub folders.
DFS.Split_with_columnNames(filepath, output_folderpath)
```
_____________________________________________

<h3>Have fun. :-) </h3>