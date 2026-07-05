# This is my implementation + breakdown + documentation of spatial hashing using VEX

My work is adapted from the algorithm and C++ code explainde by Ten Minute Physics  
[https://matthias-research.github.io/pages/tenMinutePhysics/11-hashing.pdf](https://matthias-research.github.io/pages/tenMinutePhysics/11-hashing.pdf)  
[https://github.com/matthias-research/pages/blob/master/tenMinutePhysics/11-hashing.html](https://github.com/matthias-research/pages/blob/master/tenMinutePhysics/11-hashing.html)

## The Node Setup

I started by inserting a grid and scattering points on it. The use copy to points so that we have spheres at each of the points. This is because we need a non-zero radius to work with.

//IMAGE HERE

Make sure we have spacing (which is side length of each cell in the grid) equal to twice the sphere radius. This is the assumption made in our algorithm that enables us to run it for a bounded region of 9 cells (or 27 in 3D). We use 'paste relative reference' to control the size of grid cells and spheres from the radius slider easily.

## Coding The Algorithm + Breakdown Of Code

Here, the algorithm begins. I will first store the points into an array. Then, I will create a dense array which saves memory in case of sparse data like the kind we have. Then, I will move on to the unbounded grid case (we are not limited to 9 cells anymore). Here is where spatial hashing comes into the picture. 

_Step 1:_ Defining Variables, Attributes & Data Structures

```

```

_Step 2:_ Store the points into a 1D array

```

```

To create the intermediary array, we need to have the dict keys in sorted order. VEX does not have an option to do this natively, so I used an 'ordering' array to access the elements of the dictionary in a sorted order, even though the dictionary itself is by default unsorted.

_Step 3:_ Create and intermediary array

_Step 4:_ Create the dense array (trick to save memory space)

_Step 5:_ 
