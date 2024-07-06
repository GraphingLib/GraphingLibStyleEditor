.. role:: orange

========
Handbook
========

Once you have GraphingLib Style Editor installed, you can run the following command in the terminal:

.. code-block:: bash

    glse

.. image:: _static/app_screenshots/gui_sections.png

You will be greeted with a GUI which allows you to create, edit, and delete styles. The Style Editor interface consists of a left panel and a right panel, which let you customize and preview styles respectively. In the left panel, you can adjust all the style settings for the currently opened style (:orange:`1`). These changes are immediately reflected in the right panel, which displays a figure with the applied customizations. You can see how the style appears in different contexts by browsing through the example figures (:orange:`3`) provided within the interface. If Auto Switch (:orange:`4`) is checked, the example figure will automatically switch to the most appropriate example depending on what customization tab you are currently on. Additionally, there is an option to upload a custom Python script that creates a GraphingLib figure (:orange:`5`), allowing users to apply and preview the style on their own figures. Other options are available in the file menu at the top left.

.. image:: _static/app_screenshots/file_options.png
    :width: 300
    :align: center

Create a new style
~~~~~~~~~~~~~~~~~~

To create a new style, go to File → New. You will be asked to choose an existing style to use as a starting point.

You can now customize the style by going through the different tabs in the left panel. Remember, you are choosing the default values for each object type: these are the values that will be used if you do not specify a parameter when creating an object. You will always be able to override these defaults by explicitely specifying a parameter.

Once you're happy with your style, you can go to File → Save and you will be prompted to enter a name for your new style. Any styles you create will be saved to a platform-specific user configuration directory created by GraphingLib when your first custom style is generated (you don't have to worry about choosing where to save your styles). This means that if you uninstall GraphingLib or update it, your styles will not be deleted. There is also a built-in mechanism which updates your custom styles automatically when new objects or parameters are added to GraphingLib with an update. You can therefore safely update GraphingLib without worrying about your custom styles breaking. Any new objects or parameters will be set to the same value as the "plain" style, but you can always edit your custom styles later.

Edit an existing style
~~~~~~~~~~~~~~~~~~~~~~

You can open an existing style by going to File → Open. You will be presented with a list of existing styles to choose from. You can then proceed as usual, editing the style to your liking. Once you are done, you can either save your changes to the existing style by going to File → Save, or you can save your changes to a new style by going to File → Save As.

You will notice that you can also edit GraphingLib's built-in styles (GraphingLib will prioritize your edited versions if they exist). Don't worry, this will not break anything. If you want to revert to the original style, you can always delete your custom style and GraphingLib will fall back to the built-in style again. For example, if you want to edit the "dark" style, you can open it, make your changes, and save it. GraphingLib will now use your edited version of the "dark" style instead of the built-in one. If you want to revert to the original "dark" style, you can delete your edited version of it and GraphingLib will use the built-in "dark" style again.

At any time, you can click on "View unsaved changes" (:orange:`2`) to see what changes you have made to the style since you last saved it. This can be useful if you want to make sure you haven't accidentally changed something you didn't mean to.

.. image:: _static/app_screenshots/unsaved_changes.png
    :width: 400
    :align: center

Manage styles
~~~~~~~~~~~~~

.. image:: _static/app_screenshots/manager.png
    :width: 400
    :align: center

If you want to view and manage all your styles, you can go to File → Manage styles. Here you can see a list of all your custom styles, identified by a yellow square, as well as the built-in styles identified by a blue dot. There is a color legend to help you distinguish between built-in and custom styles. You can also identify which built-in styles are currently overridden by a custom style of the same name by the small green triangle next to the style name.

Once you have selected a style in the list, you are presented with four options:

- Rename: Change the name of the style. You can only rename custom styles. Built-in styles cannot be renamed, but you can duplicate them and rename the duplicate.
- Duplicate: Create a copy of the style with a new name.
- Delete: Delete the style. You can only delete custom styles. Built-in styles cannot be deleted. Deleting a custom style which overrides a built-in style will revert GraphingLib to using the built-in style.
- Set as default: Set the style as the default style. This means that any figures created without a specified style will use this style. You can see the current default style in the top left corner of the "Manage styles" window.
