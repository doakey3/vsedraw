========
VSE Draw
========
.. image:: https://i.imgur.com/Pm9Lw8Q.gif

Usage
=====
Creating Glyphs
===============
.. image:: https://i.imgur.com/VWtzots.png

There is a user panel on the left side of the 3D view where you can
export curve objects as glyph files.

You can use the "Toggle Guide" operator to draw a box in the 3D view
that will show you how your curve will appear in a 1920x1080 video.

Importing Glyphs
================
.. image:: https://i.imgur.com/ZjfQ4ID.png

The user interface is located on the right side of the sequencer, under
the tools tab.

You have 3 buttons for quickly changing the color of drawn strokes as
well as a color picker that allows you to change strokes to any selected
color. You can also save a selected color as a quick color button.

Change the *scale* to multiply the size of an imported stroke. Change
the *speed* to increase the number of pixels / frame that will be drawn
of the stroke. Change the *thickness* to set the number of pixels wide
the stroke will be.

You can create a decorator around the text as well by changing the
decorator value. The available options are ellipse, underline, box, and
circle.

Import Glyph
------------
Click the operator, browse to the glyph file, and import.

Import Strokes
--------------
Works like the import glyph function, except each stroke becomes it's
own strip in the VSE.

Writing
-------
Type a line of text in the text box and click write.

.. image:: https://i.imgur.com/Jt7AymM.gif

Tracing
=======
Select imported glyph strips, then select the tracer strip and run the
function. This will add keyframes to the tracer so that it follows along
the strokes as they are drawn.

I like to use this image for tracing:

.. image:: https://i.imgur.com/nsOUC1c.png
