"""
Automatically save all .bp files in output folder as video.
If you have paraview and its python api installed, you can call this file by:
    pvpython.exe paraplot.py
"""

import os
import glob
# trace generated using paraview version 5.12.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

#### import the simple module from the paraview
from paraview.simple import *


def save(path, filename):
    #### disable automatic camera reset on 'Show'
    paraview.simple._DisableFirstRenderCameraReset()

    # create a new 'ADIOS2VTXReader'
    dguDG1prod0to05bp = ADIOS2VTXReader(registrationName=filename, FileName=path)

    # get animation scene
    animationScene1 = GetAnimationScene()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    dguDG1prod0to05bpDisplay = Show(dguDG1prod0to05bp, renderView1, 'UnstructuredGridRepresentation')

    # trace defaults for the display properties.
    dguDG1prod0to05bpDisplay.Representation = 'Surface'

    # reset view to fit data
    renderView1.ResetCamera(False, 0.9)

    #changing interaction mode based on data extents
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.5, 0.5, 3.35]
    renderView1.CameraFocalPoint = [0.5, 0.5, 0.0]

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(dguDG1prod0to05bpDisplay, ('POINTS', 'c'))

    # rescale color and/or opacity maps used to include current data range
    dguDG1prod0to05bpDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    dguDG1prod0to05bpDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'c'
    cLUT = GetColorTransferFunction('c')

    # get opacity transfer function/opacity map for 'c'
    cPWF = GetOpacityTransferFunction('c')

    # get 2D transfer function for 'c'
    cTF2D = GetTransferFunction2D('c')

    # Rescale transfer function
    cLUT.RescaleTransferFunction(-0.8571353902761758, 1.8545396492329345)

    # Rescale transfer function
    cPWF.RescaleTransferFunction(-0.8571353902761758, 1.8545396492329345)

    # set scalar coloring using an separate color/opacity maps
    ColorBy(dguDG1prod0to05bpDisplay, ('POINTS', 'c'), True)

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(cLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    dguDG1prod0to05bpDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    dguDG1prod0to05bpDisplay.SetScalarBarVisibility(renderView1, True)

    # get separate color transfer function/color map for 'c'
    separate_dguDG1prod0to05bpDisplay_cLUT = GetColorTransferFunction('c', dguDG1prod0to05bpDisplay, separate=True)

    # get separate opacity transfer function/opacity map for 'c'
    separate_dguDG1prod0to05bpDisplay_cPWF = GetOpacityTransferFunction('c', dguDG1prod0to05bpDisplay, separate=True)

    # get separate 2D transfer function for 'c'
    separate_dguDG1prod0to05bpDisplay_cTF2D = GetTransferFunction2D('c', dguDG1prod0to05bpDisplay, separate=True)

    # set scalar coloring
    ColorBy(dguDG1prod0to05bpDisplay, ('POINTS', 'c'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(separate_dguDG1prod0to05bpDisplay_cLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    dguDG1prod0to05bpDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    dguDG1prod0to05bpDisplay.SetScalarBarVisibility(renderView1, True)

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    cLUT.ApplyPreset('Inferno (matplotlib)', True)

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    cLUT.ApplyPreset('Cool to Warm (Extended)', True)

    # get color transfer function/color map for 'c'
    cLUT = GetColorTransferFunction('c')

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # get color legend/bar for cLUT in view renderView1
    cLUTColorBar = GetScalarBar(cLUT, renderView1)

    # Properties modified on cLUTColorBar
    cLUTColorBar.Title = 'mass density'


    # get layout
    layout1 = GetLayout()

    # layout/tab size in pixels
    layout1.SetSize(1218, 796)

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.5, 0.5, 3.35]
    renderView1.CameraFocalPoint = [0.5, 0.5, 0.0]
    renderView1.CameraParallelScale = 0.7071067811865476

    # save animation
    SaveAnimation(filename='videos/'+filename+'.mp4', viewOrLayout=renderView1, location=16, ImageResolution=[1218, 796],
        OverrideColorPalette='BlackBackground',
        FrameRate=20,
        FrameWindow=[0, 200], 
        # MP4 Writer options
        FileName='')

    #================================================================
    # addendum: following script captures some of the application
    # state to faithfully reproduce the visualization during playback
    #================================================================

    #--------------------------------
    # saving layout sizes for layouts

    # layout/tab size in pixels
    layout1.SetSize(1218, 796)

    #-----------------------------------
    # saving camera placements for views

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.5, 0.5, 3.35]
    renderView1.CameraFocalPoint = [0.5, 0.5, 0.0]
    renderView1.CameraParallelScale = 0.7071067811865476


    ##--------------------------------------------
    ## You may need to add some code at the end of this python script depending on your usage, eg:
    #
    ## Render all views to see them appears
    # RenderAllViews()
    #
    ## Interact with the view, usefull when running from pvpython
    # Interact()
    #
    ## Save a screenshot of the active view
    # SaveScreenshot("path/to/screenshot.png")
    #
    ## Save a screenshot of a layout (multiple splitted view)
    # SaveScreenshot("path/to/screenshot.png", GetLayout())
    #
    ## Save all "Extractors" from the pipeline browser
    # SaveExtracts()
    #
    ## Save a animation of the current active view
    # SaveAnimation()
    #
    ## Please refer to the documentation of paraview.simple
    ## https://kitware.github.io/paraview-docs/latest/python/paraview.simple.html
    ##--------------------------------------------

if __name__ == "__main__":
    if not os.path.exists("videos"):
        os.makedirs("videos")
    
    files = glob.glob('outputs/*.bp')
    for file in files:
        print("animating and saving ..", file)
        filename = file.split("\\")[1].split(".bp")[0]
        save(file,filename)
    