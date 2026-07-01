# Creating Publication Quality Images with VMD and Tachyon

## Create Your Initial Scene in VMD[edit](</mediawiki/index.php?title=Creating_Publication_Quality_Images_with_VMD_and_Tachyon&action=edit&section=1> "Edit section: Create Your Initial Scene in VMD")]

First, create your initial scene in VMD: 

[![Images 1.png](/mediawiki/images/f/f9/Images_1.png)](</mediawiki/index.php/File:Images_1.png>)

I really like to use pastel colors. To change the colors, 

  * Select the object you want to color in the Graphics -> Representations... window.



[![Images 2.png](/mediawiki/images/0/0e/Images_2.png)](</mediawiki/index.php/File:Images_2.png>)

  * From the "Coloring Method" drop-down box, select "ColorID." 



[![Images 3.png](/mediawiki/images/2/24/Images_3.png)](</mediawiki/index.php/File:Images_3.png>)

  * From the drop-down box that appears next to the "Coloring Method" box, select a pastel color like "ice blue."



[![Images 4.png](/mediawiki/images/a/a1/Images_4.png)](</mediawiki/index.php/File:Images_4.png>)

Try to pick contrasting colors for each of the objects in your scene. After modifying my scene some, it now looks like this: 

[![Images 5.png](/mediawiki/images/d/d2/Images_5.png)](</mediawiki/index.php/File:Images_5.png>)

For publication-quality images, it's best to increase the resolution of each object in the scene. I usually increase the resolution to something around 30. 

[![Images 7.png](/mediawiki/images/d/de/Images_7.png)](</mediawiki/index.php/File:Images_7.png>)

I also like to change the material of each object in the scene to "Glossy." 

[![Images 8.png](/mediawiki/images/1/11/Images_8.png)](</mediawiki/index.php/File:Images_8.png>)

Next, we need to set the background color to white for publication. Go to Graphics => Colors... from the VMD Main window, and change the background color this way: 

[![Images 9.png](/mediawiki/images/3/3b/Images_9.png)](</mediawiki/index.php/File:Images_9.png>)

Now, let's add some fog. Check the Display -> Depth Cueing box from the VMD Main window. The place where the fog begins can be specified by... 

  1. Clicking on the VMD OpenGL Display window, where your scene appears.
  2. Pressing the 'T' key on your keyboard.
  3. Moving the mouse across the window while holding down the right mouse button. (Check this...)



The thickness of the fog can be changed by going to Display => Display Settings... from the VMD Main window. 

[![Images 10.png](/mediawiki/images/4/40/Images_10.png)](</mediawiki/index.php/File:Images_10.png>)

Finally, we want to make sure to remove the axis bars. From the VMD Main window, click on Display -> Axes -> Off 

Be sure to save your scene now that your done. From the VMD Main window, File => Save State ... 

## Make the Image Square[edit](</mediawiki/index.php?title=Creating_Publication_Quality_Images_with_VMD_and_Tachyon&action=edit&section=2> "Edit section: Make the Image Square")]

I usually like to make my images perfectly square. To do this, go to the Tk Console (Extensions => Tk Console from the VMD Main window). 

In the Tk Console, type in the following: 
    
    
    display resize 800 800 

You may want to now center your image within the now square VMD OpenGL Display window. 

My scene now looks like this: 

[![Images 11.png](/mediawiki/images/1/12/Images_11.png)](</mediawiki/index.php/File:Images_11.png>)

## Save and Modify a Tachyon File[edit](</mediawiki/index.php?title=Creating_Publication_Quality_Images_with_VMD_and_Tachyon&action=edit&section=3> "Edit section: Save and Modify a Tachyon File")]

We're going to use a program called Tachyon to render the image. Tachyon does a much better job rendering images than VMD. 

To save a tachyon input file, go to File => Render... from the VMD Main menu. Change the "Render using:" box to "Tachyon" (not "TachyonInternal"). 

[![Images 12.png](/mediawiki/images/6/67/Images_12.png)](</mediawiki/index.php/File:Images_12.png>)

The default filename is _plot.dat_. Feel free to change that name if you wish. Finally, click on the "Start Rendering" button. 

Two files will be generated, plot.dat and plot.dat.tga. Ignore the file plot.dat.tga. **This is not your high-resolution figure!**

Open up the file _plot.dat_ in your favorite text editor (**vi** , **gedit** , etc). The opening lines look like this: 
    
    
    # 
    # Molecular graphics exported from VMD 1.8.6
    # http://www.ks.uiuc.edu/Research/vmd/
    # 
    # Requires Tachyon version 0.98 or newer
    # 
    # Default tachyon rendering command for this scene:
    #   tachyon  -aasamples 4 -trans_vmd -mediumshade %s -format TARGA -o %s.tga
    # 
    Begin_Scene
    Resolution 800 800
    Camera
      Projection Orthographic
      Zoom 0.333333
      Aspectratio 1
      Antialiasing 0
      Raydepth 30
      Center  0 0 -2
      Viewdir -0 -0 2
      Updir   0 1 -0
    End_Camera
    Directional_Light Direction 0.1 -0.1 1 Color 1 1 1
    Directional_Light Direction -1 -2 0.5 Color 1 1 1
    
    Background 1 1 1
    FOG EXP2 START 0 END 10 DENSITY 0.35 COLOR 1 1 1
    VertexArray  Numverts 254430
    
    Coords
    0.346526 0.310988 -1.22186
    0.344714 0.309855 -1.21998
    0.343276 0.308949 -1.2177
    ...
    

Increase the resolution of the image by editing the line that starts with "Resolution." I'd change it to be 2000 2000 or 3000 3000. Also, change Antialiasing to 10. Now the _plot.dat_ file looks like this: 
    
    
    # 
    # Molecular graphics exported from VMD 1.8.6
    # http://www.ks.uiuc.edu/Research/vmd/
    # 
    # Requires Tachyon version 0.98 or newer
    # 
    # Default tachyon rendering command for this scene:
    #   tachyon  -aasamples 4 -trans_vmd -mediumshade %s -format TARGA -o %s.tga
    # 
    Begin_Scene
    Resolution 2000 2000
    Camera
      Projection Orthographic
      Zoom 0.333333
      Aspectratio 1
      Antialiasing 10
      Raydepth 30
      Center  0 0 -2
      Viewdir -0 -0 2
      Updir   0 1 -0
    End_Camera
    Directional_Light Direction 0.1 -0.1 1 Color 1 1 1
    Directional_Light Direction -1 -2 0.5 Color 1 1 1
    
    Background 1 1 1
    FOG EXP2 START 0 END 10 DENSITY 0.35 COLOR 1 1 1
    VertexArray  Numverts 254430
    
    Coords
    0.346526 0.310988 -1.22186
    0.344714 0.309855 -1.21998
    0.343276 0.308949 -1.2177
    ...
    

Save this modified file. 

## Render the Image[edit](</mediawiki/index.php?title=Creating_Publication_Quality_Images_with_VMD_and_Tachyon&action=edit&section=4> "Edit section: Render the Image")]

We can now use tachyon to render the image. On our lab computers, tachyon can be found at /net/linux/pkg/vmd-1.8.6/tachyon_LINUX 

From the command line, type in: 
    
    
    /net/linux/pkg/vmd-1.8.6/tachyon_LINUX -rescale_lights 0.7 -add_skylight 0.4 plot.dat -o image.dat.tga -aasamples 8 

More details can be found [here](<http://www.ks.uiuc.edu/Research/vmd/minitutorials/tachyonao/>)

## Photoshop Processing[edit](</mediawiki/index.php?title=Creating_Publication_Quality_Images_with_VMD_and_Tachyon&action=edit&section=5> "Edit section: Photoshop Processing")]

After the image has been rendered, open the _image.dat.tga_ file in Photoshop. A number of modifications can be made, but at the very minimum I recommend: 

  1. Image -> Adjustments -> Auto Levels
  2. Image -> Adjustments -> Auto Contrast



In some cases, Image -> Adjustments -> Auto Color is also helpful. 

Here's the final image: 

[![Images 13.png](/mediawiki/images/b/b1/Images_13.png)](</mediawiki/index.php/File:Images_13.png>)
